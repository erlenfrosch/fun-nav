from typing import Annotated, Any
from enum import Enum

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

from app.routing import fetch_route, RoutingMode

app = FastAPI(title="fun-nav API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

VALID_PROFILES = {"car", "bike", "foot"}


class RouteRequest(BaseModel):
    points: list[list[float]]
    profile: str
    mode: RoutingMode = RoutingMode.fastest

    @field_validator("points")
    @classmethod
    def at_least_two_points(cls, v: list[list[float]]) -> list[list[float]]:
        if len(v) < 2:
            raise ValueError("at least two points required")
        return v

    @field_validator("profile")
    @classmethod
    def valid_profile(cls, v: str) -> str:
        if v not in VALID_PROFILES:
            raise ValueError(f"profile must be one of {sorted(VALID_PROFILES)}")
        return v


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/route")
async def route(request: RouteRequest) -> dict[str, Any]:
    return await fetch_route(request.points, request.profile, request.mode)
