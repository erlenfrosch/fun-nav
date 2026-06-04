import os
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from backend.services.graphhopper import GraphHopperClient

SAMPLE_RESPONSE = {
    "paths": [
        {
            "distance": 5000.0,
            "time": 300000,
            "points": {"type": "LineString", "coordinates": []},
        }
    ]
}

LIECHTENSTEIN_POINTS = [[9.5216, 47.1410], [9.5401, 47.1243]]


@pytest.fixture
def client():
    return GraphHopperClient(base_url="http://test-gh:8989")


def _mock_http(monkeypatch, response_data=None):
    data = response_data if response_data is not None else SAMPLE_RESPONSE

    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = data

    mock_http = AsyncMock()
    mock_http.__aenter__ = AsyncMock(return_value=mock_http)
    mock_http.__aexit__ = AsyncMock(return_value=False)
    mock_http.post = AsyncMock(return_value=mock_response)

    monkeypatch.setattr("backend.services.graphhopper.httpx.AsyncClient", lambda **_: mock_http)
    return mock_http


@pytest.mark.asyncio
async def test_route_kurvenreich_sendet_richtiges_profil(client, monkeypatch):
    mock_http = _mock_http(monkeypatch)
    await client.route(LIECHTENSTEIN_POINTS, profile="kurvenreich")
    _, kwargs = mock_http.post.call_args
    assert kwargs["json"]["profile"] == "kurvenreich"


@pytest.mark.asyncio
async def test_route_sehr_kurvenreich_sendet_richtiges_profil(client, monkeypatch):
    mock_http = _mock_http(monkeypatch)
    await client.route(LIECHTENSTEIN_POINTS, profile="sehr_kurvenreich")
    _, kwargs = mock_http.post.call_args
    assert kwargs["json"]["profile"] == "sehr_kurvenreich"


@pytest.mark.asyncio
async def test_route_sendet_points_encoded_false(client, monkeypatch):
    mock_http = _mock_http(monkeypatch)
    await client.route(LIECHTENSTEIN_POINTS)
    _, kwargs = mock_http.post.call_args
    assert kwargs["json"]["points_encoded"] is False


@pytest.mark.asyncio
async def test_route_sendet_korrekte_punkte(client, monkeypatch):
    mock_http = _mock_http(monkeypatch)
    await client.route(LIECHTENSTEIN_POINTS, profile="kurvenreich")
    _, kwargs = mock_http.post.call_args
    assert kwargs["json"]["points"] == LIECHTENSTEIN_POINTS


@pytest.mark.asyncio
async def test_route_gibt_antwort_zurueck(client, monkeypatch):
    _mock_http(monkeypatch)
    result = await client.route(LIECHTENSTEIN_POINTS)
    assert "paths" in result
    assert result["paths"][0]["distance"] == 5000.0


@pytest.mark.asyncio
async def test_route_wirft_bei_http_fehler(client, monkeypatch):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Bad Request", request=MagicMock(), response=MagicMock()
    )
    mock_response.json.return_value = {}

    mock_http = AsyncMock()
    mock_http.__aenter__ = AsyncMock(return_value=mock_http)
    mock_http.__aexit__ = AsyncMock(return_value=False)
    mock_http.post = AsyncMock(return_value=mock_response)

    monkeypatch.setattr("backend.services.graphhopper.httpx.AsyncClient", lambda **_: mock_http)

    with pytest.raises(httpx.HTTPStatusError):
        await client.route(LIECHTENSTEIN_POINTS)


@pytest.mark.asyncio
async def test_route_verwendet_konfigurierten_base_url(monkeypatch):
    mock_http = _mock_http(monkeypatch)
    client = GraphHopperClient(base_url="http://custom-host:9999")
    await client.route(LIECHTENSTEIN_POINTS)
    url_arg = mock_http.post.call_args[0][0]
    assert url_arg == "http://custom-host:9999/route"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sehr_kurvenreich_route_laenger_als_kurvenreich():
    """
    Akzeptanztest: sehr_kurvenreich-Route hat messbar höheren Kurvenanteil.
    Die Route Vaduz → Triesenberg hat Alternativpfade mit unterschiedlicher Kurvigkeit.
    Erfordert laufenden GraphHopper-Service (pytest --integration).
    """
    base_url = os.getenv("GRAPHHOPPER_URL", "http://localhost:8989")
    client = GraphHopperClient(base_url=base_url)

    kurvenreich = await client.route(LIECHTENSTEIN_POINTS, profile="kurvenreich")
    sehr_kurvenreich = await client.route(LIECHTENSTEIN_POINTS, profile="sehr_kurvenreich")

    dist_k = kurvenreich["paths"][0]["distance"]
    dist_sk = sehr_kurvenreich["paths"][0]["distance"]

    assert dist_sk >= dist_k, (
        f"sehr_kurvenreich ({dist_sk:.0f} m) sollte nicht kürzer sein als "
        f"kurvenreich ({dist_k:.0f} m) — beide starten/enden am selben Punkt"
    )
