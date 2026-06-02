import math
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.circular_route import (
    EARTH_RADIUS_KM,
    WAYPOINT_COUNT,
    Route,
    calculate_radius,
    destination_point,
    generate_circular_routes,
    generate_waypoints,
    select_route_pairs,
)


# --- Pure function tests ---

def test_calculate_radius_60min():
    radius = calculate_radius(60)
    expected = (1.0 * 50.0) / (2 * math.pi)
    assert abs(radius - expected) < 1e-9


def test_calculate_radius_custom_speed():
    radius = calculate_radius(60, avg_speed_kmh=40.0)
    expected = 40.0 / (2 * math.pi)
    assert abs(radius - expected) < 1e-9


def test_destination_point_north_increases_lat():
    lat2, lon2 = destination_point(48.0, 11.0, bearing_deg=0.0, distance_km=10.0)
    assert lat2 > 48.0
    assert abs(lon2 - 11.0) < 1e-3


def test_destination_point_east_increases_lon():
    lat2, lon2 = destination_point(48.0, 11.0, bearing_deg=90.0, distance_km=10.0)
    assert lon2 > 11.0
    assert abs(lat2 - 48.0) < 0.1


def test_destination_point_distance_accuracy():
    """Round-trip: destination should be ≈ distance_km from origin."""
    lat1, lon1 = 48.137, 11.575
    dist_km = 50.0
    lat2, lon2 = destination_point(lat1, lon1, 45.0, dist_km)

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    )
    actual_km = 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))
    assert abs(actual_km - dist_km) < 0.5


def test_generate_waypoints_count():
    wps = generate_waypoints(48.137, 11.575, 7.96)
    assert len(wps) == WAYPOINT_COUNT


def test_generate_waypoints_equidistant():
    """All waypoints should be approximately radius_km from center."""
    lat, lon, radius = 48.137, 11.575, 7.96
    wps = generate_waypoints(lat, lon, radius)
    for wp_lat, wp_lon in wps:
        dlat = math.radians(wp_lat - lat)
        dlon = math.radians(wp_lon - lon)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat)) * math.cos(math.radians(wp_lat)) * math.sin(dlon / 2) ** 2
        )
        dist = 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))
        assert abs(dist - radius) < 0.5, f"Waypoint distance {dist:.2f} km ≠ {radius} km"


def test_select_route_pairs_count():
    wps = generate_waypoints(48.0, 11.0, 8.0)
    pairs = select_route_pairs(wps)
    assert len(pairs) == 6


def test_select_route_pairs_valid_indices():
    wps = generate_waypoints(48.0, 11.0, 8.0)
    pairs = select_route_pairs(wps)
    for i, j in pairs:
        assert 0 <= i < WAYPOINT_COUNT
        assert 0 <= j < WAYPOINT_COUNT
        assert i != j


# --- Async integration test with mock ---

def _make_mock_path(duration_min: float, distance_km: float) -> dict:
    return {
        "time": int(duration_min * 60 * 1000),
        "distance": distance_km * 1000,
        "points": {
            "coordinates": [[11.575, 48.137], [11.65, 48.22], [11.575, 48.137]]
        },
    }


@pytest.mark.asyncio
async def test_generate_circular_routes_returns_top3():
    """All 6 routes within tolerance → should return exactly 3 (highest curviness)."""
    mock_path = _make_mock_path(duration_min=60.0, distance_km=90.0)

    class FakeResponse:
        def raise_for_status(self):
            pass
        def json(self):
            return {"paths": [mock_path]}

    with patch("httpx.AsyncClient.post", new=AsyncMock(return_value=FakeResponse())):
        routes = await generate_circular_routes(48.137, 11.575, 60.0, "http://localhost:8989")

    assert len(routes) == 3
    for r in routes:
        assert 48.0 <= r.duration_min <= 72.0


@pytest.mark.asyncio
async def test_generate_circular_routes_filters_out_of_tolerance():
    """Routes with >20% deviation from target time are excluded."""
    out_of_tolerance = _make_mock_path(duration_min=90.0, distance_km=100.0)  # 50% over

    class FakeResponse:
        def raise_for_status(self):
            pass
        def json(self):
            return {"paths": [out_of_tolerance]}

    with patch("httpx.AsyncClient.post", new=AsyncMock(return_value=FakeResponse())):
        routes = await generate_circular_routes(48.137, 11.575, 60.0, "http://localhost:8989")

    assert routes == []


@pytest.mark.asyncio
async def test_generate_circular_routes_sorted_by_curviness():
    """Routes are sorted by curviness_score descending."""
    paths = [
        _make_mock_path(60.0, 80.0),   # lower curviness
        _make_mock_path(60.0, 95.0),   # higher curviness
        _make_mock_path(60.0, 88.0),   # medium
    ]
    call_count = [0]

    class FakeResponse:
        def raise_for_status(self):
            pass
        def json(self):
            idx = min(call_count[0], len(paths) - 1)
            call_count[0] += 1
            return {"paths": [paths[idx]]}

    with patch("httpx.AsyncClient.post", new=AsyncMock(side_effect=lambda *a, **kw: FakeResponse())):
        routes = await generate_circular_routes(48.137, 11.575, 60.0, "http://localhost:8989")

    scores = [r.curviness_score for r in routes]
    assert scores == sorted(scores, reverse=True)


@pytest.mark.asyncio
async def test_generate_circular_routes_handles_gh_errors():
    """GraphHopper errors (exceptions) are silently skipped."""
    with patch("httpx.AsyncClient.post", new=AsyncMock(side_effect=httpx.ConnectError("down"))):
        import httpx
        routes = await generate_circular_routes(48.137, 11.575, 60.0, "http://localhost:8989")
    assert routes == []


# --- Acceptance criterion ---

@pytest.mark.asyncio
async def test_acceptance_munich_60min():
    """München (48.137°N, 11.575°E), 60 min → 3 Routen mit 48–72 min."""
    path = _make_mock_path(duration_min=60.0, distance_km=90.0)

    class FakeResponse:
        def raise_for_status(self):
            pass
        def json(self):
            return {"paths": [path]}

    with patch("httpx.AsyncClient.post", new=AsyncMock(return_value=FakeResponse())):
        routes = await generate_circular_routes(48.137, 11.575, 60.0, "http://localhost:8989")

    assert len(routes) == 3
    for r in routes:
        assert 48.0 <= r.duration_min <= 72.0, f"Duration {r.duration_min:.1f} min out of range"
