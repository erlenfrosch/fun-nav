from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import httpx

from app.services.graphhopper import CurvyMode, get_route as gh_route

app = FastAPI(title="fun-nav API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class RouteRequest(BaseModel):
    points: list[list[float]]
    mode: CurvyMode

    @field_validator("points")
    @classmethod
    def at_least_two_points(cls, v: list[list[float]]) -> list[list[float]]:
        if len(v) < 2:
            raise ValueError("at least two points required")
        return v


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/route")
def route(request: RouteRequest) -> dict[str, Any]:
    try:
        return gh_route(request.points[0], request.points[1], request.mode)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
