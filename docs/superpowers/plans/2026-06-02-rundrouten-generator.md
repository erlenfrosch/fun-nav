# Plan: Rundrouten-Generator Algorithmus

**Issue:** #6  
**Spec:** docs/superpowers/specs/2026-06-02-rundrouten-generator-design.md  
**Datum:** 2026-06-02

## Recherche-Quellen

- GraphHopper Route API: https://docs.graphhopper.com/openapi/routing/getroute  
  POST /route — points als [lon, lat], time in ms, distance in m, points_encoded=false für Array-Format
- Inverse Haversine: https://www.sqlpey.com/python/solved-haversine-formula-bearings-distance-gps/  
  Zielpunkt aus Startpunkt + Kurs + Distanz

## Dateien

| Datei | Aktion |
|---|---|
| `backend/app/services/__init__.py` | Neu (leer) |
| `backend/app/services/circular_route.py` | Neu — Kernalgorithmus |
| `backend/app/main.py` | Erweiterung — POST /routes Endpunkt |
| `backend/tests/__init__.py` | Neu (leer) |
| `backend/tests/test_circular_route.py` | Neu — Unit-Tests mit Mock-GH |
| `backend/requirements-dev.txt` | Neu — pytest, pytest-asyncio, pytest-httpx |

## Implementierungs-Tasks

1. `backend/app/services/__init__.py` anlegen
2. `circular_route.py` — Hilfsfunktionen: `destination_point`, `calculate_radius`, `generate_waypoints`, `select_route_pairs`
3. `circular_route.py` — async `fetch_route`, `generate_circular_routes`
4. `circular_route.py` — `calculate_curviness` (Detour-Faktor)
5. `main.py` — POST /routes Endpunkt (liest GRAPHHOPPER_URL aus ENV)
6. Tests schreiben (TDD-Stil): Einheitstests für pure Funktionen, async Test für Akzeptanzkriterium mit Mock
7. `requirements-dev.txt` anlegen

## Entscheidungen

- **asyncio.gather**: Alle 6 GH-Anfragen parallel → minimale Latenz
- **Detour-Faktor als Curviness**: `route_km / (2 * radius_km)` — einfach, keine GH path_details nötig
- **6 Routen**: 4 × 180°-Paare + 2 × 135°-Paare — ausreichend Vielfalt für Top-3-Selektion
- **pytest-asyncio**: async Tests für `generate_circular_routes` mit httpx-Mock
- **httpx.AsyncClient**: bereits in requirements.txt, konform mit FastAPI-Ökosystem
