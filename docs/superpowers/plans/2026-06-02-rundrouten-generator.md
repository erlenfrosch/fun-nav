# Plan: Rundrouten-Generator Algorithmus

**Datum:** 2026-06-02  
**Issue:** #6  
**Spec:** docs/superpowers/specs/2026-06-02-rundrouten-generator-design.md

## Quellen

- GraphHopper POST /route API: https://docs.graphhopper.com/openapi/routing/postroute.md
  - Format: `{"points": [[lng, lat], ...], "profile": "car", "instructions": false}`
  - Response: `{"paths": [{"time": ms, "distance": m}]}`

## Tasks

1. `backend/app/models/route.py` — Pydantic-Modelle (Request/Response)
2. `backend/app/services/circular_route.py` — Kern-Algorithmus
3. `backend/app/routes/circular_route.py` — FastAPI-Router
4. `backend/tests/__init__.py` + `backend/tests/test_circular_route.py` — Unit-Tests (TDD)
5. `backend/pytest.ini` — asyncio_mode = auto
6. `backend/requirements.txt` — pytest, pytest-asyncio ergänzen
7. `backend/app/main.py` — Router registrieren

## Entscheidungen

- **6 Routen aus 8 Wegpunkten**: Indices 0–5 (0°, 45°, 90°, 135°, 180°, 225°)
- **Curviness**: `distance_m / (2 * radius_km * 1000)` — einfach, keine GraphHopper-Details nötig
- **GRAPHHOPPER_URL**: aus env-Variable, Default `http://graphhopper:8989`
- **Timeout**: 10 s pro Request
