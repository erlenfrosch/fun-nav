# Spec: FastAPI Backend Grundstruktur

**Issue:** #3  
**Branch:** agent/issue-3  
**Datum:** 2026-06-01

## Kontext

Das Backend-Grundgerüst existiert bereits teilweise (aus Issue #1). Dieses Issue
vervollständigt die FastAPI-Struktur gemäß Akzeptanzkriterien.

## Ist-Zustand

- `backend/app/main.py` – FastAPI App mit `/health` und CORS (allow_origins=`*`)
- `backend/requirements.txt` – fastapi, uvicorn, httpx (ohne pydantic)
- `backend/Dockerfile` – Python 3.11-slim, Uvicorn

## Änderungsbedarf

| # | Was | Warum |
|---|---|---|
| 1 | CORS auf `localhost:5173` einschränken | Wildcard `*` ist in Produktion unsicher |
| 2 | `pydantic` zu requirements.txt hinzufügen | Explizite Abhängigkeit, nicht nur transitiv |
| 3 | `routers/`, `services/`, `models/` anlegen | Ordnerstruktur laut Issue-Spec |
| 4 | Tests für `/health` schreiben | TDD-Anforderung; Regressionssicherung |

## Akzeptanzkriterium

`curl localhost:8000/health` → `{"status":"ok"}`  
Alle Tests grün.
