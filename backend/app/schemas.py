from pydantic import BaseModel


class Coordinate(BaseModel):
    lat: float
    lng: float


class RouteRequest(BaseModel):
    start: Coordinate
    end: Coordinate
    profile: str = "car"


class RouteResponse(BaseModel):
    distance: float
    duration: float
    points: str
