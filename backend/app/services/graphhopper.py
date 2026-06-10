import math
import os
from typing import Literal

import httpx
from fastapi import HTTPException

GRAPHHOPPER_URL = os.getenv("GRAPHHOPPER_URL", "http://graphhopper:8989")

_SPEED_KMH: dict[str, float] = {
    "kurvenreich": 45.0,
    "sehr_kurvenreich": 35.0,
}


def _circular_waypoints(lat: float, lon: float, distance_km: float) -> list[list[float]]:
    """Generates N waypoints in a circle, ending back at start."""
    radius_deg = distance_km / 111.0
    n = 4
    points = [[lon, lat]]
    for i in range(1, n + 1):
        angle = 2 * math.pi * i / n
        wp_lon = lon + radius_deg * math.cos(angle)
        wp_lat = lat + radius_deg * math.sin(angle)
        points.append([wp_lon, wp_lat])
    points.append([lon, lat])
    return points


async def get_circular_route(
    lat: float,
    lon: float,
    duration_min: int,
    curviness: Literal["kurvenreich", "sehr_kurvenreich"],
) -> dict:
    speed = _SPEED_KMH[curviness]
    distance_km = round(speed * duration_min / 60, 1)
    waypoints = _circular_waypoints(lat, lon, distance_km)

    payload = {
        "points": waypoints,
        "profile": "auto",
        "points_encoded": False,
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(f"{GRAPHHOPPER_URL}/route", json=payload)
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"GraphHopper nicht erreichbar: {exc}") from exc

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"GraphHopper Fehler {response.status_code}: {response.text}",
        )

    gh_data = response.json()
    path = gh_data["paths"][0]
    actual_distance_km = round(path["distance"] / 1000, 1)

    return {
        "id": f"{curviness}-{duration_min}",
        "duration_min": duration_min,
        "distance_km": actual_distance_km,
        "geometry": path["points"],
    }
