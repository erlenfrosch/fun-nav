import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport, Response
from app.main import app

TEST_TRANSPORT = ASGITransport(app=app)

GH_RESPONSE = {
    "paths": [
        {
            "distance": 12500.0,
            "time": 900000,
            "points": {
                "type": "LineString",
                "coordinates": [[9.52, 47.13], [9.53, 47.14], [9.54, 47.15]],
            },
        },
        {
            "distance": 13800.0,
            "time": 980000,
            "points": {
                "type": "LineString",
                "coordinates": [[9.52, 47.13], [9.55, 47.14], [9.54, 47.15]],
            },
        },
        {
            "distance": 15000.0,
            "time": 1100000,
            "points": {
                "type": "LineString",
                "coordinates": [[9.52, 47.13], [9.56, 47.13], [9.54, 47.15]],
            },
        },
    ]
}


@pytest.mark.anyio
async def test_routes_returns_up_to_three_routes():
    mock_response = Response(200, json=GH_RESPONSE)
    with patch("app.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value = mock_client

        async with AsyncClient(transport=TEST_TRANSPORT, base_url="http://test") as client:
            response = await client.get(
                "/routes",
                params={
                    "from_lat": 47.13,
                    "from_lon": 9.52,
                    "to_lat": 47.15,
                    "to_lon": 9.54,
                },
            )

    assert response.status_code == 200
    data = response.json()
    assert "routes" in data
    assert len(data["routes"]) == 3
    route = data["routes"][0]
    assert "coordinates" in route
    assert "distance_m" in route
    assert "duration_ms" in route
    assert route["distance_m"] == 12500.0
    assert route["duration_ms"] == 900000


@pytest.mark.anyio
async def test_routes_coordinates_are_lat_lon():
    mock_response = Response(200, json=GH_RESPONSE)
    with patch("app.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value = mock_client

        async with AsyncClient(transport=TEST_TRANSPORT, base_url="http://test") as client:
            response = await client.get(
                "/routes",
                params={
                    "from_lat": 47.13,
                    "from_lon": 9.52,
                    "to_lat": 47.15,
                    "to_lon": 9.54,
                },
            )

    data = response.json()
    coords = data["routes"][0]["coordinates"]
    assert coords[0] == [47.13, 9.52], "Koordinaten müssen [lat, lon] sein (für Leaflet)"


@pytest.mark.anyio
async def test_routes_graphhopper_unavailable_returns_502():
    import httpx

    with patch("app.main.httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.get = AsyncMock(side_effect=httpx.ConnectError("refused"))
        mock_client_cls.return_value = mock_client

        async with AsyncClient(transport=TEST_TRANSPORT, base_url="http://test") as client:
            response = await client.get(
                "/routes",
                params={
                    "from_lat": 47.13,
                    "from_lon": 9.52,
                    "to_lat": 47.15,
                    "to_lon": 9.54,
                },
            )

    assert response.status_code == 502
