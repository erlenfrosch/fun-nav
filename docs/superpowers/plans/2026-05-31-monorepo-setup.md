# Plan: Monorepo-Struktur + Docker Compose Grundgerüst

**Issue:** #1  
**Spec:** docs/superpowers/specs/2026-05-31-monorepo-setup-design.md  
**Datum:** 2026-05-31

## Recherche-Quellen

- GraphHopper Docker Compose: https://discuss.graphhopper.com/t/start-with-docker-compose/7901
- FastAPI Docker: https://fastapi.tiangolo.com/deployment/docker/
- Vite React PWA Monorepo: https://github.com/sreesankarsankarayya/timescale-fastapi-react-vite-pwa

## Aufgaben

- [x] Verzeichnisstruktur anlegen: `frontend/`, `backend/`, `graphhopper/`, `scripts/`, `docs/`
- [x] Spec schreiben
- [ ] `.gitignore` (OSM `.pbf`, `node_modules`, Python venvs, `__pycache__`)
- [ ] `docker-compose.yml` mit Services `graphhopper`, `backend`, `frontend`
- [ ] `graphhopper/config.yml` (GraphHopper 7 Dropwizard-Format)
- [ ] `backend/Dockerfile` + `requirements.txt` + `app/main.py` (Health-Endpoint)
- [ ] `frontend/Dockerfile` + `package.json` + `vite.config.js` + Quellcode
- [ ] `scripts/download-osm.sh` (Liechtenstein als Test-Datensatz)
- [ ] `README.md` mit Quickstart
- [ ] Commit + Push + PR

## Entscheidungen

- GraphHopper Image-Tag `7` (stabil, nicht `latest` — für Reproduzierbarkeit)
- OSM-Daten nicht im Repo (`.pbf` gitignored) — Download-Skript stattdessen
- Frontend: Vite + React, Dev-Server mit `--host 0.0.0.0`
- Backend: Python 3.11-slim, Uvicorn
