# System Patterns: fun-nav

## Architektur-Entscheidungen
- Monorepo: frontend/, backend/, graphhopper/ nebeneinander
- Backend-Code unter `backend/app/` (FastAPI-App als Package)
- Einstiegspunkt: `app.main:app` (Uvicorn)
- Router-Modularisierung via `routers/` geplant (Issue #3)

## Wiederkehrende Muster
- REST-First: GET /health als Standardendpunkt
- CORS: Middleware mit expliziter Origin-Liste (nicht *)
- Docker Compose als einziger Deployment-Weg

## Anti-Patterns
- `allow_origins=["*"]` in Produktion vermeiden — spezifische Origins verwenden
