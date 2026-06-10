from pydantic import BaseModel
from typing import Literal


class CircularRouteRequest(BaseModel):
    lat: float
    lon: float
    duration_min: int
    curviness: Literal["kurvenreich", "sehr_kurvenreich"]
