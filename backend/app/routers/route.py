import httpx
from fastapi import APIRouter, HTTPException
from ..schemas import RouteRequest, RouteResponse
from ..graphhopper import get_route

router = APIRouter(tags=["route"])


@router.post("/route", response_model=RouteResponse)
async def route(request: RouteRequest):
    try:
        data = await get_route(
            request.start.lat,
            request.start.lng,
            request.end.lat,
            request.end.lng,
            request.profile,
        )
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    if not data.get("paths"):
        raise HTTPException(status_code=404, detail="Keine Route gefunden")

    path = data["paths"][0]
    return RouteResponse(
        distance=path["distance"],
        duration=path["time"],
        points=path["points"],
    )
