import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.services.circular_route import generate_circular_routes

app = FastAPI(title="fun-nav API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GRAPHHOPPER_URL = os.getenv("GRAPHHOPPER_URL", "http://graphhopper:8989")


@app.get("/health")
def health():
    return {"status": "ok"}


class CircularRouteRequest(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    duration_min: float = Field(..., gt=0, le=480)


@app.post("/api/circular-routes")
async def circular_routes(request: CircularRouteRequest):
    routes = await generate_circular_routes(
        lat=request.lat,
        lon=request.lon,
        duration_min=request.duration_min,
        graphhopper_url=GRAPHHOPPER_URL,
    )
    return {"routes": routes}
