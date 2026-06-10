# Plan: FastAPI Backend Grundstruktur

**Issue:** #3  
**Branch:** agent/issue-3  
**Datum:** 2026-06-10

## Aufgaben

- [x] Branch `agent/issue-3` anlegen
- [x] Tests schreiben (TDD): `tests/test_health.py`, `tests/test_routes.py`
- [x] `app/models/routes.py` — Pydantic-Modelle für Request/Response
- [x] `app/routers/health.py` — `GET /health`
- [x] `app/routers/routes.py` — `POST /api/routes/circular`
- [x] `app/services/graphhopper.py` — GraphHopper-Client (Platzhalter)
- [x] `app/main.py` refactored — Router eingebunden, CORS auf `localhost:5173` eingeschränkt
- [x] `requirements.txt` — pydantic==2.9.2 hinzugefügt
- [x] Alle 8 Tests grün

## Entscheidungen

- **CORS `*` → `localhost:5173`** — Issue verlangt explizit Frontend-Origin
- **Ordnerstruktur `routers/`, `services/`, `models/`** — laut Issue-Anforderung
- **`services/graphhopper.py`** als Platzhalter — echte GraphHopper-Integration kommt in späterem Issue
- **Response-Modell via Pydantic** — typsicher, kein Raw-Dict

## Quellen

- FastAPI Docs: https://fastapi.tiangolo.com/tutorial/bigger-applications/
- Pydantic v2: https://docs.pydantic.dev/latest/
