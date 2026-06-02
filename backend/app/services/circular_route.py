import asyncio
import math
import os
from typing import NamedTuple

import httpx

EARTH_RADIUS_KM = 6371.0
AVG_SPEED_KMPH = 40.0
TIME_TOLERANCE = 0.20
NUM_WAYPOINTS = 8
NUM_ROUTES = 6
GRAPHHOPPER_URL = os.getenv("GRAPHHOPPER_URL", "http://graphhopper:8989")


class Waypoint(NamedTuple):
    lat: float
    lng: float


def calculate_radius(duration_min: float, speed_kmh: float = AVG_SPEED_KMPH) -> float:
    return (duration_min / 60.0 * speed_kmh) / (2 * math.pi)


def haversine_waypoint(
    origin_lat: float, origin_lng: float, radius_km: float, bearing_deg: float
) -> Waypoint:
    lat1 = math.radians(origin_lat)
    lng1 = math.radians(origin_lng)
    bearing = math.radians(bearing_deg)
    d_over_r = radius_km / EARTH_RADIUS_KM

    lat2 = math.asin(
        math.sin(lat1) * math.cos(d_over_r)
        + math.cos(lat1) * math.sin(d_over_r) * math.cos(bearing)
    )
    lng2 = lng1 + math.atan2(
        math.sin(bearing) * math.sin(d_over_r) * math.cos(lat1),
        math.cos(d_over_r) - math.sin(lat1) * math.sin(lat2),
    )
    return Waypoint(lat=math.degrees(lat2), lng=math.degrees(lng2))


def generate_waypoints(
    origin_lat: float, origin_lng: float, radius_km: float, count: int = NUM_WAYPOINTS
) -> list[Waypoint]:
    step = 360.0 / count
    return [
        haversine_waypoint(origin_lat, origin_lng, radius_km, i * step)
        for i in range(count)
    ]


async def _fetch_route(
    client: httpx.AsyncClient, origin: Waypoint, via: Waypoint
) -> dict | None:
    payload = {
        "points": [
            [origin.lng, origin.lat],
            [via.lng, via.lat],
            [origin.lng, origin.lat],
        ],
        "profile": "car",
        "instructions": False,
        "calc_points": False,
    }
    try:
        resp = await client.post(f"{GRAPHHOPPER_URL}/route", json=payload, timeout=10.0)
        resp.raise_for_status()
        paths = resp.json().get("paths", [])
        return paths[0] if paths else None
    except Exception:
        return None


def calculate_curviness(distance_m: float, radius_km: float) -> float:
    optimal_m = 2 * radius_km * 1000
    if optimal_m == 0:
        return 0.0
    return distance_m / optimal_m


async def generate_circular_routes(
    origin_lat: float,
    origin_lng: float,
    duration_min: float,
) -> list[dict]:
    radius_km = calculate_radius(duration_min)
    waypoints = generate_waypoints(origin_lat, origin_lng, radius_km)
    candidates = waypoints[:NUM_ROUTES]
    origin = Waypoint(lat=origin_lat, lng=origin_lng)

    min_ms = duration_min * 60 * 1000 * (1 - TIME_TOLERANCE)
    max_ms = duration_min * 60 * 1000 * (1 + TIME_TOLERANCE)

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *[_fetch_route(client, origin, wp) for wp in candidates]
        )

    routes = []
    for path, wp in zip(results, candidates):
        if path is None:
            continue
        time_ms = path.get("time", 0)
        if min_ms <= time_ms <= max_ms:
            dist_m = path.get("distance", 0)
            routes.append(
                {
                    "duration_min": time_ms / 60000,
                    "distance_km": dist_m / 1000,
                    "waypoint": {"lat": wp.lat, "lng": wp.lng},
                    "curviness_score": calculate_curviness(dist_m, radius_km),
                }
            )

    routes.sort(key=lambda r: r["curviness_score"], reverse=True)
    return routes
