import os

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="fun-nav API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GRAPHHOPPER_URL = os.getenv("GRAPHHOPPER_URL", "http://graphhopper:8989")


class RoundTripRequest(BaseModel):
    lat: float
    lng: float
    distance: int = 10000
    profile: str = "bike"
    seed: int = 0


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/round-trip")
async def round_trip(req: RoundTripRequest):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"{GRAPHHOPPER_URL}/route",
                params={
                    "point": f"{req.lat},{req.lng}",
                    "profile": req.profile,
                    "algorithm": "round_trip",
                    "round_trip.distance": req.distance,
                    "round_trip.seed": req.seed,
                    "ch.disable": "true",
                    "points_encoded": "false",
                },
                timeout=30.0,
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=502,
                detail=f"GraphHopper-Fehler: {e.response.text}",
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"GraphHopper nicht erreichbar: {str(e)}",
            )

    data = resp.json()
    if not data.get("paths"):
        raise HTTPException(
            status_code=502,
            detail="GraphHopper hat keine Route zurückgegeben",
        )

    path = data["paths"][0]
    return {
        "distance": path["distance"],
        "time": path["time"],
        "points": path["points"],
        "bbox": path.get("bbox"),
    }
