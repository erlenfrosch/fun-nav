# System Patterns

## Architektur-Entscheidungen

- **Monorepo:** frontend/, backend/, graphhopper/ als separate Unterverzeichnisse mit eigenem Dockerfile
- **Service-Kommunikation:** Frontend → Backend (HTTP), Backend → GraphHopper (HTTP via httpx), alles über Docker-Netzwerk
- **GraphHopper Config:** YAML-Datei (`graphhopper/config.yml`), Volume-gemountet in Container
- **OSM-Daten:** lokal als `.pbf`-Datei, gitignored, via Download-Script beschafft

## Wiederkehrende Muster

- FastAPI-Endpunkte geben direkt JSON zurück (kein ORM, kein DB-Overhead)
- CORS in Backend offen (`allow_origins=["*"]`) für lokale Entwicklung
- Docker Services: `restart: unless-stopped` als Standard

## Anti-Patterns

- (noch keine bekannt)
