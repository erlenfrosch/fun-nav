"""Tests für POST /api/routes/circular.

Unit-Tests: httpx-Client via unittest.mock gepatcht.
Integration-Tests: echtes GraphHopper, markiert mit @pytest.mark.integration
"""
import os
import sys
import pytest
import httpx
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.main import app


GH_ROUTE_RESPONSE = {
    "paths": [
        {
            "time": 3498000,
            "distance": 47200.0,
            "points": {
                "type": "LineString",
                "coordinates": [[11.575, 48.137], [11.580, 48.140], [11.575, 48.137]],
            },
            "instructions": [
                {"text": "Links abbiegen", "distance": 320.0},
                {"text": "Ziel erreicht", "distance": 0.0},
            ],
        }
    ]
}


@pytest.mark.asyncio
async def test_circular_returns_three_routes():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = GH_ROUTE_RESPONSE

    with patch("app.routers.routes.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            resp = await ac.post(
                "/api/routes/circular",
                json={"lat": 48.137, "lon": 11.575, "duration_min": 60, "curviness": "high"},
            )

    assert resp.status_code == 200
    data = resp.json()
    assert len(data["routes"]) == 3
    assert data["routes"][0]["id"] == "route_1"
    assert data["routes"][2]["id"] == "route_3"


@pytest.mark.asyncio
async def test_route_response_schema():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = GH_ROUTE_RESPONSE

    with patch("app.routers.routes.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            resp = await ac.post(
                "/api/routes/circular",
                json={"lat": 48.137, "lon": 11.575, "duration_min": 60, "curviness": "high"},
            )

    route = resp.json()["routes"][0]
    assert route["id"] == "route_1"
    assert route["duration_min"] == 58.3
    assert route["distance_km"] == 47.2
    assert route["geojson"]["type"] == "LineString"
    assert len(route["geojson"]["coordinates"]) == 3
    assert route["instructions"][0]["text"] == "Links abbiegen"
    assert route["instructions"][0]["distance"] == 320.0


@pytest.mark.asyncio
async def test_very_high_curviness_accepted():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = GH_ROUTE_RESPONSE

    with patch("app.routers.routes.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            resp = await ac.post(
                "/api/routes/circular",
                json={"lat": 48.137, "lon": 11.575, "duration_min": 60, "curviness": "very_high"},
            )

    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_503_when_graphhopper_unreachable():
    with patch("app.routers.routes.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            side_effect=httpx.ConnectError("Connection refused")
        )
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            resp = await ac.post(
                "/api/routes/circular",
                json={"lat": 48.137, "lon": 11.575, "duration_min": 60, "curviness": "high"},
            )

    assert resp.status_code == 503


@pytest.mark.asyncio
async def test_404_when_no_route_found():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"paths": []}

    with patch("app.routers.routes.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            resp = await ac.post(
                "/api/routes/circular",
                json={"lat": 48.137, "lon": 11.575, "duration_min": 60, "curviness": "high"},
            )

    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_invalid_curviness_returns_422():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.post(
            "/api/routes/circular",
            json={"lat": 48.137, "lon": 11.575, "duration_min": 60, "curviness": "medium"},
        )
    assert resp.status_code == 422


@pytest.mark.integration
@pytest.mark.asyncio
async def test_integration_three_routes_with_geojson():
    """Benötigt laufenden GraphHopper. Ausführen mit: pytest -m integration"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.post(
            "/api/routes/circular",
            json={"lat": 48.137, "lon": 11.575, "duration_min": 60, "curviness": "high"},
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
