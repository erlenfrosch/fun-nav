"""
Endpoint-Tests für POST /route

Prüft die HTTP-Schicht: Validierung, Fehlercodes, korrekte Service-Delegation.
"""

import pytest
from unittest.mock import patch, MagicMock
import httpx
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

SAMPLE_POINTS = [[9.5, 47.1], [9.6, 47.2]]
GH_SUCCESS = {"paths": [{"distance": 12345.0, "time": 600000}]}


def _mock_gh(response_data=None, raise_exc=None):
    mock = MagicMock()
    if raise_exc:
        mock.side_effect = raise_exc
    else:
        mock.return_value.json.return_value = response_data or GH_SUCCESS
        mock.return_value.raise_for_status.return_value = None
    return mock


class TestRouteEndpoint:
    def test_kurvenreich_returns_200(self):
        with patch("services.graphhopper.httpx.post", _mock_gh()):
            resp = client.post("/route", json={"points": SAMPLE_POINTS, "mode": "kurvenreich"})
        assert resp.status_code == 200

    def test_sehr_kurvenreich_returns_200(self):
        with patch("services.graphhopper.httpx.post", _mock_gh()):
            resp = client.post("/route", json={"points": SAMPLE_POINTS, "mode": "sehr_kurvenreich"})
        assert resp.status_code == 200

    def test_response_contains_paths(self):
        with patch("services.graphhopper.httpx.post", _mock_gh()):
            resp = client.post("/route", json={"points": SAMPLE_POINTS, "mode": "kurvenreich"})
        assert "paths" in resp.json()

    def test_invalid_mode_returns_422(self):
        resp = client.post("/route", json={"points": SAMPLE_POINTS, "mode": "direktfahrt"})
        assert resp.status_code == 422

    def test_too_few_points_returns_422(self):
        resp = client.post("/route", json={"points": [SAMPLE_POINTS[0]], "mode": "kurvenreich"})
        assert resp.status_code == 422

    def test_graphhopper_http_error_returns_502(self):
        request = httpx.Request("POST", "http://test")
        response = httpx.Response(500, request=request)
        exc = httpx.HTTPStatusError("error", request=request, response=response)
        with patch("services.graphhopper.httpx.post", _mock_gh(raise_exc=exc)):
            resp = client.post("/route", json={"points": SAMPLE_POINTS, "mode": "kurvenreich"})
        assert resp.status_code == 502

    def test_health_still_works(self):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}
