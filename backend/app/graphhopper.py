import httpx
from .config import GRAPHHOPPER_URL


async def get_route(
    start_lat: float,
    start_lng: float,
    end_lat: float,
    end_lng: float,
    profile: str = "car",
) -> dict:
    params = [
        ("point", f"{start_lat},{start_lng}"),
        ("point", f"{end_lat},{end_lng}"),
        ("profile", profile),
        ("type", "json"),
    ]
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GRAPHHOPPER_URL}/route", params=params)
        response.raise_for_status()
        return response.json()
