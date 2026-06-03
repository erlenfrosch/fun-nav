# fun-nav

Navigationsdienst auf Basis von GraphHopper, FastAPI und React PWA.

## Services

| Service     | URL                        | Beschreibung              |
|---|---|---|
| GraphHopper | http://localhost:8989      | Routing-Engine            |
| Backend     | http://localhost:8000      | FastAPI REST-API          |
| Frontend    | http://localhost:5173      | React PWA                 |

## Quickstart

### Voraussetzungen

- Docker >= 24
- Docker Compose >= 2.20

### 1. OSM-Daten laden

```bash
chmod +x scripts/download-osm.sh
./scripts/download-osm.sh
```

Standard lädt DACH (~3.6 GB). Über die Umgebungsvariable `OSM_REGION` kann eine
kleinere Region gewählt werden:

| `OSM_REGION` | Quelle | Größe |
|---|---|---|
| `dach` (Standard) | Geofabrik DACH | ~3.6 GB |
| `germany` | Geofabrik Germany | ~4 GB |
| `austria` | Geofabrik Austria | ~600 MB |
| `switzerland` | Geofabrik Switzerland | ~400 MB |
| `test` | Liechtenstein | ~1 MB |

Beispiel für schnellen Teststart:

```bash
OSM_REGION=test ./scripts/download-osm.sh
```

### 2. Services starten

```bash
docker-compose up
```

Beim ersten Start verarbeitet GraphHopper die OSM-Daten (ca. 1–2 Minuten).
Anschließend ist die Routing-API unter http://localhost:8989 erreichbar.

### 3. Health-Check

```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

## Struktur

```
.
├── frontend/       React Vite PWA
├── backend/        FastAPI + Uvicorn
├── graphhopper/    Routing-Engine (Config + Datenpfad)
│   └── data/       OSM-Daten (gitignored: *.pbf)
├── scripts/        Hilfsskripte
├── docs/           Dokumentation
└── docker-compose.yml
```

## Entwicklung

Einzelnen Service neu bauen:

```bash
docker-compose build backend
docker-compose up backend
```

Logs eines Service verfolgen:

```bash
docker-compose logs -f graphhopper
```
