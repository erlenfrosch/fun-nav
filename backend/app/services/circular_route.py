import asyncio
import math
from typing import NamedTuple

import httpx

EARTH_RADIUS_KM = 6371.0
AVG_SPEED_KMH = 50.0
WAYPOINT_COUNT = 8


class Route(NamedTuple):
    coordinates: list
    distance_km: float
    duration_min: float
    curviness_score: float


def destination_point(lat: float, lon: float, bearing_deg: float, distance_km: float) -> tuple[float, float]:
    """Inverse Haversine: compute destination from start, bearing, and distance."""
    lat_r = math.radians(lat)
    lon_r = math.radians(lon)
    bearing_r = math.radians(bearing_deg)
    d = distance_km / EARTH_RADIUS_KM

    lat2 = math.asin(
        math.sin(lat_r) * math.cos(d)
        + math.cos(lat_r) * math.sin(d) * math.cos(bearing_r)
    )
    lon2 = lon_r + math.atan2(
        math.sin(bearing_r) * math.sin(d) * math.cos(lat_r),
        math.cos(d) - math.sin(lat_r) * math.sin(lat2),
    )
    return math.degrees(lat2), math.degrees(lon2)


def calculate_radius(fahrtzeit_min: float, avg_speed_kmh: float = AVG_SPEED_KMH) -> float:
    """Circle radius in km for given travel time and average speed."""
    return (fahrtzeit_min / 60.0 * avg_speed_kmh) / (2 * math.pi)


def generate_waypoints(lat: float, lon: float, radius_km: float) -> list[tuple[float, float]]:
    """8 evenly-distributed waypoints on the circle via inverse Haversine."""
    step = 360 / WAYPOINT_COUNT
    return [destination_point(lat, lon, i * step, radius_km) for i in range(WAYPOINT_COUNT)]


def select_route_pairs(waypoints: list[tuple[float, float]]) -> list[tuple[int, int]]:
    """
    6 index pairs for route variants:
    4 pairs at 180° separation + 2 pairs at 135° separation.
    """
    n = len(waypoints)
    half = n // 2
    pairs: list[tuple[int, int]] = [(i, i + half) for i in range(half)]  # 4 opposing
    step_135 = round(n * 3 / 8)
    pairs.append((0, step_135 % n))
    pairs.append((half // 2, (half // 2 + step_135) % n))
    return pairs[:6]


async def _fetch_route(
    client: httpx.AsyncClient,
    graphhopper_url: str,
    points: list,
    profile: str,
) -> dict | None:
    payload = {
        "points": points,
        "profile": profile,
        "points_encoded": False,
    }
    try:
        resp = await client.post(f"{graphhopper_url}/route", json=payload, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()
        paths = data.get("paths")
        return paths[0] if paths else None
    except Exception:
        return None


async def generate_circular_routes(
    lat: float,
    lon: float,
    fahrtzeit_min: float,
    graphhopper_url: str,
    profile: str = "car",
) -> list[Route]:
    """
    Generate up to 3 circular routes sorted by curviness (highest first).

    Acceptance criterion: München 48.137°N 11.575°E, 60 min → 3 routes with 48–72 min.
    """
    radius_km = calculate_radius(fahrtzeit_min)
    waypoints = generate_waypoints(lat, lon, radius_km)
    pairs = select_route_pairs(waypoints)

    # GraphHopper expects [lon, lat]
    start = [lon, lat]

    async with httpx.AsyncClient() as client:
        tasks = [
            _fetch_route(
                client,
                graphhopper_url,
                [start, [waypoints[j][1], waypoints[j][0]], [waypoints[k][1], waypoints[k][0]], start],
                profile,
            )
            for j, k in pairs
        ]
        results = await asyncio.gather(*tasks)

    target_sec = fahrtzeit_min * 60.0
    tolerance = 0.20

    routes: list[Route] = []
    for path in results:
        if path is None:
            continue
        duration_sec = path["time"] / 1000.0
        if abs(duration_sec - target_sec) / target_sec > tolerance:
            continue
        distance_km = path["distance"] / 1000.0
        curviness = distance_km / (2.0 * radius_km)
        routes.append(Route(
            coordinates=path["points"]["coordinates"],
            distance_km=distance_km,
            duration_min=duration_sec / 60.0,
            curviness_score=curviness,
        ))

    routes.sort(key=lambda r: r.curviness_score, reverse=True)
    return routes[:3]
