# Plan: FastAPI Backend Grundstruktur (Issue #3)

**Spec:** docs/superpowers/specs/2026-06-10-fastapi-backend-grundstruktur-design.md  
**Datum:** 2026-06-10

## Recherche

- FastAPI `include_router` + `APIRouter(prefix=...)`: offizielle Docs bestätigt
- `TestClient` (sync) aus `fastapi.testclient`: direkt nutzbar, keine extra Deps
- `httpx` bereits in `requirements.txt` — TestClient nutzt es intern (FastAPI 0.115+)

## Schritte

1. **Tests schreiben** (TDD):
   - `backend/tests/conftest.py` — TestClient-Fixture
   - `backend/tests/test_health.py` — `/health` Endpunkt
   - `backend/tests/test_routes_circular.py` — `/api/routes/circular` Endpunkt

2. **Module anlegen**:
   - `backend/app/config.py` — `GRAPHHOPPER_URL`
   - `backend/app/models/__init__.py`, `backend/app/models/routes.py`
   - `backend/app/routers/__init__.py`, `backend/app/routers/health.py`,
     `backend/app/routers/routes.py`

3. **`backend/app/main.py` refaktorieren** — nur App-Setup + include_router

4. **Tests ausführen** — alle grün

5. **Commit + PR**
