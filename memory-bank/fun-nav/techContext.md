# Tech Context

## Stack

- **Backend:** Python 3.11, FastAPI 0.115, Uvicorn 0.30, httpx 0.27
- **Frontend:** Node 20, React 18.3, Vite 5.4 (PWA)
- **Routing-Engine:** GraphHopper (graphhopper/graphhopper:7), Port 8989
- **Infra:** Docker Compose, alle Services containerisiert

## Tools & Infrastruktur

- Build: `docker-compose build`
- Start: `docker-compose up`
- OSM-Daten laden: `./scripts/download-osm.sh`
- Backend dev: `uvicorn app.main:app --reload`
- Frontend dev: `npm run dev` (Vite, Port 5173)

## Constraints

- GraphHopper erwartet OSM `.pbf` unter `graphhopper/data/map.osm.pbf`
- Graph-Cache unter `graphhopper/data/graph-cache/` (gitignored)
- DACH-Datei ~800 MB, Liechtenstein ~1 MB (Test)
- Backend braucht `GRAPHHOPPER_URL=http://graphhopper:8989`
- Frontend braucht `VITE_API_URL=http://localhost:8000`
