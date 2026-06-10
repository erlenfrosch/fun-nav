import math
from fastapi import APIRouter
from app.models.routes import CircularRouteRequest, CircularRouteResponse, RouteOption, RouteGeometry

router = APIRouter(prefix="/api/routes")


@router.post("/circular", response_model=CircularRouteResponse)
def calculate_circular_route(body: CircularRouteRequest) -> CircularRouteResponse:
    avg_speed_kmh = 40 if body.curviness == "sehr_kurvenreich" else 50
    distance_km = round(avg_speed_kmh * body.duration_min / 60, 1)

    radius_deg = distance_km / 111.0
    steps = 8
    coordinates = [
        [
            body.lon + radius_deg * math.cos(2 * math.pi * i / steps),
            body.lat + radius_deg * math.sin(2 * math.pi * i / steps),
        ]
        for i in range(steps + 1)
    ]

    return CircularRouteResponse(
        routes=[
            RouteOption(
                id=f"{body.curviness}-{body.duration_min}",
                duration_min=body.duration_min,
                distance_km=distance_km,
                geometry=RouteGeometry(type="LineString", coordinates=coordinates),
            )
        ]
    )
