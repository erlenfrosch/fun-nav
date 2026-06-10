import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "lat": 47.5,
    "lon": 9.7,
    "duration_min": 60,
    "curviness": "kurvenreich",
}


def test_circular_route_returns_routes():
    response = client.post("/api/routes/circular", json=VALID_PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert "routes" in body
    assert len(body["routes"]) == 1


def test_circular_route_has_expected_fields():
    response = client.post("/api/routes/circular", json=VALID_PAYLOAD)
    route = response.json()["routes"][0]
    assert route["duration_min"] == 60
    assert route["distance_km"] > 0
    assert route["geometry"]["type"] == "LineString"
    assert len(route["geometry"]["coordinates"]) >= 2


def test_circular_route_sehr_kurvenreich_uses_lower_speed():
    payload = {**VALID_PAYLOAD, "curviness": "sehr_kurvenreich", "duration_min": 60}
    response = client.post("/api/routes/circular", json=payload)
    route = response.json()["routes"][0]
    # 40 km/h * 60 min / 60 = 40 km
    assert route["distance_km"] == pytest.approx(40.0, abs=0.1)


def test_circular_route_kurvenreich_uses_higher_speed():
    payload = {**VALID_PAYLOAD, "curviness": "kurvenreich", "duration_min": 60}
    response = client.post("/api/routes/circular", json=payload)
    route = response.json()["routes"][0]
    # 50 km/h * 60 min / 60 = 50 km
    assert route["distance_km"] == pytest.approx(50.0, abs=0.1)


def test_circular_route_invalid_curviness_returns_422():
    payload = {**VALID_PAYLOAD, "curviness": "falsch"}
    response = client.post("/api/routes/circular", json=payload)
    assert response.status_code == 422


def test_circular_route_missing_field_returns_422():
    response = client.post("/api/routes/circular", json={"lat": 47.5, "lon": 9.7})
    assert response.status_code == 422
