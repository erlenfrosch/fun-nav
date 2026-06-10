from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_circular_route_returns_geometry():
    response = client.post(
        "/api/routes/circular",
        json={"lat": 47.5, "lon": 9.7, "duration_min": 60, "curviness": "kurvenreich"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "routes" in data
    assert len(data["routes"]) == 1
    route = data["routes"][0]
    assert route["duration_min"] == 60
    assert route["geometry"]["type"] == "LineString"
    assert len(route["geometry"]["coordinates"]) > 0


def test_circular_route_sehr_kurvenreich_slower():
    r1 = client.post(
        "/api/routes/circular",
        json={"lat": 47.5, "lon": 9.7, "duration_min": 60, "curviness": "kurvenreich"},
    ).json()
    r2 = client.post(
        "/api/routes/circular",
        json={"lat": 47.5, "lon": 9.7, "duration_min": 60, "curviness": "sehr_kurvenreich"},
    ).json()
    assert r1["routes"][0]["distance_km"] > r2["routes"][0]["distance_km"]


def test_circular_route_invalid_curviness():
    response = client.post(
        "/api/routes/circular",
        json={"lat": 47.5, "lon": 9.7, "duration_min": 60, "curviness": "invalid"},
    )
    assert response.status_code == 422
