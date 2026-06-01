from pydantic import BaseModel
from typing import Literal, List, Any


class CircularRouteRequest(BaseModel):
    lat: float
    lon: float
    duration_min: float
    curviness: Literal["high", "very_high"]


class Instruction(BaseModel):
    text: str
    distance: float


class GeoJSON(BaseModel):
    type: str
    coordinates: List[Any]


class Route(BaseModel):
    id: str
    duration_min: float
    distance_km: float
    geojson: GeoJSON
    instructions: List[Instruction]


class CircularRouteResponse(BaseModel):
    routes: List[Route]
