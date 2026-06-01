# Plan: FastAPI Backend Grundstruktur (Issue #3)

## Quellen
- FastAPI Bigger Applications: https://fastapi.tiangolo.com/tutorial/bigger-applications
- FastAPI CORS: https://fastapi.tiangolo.com/tutorial/cors

## Implementierungsschritte

1. **requirements.txt** — `pydantic` ergänzen (Version >=2.0)
2. **Ordnerstruktur anlegen**
   - `backend/app/routers/__init__.py`
   - `backend/app/routers/health.py` — `APIRouter` mit `GET /health`
   - `backend/app/services/__init__.py`
   - `backend/app/models/__init__.py`
3. **main.py aktualisieren**
   - CORS: `allow_origins=["http://localhost:5173"]`
   - `include_router(health.router)`
   - Direkten `/health`-Handler entfernen (liegt jetzt im Router)
4. **Tests schreiben (zuerst)**
   - `backend/tests/__init__.py`
   - `backend/tests/test_health.py` — `TestClient` prüft GET /health → 200, body `{"status":"ok"}`
5. **Tests grün**
