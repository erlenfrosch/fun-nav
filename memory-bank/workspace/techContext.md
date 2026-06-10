# Tech Context: fun-nav

## Stack
- **Backend**: Python 3.11, FastAPI 0.115.0, Uvicorn 0.30.6, httpx 0.27.2
- **Frontend**: React 18.3.1, Vite 5.4.1 (läuft auf Port 5173)
- **Routing-Engine**: GraphHopper 7 (Docker, Port 8989)
- **Infra**: Docker Compose

## Abhängigkeiten (backend/requirements.txt)
- fastapi==0.115.0
- uvicorn[standard]==0.30.6
- httpx==0.27.2
- pydantic (fehlt noch, Issue #3)

## Tools & Build
- Backend: `docker-compose build backend` / `docker-compose up backend`
- Frontend: `npm run dev` (Port 5173) / `npm run build`
- Starten: `docker-compose up`

## Constraints
- GraphHopper-URL via Env `GRAPHHOPPER_URL=http://graphhopper:8989`
- Frontend-API-URL via Env `VITE_API_URL=http://localhost:8000`
- CORS muss `http://localhost:5173` erlauben
