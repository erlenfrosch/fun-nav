# Plan: FastAPI Backend Grundstruktur

**Issue:** #3  
**Spec:** docs/superpowers/specs/2026-05-31-fastapi-backend-struktur-design.md  
**Datum:** 2026-05-31

## Recherche-Quellen

- FastAPI Bigger Applications: https://fastapi.tiangolo.com/tutorial/bigger-applications/
- FastAPI APIRouter Reference: https://fastapi.tiangolo.com/reference/apirouter/

## Aufgaben

- [x] Branch `agent/issue-3` anlegen
- [x] Spec schreiben
- [x] `backend/app/routers/__init__.py` anlegen
- [x] `backend/app/routers/health.py` — Health-Router mit GET /health
- [x] `backend/app/services/__init__.py` anlegen
- [x] `backend/app/models/__init__.py` anlegen
- [x] `backend/app/main.py` aktualisieren — Router einbinden, CORS auf localhost:5173
- [x] `backend/requirements.txt` — pydantic explizit eintragen
- [ ] Commit + Push + PR

## Entscheidungen

- Health-Endpoint in `routers/health.py` auslagern (statt direkt in main.py) — folgt
  FastAPI "Bigger Applications"-Muster, erleichtert zukünftige Erweiterungen
- CORS: `http://localhost:5173` explizit statt `*` (Issue-Anforderung, sicherer für Dev)
- `pydantic` explizit in requirements.txt — Abhängigkeit ist implizit durch FastAPI,
  aber explizit besser für Reproduzierbarkeit
- `services/` und `models/` zunächst nur als leere Module — Platzhalter für Issues #4+
