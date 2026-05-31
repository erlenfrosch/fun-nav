# Spec: FastAPI Backend Grundstruktur

**Issue:** #3  
**Branch:** agent/issue-3  
**Datum:** 2026-05-31

## Problem

Das Backend `backend/app/main.py` enthält bereits einen Health-Endpoint und CORS-Middleware,
aber es fehlen die modularen Unterverzeichnisse (`routers/`, `services/`, `models/`) für
eine skalierbare FastAPI-Applikationsstruktur gemäß FastAPI "Bigger Applications"-Pattern.

## Lösung

Modulare Projektstruktur unter `backend/app/` einführen:

- `routers/` — APIRouter-Instanzen pro Funktionsbereich
- `services/` — Business-Logik, entkoppelt von HTTP-Schicht  
- `models/` — Pydantic-Modelle für Request/Response-Schemas

Den Health-Endpoint in einen eigenen Router extrahieren. CORS auf `http://localhost:5173`
einschränken (statt Wildcard). `pydantic` explizit in `requirements.txt` eintragen.

## Struktur nach Implementierung

```
backend/app/
├── __init__.py
├── main.py          # FastAPI-App, bindet Router ein
├── routers/
│   ├── __init__.py
│   └── health.py    # GET /health
├── services/
│   └── __init__.py
└── models/
    └── __init__.py
```

## Akzeptanzkriterium

`curl localhost:8000/health` → `{"status":"ok"}`  
`curl localhost:8000/docs` → OpenAPI-Doku erreichbar
