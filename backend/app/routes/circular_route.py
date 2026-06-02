from fastapi import APIRouter, HTTPException

from ..models.route import CircularRouteRequest, CircularRouteResponse
from ..services.circular_route import generate_circular_routes

router = APIRouter(prefix="/api", tags=["routing"])


@router.post("/circular-routes", response_model=list[CircularRouteResponse])
async def create_circular_routes(req: CircularRouteRequest):
    routes = await generate_circular_routes(req.lat, req.lng, req.duration_min)
    if not routes:
        raise HTTPException(status_code=404, detail="Keine passenden Routen gefunden")
    return routes
