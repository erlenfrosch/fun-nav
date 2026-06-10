from fastapi import APIRouter
from app.models.requests import CircularRouteRequest
from app.services.routing import calculate_circular_route

router = APIRouter(prefix="/api/routes")


@router.post("/circular")
def circular_route(body: CircularRouteRequest):
    return calculate_circular_route(body)
