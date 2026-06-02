# Plan: Rundrouten-Generator Algorithmus

**Issue:** #6  
**Spec:** docs/superpowers/specs/2026-06-02-rundrouten-generator-design.md  
**Datum:** 2026-06-02

## Recherche-Quellen

- GraphHopper Route API: https://docs.graphhopper.com/openapi/routing/getroute  
  POST /route — points als [lon, lat], time in ms, distance in m
- Inverse Haversine: bearing + Distanz → Zielpunkt

## Dateien

| Datei | Aktion |
|---|---|
| `backend/app/services/circular_route.py` | Neu — Kernalgorithmus |
| `backend/app/main.py` | Erweiterung — POST /api/circular-routes Endpunkt |
| `backend/tests/test_circular_route.py` | Neu — 22 Unit-Tests mit Mock-GH |
| `backend/pytest.ini` | Neu — asyncio_mode = auto |
| `backend/requirements.txt` | Ergänzt — pytest, pytest-asyncio |

## Entscheidungen

- **asyncio.gather**: Alle 6 GH-Anfragen parallel → minimale Latenz
- **Curviness**: Referenz-Geschwindigkeit / tatsächliche Geschwindigkeit — höherer Score = langsamere, kurvenreichere Route
- **6 Routen**: 3 × 180°-Paare, je beide Richtungen — ausreichend Vielfalt für Top-3-Selektion
- **pytest-asyncio**: async Tests für `generate_circular_routes` mit httpx-Mock
