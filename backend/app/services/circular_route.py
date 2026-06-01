import asyncio
import math

from fastapi import HTTPException

from app.models.schemas import Curviness, GeoJSONLineString, Instruction, Route
from app.services.graphhopper import query_route

EARTH_RADIUS_KM = 6371.0
AVG_SPEED_KMH: dict[Curviness, float] = {
    Curviness.high: 50.0,
    Curviness.very_high: 40.0,
}
TIME_TOLERANCE = 0.20


def _waypoints_on_circle(
    lat: float, lon: float, radius_km: float, n: int = 8
) -> list[tuple[float, float]]:
    lat_rad = math.radians(lat)
    waypoints = []
    for i in range(n):
        angle = math.radians(i * 360 / n)
        delta_lat = math.degrees(radius_km / EARTH_RADIUS_KM * math.cos(angle))
        delta_lon = math.degrees(
            radius_km / EARTH_RADIUS_KM * math.sin(angle) / math.cos(lat_rad)
        )
        waypoints.append((lat + delta_lat, lon + delta_lon))
    return waypoints


def _parse_route(path: dict, route_id: str) -> Route:
    return Route(
        id=route_id,
        duration_min=round(path["time"] / 60_000, 1),
        distance_km=round(path["distance"] / 1_000, 1),
        geojson=GeoJSONLineString(
            type="LineString",
            coordinates=path["points"]["coordinates"],
        ),
        instructions=[
            Instruction(text=instr["text"], distance=instr["distance"])
            for instr in path.get("instructions", [])
        ],
    )


async def generate_circular_routes(
    lat: float, lon: float, duration_min: int, curviness: Curviness
) -> list[Route]:
    avg_speed = AVG_SPEED_KMH[curviness]
    radius_km = (duration_min / 60 * avg_speed) / (2 * math.pi)

    waypoints = _waypoints_on_circle(lat, lon, radius_km, n=8)

    # 3 opposing pairs × 2 directions = 6 route variants
    opposing_pairs = [(0, 4), (1, 5), (2, 6)]
    start = [lon, lat]
    route_requests: list[list[list[float]]] = []
    for a_idx, b_idx in opposing_pairs:
        wp_a = [waypoints[a_idx][1], waypoints[a_idx][0]]
        wp_b = [waypoints[b_idx][1], waypoints[b_idx][0]]
        route_requests.append([start, wp_a, wp_b, start])
        route_requests.append([start, wp_b, wp_a, start])

    async def _fetch(points: list[list[float]], idx: int) -> tuple[int, dict]:
        result = await query_route(points, curviness.value)
        return idx, result

    raw = await asyncio.gather(
        *[_fetch(req, i) for i, req in enumerate(route_requests)],
        return_exceptions=True,
    )

    # Surface GH-level errors (unreachable / 5xx) before processing results
    for r in raw:
        if isinstance(r, HTTPException) and r.status_code >= 500:
            raise r

    min_dur = duration_min * (1 - TIME_TOLERANCE)
    max_dur = duration_min * (1 + TIME_TOLERANCE)

    valid: list[Route] = []
    for r in raw:
        if isinstance(r, Exception):
            continue
        idx, result = r
        if not result or not result.get("paths"):
            continue
        path = result["paths"][0]
        route_dur = path["time"] / 60_000
        if not (min_dur <= route_dur <= max_dur):
            continue
        try:
            valid.append(_parse_route(path, f"route_{idx + 1}"))
        except (KeyError, TypeError):
            continue

    if not valid:
        raise HTTPException(
            status_code=404,
            detail="Keine Route gefunden, die den Zeitvorgaben entspricht",
        )

    # Sort by distance-to-time ratio: more km per minute → more curves
    valid.sort(key=lambda r: r.distance_km / max(r.duration_min, 0.1), reverse=True)

    return valid[:3]
