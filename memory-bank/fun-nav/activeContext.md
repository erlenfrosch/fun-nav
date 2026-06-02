# Active Context

## Aktueller Fokus

Issue #5: GraphHopper Custom Model für Kurvigkeits-Modi — implementiert auf Branch `agent/issue-5`.

Implementiert:
- `graphhopper/config.yml`: Motorcycle-Profil mit `weighting: custom` + leeres Default-Custom-Model
- `backend/app/services/graphhopper.py`: HTTP-Client `get_route()` + `average_curvature()`
- `backend/tests/test_graphhopper_service.py`: 7 Unit-Tests (alle grün)
- `backend/requirements.txt`: pytest + respx ergänzt

PR steht kurz vor der Erstellung.

## Offene Fragen

- Frontend-Integration (Route-Endpunkt in main.py, UI-Anbindung) — out of scope für Issue #5
- Integration-Tests mit echter GH-Instanz — für späteren Milestone

## Bekannte Blocker

Keine.
