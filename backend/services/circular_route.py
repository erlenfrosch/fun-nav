import math
import asyncio
import os
from dataclasses import dataclass, field

import httpx

GH_URL = os.getenv("GRAPHHOPPER_URL", "http://localhost:8989")

EARTH_RADIUS_KM = 6371.0
NUM_WAYPOINTS = 8
MAX_TIME_DEVIATION = 0.20

# Average speeds used to estimate how far the radius should be
AVG_SPEED_CURVY_KMH = 50.0
AVG_SPEED_VERY_CURVY_KMH = 40.0


@dataclass
class CircularRoute:
    duration_ms: int
    distance_m: float
    curviness_score: float
    waypoints: list = field(default_factory=list)


def calculate_radius_km(target_minutes: float, very_curvy: bool = False) -> float:
    """Return circle radius so that a route around it matches target_minutes."""
    avg_speed = AVG_SPEED_VERY_CURVY_KMH if very_curvy else AVG_SPEED_CURVY_KMH
    return (target_minutes / 60.0 * avg_speed) / (2 * math.pi)


def haversine_waypoint(
    center_lat: float, center_lon: float, radius_km: float, bearing_deg: float
) -> tuple[float, float]:
    """Return (lat, lon) of a point at bearing_deg and radius_km from center."""
    bearing = math.radians(bearing_deg)
    lat1 = math.radians(center_lat)
    lon1 = math.radians(center_lon)
    d_r = radius_km / EARTH_RADIUS_KM

    lat2 = math.asin(
        math.sin(lat1) * math.cos(d_r)
        + math.cos(lat1) * math.sin(d_r) * math.cos(bearing)
    )
    lon2 = lon1 + math.atan2(
        math.sin(bearing) * math.sin(d_r) * math.cos(lat1),
        math.cos(d_r) - math.sin(lat1) * math.sin(lat2),
    )
    return math.degrees(lat2), math.degrees(lon2)


def candidate_waypoints(
    lat: float, lon: float, radius_km: float
) -> list[tuple[float, float]]:
    """Return 8 waypoints equally spaced (every 45°) on a circle."""
    step = 360 // NUM_WAYPOINTS
    return [haversine_waypoint(lat, lon, radius_km, bearing) for bearing in range(0, 360, step)]


def _curviness(distance_m: float, duration_ms: float) -> float:
    """Lower average speed → more curves → higher score."""
    if duration_ms <= 0 or distance_m <= 0:
        return 0.0
    avg_speed_kmh = (distance_m / 1000.0) / (duration_ms / 3_600_000.0)
    return 1.0 / avg_speed_kmh


async def _gh_route(
    client: httpx.AsyncClient,
    points: list[tuple[float, float]],
    profile: str = "car",
) -> dict | None:
    """POST a route request to GraphHopper; returns first path or None on error."""
    gh_points = [[lon, lat] for lat, lon in points]
    try:
        resp = await client.post(
            f"{GH_URL}/route",
            json={"points": gh_points, "profile": profile, "calc_points": False, "instructions": False},
            timeout=10.0,
        )
        resp.raise_for_status()
        data = resp.json()
        paths = data.get("paths", [])
        return paths[0] if paths else None
    except Exception:
        return None


def _build_route_requests(
    start: tuple[float, float], waypoints: list[tuple[float, float]]
) -> list[list[tuple[float, float]]]:
    """
    Build 6 route-point lists:
      - 4 opposing-pair loops: start → wp[i] → wp[i+4] → start
      - 2 single-waypoint loops at 0° and 90°: start → wp[i] → start
    """
    half = NUM_WAYPOINTS // 2  # 4
    requests = [
        [start, waypoints[i], waypoints[i + half], start] for i in range(half)
    ]
    requests += [
        [start, waypoints[0], start],
        [start, waypoints[2], start],
    ]
    return requests


async def generate_circular_routes(
    lat: float,
    lon: float,
    target_minutes: float,
    very_curvy: bool = False,
    profile: str = "car",
    _client: httpx.AsyncClient | None = None,
) -> list[CircularRoute]:
    """
    Generate up to 3 circular routes starting and ending at (lat, lon).

    Routes are filtered to ±20 % of target_minutes and sorted by curviness
    (lower average speed = higher score).
    """
    radius_km = calculate_radius_km(target_minutes, very_curvy)
    waypoints = candidate_waypoints(lat, lon, radius_km)
    start = (lat, lon)
    requests = _build_route_requests(start, waypoints)

    target_ms = target_minutes * 60 * 1_000
    min_ms = target_ms * (1 - MAX_TIME_DEVIATION)
    max_ms = target_ms * (1 + MAX_TIME_DEVIATION)

    close_client = _client is None
    client = _client or httpx.AsyncClient()
    try:
        paths = await asyncio.gather(
            *[_gh_route(client, req, profile) for req in requests]
        )
    finally:
        if close_client:
            await client.aclose()

    routes: list[CircularRoute] = []
    for path, req_points in zip(paths, requests):
        if path is None:
            continue
        duration_ms: int = path["time"]
        distance_m: float = path["distance"]
        if not (min_ms <= duration_ms <= max_ms):
            continue
        routes.append(
            CircularRoute(
                duration_ms=duration_ms,
                distance_m=distance_m,
                curviness_score=_curviness(distance_m, duration_ms),
                waypoints=req_points,
            )
        )

    routes.sort(key=lambda r: r.curviness_score, reverse=True)
    return routes[:3]
