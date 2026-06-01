# Plan: FastAPI Backend Grundstruktur

**Issue:** #3  
**Branch:** agent/issue-3  
**Datum:** 2026-06-01

## Quellen

- FastAPI CORS-Doku: https://fastapi.tiangolo.com/reference/middleware
- FastAPI Testing: https://fastapi.tiangolo.com/tutorial/testing

## Aufgaben

### 1. requirements.txt – pydantic ergänzen
Pydantic als explizite Abhängigkeit eintragen (wird von FastAPI transitiv benötigt,
soll aber explizit versioniert sein).

### 2. CORS einschränken (main.py)
`allow_origins=["*"]` → `allow_origins=["http://localhost:5173"]`

### 3. Ordnerstruktur anlegen
```
backend/app/
  routers/__init__.py
  services/__init__.py
  models/__init__.py
```

### 4. Tests schreiben (TDD – vor Fix)
```
backend/tests/__init__.py
backend/tests/test_health.py
```
Test: GET /health → 200, body == {"status": "ok"}

### 5. Commit & PR
- Alle Änderungen commiten
- PR öffnen mit "Closes #3"
