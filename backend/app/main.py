import os
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="fun-nav API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GRAPHHOPPER_URL = os.getenv("GRAPHHOPPER_URL", "http://localhost:8989")

MOCK_ROUTES = {
    "routes": [
        {
            "distance": 8750,
            "duration": 1050,
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [9.5209, 47.1410],
                    [9.5230, 47.1430],
                    [9.5260, 47.1470],
                    [9.5240, 47.1530],
                    [9.5190, 47.1580],
                    [9.5150, 47.1630],
                    [9.5097, 47.1673],
                ],
            },
        },
        {
            "distance": 11200,
            "duration": 1320,
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [9.5209, 47.1410],
                    [9.5170, 47.1420],
                    [9.5130, 47.1460],
                    [9.5110, 47.1510],
                    [9.5090, 47.1560],
                    [9.5070, 47.1620],
                    [9.5097, 47.1673],
                ],
            },
        },
        {
            "distance": 9800,
            "duration": 1140,
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [9.5209, 47.1410],
                    [9.5200, 47.1450],
                    [9.5180, 47.1500],
                    [9.5160, 47.1550],
                    [9.5130, 47.1610],
                    [9.5097, 47.1673],
                ],
            },
        },
    ]
}


def _parse_graphhopper_routes(data: dict) -> dict:
    routes = []
    for path in data.get("paths", [])[:3]:
        coords = [
            [pt[0], pt[1]]
            for pt in path.get("points", {}).get("coordinates", [])
        ]
        routes.append(
            {
                "distance": path.get("distance", 0),
                "duration": path.get("time", 0) / 1000,
                "geometry": {"type": "LineString", "coordinates": coords},
            }
        )
    return {"routes": routes}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/routes")
async def get_routes(
    from_lat: float = 47.1410,
    from_lng: float = 9.5209,
    to_lat: float = 47.1673,
    to_lng: float = 9.5097,
):
    params = {
        "point": [f"{from_lat},{from_lng}", f"{to_lat},{to_lng}"],
        "algorithm": "alternative_route",
        "alternative_route.max_paths": 3,
        "type": "json",
        "points_encoded": False,
    }
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{GRAPHHOPPER_URL}/route", params=params)
            resp.raise_for_status()
            data = _parse_graphhopper_routes(resp.json())
            if data["routes"]:
                return data
    except Exception:
        pass
    return MOCK_ROUTES
