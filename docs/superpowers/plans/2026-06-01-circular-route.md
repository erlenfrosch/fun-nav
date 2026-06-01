# Plan: POST /api/routes/circular

Spec: `docs/superpowers/specs/2026-06-01-circular-route-design.md`

## Implementierungsschritte

1. **Branch** — `agent/issue-7` erstellen (erledigt)
2. **Tests schreiben (TDD)** — `backend/tests/test_routes_circular.py`
3. **Pydantic-Schemas** — `backend/app/models/schemas.py`
4. **Router** — `backend/app/routers/routes.py`
5. **main.py erweitern** — Router einbinden
6. **Dev-Requirements & pytest.ini** — für lokale Testausführung
7. **Tests ausführen** — alle Unit-Tests grün
8. **Commit & Push** — auf `agent/issue-7`
9. **PR erstellen** — gegen `main`

## Datei-Liste

| Datei | Aktion |
|---|---|
| `backend/tests/__init__.py` | neu (leer) |
| `backend/tests/test_routes_circular.py` | neu |
| `backend/app/models/__init__.py` | neu (leer) |
| `backend/app/models/schemas.py` | neu |
| `backend/app/routers/__init__.py` | neu (leer) |
| `backend/app/routers/routes.py` | neu |
| `backend/app/main.py` | erweitern |
| `backend/requirements-dev.txt` | neu |
| `backend/pytest.ini` | neu |

## Test-Strategie

### Unit-Tests (kein echtes GraphHopper)
- `httpx.AsyncClient` via `unittest.mock.patch` gemockt
- Testen: 3 Routen zurückgegeben, korrektes Response-Schema, `very_high` akzeptiert
- Fehlerfälle: 503 bei `ConnectError`, 404 bei leeren `paths`, 422 bei ungültigem `curviness`

### Integration-Tests (`@pytest.mark.integration`)
- Benötigen laufenden GraphHopper auf Port 8989
- Ausführen mit: `pytest -m integration`
- Prüfen: 3 Routen, GeoJSON vorhanden, `duration_min` und `distance_km` > 0

## Quellen
- GraphHopper Round-Trip-API: https://docs.graphhopper.com/#operation/getRoute (round_trip algorithm)
- FastAPI Routing: https://fastapi.tiangolo.com/tutorial/bigger-applications/
