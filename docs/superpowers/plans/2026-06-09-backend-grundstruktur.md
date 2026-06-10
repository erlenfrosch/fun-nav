# Plan: FastAPI Backend Grundstruktur

**Spec:** docs/superpowers/specs/2026-06-09-backend-grundstruktur-design.md  
**Branch:** agent/issue-3  
**Datum:** 2026-06-09

## Tasks

1. [x] Branch `agent/issue-3` anlegen
2. [ ] `backend/app/models.py` — Pydantic-Modelle
3. [ ] `backend/app/services/__init__.py` + `graphhopper.py` — Async-HTTP-Client
4. [ ] `backend/app/routers/__init__.py` + `routes.py` — Route-Endpoint
5. [ ] `backend/app/main.py` — aufräumen, Router einbinden
6. [ ] `backend/requirements-dev.txt` — pytest, respx, pytest-asyncio
7. [ ] `backend/tests/__init__.py` + `test_routes.py` — TDD-Tests
8. [ ] Tests laufen lassen (`pytest backend/tests/`)
9. [ ] PR erstellen

## Implementierungsreihenfolge (TDD)

Tests zuerst schreiben (rot), dann Implementierung (grün).

### Test-Cases

1. `test_health` — GET /health → 200, `{"status": "ok"}`
2. `test_circular_route_success` — POST mit gemocktem GraphHopper → 200 + GeoJSON
3. `test_circular_route_graphhopper_down` — POST, GraphHopper nicht erreichbar → 502
4. `test_circular_route_graphhopper_error` — POST, GraphHopper antwortet mit 400 → 502
5. `test_circular_route_validation_error` — POST mit ungültigem Body → 422
