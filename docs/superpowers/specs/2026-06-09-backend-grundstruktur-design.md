# Spec: FastAPI Backend Grundstruktur

**Issue:** #3  
**Branch:** agent/issue-3  
**Datum:** 2026-06-09

## Problem

Das bestehende `backend/app/main.py` enthält Platzhalter-Geometrie (Kreispunkte ohne
GraphHopper-Aufruf) und hat keine Testabdeckung. Für eine produktionsnahe Architektur
braucht das Backend:

- Klare Schichtentrennung (Router / Service / Modelle)
- Echte GraphHopper-Integration via `httpx`
- Pytest-Tests mit gemocktem GraphHopper

## Lösung

### Projektstruktur

```
backend/
  app/
    __init__.py
    main.py              FastAPI-App, CORS, Router einbinden
    models.py            Pydantic Request/Response-Modelle
    routers/
      __init__.py
      routes.py          POST /api/routes/circular
    services/
      __init__.py
      graphhopper.py     Async-Client für GraphHopper /route
  tests/
    __init__.py
    test_routes.py       TestClient + respx-Mocks
  requirements.txt       Runtime-Dependencies
  requirements-dev.txt   Test-Dependencies (pytest, respx, …)
```

### GraphHopper-Integration

Algorithmus für Kreisroute:
1. Geschwindigkeit je Kurvigkeit: `sehr_kurvenreich` → 35 km/h, `kurvenreich` → 45 km/h
2. Distanz = Geschwindigkeit × duration_min / 60
3. 4 Zwischenpunkte im Kreis (N/E/S/W) + Startpunkt als Rückgabe-Ziel
4. POST `GRAPHHOPPER_URL/route` mit `points`, `profile=auto`, `points_encoded=false`

Fehlerbehandlung:
- GraphHopper nicht erreichbar → HTTP 502 mit klarer Fehlermeldung
- GraphHopper gibt Fehler zurück → HTTP 502, Fehlermeldung weitergeben

### Modelle

**Request:** `CircularRouteRequest`
- `lat: float`, `lon: float`
- `duration_min: int` (10–480)
- `curviness: Literal["kurvenreich", "sehr_kurvenreich"]`

**Response:** `CircularRouteResponse`
- `routes: list[Route]`

**Route:**
- `id: str`
- `duration_min: int`
- `distance_km: float`
- `geometry: dict`  (GeoJSON LineString)

## Akzeptanzkriterien

- [ ] `GET /health` → `{"status": "ok"}`
- [ ] `POST /api/routes/circular` → Route mit echter Geometrie (GraphHopper)
- [ ] Bei GraphHopper-Ausfall → HTTP 502 mit Fehlermeldung
- [ ] Alle Tests grün (`pytest backend/tests/`)
- [ ] Kein Raw-SQL, kein ORM (nur HTTP-Calls)

## Recherche-Quellen

- FastAPI Docs: https://fastapi.tiangolo.com/tutorial/bigger-applications/
- GraphHopper Routing API: https://docs.graphhopper.com/#operation/postRoute
