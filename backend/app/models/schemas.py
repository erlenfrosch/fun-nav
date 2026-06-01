from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class Curviness(str, Enum):
    high = "high"
    very_high = "very_high"


class CircularRouteRequest(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    duration_min: float = Field(..., gt=0)
    curviness: Curviness


class RouteInstruction(BaseModel):
    text: str
    distance: float


class GeoJsonLineString(BaseModel):
    type: str = "LineString"
    coordinates: List[List[float]]


class RouteResult(BaseModel):
    id: str
    duration_min: float
    distance_km: float
    geojson: GeoJsonLineString
    instructions: List[RouteInstruction]


class CircularRouteResponse(BaseModel):
    routes: List[RouteResult]
