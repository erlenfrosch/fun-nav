from enum import Enum

from pydantic import BaseModel, Field


class Curviness(str, Enum):
    high = "high"
    very_high = "very_high"


class CircularRouteRequest(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    duration_min: int = Field(..., gt=0, le=480)
    curviness: Curviness


class GeoJSONLineString(BaseModel):
    type: str = "LineString"
    coordinates: list[list[float]]


class Instruction(BaseModel):
    text: str
    distance: float


class Route(BaseModel):
    id: str
    duration_min: float
    distance_km: float
    geojson: GeoJSONLineString
    instructions: list[Instruction]


class CircularRouteResponse(BaseModel):
    routes: list[Route]
