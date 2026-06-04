import os
from typing import Literal

import httpx

GRAPHHOPPER_BASE_URL = os.getenv("GRAPHHOPPER_URL", "http://graphhopper:8989")
GRAPHHOPPER_URL = GRAPHHOPPER_BASE_URL  # Alias für Rückwärtskompatibilität

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

CUSTOM_MODELS: dict[str, dict] = {
    "kurvenreich": CURVY_MODEL,
    "sehr_kurvenreich": VERY_CURVY_MODEL,
}


def average_curvature(path: dict) -> float:
    segments: list = path.get("details", {}).get("curvature", [])
    if not segments:
        return 1.0
    total_length = sum(seg[1] - seg[0] for seg in segments)
    if total_length == 0:
        return 1.0
    weighted_sum = sum((seg[1] - seg[0]) * seg[2] for seg in segments)
    return weighted_sum / total_length


def build_route_request(points: list[list[float]], mode: CurvyMode) -> dict:
    if mode not in CUSTOM_MODELS:
        raise ValueError(f"Unbekannter Modus {mode!r}. Gültig: {list(CUSTOM_MODELS)}")
    return {
        "points": points,
        "profile": "bike_custom",
        "ch.disable": True,
        "custom_model": CUSTOM_MODELS[mode],
        "details": ["road_class", "curvature"],
    }


def route(points: list[list[float]], mode: CurvyMode, base_url: str = GRAPHHOPPER_BASE_URL) -> dict:
    payload = build_route_request(points, mode)
    with httpx.Client() as client:
        response = client.post(f"{base_url}/route", json=payload, timeout=30.0)
        response.raise_for_status()
        return response.json()


def get_route(
    start: list[float],
    end: list[float],
    mode: CurvyMode,
    base_url: str = GRAPHHOPPER_BASE_URL,
) -> dict:
    return route([start, end], mode, base_url)
