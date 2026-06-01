import os
from typing import Literal

import httpx

GRAPHHOPPER_URL = os.getenv("GRAPHHOPPER_URL", "http://graphhopper:8989")

CURVY_MODEL = {
    "priority": [
        {"if": "curvature < 0.7", "multiply_by": 1.5},
        {"if": "road_class == MOTORWAY", "multiply_by": 0.1},
    ]
}

VERY_CURVY_MODEL = {
    "priority": [
        {"if": "curvature < 0.4", "multiply_by": 3.0},
        {"if": "road_class == MOTORWAY || road_class == TRUNK", "multiply_by": 0.05},
    ]
}

CurvyMode = Literal["kurvenreich", "sehr_kurvenreich"]

_MODELS: dict[str, dict] = {
    "kurvenreich": CURVY_MODEL,
    "sehr_kurvenreich": VERY_CURVY_MODEL,
}


def get_route(
    start: list[float],
    end: list[float],
    mode: CurvyMode,
    base_url: str = GRAPHHOPPER_URL,
) -> dict:
    if mode not in _MODELS:
        raise ValueError(f"Unbekannter Modus {mode!r}. Gültig: {list(_MODELS)}")

    payload = {
        "profile": "car_custom",
        "points": [start, end],
        "ch.disable": True,
        "custom_model": _MODELS[mode],
        "details": ["road_class", "curvature"],
    }
    with httpx.Client() as client:
        response = client.post(
            f"{base_url}/route",
            json=payload,
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()


def average_curvature(path: dict) -> float:
    segments: list = path.get("details", {}).get("curvature", [])
    if not segments:
        return 1.0
    total_length = sum(seg[1] - seg[0] for seg in segments)
    if total_length == 0:
        return 1.0
    weighted_sum = sum((seg[1] - seg[0]) * seg[2] for seg in segments)
    return weighted_sum / total_length
