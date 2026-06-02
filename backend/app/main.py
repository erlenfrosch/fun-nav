import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.services.circular_route import Route, generate_circular_routes

GRAPHHOPPER_URL = os.getenv("GRAPHHOPPER_URL", "http://localhost:8989")

app = FastAPI(title="fun-nav API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


class RouteRequest(BaseModel):
    lat: float = Field(..., description="Start-Breitengrad")
    lon: float = Field(..., description="Start-Längengrad")
    fahrtzeit_min: float = Field(..., gt=0, description="Gewünschte Fahrtzeit in Minuten")
    profile: str = Field("car", description="GraphHopper-Profil")


class RouteResponse(BaseModel):
    coordinates: list
    distance_km: float
    duration_min: float
    curviness_score: float


@app.post("/routes", response_model=list[RouteResponse])
async def get_routes(request: RouteRequest):
    routes: list[Route] = await generate_circular_routes(
        lat=request.lat,
        lon=request.lon,
        fahrtzeit_min=request.fahrtzeit_min,
        graphhopper_url=GRAPHHOPPER_URL,
        profile=request.profile,
    )
    if not routes:
        raise HTTPException(status_code=404, detail="Keine Routen gefunden")
    return [RouteResponse(**r._asdict()) for r in routes]
