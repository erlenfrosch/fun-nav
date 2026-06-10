import pytest

VALID_REQUEST = {
    "lat": 47.5,
    "lon": 9.7,
    "duration_min": 60,
    "curviness": "kurvenreich",
}


def test_circular_route_returns_routes_list(client):
    response = client.post("/api/routes/circular", json=VALID_REQUEST)
    assert response.status_code == 200
    data = response.json()
    assert "routes" in data
    assert isinstance(data["routes"], list)
    assert len(data["routes"]) >= 1


def test_circular_route_result_has_required_fields(client):
    response = client.post("/api/routes/circular", json=VALID_REQUEST)
    route = response.json()["routes"][0]
    assert "id" in route
    assert "duration_min" in route
    assert "distance_km" in route
    assert "geometry" in route
    assert route["geometry"]["type"] == "LineString"
    assert len(route["geometry"]["coordinates"]) > 0


def test_circular_route_duration_preserved(client):
    response = client.post("/api/routes/circular", json=VALID_REQUEST)
    route = response.json()["routes"][0]
    assert route["duration_min"] == VALID_REQUEST["duration_min"]


def test_circular_route_sehr_kurvenreich_shorter_distance(client):
    body_k = {**VALID_REQUEST, "curviness": "kurvenreich"}
    body_sk = {**VALID_REQUEST, "curviness": "sehr_kurvenreich"}
    dist_k = client.post("/api/routes/circular", json=body_k).json()["routes"][0]["distance_km"]
    dist_sk = client.post("/api/routes/circular", json=body_sk).json()["routes"][0]["distance_km"]
    assert dist_sk < dist_k


def test_circular_route_invalid_curviness_returns_422(client):
    body = {**VALID_REQUEST, "curviness": "gerade"}
    response = client.post("/api/routes/circular", json=body)
    assert response.status_code == 422


def test_circular_route_missing_fields_returns_422(client):
    response = client.post("/api/routes/circular", json={"lat": 47.5})
    assert response.status_code == 422


def test_circular_route_invalid_types_returns_422(client):
    body = {**VALID_REQUEST, "lat": "nicht-eine-zahl"}
    response = client.post("/api/routes/circular", json=body)
    assert response.status_code == 422
