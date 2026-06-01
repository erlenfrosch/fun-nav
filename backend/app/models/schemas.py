from enum import Enum
from typing import Any, List

from pydantic import BaseModel, Field


class Curviness(str, Enum):
    high = "high"
    very_high = "very_high"


class CircularRouteRequest(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    duration_min: float = Field(..., gt=0, le=480)
    curviness: Curviness


class GeoJSONLineString(BaseModel):
    type: str = "LineString"
    coordinates: List[Any]


class GeoJSON(BaseModel):
    type: str
    coordinates: List[Any]


class Instruction(BaseModel):
    text: str
    distance: float


class Route(BaseModel):
    id: str
    duration_min: float
    distance_km: float
    geojson: GeoJSON
    instructions: List[Instruction]


class CircularRouteResponse(BaseModel):
    routes: List[Route]
