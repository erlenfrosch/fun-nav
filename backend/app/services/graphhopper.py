import os
from typing import Tuple

import httpx

_DEFAULT_URL = os.getenv("GRAPHHOPPER_URL", "http://graphhopper:8989")

CUSTOM_MODELS: dict[str, dict] = {
    "kurvenreich": {
        "priority": [
            {"if": "curvature < 0.7", "multiply_by": 1.5},
            {"if": "road_class == MOTORWAY", "multiply_by": 0.1},
        ]
    },
    "sehr_kurvenreich": {
        "priority": [
            {"if": "curvature < 0.4", "multiply_by": 3.0},
            {"if": "road_class == MOTORWAY || road_class == TRUNK", "multiply_by": 0.05},
        ]
    },
}


async def route_curvy(
    start: Tuple[float, float],
    end: Tuple[float, float],
    mode: str,
    base_url: str = _DEFAULT_URL,
) -> dict:
    """Route from start to end using a curviness custom model.

    Args:
        start: (lat, lon) of the starting point.
        end:   (lat, lon) of the destination.
        mode:  One of 'kurvenreich' or 'sehr_kurvenreich'.
        base_url: GraphHopper base URL.

    Returns:
        The raw GraphHopper JSON response.

    Raises:
        ValueError: For unknown mode.
        httpx.HTTPStatusError: On non-2xx GraphHopper responses.
    """
    if mode not in CUSTOM_MODELS:
        raise ValueError(f"Unbekannter Modus {mode!r}. Gültig: {list(CUSTOM_MODELS)}")

    payload = {
        "profile": "bike_custom",
        # GraphHopper expects [lon, lat] order
        "points": [[start[1], start[0]], [end[1], end[0]]],
        "custom_model": CUSTOM_MODELS[mode],
        "calc_points": True,
        "instructions": False,
        "points_encoded": False,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/route", json=payload)
        response.raise_for_status()
        return response.json()
