import httpx
import pytest
import respx
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

MOCK_GH_RESPONSE = {
    "paths": [
        {
            "distance": 10243.5,
            "time": 2345678,
            "points": {
                "type": "LineString",
                "coordinates": [[9.5, 47.1], [9.51, 47.11], [9.5, 47.1]],
            },
            "bbox": [9.5, 47.1, 9.51, 47.11],
        }
    ]
}


@respx.mock
def test_round_trip_success():
    respx.get("http://graphhopper:8989/route").mock(
        return_value=httpx.Response(200, json=MOCK_GH_RESPONSE)
    )
    resp = client.post(
        "/api/round-trip",
        json={"lat": 47.1, "lng": 9.5, "distance": 10000, "profile": "bike"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["distance"] == 10243.5
    assert data["points"]["type"] == "LineString"
    assert data["time"] == 2345678


@respx.mock
def test_round_trip_graphhopper_down():
    respx.get("http://graphhopper:8989/route").mock(
        side_effect=httpx.ConnectError("Connection refused")
    )
    resp = client.post(
        "/api/round-trip",
        json={"lat": 47.1, "lng": 9.5, "distance": 10000, "profile": "bike"},
    )
    assert resp.status_code == 503


@respx.mock
def test_round_trip_graphhopper_error():
    respx.get("http://graphhopper:8989/route").mock(
        return_value=httpx.Response(400, json={"message": "Bad Request"})
    )
    resp = client.post(
        "/api/round-trip",
        json={"lat": 47.1, "lng": 9.5, "distance": 10000, "profile": "bike"},
    )
    assert resp.status_code == 502


def test_round_trip_invalid_input():
    resp = client.post("/api/round-trip", json={"lat": "invalid", "lng": 9.5})
    assert resp.status_code == 422


@respx.mock
def test_round_trip_uses_correct_gh_parameters():
    route_mock = respx.get("http://graphhopper:8989/route").mock(
        return_value=httpx.Response(200, json=MOCK_GH_RESPONSE)
    )
    client.post(
        "/api/round-trip",
        json={"lat": 47.1, "lng": 9.5, "distance": 5000, "profile": "foot", "seed": 42},
    )
    url = str(route_mock.calls[0].request.url)
    assert "algorithm=round_trip" in url
    assert "round_trip.distance=5000" in url
    assert "profile=foot" in url
    assert "ch.disable=true" in url
    assert "seed=42" in url
