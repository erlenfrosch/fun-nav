import os
from typing import Literal

import httpx

GRAPHHOPPER_BASE_URL = os.getenv("GRAPHHOPPER_URL", "http://graphhopper:8989")

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

CurvyMode = Literal["kurvenreich", "sehr_kurvenreich"]


def build_route_request(points: list[list[float]], mode: CurvyMode) -> dict:
    if mode not in CUSTOM_MODELS:
        raise ValueError(f"Unbekannter Modus {mode!r}. Gültig: {list(CUSTOM_MODELS)}")
    return {
        "points": points,
        "profile": "bike_custom",
        "ch.disable": True,
        "custom_model": CUSTOM_MODELS[mode],
    }


def route(points: list[list[float]], mode: CurvyMode, base_url: str = GRAPHHOPPER_BASE_URL) -> dict:
    payload = build_route_request(points, mode)
    response = httpx.post(f"{base_url}/route", json=payload, timeout=30.0)
    response.raise_for_status()
    return response.json()


def get_route(
    start: list[float],
    end: list[float],
    mode: CurvyMode,
    base_url: str = GRAPHHOPPER_BASE_URL,
) -> dict:
    return route([start, end], mode, base_url)
