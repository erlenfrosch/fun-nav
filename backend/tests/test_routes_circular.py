import httpx
import pytest
import respx
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport, Response

from app.main import app

client = TestClient(app)

_GH_URL = "http://graphhopper:8989/route"

_MOCK_PATH = {
    "distance": 47200.0,
    "time": 3_498_000,
    "points": {
        "type": "LineString",
        "coordinates": [[11.575, 48.137], [11.600, 48.150], [11.575, 48.137]],
    },
    "instructions": [
        {"text": "Links abbiegen", "distance": 320.0},
        {"text": "Ziel erreicht", "distance": 0.0},
    ],
}

_VALID_BODY = {"lat": 48.137, "lon": 11.575, "duration_min": 60, "curviness": "high"}


@respx.mock
def test_circular_returns_three_routes():
    respx.post(_GH_URL).mock(return_value=Response(200, json={"paths": [_MOCK_PATH]}))

    resp = client.post("/api/routes/circular", json=_VALID_BODY)

    assert resp.status_code == 200
    data = resp.json()
    assert len(data["routes"]) == 3
    for i, route in enumerate(data["routes"]):
        assert route["id"] == f"route_{i + 1}"
        assert route["geojson"]["type"] == "LineString"
        assert len(route["geojson"]["coordinates"]) > 0
        assert route["duration_min"] == pytest.approx(58.3, abs=0.1)
        assert route["distance_km"] == pytest.approx(47.2, abs=0.1)
        assert len(route["instructions"]) == 2


@respx.mock
def test_route_response_schema():
    respx.post(_GH_URL).mock(return_value=Response(200, json={"paths": [_MOCK_PATH]}))

    resp = client.post("/api/routes/circular", json=_VALID_BODY)
    route = resp.json()["routes"][0]

    assert route["id"] == "route_1"
    assert route["duration_min"] == pytest.approx(58.3, abs=0.1)
    assert route["distance_km"] == pytest.approx(47.2, abs=0.1)
    assert route["geojson"]["type"] == "LineString"
    assert len(route["geojson"]["coordinates"]) == 3
    assert route["instructions"][0]["text"] == "Links abbiegen"
    assert route["instructions"][0]["distance"] == 320.0


@respx.mock
def test_circular_very_high_curviness():
    respx.post(_GH_URL).mock(return_value=Response(200, json={"paths": [_MOCK_PATH]}))

    resp = client.post(
        "/api/routes/circular",
        json={**_VALID_BODY, "curviness": "very_high"},
    )

    assert resp.status_code == 200
    assert len(resp.json()["routes"]) == 3


@respx.mock
def test_circular_503_when_graphhopper_down():
    respx.post(_GH_URL).mock(side_effect=httpx.ConnectError("Connection refused"))

    resp = client.post("/api/routes/circular", json=_VALID_BODY)

    assert resp.status_code == 503
    assert "GraphHopper" in resp.json()["detail"]


@respx.mock
def test_circular_404_when_no_routes_found():
    respx.post(_GH_URL).mock(return_value=Response(200, json={"paths": []}))

    resp = client.post("/api/routes/circular", json=_VALID_BODY)

    assert resp.status_code == 404


def test_circular_rejects_invalid_curviness():
    resp = client.post(
        "/api/routes/circular",
        json={**_VALID_BODY, "curviness": "low"},
    )

    assert resp.status_code == 422


def test_circular_rejects_missing_fields():
    resp = client.post("/api/routes/circular", json={"lat": 48.137})

    assert resp.status_code == 422


@pytest.mark.integration
@pytest.mark.asyncio
async def test_integration_three_routes_with_geojson():
    """Benötigt laufenden GraphHopper. Ausführen mit: pytest -m integration"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.post(
            "/api/routes/circular",
            json=_VALID_BODY,
            timeout=10.0,
        )

    assert resp.status_code == 200
    data = resp.json()
    assert len(data["routes"]) == 3
    for route in data["routes"]:
        assert route["geojson"]["type"] == "LineString"
        assert len(route["geojson"]["coordinates"]) > 2
        assert route["duration_min"] > 0
        assert route["distance_km"] > 0
