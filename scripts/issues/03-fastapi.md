## Beschreibung
FastAPI Backend mit Health-Endpoint und CORS einrichten.

## Aufgaben
- [ ] `backend/main.py` mit FastAPI App
- [ ] `GET /health` → `{"status":"ok"}`
- [ ] CORS für Frontend (localhost:5173)
- [ ] `requirements.txt`: fastapi, uvicorn, httpx, pydantic
- [ ] `Dockerfile` für Docker Compose
- [ ] Ordnerstruktur: `routers/`, `services/`, `models/`

## Akzeptanzkriterium
`curl localhost:8000/health` → `{"status":"ok"}`
