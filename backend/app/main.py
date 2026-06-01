import os
import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="fun-nav API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GRAPHHOPPER_URL = os.getenv("GRAPHHOPPER_URL", "http://localhost:8989")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/routes")
async def get_routes(
    from_lat: float = Query(...),
    from_lon: float = Query(...),
    to_lat: float = Query(...),
    to_lon: float = Query(...),
):
    params = {
        "point": [f"{from_lat},{from_lon}", f"{to_lat},{to_lon}"],
        "profile": "car",
        "algorithm": "alternative_route",
        "alternative_route.max_paths": 3,
        "ch.disable": "true",
        "points_encoded": "false",
        "type": "json",
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{GRAPHHOPPER_URL}/route", params=params)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"GraphHopper nicht erreichbar: {e}")

    data = response.json()
    routes = []
    for path in data.get("paths", []):
        coords_lonlat = path["points"]["coordinates"]
        coords_latlon = [[lat, lon] for lon, lat in coords_lonlat]
        routes.append(
            {
                "coordinates": coords_latlon,
                "distance_m": path["distance"],
                "duration_ms": path["time"],
            }
        )

    return {"routes": routes}
