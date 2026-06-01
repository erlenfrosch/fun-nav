import pytest
import httpx
import respx
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def make_gh_path(duration_ms: int = 3_500_000, distance_m: int = 47_000) -> dict:
    return {
        "paths": [
            {
                "distance": distance_m,
                "time": duration_ms,
                "points": {
                    "type": "LineString",
                    "coordinates": [
                        [11.575, 48.137],
                        [11.610, 48.160],
                        [11.640, 48.140],
                        [11.575, 48.137],
                    ],
                },
                "instructions": [
                    {"text": "Links abbiegen", "distance": 320},
                    {"text": "Ziel erreicht", "distance": 0},
                ],
            }
        ]
    }
