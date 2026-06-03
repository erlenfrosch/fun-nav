import pytest
from unittest.mock import patch, MagicMock

from services.graphhopper import (
    build_route_request,
    route,
    CUSTOM_MODELS,
    GRAPHHOPPER_BASE_URL,
)

SAMPLE_POINTS = [[13.388860, 52.517037], [13.397634, 52.529407]]


class TestBuildRouteRequest:
    def test_kurvenreich_sets_profile(self):
        req = build_route_request(SAMPLE_POINTS, "kurvenreich")
        assert req["profile"] == "car_custom"

    def test_kurvenreich_sets_correct_custom_model(self):
        req = build_route_request(SAMPLE_POINTS, "kurvenreich")
        assert req["custom_model"] == CUSTOM_MODELS["kurvenreich"]

    def test_sehr_kurvenreich_sets_correct_custom_model(self):
        req = build_route_request(SAMPLE_POINTS, "sehr_kurvenreich")
        assert req["custom_model"] == CUSTOM_MODELS["sehr_kurvenreich"]

    def test_passes_points_through(self):
        req = build_route_request(SAMPLE_POINTS, "kurvenreich")
        assert req["points"] == SAMPLE_POINTS

    def test_ch_disabled_in_request(self):
        req = build_route_request(SAMPLE_POINTS, "kurvenreich")
        assert req["ch.disable"] is True

    def test_invalid_mode_raises(self):
        with pytest.raises(ValueError, match="Unknown mode"):
            build_route_request(SAMPLE_POINTS, "unbekannt")


class TestCustomModelDifferences:
    def test_sehr_kurvenreich_has_stricter_curvature_threshold(self):
        k_condition = CUSTOM_MODELS["kurvenreich"]["priority"][0]["if"]
        sk_condition = CUSTOM_MODELS["sehr_kurvenreich"]["priority"][0]["if"]
        # kurvenreich bevorzugt Straßen mit curvature < 0.7 (großzügiger)
        # sehr_kurvenreich bevorzugt nur curvature < 0.4 (strenger = kurvigere Straßen)
        k_threshold = float(k_condition.split("< ")[1])
        sk_threshold = float(sk_condition.split("< ")[1])
        assert sk_threshold < k_threshold

    def test_sehr_kurvenreich_has_higher_curvature_boost(self):
        k_boost = CUSTOM_MODELS["kurvenreich"]["priority"][0]["multiply_by"]
        sk_boost = CUSTOM_MODELS["sehr_kurvenreich"]["priority"][0]["multiply_by"]
        assert sk_boost > k_boost

    def test_sehr_kurvenreich_also_avoids_trunk_roads(self):
        sk_motorway_condition = CUSTOM_MODELS["sehr_kurvenreich"]["priority"][1]["if"]
        k_motorway_condition = CUSTOM_MODELS["kurvenreich"]["priority"][1]["if"]
        assert "TRUNK" in sk_motorway_condition
        assert "TRUNK" not in k_motorway_condition

    def test_sehr_kurvenreich_has_lower_motorway_penalty(self):
        k_penalty = CUSTOM_MODELS["kurvenreich"]["priority"][1]["multiply_by"]
        sk_penalty = CUSTOM_MODELS["sehr_kurvenreich"]["priority"][1]["multiply_by"]
        assert sk_penalty < k_penalty

    def test_modes_produce_different_custom_models(self):
        assert CUSTOM_MODELS["kurvenreich"] != CUSTOM_MODELS["sehr_kurvenreich"]


class TestRoute:
    def _mock_response(self, data: dict):
        mock = MagicMock()
        mock.json.return_value = data
        mock.raise_for_status.return_value = None
        return mock

    def test_route_calls_graphhopper_endpoint(self):
        with patch("services.graphhopper.httpx.post") as mock_post:
            mock_post.return_value = self._mock_response({"paths": []})
            route(SAMPLE_POINTS, "kurvenreich")
            url = mock_post.call_args[0][0]
            assert url.endswith("/route")

    def test_route_sends_kurvenreich_custom_model(self):
        with patch("services.graphhopper.httpx.post") as mock_post:
            mock_post.return_value = self._mock_response({"paths": []})
            route(SAMPLE_POINTS, "kurvenreich")
            sent_json = mock_post.call_args[1]["json"]
            assert sent_json["custom_model"] == CUSTOM_MODELS["kurvenreich"]

    def test_route_sends_sehr_kurvenreich_custom_model(self):
        with patch("services.graphhopper.httpx.post") as mock_post:
            mock_post.return_value = self._mock_response({"paths": []})
            route(SAMPLE_POINTS, "sehr_kurvenreich")
            sent_json = mock_post.call_args[1]["json"]
            assert sent_json["custom_model"] == CUSTOM_MODELS["sehr_kurvenreich"]

    def test_route_sends_car_custom_profile(self):
        with patch("services.graphhopper.httpx.post") as mock_post:
            mock_post.return_value = self._mock_response({"paths": []})
            route(SAMPLE_POINTS, "kurvenreich")
            sent_json = mock_post.call_args[1]["json"]
            assert sent_json["profile"] == "car_custom"

    def test_route_returns_graphhopper_response(self):
        expected = {"paths": [{"distance": 2500.0, "time": 300000}]}
        with patch("services.graphhopper.httpx.post") as mock_post:
            mock_post.return_value = self._mock_response(expected)
            result = route(SAMPLE_POINTS, "kurvenreich")
            assert result == expected

    def test_route_custom_base_url(self):
        with patch("services.graphhopper.httpx.post") as mock_post:
            mock_post.return_value = self._mock_response({"paths": []})
            route(SAMPLE_POINTS, "kurvenreich", base_url="http://localhost:8989")
            url = mock_post.call_args[0][0]
            assert url == "http://localhost:8989/route"

    def test_kurvenreich_and_sehr_kurvenreich_send_different_payloads(self):
        with patch("services.graphhopper.httpx.post") as mock_post:
            mock_post.return_value = self._mock_response({"paths": []})

            route(SAMPLE_POINTS, "kurvenreich")
            payload_k = mock_post.call_args[1]["json"]["custom_model"]

            route(SAMPLE_POINTS, "sehr_kurvenreich")
            payload_sk = mock_post.call_args[1]["json"]["custom_model"]

            assert payload_k != payload_sk
