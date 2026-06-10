import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "lat": 47.8,
    "lon": 13.0,
    "duration_min": 60,
    "curviness": "kurvenreich",
}


def test_circular_route_returns_200():
    response = client.post("/api/routes/circular", json=VALID_PAYLOAD)
    assert response.status_code == 200


def test_circular_route_returns_routes_list():
    response = client.post("/api/routes/circular", json=VALID_PAYLOAD)
    data = response.json()
    assert "routes" in data
    assert isinstance(data["routes"], list)
    assert len(data["routes"]) > 0


def test_circular_route_route_has_required_fields():
    response = client.post("/api/routes/circular", json=VALID_PAYLOAD)
    route = response.json()["routes"][0]
    assert "id" in route
    assert "duration_min" in route
    assert "distance_km" in route
    assert "geometry" in route


def test_circular_route_geometry_is_linestring():
    response = client.post("/api/routes/circular", json=VALID_PAYLOAD)
    geometry = response.json()["routes"][0]["geometry"]
    assert geometry["type"] == "LineString"
    assert isinstance(geometry["coordinates"], list)
    assert len(geometry["coordinates"]) > 0


def test_circular_route_missing_fields_returns_422():
    response = client.post("/api/routes/circular", json={"lat": 47.8})
    assert response.status_code == 422


def test_circular_route_invalid_curviness_returns_422():
    payload = {**VALID_PAYLOAD, "curviness": "flach"}
    response = client.post("/api/routes/circular", json=payload)
    assert response.status_code == 422
