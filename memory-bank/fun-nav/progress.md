# Progress

## Fertig

- Monorepo-Setup (Issue #1): frontend, backend, graphhopper, docker-compose, scripts
- GraphHopper DACH-Setup (Issue #2, Branch agent/issue-2):
  - config.yml mit car + car_custom (Custom Model) + LM-Profil
  - download-osm.sh mit OSM_REGION-Variable (dach/germany/austria/switzerland/test)
  - docker-compose.yml healthcheck + latest-Image
  - Infrastruktur-Tests (tests/test_infrastructure.sh)
- FastAPI Backend Grundstruktur (Issue #3, Branch agent/issue-3):
  - Schichtenarchitektur: routers/, services/, models/
  - POST /api/routes/circular mit echter GraphHopper-Integration
  - Fehlerbehandlung: 502 bei GraphHopper-Ausfall
  - 11 pytest-Tests (alle grün)

## In Arbeit

- PR für Issue #3 öffnen

## Nächste Schritte

- Issue #4 (Frontend React PWA)
