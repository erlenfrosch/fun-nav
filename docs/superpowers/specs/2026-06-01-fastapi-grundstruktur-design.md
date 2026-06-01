# Spec: FastAPI Backend Grundstruktur (Issue #3)

Branch: `agent/issue-3`
Issue: https://github.com/erlenfrosch/fun-nav/issues/3

## Ziel
Vollständige FastAPI-Grundstruktur mit Health-Endpoint, restriktivem CORS und modularer Ordnerstruktur.

## Akzeptanzkriterium
`curl localhost:8000/health` → `{"status":"ok"}`

## Scope
- `requirements.txt`: `pydantic` ergänzen
- CORS: `allow_origins=["http://localhost:5173"]` statt `*`
- Ordnerstruktur: `routers/`, `services/`, `models/` mit `__init__.py`
- Health-Route in eigenen Router auslagern (`routers/health.py`)
- Tests: `backend/tests/test_health.py` mit pytest + httpx

## Nicht in Scope
- Routing-Endpunkte (GraphHopper-Proxy) → eigenes Issue
- Auth, DB, Sessions
