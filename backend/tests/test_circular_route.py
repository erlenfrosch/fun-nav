import math
import pytest

from services.circular_route import (
    CircularRoute,
    _build_route_requests,
    _curviness,
    _gh_route,
    calculate_radius_km,
    candidate_waypoints,
    generate_circular_routes,
    haversine_waypoint,
)

# ---------------------------------------------------------------------------
# Pure-math helpers
# ---------------------------------------------------------------------------

def test_calculate_radius_curvy():
    # 60 min at 50 km/h: circumference = 50 km → radius = 50 / (2π)
    r = calculate_radius_km(60.0, very_curvy=False)
    assert abs(r - 50.0 / (2 * math.pi)) < 1e-9


def test_calculate_radius_very_curvy():
    r = calculate_radius_km(60.0, very_curvy=True)
    assert abs(r - 40.0 / (2 * math.pi)) < 1e-9


def test_calculate_radius_scales_with_time():
    r30 = calculate_radius_km(30.0)
    r60 = calculate_radius_km(60.0)
    assert abs(r60 / r30 - 2.0) < 1e-9


def test_haversine_waypoint_north():
    # Moving north 1° should increase latitude by ~1° (≈111 km)
    lat, lon = haversine_waypoint(48.0, 11.0, 111.195, 0.0)
    assert abs(lat - 49.0) < 0.01
    assert abs(lon - 11.0) < 0.01


def test_haversine_waypoint_east():
    lat, lon = haversine_waypoint(0.0, 0.0, 111.195, 90.0)
    # At equator 1° longitude ≈ 111 km
    assert abs(lat) < 0.01
    assert abs(lon - 1.0) < 0.01


def test_haversine_waypoint_roundtrip():
    # Waypoint at 0° and 180° should be symmetric around the center latitude
    lat0, _ = haversine_waypoint(48.0, 11.0, 50.0, 0.0)
    lat180, _ = haversine_waypoint(48.0, 11.0, 50.0, 180.0)
    assert lat0 > 48.0
    assert lat180 < 48.0
    assert abs((lat0 - 48.0) - (48.0 - lat180)) < 0.01


def test_candidate_waypoints_count():
    wps = candidate_waypoints(48.137, 11.575, 7.96)
    assert len(wps) == 8


def test_candidate_waypoints_all_tuples():
    wps = candidate_waypoints(48.137, 11.575, 7.96)
    for lat, lon in wps:
        assert -90 <= lat <= 90
        assert -180 <= lon <= 180


def test_candidate_waypoints_roughly_equal_distance():
    lat0, lon0 = 48.137, 11.575
    radius = 7.96
    wps = candidate_waypoints(lat0, lon0, radius)
    for lat, lon in wps:
        dlat = math.radians(lat - lat0)
        dlon = math.radians(lon - lon0)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat0)) * math.cos(math.radians(lat)) * math.sin(dlon / 2) ** 2
        dist = 6371.0 * 2 * math.asin(math.sqrt(a))
        assert abs(dist - radius) < 0.5  # within 500 m


def test_build_route_requests():
    start = (48.137, 11.575)
    wps = candidate_waypoints(*start, 7.96)
    reqs = _build_route_requests(start, wps)
    assert len(reqs) == 6
    for req in reqs:
        assert req[0] == start
        assert req[-1] == start


def test_curviness_lower_speed_higher_score():
    # 50 km at 60 min (50 km/h) vs 50 km at 90 min (33 km/h)
    score_fast = _curviness(50_000, 60 * 60 * 1_000)
    score_slow = _curviness(50_000, 90 * 60 * 1_000)
    assert score_slow > score_fast


def test_curviness_zero_duration():
    assert _curviness(50_000, 0) == 0.0


# ---------------------------------------------------------------------------
# GraphHopper HTTP mock
# ---------------------------------------------------------------------------

class _FakeResponse:
    """Minimal httpx-Response-Ersatz ohne Request-Objekt."""
    def __init__(self, data: dict) -> None:
        self._data = data

    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict:
        return self._data


