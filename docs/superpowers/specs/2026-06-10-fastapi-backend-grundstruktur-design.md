# Spec: FastAPI Backend Grundstruktur (Issue #3)

**Datum:** 2026-06-10  
**Branch:** agent/issue-3  
**Issue:** #3

## Ziel

Saubere Modulstruktur für das FastAPI-Backend: Routers, Models und Konfiguration
als separate Module. Tests für alle Endpunkte.

## Ist-Zustand

Alles in `backend/app/main.py` — kein Routing-Modul, keine Models-Datei, keine Tests.

## Soll-Zustand

```
backend/
  app/
    __init__.py
    main.py           # App-Setup, CORS, include_router
    config.py         # GRAPHHOPPER_URL aus Umgebung
    models/
      __init__.py
      routes.py       # CircularRouteRequest (Pydantic)
    routers/
      __init__.py
      health.py       # GET /health
      routes.py       # POST /api/routes/circular
  tests/
    __init__.py
    conftest.py       # TestClient-Fixture
    test_health.py
    test_routes_circular.py
```

## Endpunkte

| Methode | Pfad                   | Beschreibung                    |
|---------|------------------------|---------------------------------|
| GET     | /health                | Gibt `{"status": "ok"}` zurück  |
| POST    | /api/routes/circular   | Berechnet Rundrouten-Vorschläge |

## Akzeptanzkriterien

- `GET /health` → 200 `{"status": "ok"}`
- `POST /api/routes/circular` mit gültigen Daten → 200, enthält `routes`-Liste
- `POST /api/routes/circular` mit ungültiger `curviness` → 422
- `POST /api/routes/circular` mit fehlenden Feldern → 422
- Alle Tests grün: `pytest backend/`
- Keine Funktionsänderung an bestehenden Endpunkten
