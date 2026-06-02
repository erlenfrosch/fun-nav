import asyncio
import math
from typing import NamedTuple

import httpx

EARTH_RADIUS_KM = 6371.0
AVG_SPEED_KMH = 50.0
REFERENCE_SPEED_KMH = 80.0


class Waypoint(NamedTuple):
    lat: float
    lon: float


def compute_radius_km(duration_min: float, avg_speed_kmh: float = AVG_SPEED_KMH) -> float:
    return (duration_min / 60.0 * avg_speed_kmh) / (2 * math.pi)


def destination_point(lat: float, lon: float, bearing_deg: float, distance_km: float) -> Waypoint:
    d = distance_km / EARTH_RADIUS_KM
    lat_r = math.radians(lat)
    lon_r = math.radians(lon)
    b_r = math.radians(bearing_deg)

    lat2_r = math.asin(
        math.sin(lat_r) * math.cos(d)
        + math.cos(lat_r) * math.sin(d) * math.cos(b_r)
    )
    lon2_r = lon_r + math.atan2(
        math.sin(b_r) * math.sin(d) * math.cos(lat_r),
        math.cos(d) - math.sin(lat_r) * math.sin(lat2_r),
    )
    return Waypoint(lat=math.degrees(lat2_r), lon=math.degrees(lon2_r))


def generate_waypoints(lat: float, lon: float, radius_km: float, count: int = 8) -> list[Waypoint]:
    step = 360.0 / count
    return [destination_point(lat, lon, i * step, radius_km) for i in range(count)]


def curviness_score(time_ms: float, distance_m: float) -> float:
    if distance_m <= 0:
        return 0.0
    actual_speed_kmh = (distance_m / 1000.0) / (time_ms / 3_600_000.0)
    return round(REFERENCE_SPEED_KMH / max(actual_speed_kmh, 0.1), 2)


async def _fetch_route(
    client: httpx.AsyncClient,
    graphhopper_url: str,
    points: list[Waypoint],
    profile: str,
) -> dict | None:
    payload = {
        "points": [[p.lon, p.lat] for p in points],
        "profile": profile,
        "instructions": False,
        "calc_points": False,
    }
    try:
        resp = await client.post(f"{graphhopper_url}/route", json=payload, timeout=10.0)
        resp.raise_for_status()
        paths = resp.json().get("paths", [])
        if not paths:
            return None
        return {"time_ms": paths[0]["time"], "distance_m": paths[0]["distance"]}
    except (httpx.HTTPError, KeyError):
        return None


async def generate_circular_routes(
    lat: float,
    lon: float,
    duration_min: float,
    graphhopper_url: str = "http://graphhopper:8989",
    profile: str = "car",
    tolerance: float = 0.20,
    top_n: int = 3,
) -> list[dict]:
    radius_km = compute_radius_km(duration_min)
    waypoints = generate_waypoints(lat, lon, radius_km)
    start = Waypoint(lat=lat, lon=lon)

    opposite_pairs = [(0, 4), (1, 5), (2, 6)]
    route_point_sets = []
    for i, j in opposite_pairs:
        route_point_sets.append([start, waypoints[i], waypoints[j], start])
        route_point_sets.append([start, waypoints[j], waypoints[i], start])

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *[_fetch_route(client, graphhopper_url, pts, profile) for pts in route_point_sets]
        )

    target_ms = duration_min * 60.0 * 1000.0
    routes = []
    for result in results:
        if result is None:
            continue
        deviation = abs(result["time_ms"] - target_ms) / target_ms
        if deviation > tolerance:
            continue
        routes.append({
            "duration_min": round(result["time_ms"] / 60_000.0, 1),
            "distance_km": round(result["distance_m"] / 1000.0, 1),
            "curviness_score": curviness_score(result["time_ms"], result["distance_m"]),
        })

    routes.sort(key=lambda r: r["curviness_score"], reverse=True)
    return routes[:top_n]
