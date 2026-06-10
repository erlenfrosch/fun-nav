import math
from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/routes", tags=["routes"])


class CircularRouteRequest(BaseModel):
    lat: float
    lon: float
    duration_min: int
    curviness: Literal["kurvenreich", "sehr_kurvenreich"]


def _placeholder_geometry(lat: float, lon: float, distance_km: float) -> dict:
    radius_deg = distance_km / 111.0
    steps = 8
    coordinates = [
        [
            lon + radius_deg * math.cos(2 * math.pi * i / steps),
            lat + radius_deg * math.sin(2 * math.pi * i / steps),
        ]
        for i in range(steps + 1)
    ]
    return {"type": "LineString", "coordinates": coordinates}


@router.post("/circular")
def calculate_circular_route(body: CircularRouteRequest):
    avg_speed_kmh = 40 if body.curviness == "sehr_kurvenreich" else 50
    distance_km = round(avg_speed_kmh * body.duration_min / 60, 1)

    return {
        "routes": [
            {
                "id": f"{body.curviness}-{body.duration_min}",
                "duration_min": body.duration_min,
                "distance_km": distance_km,
                "geometry": _placeholder_geometry(body.lat, body.lon, distance_km),
            }
        ]
    }
