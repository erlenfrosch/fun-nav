from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
import math

app = FastAPI(title="fun-nav API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CircularRouteRequest(BaseModel):
    lat: float
    lon: float
    duration_min: int
    curviness: Literal["kurvenreich", "sehr_kurvenreich"]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/routes/circular")
def calculate_circular_route(body: CircularRouteRequest):
    avg_speed_kmh = 40 if body.curviness == "sehr_kurvenreich" else 50
    distance_km = round(avg_speed_kmh * body.duration_min / 60, 1)

    # Einfacher Kreispfad als Platzhalter-Geometrie (wird durch GraphHopper ersetzt)
    radius_deg = distance_km / 111.0
    steps = 8
    coordinates = [
        [
            body.lon + radius_deg * math.cos(2 * math.pi * i / steps),
            body.lat + radius_deg * math.sin(2 * math.pi * i / steps),
        ]
        for i in range(steps + 1)
    ]

    return {
        "routes": [
            {
                "id": f"{body.curviness}-{body.duration_min}",
                "duration_min": body.duration_min,
                "distance_km": distance_km,
                "geometry": {"type": "LineString", "coordinates": coordinates},
            }
        ]
    }
