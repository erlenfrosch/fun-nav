import math
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.circular_route import (
    AVG_SPEED_KMPH,
    EARTH_RADIUS_KM,
    NUM_ROUTES,
    NUM_WAYPOINTS,
    TIME_TOLERANCE,
    calculate_curviness,
    calculate_radius,
    generate_circular_routes,
    generate_waypoints,
    haversine_waypoint,
)


def test_calculate_radius_60min():
    r = calculate_radius(60.0)
    expected = (60.0 / 60.0 * AVG_SPEED_KMPH) / (2 * math.pi)
    assert abs(r - expected) < 0.001


def test_calculate_radius_scales_linearly():
    r30 = calculate_radius(30.0)
    r60 = calculate_radius(60.0)
    assert abs(r60 / r30 - 2.0) < 0.001


def test_haversine_waypoint_north():
    # bearing 0° = north; 1° lat ≈ 111.32 km
    dist_km = 111.32
    wp = haversine_waypoint(48.0, 11.0, dist_km, 0.0)
    assert abs(wp.lat - 49.0) < 0.05
    assert abs(wp.lng - 11.0) < 0.01


def test_haversine_waypoint_east_moves_lng():
    wp = haversine_waypoint(48.0, 11.0, 100.0, 90.0)
    assert wp.lng > 11.0


def test_haversine_waypoint_south_moves_lat_down():
    wp = haversine_waypoint(48.0, 11.0, 100.0, 180.0)
    assert wp.lat < 48.0


def test_generate_waypoints_count():
    wps = generate_waypoints(48.137, 11.575, 6.366)
    assert len(wps) == NUM_WAYPOINTS


def test_generate_waypoints_equidistant():
    origin_lat, origin_lng = 48.137, 11.575
    radius = 6.366
    for wp in generate_waypoints(origin_lat, origin_lng, radius):
        dlat = math.radians(wp.lat - origin_lat)
        dlng = math.radians(wp.lng - origin_lng)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(origin_lat))
            * math.cos(math.radians(wp.lat))
            * math.sin(dlng / 2) ** 2
        )
        dist = 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))
        assert abs(dist - radius) < 0.1


def test_generate_waypoints_angles_equidistant():
    """Consecutive waypoints should span equal angular separations."""
    origin_lat, origin_lng = 48.0, 11.0
    radius = 10.0
    wps = generate_waypoints(origin_lat, origin_lng, radius)
    # Each adjacent pair should be the same chord distance
    def chord(a, b):
        dlat = math.radians(b.lat - a.lat)
        dlng = math.radians(b.lng - a.lng)
        x = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(a.lat))
            * math.cos(math.radians(b.lat))
            * math.sin(dlng / 2) ** 2
        )
        return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(x))

    chords = [chord(wps[i], wps[(i + 1) % NUM_WAYPOINTS]) for i in range(NUM_WAYPOINTS)]
    assert max(chords) - min(chords) < 0.01


def test_calculate_curviness_optimal_is_one():
    # distance equals 2×radius → score = 1.0
    score = calculate_curviness(2000.0, 1.0)
    assert abs(score - 1.0) < 0.001


def test_calculate_curviness_higher_distance_higher_score():
    s1 = calculate_curviness(80000.0, 6.0)
    s2 = calculate_curviness(120000.0, 6.0)
    assert s2 > s1


def test_calculate_curviness_zero_radius_returns_zero():
    score = calculate_curviness(1000.0, 0.0)
    assert score == 0.0


def _make_mock_client(responses):
    """Build an AsyncMock httpx.AsyncClient that returns responses in order."""
    call_count = 0

    async def mock_post(*args, **kwargs):
        nonlocal call_count
        data = responses[call_count % len(responses)]
        call_count += 1
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {"paths": [data]} if data else {"paths": []}
        return mock_resp

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    mock_client.post = mock_post
    return mock_client


@pytest.mark.asyncio
async def test_generate_routes_filters_outside_tolerance():
    target_min = 60.0
    base_ms = int(target_min * 60 * 1000)
    # First 3 within ±20%, last 3 outside
    responses = [
        {"time": int(base_ms * 0.95), "distance": 80000},
        {"time": base_ms, "distance": 80000},
        {"time": int(base_ms * 1.10), "distance": 80000},
        {"time": int(base_ms * 0.50), "distance": 40000},
        {"time": int(base_ms * 1.50), "distance": 120000},
        {"time": int(base_ms * 1.30), "distance": 100000},
    ]
    mock_client = _make_mock_client(responses)
    with patch("httpx.AsyncClient", return_value=mock_client):
        routes = await generate_circular_routes(48.137, 11.575, target_min)

    assert len(routes) == 3
    for r in routes:
        assert 48.0 <= r["duration_min"] <= 72.0


@pytest.mark.asyncio
async def test_generate_routes_sorted_by_curviness_desc():
    target_min = 60.0
    base_ms = int(target_min * 60 * 1000)
    distances = [50000, 120000, 80000, 60000, 90000, 70000]
    responses = [{"time": base_ms, "distance": d} for d in distances]
    mock_client = _make_mock_client(responses)
    with patch("httpx.AsyncClient", return_value=mock_client):
        routes = await generate_circular_routes(48.137, 11.575, target_min)

    scores = [r["curviness_score"] for r in routes]
    assert scores == sorted(scores, reverse=True)


@pytest.mark.asyncio
async def test_generate_routes_handles_graphhopper_error():
    """Failed GraphHopper requests are silently skipped."""
    target_min = 60.0
    base_ms = int(target_min * 60 * 1000)

    async def mock_post_raises(*args, **kwargs):
        raise Exception("connection refused")

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    mock_client.post = mock_post_raises

    with patch("httpx.AsyncClient", return_value=mock_client):
        routes = await generate_circular_routes(48.137, 11.575, target_min)

    assert routes == []


@pytest.mark.asyncio
async def test_munich_acceptance_three_routes_48_to_72_min():
    """Acceptance: Munich 60 min → 3 routes within 48–72 min."""
    target_min = 60.0
    base_ms = int(target_min * 60 * 1000)
    responses = [
        {"time": int(base_ms * 0.85), "distance": 75000},  # 51 min ✓
        {"time": int(base_ms * 1.10), "distance": 95000},  # 66 min ✓
        {"time": int(base_ms * 0.92), "distance": 80000},  # 55 min ✓
        {"time": int(base_ms * 0.50), "distance": 40000},  # 30 min ✗
        {"time": int(base_ms * 1.40), "distance": 110000}, # 84 min ✗
        {"time": int(base_ms * 1.60), "distance": 120000}, # 96 min ✗
    ]
    mock_client = _make_mock_client(responses)
    with patch("httpx.AsyncClient", return_value=mock_client):
        routes = await generate_circular_routes(48.137, 11.575, target_min)

    assert len(routes) == 3
    for r in routes:
        assert 48.0 <= r["duration_min"] <= 72.0
