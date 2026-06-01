# Tech Context

## Stack

- **Backend**: Python 3.11, FastAPI 0.115, Uvicorn, httpx 0.27, pydantic
- **Frontend**: React 18, Vite 5, JavaScript (kein TypeScript)
- **Routing**: GraphHopper 7 (Docker Image)
- **Infrastruktur**: Docker Compose, Docker >= 24

## Tools & Infrastruktur

- Build Backend: `docker-compose build backend`
- Build Frontend: `npm run build` (Vite)
- Start alle Services: `docker-compose up`
- Dev Frontend: `npm run dev` (Vite, Port 5173)
- Backend läuft auf Port 8000, GraphHopper auf 8989
- OSM-Daten: `scripts/download-osm.sh` (lädt Liechtenstein als Testdatensatz)
- Tests: `pytest` (Backend), kein Test-Setup Frontend bisher

## Constraints

- Python 3.11-slim als Base Image (kein Alpine wegen C-Extensions)
- Docker Compose als einzige Deployment-Methode in M1
- CORS: Frontend auf localhost:5173, Backend auf localhost:8000
- GraphHopper benötigt OSM `.pbf`-Datei in `graphhopper/data/`
