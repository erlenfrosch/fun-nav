from pydantic import BaseModel, Field


class CircularRouteRequest(BaseModel):
    lat: float = Field(..., description="Startpunkt Breitengrad")
    lng: float = Field(..., description="Startpunkt Längengrad")
    duration_min: float = Field(..., gt=0, description="Gewünschte Fahrtzeit in Minuten")


class WaypointModel(BaseModel):
    lat: float
    lng: float


class CircularRouteResponse(BaseModel):
    duration_min: float
    distance_km: float
    waypoint: WaypointModel
    curviness_score: float
