import os

import httpx

GRAPHHOPPER_URL = os.getenv("GRAPHHOPPER_URL", "http://localhost:8989")


class GraphHopperClient:
    def __init__(self, base_url: str = GRAPHHOPPER_URL):
        self.base_url = base_url.rstrip("/")

    async def route(self, points: list[list[float]], profile: str = "car") -> dict:
        payload = {
            "points": points,
            "profile": profile,
            "points_encoded": False,
        }
        async with httpx.AsyncClient() as http:
            response = await http.post(
                f"{self.base_url}/route",
                json=payload,
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()


graphhopper_client = GraphHopperClient()
