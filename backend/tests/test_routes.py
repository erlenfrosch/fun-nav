import httpx
import pytest
import respx

from tests.conftest import make_gh_path

GH_URL = "http://localhost:8989/route"
VALID_PAYLOAD = {
    "lat": 48.137,
    "lon": 11.575,
    "duration_min": 60,
    "curviness": "high",
}


@pytest.mark.asyncio
@respx.mock
async def test_circular_route_returns_up_to_three_routes(client):
    respx.post(GH_URL).mock(return_value=httpx.Response(200, json=make_gh_path()))

    resp = client.post("/api/routes/circular", json=VALID_PAYLOAD)

    assert resp.status_code == 200
    body = resp.json()
    assert "routes" in body
    routes = body["routes"]
    assert 1 <= len(routes) <= 3
    for route in routes:
        assert "id" in route
        assert "duration_min" in route
        assert "distance_km" in route
        assert route["geojson"]["type"] == "LineString"
        assert isinstance(route["instructions"], list)


@pytest.mark.asyncio
@respx.mock
async def test_circular_route_very_high_curviness(client):
    respx.post(GH_URL).mock(return_value=httpx.Response(200, json=make_gh_path()))

    resp = client.post(
        "/api/routes/circular",
        json={**VALID_PAYLOAD, "curviness": "very_high"},
    )

    assert resp.status_code == 200
    assert len(resp.json()["routes"]) >= 1


@pytest.mark.asyncio
@respx.mock
async def test_circular_route_no_routes_in_time_window(client):
    # duration 10 h → far outside the ±20 % window of 60 min
    gh_response = make_gh_path(duration_ms=36_000_000)
    respx.post(GH_URL).mock(return_value=httpx.Response(200, json=gh_response))

    resp = client.post("/api/routes/circular", json=VALID_PAYLOAD)

    assert resp.status_code == 404


@pytest.mark.asyncio
@respx.mock
async def test_circular_route_graphhopper_unreachable(client):
    respx.post(GH_URL).mock(side_effect=httpx.ConnectError("refused"))

    resp = client.post("/api/routes/circular", json=VALID_PAYLOAD)

    assert resp.status_code == 503


@pytest.mark.asyncio
@respx.mock
async def test_circular_route_graphhopper_error_status(client):
    respx.post(GH_URL).mock(return_value=httpx.Response(500, text="internal error"))

    resp = client.post("/api/routes/circular", json=VALID_PAYLOAD)

    assert resp.status_code == 503


def test_circular_route_invalid_curviness(client):
    resp = client.post(
        "/api/routes/circular",
        json={**VALID_PAYLOAD, "curviness": "medium"},
    )
    assert resp.status_code == 422


def test_circular_route_missing_field(client):
    resp = client.post("/api/routes/circular", json={"lat": 48.137, "lon": 11.575})
    assert resp.status_code == 422


@pytest.mark.integration
@pytest.mark.asyncio
async def test_circular_route_real_graphhopper(client):
    """Integrations-Test gegen echten GraphHopper – wird übersprungen wenn GH nicht erreichbar."""
    import httpx as _httpx

    try:
        async with _httpx.AsyncClient(timeout=3.0) as hc:
            health = await hc.get("http://localhost:8989/health")
        if health.status_code != 200:
            pytest.skip("GraphHopper nicht bereit")
    except _httpx.ConnectError:
        pytest.skip("GraphHopper nicht erreichbar")

    resp = client.post("/api/routes/circular", json=VALID_PAYLOAD)
    assert resp.status_code == 200
    routes = resp.json()["routes"]
    assert 1 <= len(routes) <= 3
    for route in routes:
        assert 48 <= route["duration_min"] <= 72
