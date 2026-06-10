import os
import httpx

GRAPHHOPPER_URL = os.getenv("GRAPHHOPPER_URL", "http://localhost:8989")


async def check_health() -> bool:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{GRAPHHOPPER_URL}/health")
            return response.status_code == 200
    except httpx.RequestError:
        return False
