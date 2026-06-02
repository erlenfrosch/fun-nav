import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.routing import build_custom_model, RoutingMode

client = TestClient(app)

SAMPLE_POINTS = [[9.5, 47.1], [9.6, 47.2]]
GH_SUCCESS = {
    "paths": [
        {
            "distance": 15000.0,
            "time": 720000,
            "points": "encoded_polyline_here",
        }
    ],
    "info": {"took": 42},
}


class TestBuildCustomModel:
    def test_fastest_returns_none(self):
        assert build_custom_model(RoutingMode.fastest) is None

    def test_kurvig_boosts_curvy_roads(self):
        model = build_custom_model(RoutingMode.kurvig)
        assert model is not None
        assert "priority" in model
        # lowest curvature bracket must have multiply_by > 1
        low_bracket = next(s for s in model["priority"] if "curvature < 0.3" in s.get("if", ""))
        assert float(low_bracket["multiply_by"]) > 1.0
        assert model.get("distance_influence", 0) > 0

    def test_direkt_penalises_curvy_roads(self):
        model = build_custom_model(RoutingMode.direkt)
        assert model is not None
        assert "priority" in model
        low_bracket = next(s for s in model["priority"] if "curvature < 0.3" in s.get("if", ""))
        assert float(low_bracket["multiply_by"]) < 1.0
        assert model.get("distance_influence", 1) == 0


class TestRouteEndpoint:
    def _mock_gh_response(self, status_code=200, json_body=None):
        mock_resp = MagicMock(spec=httpx.Response)
        mock_resp.status_code = status_code
        mock_resp.json.return_value = json_body or GH_SUCCESS
        mock_resp.raise_for_status = MagicMock()
        return mock_resp

    def test_fastest_mode_calls_standard_profile(self):
        with patch("app.routing.httpx.AsyncClient") as MockClient:
            mock_instance = AsyncMock()
            MockClient.return_value.__aenter__.return_value = mock_instance
            mock_instance.post.return_value = self._mock_gh_response()

            resp = client.post(
                "/route",
                json={"points": SAMPLE_POINTS, "profile": "car", "mode": "fastest"},
            )

        assert resp.status_code == 200
        call_kwargs = mock_instance.post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs.args[1]
        assert payload["profile"] == "car"
        assert "custom_model" not in payload
        assert payload.get("ch.disable") is not True

    def test_kurvig_mode_sends_custom_model(self):
        with patch("app.routing.httpx.AsyncClient") as MockClient:
            mock_instance = AsyncMock()
            MockClient.return_value.__aenter__.return_value = mock_instance
            mock_instance.post.return_value = self._mock_gh_response()

            resp = client.post(
                "/route",
                json={"points": SAMPLE_POINTS, "profile": "car", "mode": "kurvig"},
            )

        assert resp.status_code == 200
        call_kwargs = mock_instance.post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs.args[1]
        assert payload["profile"] == "car_custom"
        assert "custom_model" in payload
        assert payload["ch.disable"] is True

    def test_direkt_mode_sends_custom_model(self):
        with patch("app.routing.httpx.AsyncClient") as MockClient:
            mock_instance = AsyncMock()
            MockClient.return_value.__aenter__.return_value = mock_instance
            mock_instance.post.return_value = self._mock_gh_response()

            resp = client.post(
                "/route",
                json={"points": SAMPLE_POINTS, "profile": "bike", "mode": "direkt"},
            )

        assert resp.status_code == 200
        call_kwargs = mock_instance.post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs.args[1]
        assert payload["profile"] == "bike_custom"
        assert "custom_model" in payload

    def test_foot_profile_kurvig_uses_foot_profile(self):
        """foot hat kein _custom-Profil; kurvig-Modus fällt auf foot zurück."""
        with patch("app.routing.httpx.AsyncClient") as MockClient:
            mock_instance = AsyncMock()
            MockClient.return_value.__aenter__.return_value = mock_instance
            mock_instance.post.return_value = self._mock_gh_response()

            resp = client.post(
                "/route",
                json={"points": SAMPLE_POINTS, "profile": "foot", "mode": "kurvig"},
            )

        assert resp.status_code == 200
        call_kwargs = mock_instance.post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs.args[1]
        assert payload["profile"] == "foot"

    def test_invalid_mode_returns_422(self):
        resp = client.post(
            "/route",
            json={"points": SAMPLE_POINTS, "profile": "car", "mode": "unknownmode"},
        )
        assert resp.status_code == 422

    def test_invalid_profile_returns_422(self):
        resp = client.post(
            "/route",
            json={"points": SAMPLE_POINTS, "profile": "hovercraft", "mode": "fastest"},
        )
        assert resp.status_code == 422

    def test_too_few_points_returns_422(self):
        resp = client.post(
            "/route",
            json={"points": [[9.5, 47.1]], "profile": "car", "mode": "fastest"},
        )
        assert resp.status_code == 422

    def test_graphhopper_error_returns_502(self):
        with patch("app.routing.httpx.AsyncClient") as MockClient:
            mock_instance = AsyncMock()
            MockClient.return_value.__aenter__.return_value = mock_instance
            error_resp = self._mock_gh_response(status_code=400, json_body={"message": "bad request"})
            mock_instance.post.return_value = error_resp

            resp = client.post(
                "/route",
                json={"points": SAMPLE_POINTS, "profile": "car", "mode": "fastest"},
            )

        assert resp.status_code == 502

    def test_response_contains_paths(self):
        with patch("app.routing.httpx.AsyncClient") as MockClient:
            mock_instance = AsyncMock()
            MockClient.return_value.__aenter__.return_value = mock_instance
            mock_instance.post.return_value = self._mock_gh_response()

            resp = client.post(
                "/route",
                json={"points": SAMPLE_POINTS, "profile": "car", "mode": "fastest"},
            )

        assert resp.status_code == 200
        data = resp.json()
        assert "paths" in data
