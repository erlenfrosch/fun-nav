"""
Unit-Tests für backend/app/services/graphhopper.py

Testet:
- Korrekte Custom-Model-Payloads pro Modus
- Fehler bei unbekanntem Modus
- Akzeptanzkriterium: sehr_kurvenreich hat niedrigeren Ø-Curvature-Wert als kurvenreich
"""

import json
import pytest
import httpx
import respx

from backend.app.services.graphhopper import (
    CURVY_MODEL,
    VERY_CURVY_MODEL,
    average_curvature,
    get_route,
)

GH_URL = "http://graphhopper:8989"

_FAKE_PATH_STRAIGHT = {
    "distance": 50000.0,
    "time": 3600000,
    "weight": 100.0,
    "points": {"type": "LineString", "coordinates": [[7.0, 47.0], [7.5, 47.5]]},
    "details": {
        "curvature": [[0, 5, 0.85], [5, 10, 0.90], [10, 15, 0.80]],
    },
}

_FAKE_PATH_CURVY = {
    "distance": 65000.0,
    "time": 4200000,
    "weight": 80.0,
    "points": {"type": "LineString", "coordinates": [[7.0, 47.0], [7.3, 47.4], [7.5, 47.5]]},
    "details": {
        "curvature": [[0, 5, 0.30], [5, 10, 0.25], [10, 15, 0.35]],
    },
}


def _make_gh_response(path: dict) -> dict:
    return {"paths": [path], "info": {"copyrights": ["GraphHopper"], "took": 12}}


# ---------------------------------------------------------------------------
# Custom-Model-Payload Tests
# ---------------------------------------------------------------------------

@respx.mock
def test_kurvenreich_sends_correct_custom_model():
    route_mock = respx.post(f"{GH_URL}/route").mock(
        return_value=httpx.Response(200, json=_make_gh_response(_FAKE_PATH_STRAIGHT))
    )

    get_route([7.0, 47.0], [7.5, 47.5], "kurvenreich", base_url=GH_URL)

    assert route_mock.called
    body = json.loads(route_mock.calls.last.request.content)
    assert body["custom_model"] == CURVY_MODEL
    assert body["ch.disable"] is True
    assert body["profile"] == "motorcycle"


@respx.mock
def test_sehr_kurvenreich_sends_correct_custom_model():
    route_mock = respx.post(f"{GH_URL}/route").mock(
        return_value=httpx.Response(200, json=_make_gh_response(_FAKE_PATH_CURVY))
    )

    get_route([7.0, 47.0], [7.5, 47.5], "sehr_kurvenreich", base_url=GH_URL)

    assert route_mock.called
    body = json.loads(route_mock.calls.last.request.content)
    assert body["custom_model"] == VERY_CURVY_MODEL
    assert body["ch.disable"] is True


@respx.mock
def test_unknown_mode_raises_value_error():
    with pytest.raises(ValueError, match="Unbekannter Modus"):
        get_route([7.0, 47.0], [7.5, 47.5], "unbekannt", base_url=GH_URL)


@respx.mock
def test_http_error_is_propagated():
    respx.post(f"{GH_URL}/route").mock(
        return_value=httpx.Response(500, json={"message": "Internal Server Error"})
    )
    with pytest.raises(httpx.HTTPStatusError):
        get_route([7.0, 47.0], [7.5, 47.5], "kurvenreich", base_url=GH_URL)


# ---------------------------------------------------------------------------
# average_curvature Helper
# ---------------------------------------------------------------------------

def test_average_curvature_returns_weighted_mean():
    path = {
        "details": {
            "curvature": [[0, 5, 0.8], [5, 10, 0.6]],
        }
    }
    result = average_curvature(path)
    assert abs(result - 0.7) < 1e-6


def test_average_curvature_empty_details_returns_one():
    result = average_curvature({"details": {"curvature": []}})
    assert result == 1.0


# ---------------------------------------------------------------------------
# Akzeptanzkriterium
# ---------------------------------------------------------------------------

@respx.mock
def test_sehr_kurvenreich_has_lower_avg_curvature_than_kurvenreich():
    """
    Akzeptanzkriterium (Issue #5):
    Die sehr-kurvenreich-Route hat einen niedrigeren Ø-Curvature-Wert
    (= mehr Kurven) als die kurvenreich-Route.
    """
    start = [7.0, 47.0]
    end = [7.5, 47.5]

    respx.post(f"{GH_URL}/route").mock(
        side_effect=[
            httpx.Response(200, json=_make_gh_response(_FAKE_PATH_STRAIGHT)),
            httpx.Response(200, json=_make_gh_response(_FAKE_PATH_CURVY)),
        ]
    )

    route_kurvenreich = get_route(start, end, "kurvenreich", base_url=GH_URL)
    route_sehr_kurvenreich = get_route(start, end, "sehr_kurvenreich", base_url=GH_URL)

    avg_kurvenreich = average_curvature(route_kurvenreich["paths"][0])
    avg_sehr_kurvenreich = average_curvature(route_sehr_kurvenreich["paths"][0])

    assert avg_sehr_kurvenreich < avg_kurvenreich, (
        f"sehr_kurvenreich ({avg_sehr_kurvenreich:.3f}) sollte weniger gerade sein "
        f"als kurvenreich ({avg_kurvenreich:.3f})"
    )