class _MockHttpxClient:
    """Einfacher Mock-Client, der nacheinander vordefinierte Antworten liefert."""

    def __init__(self, responses: list[dict | None]) -> None:
        self._iter = iter(responses)

    async def post(self, url: str, **kwargs) -> _FakeResponse:
        data = next(self._iter)
        if data is None:
            raise Exception("mock connection error")
        return _FakeResponse(data)

    async def aclose(self) -> None:
        pass


def _make_mock_client(responses: list[dict | None]) -> _MockHttpxClient:
    return _MockHttpxClient(responses)


def _path(duration_min: float, distance_km: float) -> dict:
    return {"time": int(duration_min * 60 * 1_000), "distance": distance_km * 1_000}


# ---------------------------------------------------------------------------
# generate_circular_routes integration tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_acceptance_munich_60min():
    """
    Acceptance: München (48.137°N, 11.575°E), 60 min →
    3 routes with 48–72 min duration.
    """
    # All 6 mock paths return 60 min / different distances for varied curviness
    responses = [
        {"paths": [_path(60, 55)]},
        {"paths": [_path(58, 50)]},
        {"paths": [_path(65, 60)]},
        {"paths": [_path(62, 52)]},
        {"paths": [_path(70, 65)]},
        {"paths": [_path(55, 48)]},
    ]
    client = _make_mock_client(responses)

    routes = await generate_circular_routes(48.137, 11.575, 60.0, _client=client)

    assert len(routes) == 3
    for r in routes:
        duration_min = r.duration_ms / 60_000
        assert 48 <= duration_min <= 72, f"Duration {duration_min:.1f} min out of range"


@pytest.mark.asyncio
async def test_filters_out_of_range_routes():
    # Only 2 of 6 responses are within ±20% of 60 min
    responses = [
        {"paths": [_path(20, 20)]},   # too short
        {"paths": [_path(60, 55)]},   # ok
        {"paths": [_path(100, 90)]},  # too long
        {"paths": [_path(62, 53)]},   # ok
        {"paths": [_path(10, 10)]},   # too short
        {"paths": [_path(60, 50)]},   # ok
    ]
    client = _make_mock_client(responses)
    routes = await generate_circular_routes(48.137, 11.575, 60.0, _client=client)
    assert len(routes) == 3
    for r in routes:
        assert 48 <= r.duration_ms / 60_000 <= 72


@pytest.mark.asyncio
async def test_returns_empty_when_no_valid_routes():
    responses = [{"paths": [_path(10, 10)]}] * 6
    client = _make_mock_client(responses)
    routes = await generate_circular_routes(48.137, 11.575, 60.0, _client=client)
    assert routes == []


@pytest.mark.asyncio
async def test_handles_gh_errors_gracefully():
    # Mix of errors and valid responses
    responses = [
        None,
        {"paths": [_path(60, 55)]},
        None,
        {"paths": [_path(58, 50)]},
        None,
        {"paths": [_path(65, 60)]},
    ]
    client = _make_mock_client(responses)
    routes = await generate_circular_routes(48.137, 11.575, 60.0, _client=client)
    assert len(routes) == 3


@pytest.mark.asyncio
async def test_sorted_by_curviness_descending():
    # Route A: 60 min / 40 km → avg 40 km/h (more curvy)
    # Route B: 60 min / 50 km → avg 50 km/h (less curvy)
    # Route C: 60 min / 55 km → avg 55 km/h (least curvy)
    responses = [
        {"paths": [_path(60, 50)]},  # B
        {"paths": [_path(60, 40)]},  # A
        {"paths": [_path(60, 55)]},  # C
        {"paths": [_path(90, 90)]},  # filtered out
        {"paths": [_path(60, 48)]},
        {"paths": [_path(60, 52)]},
    ]
    client = _make_mock_client(responses)
    routes = await generate_circular_routes(48.137, 11.575, 60.0, _client=client)
    scores = [r.curviness_score for r in routes]
    assert scores == sorted(scores, reverse=True)


@pytest.mark.asyncio
async def test_empty_paths_response_ignored():
    responses = [{"paths": []}] * 6
    client = _make_mock_client(responses)
    routes = await generate_circular_routes(48.137, 11.575, 60.0, _client=client)
    assert routes == []
