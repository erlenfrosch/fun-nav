# System Patterns

## Architektur-Entscheidungen

- **Monorepo**: `backend/`, `frontend/`, `graphhopper/` als gleichwertige Unterverzeichnisse
- **Backend-Struktur**: `backend/app/` ist das Python-Package mit `main.py` als Einstiegspunkt; Unterverzeichnisse `routers/`, `services/`, `models/` für zukünftige Erweiterungen
- **Docker Compose**: Alle Services in einem `docker-compose.yml`; Backend hängt von GraphHopper ab, Frontend von Backend
- **Umgebungsvariablen**: `GRAPHHOPPER_URL` im Backend-Container, `VITE_API_URL` im Frontend-Container

## Wiederkehrende Muster

- FastAPI-Routen als separate Router-Module unter `app/routers/`
- Health-Endpoint `/health` → `{"status": "ok"}` ohne Auth
- CORS explizit auf `localhost:5173` beschränkt (kein Wildcard in Produktion)
- Keine Raw-Queries; Pydantic-Modelle für Request/Response-Validation

## Anti-Patterns

- (Keine bekannten Anti-Patterns bisher)
