import math
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.circular_route import (
    compute_radius_km,
    curviness_score,
    destination_point,
    generate_circular_routes,
    generate_waypoints,
)

# ---------------------------------------------------------------------------
# Pure-math helpers
# ---------------------------------------------------------------------------


def test_compute_radius_km_60min():
    r = compute_radius_km(60)
    expected = (60 / 60 * 50) / (2 * math.pi)
    assert abs(r - expected) < 0.01


def test_compute_radius_km_30min():
    r = compute_radius_km(30)
    expected = (30 / 60 * 50) / (2 * math.pi)
    assert abs(r - expected) < 0.01


def test_compute_radius_km_scales_linearly():
    assert abs(compute_radius_km(60) / compute_radius_km(30) - 2.0) < 1e-9


def test_destination_point_north():
    wp = destination_point(48.137, 11.575, bearing_deg=0, distance_km=100)
    assert wp.lat > 48.137
    assert abs(wp.lon - 11.575) < 0.2


def test_destination_point_east():
    wp = destination_point(48.137, 11.575, bearing_deg=90, distance_km=100)
    assert wp.lon > 11.575
    assert abs(wp.lat - 48.137) < 0.5


def test_destination_point_south():
    wp = destination_point(48.137, 11.575, bearing_deg=180, distance_km=100)
    assert wp.lat < 48.137
    assert abs(wp.lon - 11.575) < 0.2


def test_destination_point_roundtrip():
    wp1 = destination_point(48.137, 11.575, 0, 100)
    wp2 = destination_point(wp1.lat, wp1.lon, 180, 100)
    assert abs(wp2.lat - 48.137) < 0.01
    assert abs(wp2.lon - 11.575) < 0.01


def test_generate_waypoints_count():
    wps = generate_waypoints(48.137, 11.575, radius_km=7.96)
    assert len(wps) == 8


def test_generate_waypoints_opposites_symmetric():
    lat, lon = 48.137, 11.575
    r = 10.0
    wps = generate_waypoints(lat, lon, r)
    assert abs(wps[0].lat - lat) == pytest.approx(abs(wps[4].lat - lat), abs=0.01)
    assert abs(wps[0].lon - lon) == pytest.approx(abs(wps[4].lon - lon), abs=0.01)


def test_generate_waypoints_all_valid_coords():
    wps = generate_waypoints(48.137, 11.575, radius_km=7.96)
    for wp in wps:
        assert -90 <= wp.lat <= 90
        assert -180 <= wp.lon <= 180


def test_curviness_score_at_80kmh():
    score = curviness_score(time_ms=3_600_000, distance_m=80_000)
    assert score == pytest.approx(1.0, abs=0.01)


def test_curviness_score_at_50kmh():
    score = curviness_score(time_ms=3_600_000, distance_m=50_000)
    assert score == pytest.approx(1.6, abs=0.01)


def test_curviness_score_at_40kmh():
    score = curviness_score(time_ms=3_600_000, distance_m=40_000)
    assert score == pytest.approx(2.0, abs=0.01)


def test_curviness_score_zero_distance():
    assert curviness_score(time_ms=3_600_000, distance_m=0) == 0.0


def test_curviness_lower_speed_higher_score():
    slow = curviness_score(time_ms=3_600_000, distance_m=40_000)
    fast = curviness_score(time_ms=3_600_000, distance_m=60_000)
    assert slow > fast


# ---------------------------------------------------------------------------
# Mock helpers
# ---------------------------------------------------------------------------


def _make_mock_response(time_ms: int, distance_m: int) -> MagicMock:
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json.return_value = {"paths": [{"time": time_ms, "distance": distance_m}]}
    return resp


# ---------------------------------------------------------------------------
# generate_circular_routes integration tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_acceptance_munich_60min():
    """
    Akzeptanztest: München (48.137°N, 11.575°E), 60 min →
    3 Routen mit 48–72 min Dauer.
    """
    target_ms = 60 * 60 * 1000
    mock_resp = _make_mock_response(time_ms=target_ms, distance_m=50_000)

    with patch("app.services.circular_route.httpx.AsyncClient") as MockClient:
        mock_client = AsyncMock()
        MockClient.return_value.__aenter__.return_value = mock_client
        mock_client.post = AsyncMock(return_value=mock_resp)

        routes = await generate_circular_routes(
            lat=48.137,
            lon=11.575,
            duration_min=60,
            graphhopper_url="http://localhost:8989",
        )

    assert len(routes) == 3
    for r in routes:
        assert 48.0 <= r["duration_min"] <= 72.0


