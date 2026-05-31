import json
import pytest
import respx
import httpx

from app.services.graphhopper import route_curvy, CUSTOM_MODELS

GH_URL = "http://gh-test:8989"
START = (48.137, 11.576)  # München
END = (48.200, 11.700)

MOCK_ROUTE_RESPONSE = {
    "paths": [
        {
            "distance": 15000.0,
            "time": 3600000,
            "points": {"type": "LineString", "coordinates": []},
        }
    ]
}


@pytest.mark.asyncio
@respx.mock
async def test_route_curvy_sendet_kurvenreich_custom_model():
    route = respx.post(f"{GH_URL}/route").mock(
        return_value=httpx.Response(200, json=MOCK_ROUTE_RESPONSE)
    )

    await route_curvy(START, END, "kurvenreich", base_url=GH_URL)

    assert route.called
    body = json.loads(route.calls[0].request.content)
    assert body["custom_model"] == CUSTOM_MODELS["kurvenreich"]
    assert body["profile"] == "bike_custom"


@pytest.mark.asyncio
@respx.mock
async def test_route_curvy_sendet_sehr_kurvenreich_custom_model():
    route = respx.post(f"{GH_URL}/route").mock(
        return_value=httpx.Response(200, json=MOCK_ROUTE_RESPONSE)
    )

    await route_curvy(START, END, "sehr_kurvenreich", base_url=GH_URL)

    assert route.called
    body = json.loads(route.calls[0].request.content)
    assert body["custom_model"] == CUSTOM_MODELS["sehr_kurvenreich"]
    assert body["profile"] == "bike_custom"


@pytest.mark.asyncio
@respx.mock
async def test_koordinaten_werden_als_lon_lat_gesendet():
    """GraphHopper erwartet [lon, lat], nicht [lat, lon]."""
    route = respx.post(f"{GH_URL}/route").mock(
        return_value=httpx.Response(200, json=MOCK_ROUTE_RESPONSE)
    )

    await route_curvy(START, END, "kurvenreich", base_url=GH_URL)

    body = json.loads(route.calls[0].request.content)
    # START = (lat=48.137, lon=11.576) → GH Point = [11.576, 48.137]
    assert body["points"][0] == [START[1], START[0]]
    assert body["points"][1] == [END[1], END[0]]


def test_sehr_kurvenreich_hat_striktere_curvature_schwelle():
    """sehr_kurvenreich bevorzugt nur stärker kurvige Straßen (Schwelle 0.4 < 0.7)."""
    k = CUSTOM_MODELS["kurvenreich"]
    sk = CUSTOM_MODELS["sehr_kurvenreich"]

    k_threshold = float(k["priority"][0]["if"].split("< ")[1])
    sk_threshold = float(sk["priority"][0]["if"].split("< ")[1])

    assert sk_threshold < k_threshold, (
        "sehr_kurvenreich muss strengere Curvature-Schwelle haben als kurvenreich"
    )


def test_sehr_kurvenreich_hat_hoehere_prioritaet():
    """sehr_kurvenreich gewichtet kurvige Straßen stärker (3.0 > 1.5)."""
    k_multiplier = float(CUSTOM_MODELS["kurvenreich"]["priority"][0]["multiply_by"])
    sk_multiplier = float(CUSTOM_MODELS["sehr_kurvenreich"]["priority"][0]["multiply_by"])

    assert sk_multiplier > k_multiplier, (
        "sehr_kurvenreich muss kurvige Straßen stärker gewichten als kurvenreich"
    )


@pytest.mark.asyncio
async def test_unbekannter_modus_wirft_valueerror():
    with pytest.raises(ValueError, match="Unbekannter Modus"):
        await route_curvy(START, END, "turbo_kurvig", base_url=GH_URL)


@pytest.mark.asyncio
@respx.mock
async def test_gh_fehler_wirft_http_status_error():
    respx.post(f"{GH_URL}/route").mock(
        return_value=httpx.Response(400, json={"message": "Bad request"})
    )

    with pytest.raises(httpx.HTTPStatusError):
        await route_curvy(START, END, "kurvenreich", base_url=GH_URL)
