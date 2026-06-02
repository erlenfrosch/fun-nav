from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import httpx

from services.graphhopper import route as gh_route, CUSTOM_MODELS

app = FastAPI(title="fun-nav API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

VALID_MODES = set(CUSTOM_MODELS.keys())


class RouteRequest(BaseModel):
    points: list[list[float]]
    mode: str

    @field_validator("points")
    @classmethod
    def at_least_two_points(cls, v: list[list[float]]) -> list[list[float]]:
        if len(v) < 2:
            raise ValueError("at least two points required")
        return v

    @field_validator("mode")
    @classmethod
    def valid_mode(cls, v: str) -> str:
        if v not in VALID_MODES:
            raise ValueError(f"mode must be one of {sorted(VALID_MODES)}")
        return v


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/route")
def route(request: RouteRequest) -> dict[str, Any]:
    try:
        return gh_route(request.points, request.mode)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
