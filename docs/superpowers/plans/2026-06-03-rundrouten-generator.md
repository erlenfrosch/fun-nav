# Plan: Rundrouten-Generator

**Issue:** #6
**Spec:** docs/superpowers/specs/2026-06-03-rundrouten-generator-design.md
**Datum:** 2026-06-03

## Recherche-Quellen

- GraphHopper API-Doku: https://github.com/graphhopper/graphhopper/blob/master/docs/web/api-doc.md
- GraphHopper Round-Trip-Curl: `algorithm=round_trip` + `round_trip.distance` + `ch.disable=true`
- FastAPI: https://fastapi.tiangolo.com/

## Aufgaben

- [x] Branch `agent/issue-6` anlegen
- [x] Spec schreiben
- [x] Plan schreiben
- [ ] Tests schreiben (TDD): `backend/tests/test_round_trip.py`
- [ ] `backend/requirements.txt` um pytest + respx erweitern
- [ ] Backend-Endpunkt implementieren: `POST /api/round-trip` in `backend/app/main.py`
- [ ] Frontend-Formular: `frontend/src/RoundTripForm.jsx` + `frontend/src/App.jsx` anpassen
- [ ] Tests lokal ausführen
- [ ] Committen + Pushen + PR öffnen

## Entscheidungen

- Endpunkt direkt in `main.py` — Codebase ist noch klein, kein Router-Submodul nötig
- `respx` für httpx-Mocking (passt zu bereits verwendetem `httpx`)
- `GRAPHHOPPER_URL` per Env-Variable konfigurierbar (default: `http://graphhopper:8989`)
- Kein Leaflet/Kartenvisualisierung — Scope ist der Algorithmus, nicht das UI
