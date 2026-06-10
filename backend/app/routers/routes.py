from fastapi import APIRouter

from app.models import CircularRouteRequest, CircularRouteResponse
from app.services.graphhopper import get_circular_route

router = APIRouter(prefix="/api/routes", tags=["routes"])


@router.post("/circular", response_model=CircularRouteResponse)
async def circular_route(body: CircularRouteRequest):
    route = await get_circular_route(
        lat=body.lat,
        lon=body.lon,
        duration_min=body.duration_min,
        curviness=body.curviness,
    )
    return CircularRouteResponse(routes=[route])
