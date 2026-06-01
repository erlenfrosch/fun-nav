from fastapi import APIRouter

from app.models.schemas import CircularRouteRequest, CircularRouteResponse
from app.services.circular_route import generate_circular_routes

router = APIRouter(prefix="/api/routes", tags=["routes"])


@router.post("/circular", response_model=CircularRouteResponse)
async def post_circular_route(request: CircularRouteRequest) -> CircularRouteResponse:
    routes = await generate_circular_routes(
        lat=request.lat,
        lon=request.lon,
        duration_min=request.duration_min,
        curviness=request.curviness,
    )
    return CircularRouteResponse(routes=routes)
