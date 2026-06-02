import os
from enum import Enum
from typing import Any

import httpx
from fastapi import HTTPException

GRAPHHOPPER_URL = os.getenv("GRAPHHOPPER_URL", "http://localhost:8989")

PROFILES_WITH_CUSTOM = {"car", "bike"}


class RoutingMode(str, Enum):
    fastest = "fastest"
    kurvig = "kurvig"
    direkt = "direkt"


def build_custom_model(mode: RoutingMode) -> dict[str, Any] | None:
    if mode == RoutingMode.fastest:
        return None
    if mode == RoutingMode.kurvig:
        return {
            "priority": [
                {"if": "curvature < 0.3", "multiply_by": "3.0"},
                {"else_if": "curvature < 0.6", "multiply_by": "2.0"},
            ],
            "distance_influence": 50,
        }
    # direkt
    return {
        "priority": [
            {"if": "curvature < 0.3", "multiply_by": "0.1"},
            {"else_if": "curvature < 0.6", "multiply_by": "0.5"},
        ],
        "distance_influence": 0,
    }


def _resolve_profile(profile: str, mode: RoutingMode) -> str:
    if mode != RoutingMode.fastest and profile in PROFILES_WITH_CUSTOM:
        return f"{profile}_custom"
    return profile


async def fetch_route(
    points: list[list[float]],
    profile: str,
    mode: RoutingMode,
) -> dict[str, Any]:
    resolved_profile = _resolve_profile(profile, mode)
    custom_model = build_custom_model(mode)

    payload: dict[str, Any] = {
        "points": points,
        "profile": resolved_profile,
        "points_encoded": True,
    }
    if custom_model is not None:
        payload["custom_model"] = custom_model
        payload["ch.disable"] = True

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{GRAPHHOPPER_URL}/route",
            json=payload,
        )

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail=response.json())

    return response.json()
