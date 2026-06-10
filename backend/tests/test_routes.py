import pytest
import httpx
import respx
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

GH_ROUTE_RESPONSE = {
    "paths": [
        {
            "distance": 42000.0,
            "time": 3600000,
            "points": {
                "type": "LineString",
                "coordinates": [
                    [13.4, 48.1],
                    [13.5, 48.2],
                    [13.4, 48.3],
                    [13.4, 48.1],
                ],
            },
        }
    ]
}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@respx.mock
def test_circular_route_success():
    respx.post("http://graphhopper:8989/route").mock(
        return_value=httpx.Response(200, json=GH_ROUTE_RESPONSE)
    )
    response = client.post(
        "/api/routes/circular",
        json={"lat": 48.1, "lon": 13.4, "duration_min": 60, "curviness": "kurvenreich"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "routes" in data
    assert len(data["routes"]) == 1
    route = data["routes"][0]
    assert route["duration_min"] == 60
    assert "distance_km" in route
    assert route["geometry"]["type"] == "LineString"
    assert len(route["geometry"]["coordinates"]) >= 2


@respx.mock
def test_circular_route_sehr_kurvenreich():
    respx.post("http://graphhopper:8989/route").mock(
        return_value=httpx.Response(200, json=GH_ROUTE_RESPONSE)
    )
    response = client.post(
        "/api/routes/circular",
        json={"lat": 48.1, "lon": 13.4, "duration_min": 60, "curviness": "sehr_kurvenreich"},
    )
    assert response.status_code == 200
    data = response.json()
    route = data["routes"][0]
    assert route["id"] == "sehr_kurvenreich-60"


@respx.mock
def test_circular_route_graphhopper_down():
    respx.post("http://graphhopper:8989/route").mock(
        side_effect=httpx.ConnectError("Connection refused")
    )
    response = client.post(
        "/api/routes/circular",
        json={"lat": 48.1, "lon": 13.4, "duration_min": 60, "curviness": "kurvenreich"},
    )
    assert response.status_code == 502
    assert "detail" in response.json()


@respx.mock
def test_circular_route_graphhopper_error():
    respx.post("http://graphhopper:8989/route").mock(
        return_value=httpx.Response(400, json={"message": "Invalid profile"})
    )
    response = client.post(
        "/api/routes/circular",
        json={"lat": 48.1, "lon": 13.4, "duration_min": 60, "curviness": "kurvenreich"},
    )
    assert response.status_code == 502
    assert "detail" in response.json()


def test_circular_route_validation_error_missing_field():
    response = client.post(
        "/api/routes/circular",
        json={"lat": 48.1, "lon": 13.4, "duration_min": 60},
    )
    assert response.status_code == 422


def test_circular_route_validation_error_invalid_curviness():
    response = client.post(
        "/api/routes/circular",
        json={"lat": 48.1, "lon": 13.4, "duration_min": 60, "curviness": "gerade"},
    )
    assert response.status_code == 422
