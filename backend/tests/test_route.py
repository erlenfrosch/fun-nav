import httpx
import respx
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

GH_SUCCESS = {
    "paths": [
        {
            "distance": 5432.1,
            "time": 432000,
            "points": "_p~iF~ps|U_ulLnnqC_mqNvxq`@",
        }
    ]
}


@respx.mock
def test_route_success():
    respx.get("http://localhost:8989/route").mock(
        return_value=httpx.Response(200, json=GH_SUCCESS)
    )
    response = client.post(
        "/route",
        json={"start": {"lat": 47.1, "lng": 9.5}, "end": {"lat": 47.2, "lng": 9.6}},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["distance"] == 5432.1
    assert data["duration"] == 432000
    assert "points" in data


@respx.mock
def test_route_graphhopper_error():
    respx.get("http://localhost:8989/route").mock(
        return_value=httpx.Response(500, text="Internal Server Error")
    )
    response = client.post(
        "/route",
        json={"start": {"lat": 47.1, "lng": 9.5}, "end": {"lat": 47.2, "lng": 9.6}},
    )
    assert response.status_code == 502


@respx.mock
def test_route_no_path():
    respx.get("http://localhost:8989/route").mock(
        return_value=httpx.Response(200, json={"paths": []})
    )
    response = client.post(
        "/route",
        json={"start": {"lat": 47.1, "lng": 9.5}, "end": {"lat": 47.2, "lng": 9.6}},
    )
    assert response.status_code == 404


def test_route_invalid_body():
    response = client.post("/route", json={"start": {"lat": 47.1}})
    assert response.status_code == 422
