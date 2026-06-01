import os
from fastapi import APIRouter, HTTPException
import httpx

from app.models.schemas import (
    CircularRouteRequest,
    CircularRouteResponse,
    Route,
    GeoJSON,
    Instruction,
)

router = APIRouter(prefix="/api/routes", tags=["routes"])

GRAPHHOPPER_URL = os.getenv("GRAPHHOPPER_URL", "http://localhost:8989")
NUM_ROUTES = 3

CURVINESS_M_PER_MIN = {
    "high": 250,
    "very_high": 167,
}


@router.post("/circular", response_model=CircularRouteResponse)
async def circular_route(req: CircularRouteRequest) -> CircularRouteResponse:
    distance_m = int(req.duration_min * CURVINESS_M_PER_MIN.get(req.curviness, 250))

    routes: list[Route] = []
    async with httpx.AsyncClient(timeout=30.0) as client:
        for seed in range(NUM_ROUTES):
            params = {
                "point": f"{req.lat},{req.lon}",
                "profile": "bike",
                "algorithm": "round_trip",
                "round_trip.distance": distance_m,
                "round_trip.seed": seed,
                "locale": "de",
                "calc_points": "true",
                "instructions": "true",
                "points_encoded": "false",
            }
            try:
                resp = await client.get(f"{GRAPHHOPPER_URL}/route", params=params)
            except httpx.ConnectError as exc:
                raise HTTPException(
                    status_code=503, detail="GraphHopper nicht erreichbar"
                ) from exc

            if resp.status_code != 200:
                raise HTTPException(
                    status_code=503, detail=f"GraphHopper-Fehler: {resp.status_code}"
                )

            data = resp.json()
            paths = data.get("paths", [])
            if not paths:
                raise HTTPException(status_code=404, detail="Keine Route gefunden")

            path = paths[0]
            routes.append(
                Route(
                    id=f"route_{seed + 1}",
                    duration_min=round(path["time"] / 60_000, 1),
                    distance_km=round(path["distance"] / 1_000, 1),
                    geojson=GeoJSON(**path["points"]),
                    instructions=[
                        Instruction(
                            text=instr.get("text", ""),
                            distance=instr.get("distance", 0.0),
                        )
                        for instr in path.get("instructions", [])
                    ],
                )
            )

    return CircularRouteResponse(routes=routes)
