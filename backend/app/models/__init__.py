from pydantic import BaseModel
from typing import Literal


class CircularRouteRequest(BaseModel):
    lat: float
    lon: float
    duration_min: int
    curviness: Literal["kurvenreich", "sehr_kurvenreich"]


class RouteGeometry(BaseModel):
    type: str
    coordinates: list


class Route(BaseModel):
    id: str
    duration_min: int
    distance_km: float
    geometry: RouteGeometry


class CircularRouteResponse(BaseModel):
    routes: list[Route]