@pytest.mark.asyncio
async def test_generate_circular_routes_returns_top3():
    target_ms = 60 * 60 * 1000
    mock_resp = _make_mock_response(time_ms=target_ms, distance_m=50_000)

    with patch("app.services.circular_route.httpx.AsyncClient") as MockClient:
        mock_client = AsyncMock()
        MockClient.return_value.__aenter__.return_value = mock_client
        mock_client.post = AsyncMock(return_value=mock_resp)

        routes = await generate_circular_routes(
            lat=48.137,
            lon=11.575,
            duration_min=60,
            graphhopper_url="http://localhost:8989",
        )

    assert len(routes) == 3


@pytest.mark.asyncio
async def test_generate_circular_routes_filters_out_of_range():
    # 40 min ist 33% unter 60 min → rausgefiltert (>20% Toleranz)
    too_short_ms = 40 * 60 * 1000
    mock_resp = _make_mock_response(time_ms=too_short_ms, distance_m=30_000)

    with patch("app.services.circular_route.httpx.AsyncClient") as MockClient:
        mock_client = AsyncMock()
        MockClient.return_value.__aenter__.return_value = mock_client
        mock_client.post = AsyncMock(return_value=mock_resp)

        routes = await generate_circular_routes(
            lat=48.137,
            lon=11.575,
            duration_min=60,
            graphhopper_url="http://localhost:8989",
        )

    assert len(routes) == 0


@pytest.mark.asyncio
async def test_generate_circular_routes_sorted_by_curviness():
    target_ms = 60 * 60 * 1000
    call_count = 0

    async def varying_response(*args, **kwargs):
        nonlocal call_count
        dist = 40_000 if call_count % 2 == 0 else 55_000
        call_count += 1
        return _make_mock_response(time_ms=target_ms, distance_m=dist)

    with patch("app.services.circular_route.httpx.AsyncClient") as MockClient:
        mock_client = AsyncMock()
        MockClient.return_value.__aenter__.return_value = mock_client
        mock_client.post = varying_response

        routes = await generate_circular_routes(
            lat=48.137,
            lon=11.575,
            duration_min=60,
            graphhopper_url="http://localhost:8989",
        )

    scores = [r["curviness_score"] for r in routes]
    assert scores == sorted(scores, reverse=True)


@pytest.mark.asyncio
async def test_generate_circular_routes_handles_graphhopper_error():
    import httpx

    with patch("app.services.circular_route.httpx.AsyncClient") as MockClient:
        mock_client = AsyncMock()
        MockClient.return_value.__aenter__.return_value = mock_client
        mock_client.post = AsyncMock(side_effect=httpx.ConnectError("GH down"))

        routes = await generate_circular_routes(
            lat=48.137,
            lon=11.575,
            duration_min=60,
            graphhopper_url="http://localhost:8989",
        )

    assert routes == []


@pytest.mark.asyncio
async def test_generate_circular_routes_6_requests_sent():
    target_ms = 60 * 60 * 1000
    mock_resp = _make_mock_response(time_ms=target_ms, distance_m=50_000)

    with patch("app.services.circular_route.httpx.AsyncClient") as MockClient:
        mock_client = AsyncMock()
        MockClient.return_value.__aenter__.return_value = mock_client
        mock_client.post = AsyncMock(return_value=mock_resp)

        await generate_circular_routes(
            lat=48.137,
            lon=11.575,
            duration_min=60,
            graphhopper_url="http://localhost:8989",
        )

    assert mock_client.post.call_count == 6


@pytest.mark.asyncio
async def test_generate_circular_routes_partial_errors():
    """Drei von sechs GH-Anfragen schlagen fehl → trotzdem 3 gültige Routen."""
    import httpx as _httpx

    target_ms = 60 * 60 * 1000
    call_count = 0

    async def alternating(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count % 2 == 0:
            raise _httpx.ConnectError("down")
        return _make_mock_response(time_ms=target_ms, distance_m=50_000)

    with patch("app.services.circular_route.httpx.AsyncClient") as MockClient:
        mock_client = AsyncMock()
        MockClient.return_value.__aenter__.return_value = mock_client
        mock_client.post = alternating

        routes = await generate_circular_routes(
            lat=48.137,
            lon=11.575,
            duration_min=60,
            graphhopper_url="http://localhost:8989",
        )

    assert len(routes) == 3
