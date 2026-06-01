import asyncio
import os
from typing import List

import httpx
from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    CircularRouteRequest,
    CircularRouteResponse,
    GeoJsonLineString,
    RouteInstruction,
    RouteResult,
)

router = APIRouter(prefix="/api/routes", tags=["routes"])

GRAPHHOPPER_URL = os.getenv("GRAPHHOPPER_URL", "http://graphhopper:8989")

_SPEED_M_PER_MIN: dict = {
    "high": 250.0,
    "very_high": 200.0,
}

_NUM_ROUTES = 3


async def _fetch_route(
    client: httpx.AsyncClient,
    lat: float,
    lon: float,
    distance_m: float,
    seed: int,
) -> dict:
    payload = {
        "points": [[lon, lat]],
        "profile": "bike",
        "algorithm": "round_trip",
        "round_trip.distance": distance_m,
        "round_trip.seed": seed,
        "points_encoded": False,
        "instructions": True,
    }
    response = await client.post(
        f"{GRAPHHOPPER_URL}/route",
        json=payload,
        timeout=10.0,
    )
    response.raise_for_status()
    return response.json()


def _parse_path(path: dict, route_id: str) -> RouteResult:
    coords = path["points"]["coordinates"]
    return RouteResult(
        id=route_id,
        duration_min=round(path["time"] / 60_000, 1),
        distance_km=round(path["distance"] / 1000, 1),
        geojson=GeoJsonLineString(type="LineString", coordinates=coords),
        instructions=[
            RouteInstruction(text=i.get("text", ""), distance=i.get("distance", 0.0))
            for i in path.get("instructions", [])
        ],
    )


@router.post("/circular", response_model=CircularRouteResponse)
async def post_circular_route(body: CircularRouteRequest) -> CircularRouteResponse:
    distance_m = body.duration_min * _SPEED_M_PER_MIN[body.curviness.value]

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *[
                _fetch_route(client, body.lat, body.lon, distance_m, seed)
                for seed in range(_NUM_ROUTES)
            ],
            return_exceptions=True,
        )

    routes: List[RouteResult] = []

    for i, result in enumerate(results):
        if isinstance(result, httpx.ConnectError):
            raise HTTPException(status_code=503, detail="GraphHopper nicht erreichbar")
        if isinstance(result, Exception):
            continue
        paths = result.get("paths", [])
        if paths:
            routes.append(_parse_path(paths[0], f"route_{i + 1}"))

    if not routes:
        raise HTTPException(status_code=404, detail="Keine Routen gefunden")

    return CircularRouteResponse(routes=routes)
