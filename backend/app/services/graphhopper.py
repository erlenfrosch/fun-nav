import os

import httpx
from fastapi import HTTPException

GRAPHHOPPER_URL = os.getenv("GRAPHHOPPER_URL", "http://localhost:8989")

CUSTOM_MODELS: dict[str, dict] = {
    "high": {
        "priority": [
            {"if": "curvature < 0.7", "multiply_by": "1.5"},
            {"if": "road_class == MOTORWAY", "multiply_by": "0.1"},
        ]
    },
    "very_high": {
        "priority": [
            {"if": "curvature < 0.4", "multiply_by": "3.0"},
            {"if": "road_class == MOTORWAY || road_class == TRUNK", "multiply_by": "0.05"},
        ]
    },
}


async def query_route(points: list[list[float]], curviness: str) -> dict:
    payload = {
        "points": points,
        "profile": "car_custom",
        "custom_model": CUSTOM_MODELS[curviness],
        "instructions": True,
        "points_encoded": False,
    }
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(f"{GRAPHHOPPER_URL}/route", json=payload)
    except httpx.ConnectError as exc:
        raise HTTPException(status_code=503, detail="GraphHopper nicht erreichbar") from exc
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=503, detail="GraphHopper Timeout") from exc

    if resp.status_code != 200:
        raise HTTPException(
            status_code=503,
            detail=f"GraphHopper Fehler {resp.status_code}: {resp.text[:200]}",
        )

    return resp.json()
