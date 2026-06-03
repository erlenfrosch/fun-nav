import os
import httpx

GRAPHHOPPER_BASE_URL = os.getenv("GRAPHHOPPER_URL", "http://graphhopper:8989")

CUSTOM_MODELS = {
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


def build_route_request(points: list, mode: str) -> dict:
    if mode not in CUSTOM_MODELS:
        raise ValueError(f"Unknown mode: {mode!r}. Must be one of {list(CUSTOM_MODELS)}")
    return {
        "points": points,
        "profile": "car_custom",
        "ch.disable": True,
        "custom_model": CUSTOM_MODELS[mode],
    }


def route(points: list, mode: str, base_url: str = GRAPHHOPPER_BASE_URL) -> dict:
    payload = build_route_request(points, mode)
    response = httpx.post(f"{base_url}/route", json=payload, timeout=30.0)
    response.raise_for_status()
    return response.json()
