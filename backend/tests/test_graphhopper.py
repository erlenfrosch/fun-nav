import pytest
from unittest.mock import patch, MagicMock

from app.services.graphhopper import (
    build_route_request,
    route,
    get_route,
    CUSTOM_MODELS,
    GRAPHHOPPER_BASE_URL,
)

SAMPLE_POINTS = [[13.388860, 52.517037], [13.397634, 52.529407]]


class TestBuildRouteRequest:
    def test_kurvenreich_sets_profile(self):
        req = build_route_request(SAMPLE_POINTS, "kurvenreich")
        assert req["profile"] == "bike_custom"

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
        with pytest.raises(ValueError, match="Unbekannter Modus"):
            build_route_request(SAMPLE_POINTS, "unbekannt")


class TestCustomModelDifferences:
    def test_sehr_kurvenreich_has_stricter_curvature_threshold(self):
        k_condition = CUSTOM_MODELS["kurvenreich"]["priority"][0]["if"]
        sk_condition = CUSTOM_MODELS["sehr_kurvenreich"]["priority"][0]["if"]
        k_threshold = float(k_condition.split("< ")[1])
        sk_threshold = float(sk_condition.split("< ")[1])
        assert sk_threshold < k_threshold

    def test_sehr_kurvenreich_has_higher_curvature_boost(self):
        k_boost = CUSTOM_MODELS["kurvenreich"]["priority"][0]["multiply_by"]
        sk_boost = CUSTOM_MODELS["sehr_kurvenreich"]["priority"][0]["multiply_by"]
        assert sk_boost > k_boost

    def test_sehr_kurvenreich_also_avoids_trunk_roads(self):
        sk_condition = CUSTOM_MODELS["sehr_kurvenreich"]["priority"][1]["if"]
        k_condition = CUSTOM_MODELS["kurvenreich"]["priority"][1]["if"]
        assert "TRUNK" in sk_condition
        assert "TRUNK" not in k_condition

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
        with patch("app.services.graphhopper.httpx.Client") as mock_cls:
            mock_client = MagicMock()
            mock_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_cls.return_value.__exit__ = MagicMock(return_value=False)
            mock_client.post.return_value = self._mock_response({"paths": []})
            route(SAMPLE_POINTS, "kurvenreich")
            url = mock_client.post.call_args[0][0]
            assert url.endswith("/route")

    def test_route_sends_kurvenreich_custom_model(self):
        with patch("app.services.graphhopper.httpx.Client") as mock_cls:
            mock_client = MagicMock()
            mock_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_cls.return_value.__exit__ = MagicMock(return_value=False)
            mock_client.post.return_value = self._mock_response({"paths": []})
            route(SAMPLE_POINTS, "kurvenreich")
            sent_json = mock_client.post.call_args[1]["json"]
            assert sent_json["custom_model"] == CUSTOM_MODELS["kurvenreich"]

    def test_kurvenreich_and_sehr_kurvenreich_send_different_payloads(self):
        with patch("app.services.graphhopper.httpx.Client") as mock_cls:
            mock_client = MagicMock()
            mock_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_cls.return_value.__exit__ = MagicMock(return_value=False)
            mock_client.post.return_value = self._mock_response({"paths": []})

            route(SAMPLE_POINTS, "kurvenreich")
            payload_k = mock_client.post.call_args[1]["json"]["custom_model"]

            route(SAMPLE_POINTS, "sehr_kurvenreich")
            payload_sk = mock_client.post.call_args[1]["json"]["custom_model"]

            assert payload_k != payload_sk


class TestGetRoute:
    def _mock_response(self, data: dict):
        mock = MagicMock()
        mock.json.return_value = data
        mock.raise_for_status.return_value = None
        return mock

    def test_get_route_wraps_start_and_end_as_points(self):
        with patch("app.services.graphhopper.httpx.Client") as mock_cls:
            mock_client = MagicMock()
            mock_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_cls.return_value.__exit__ = MagicMock(return_value=False)
            mock_client.post.return_value = self._mock_response({"paths": []})
            start, end = [13.388860, 52.517037], [13.397634, 52.529407]
            get_route(start, end, "kurvenreich")
            sent_json = mock_client.post.call_args[1]["json"]
            assert sent_json["points"] == [start, end]
