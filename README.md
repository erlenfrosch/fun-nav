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

Standardmäßig wird Liechtenstein (~1 MB) als Testdatensatz geladen. Region über
`--region` oder `REGION`-Variable wählbar:

| Region | Größe | Befehl |
|---|---|---|
| `liechtenstein` | ~1 MB | `./scripts/download-osm.sh` (default) |
| `austria` | ~740 MB | `./scripts/download-osm.sh --region austria` |
| `switzerland` | ~360 MB | `./scripts/download-osm.sh --region switzerland` |
| `dach` | ~800 MB | `./scripts/download-osm.sh --region dach` |
| `germany` | ~3.7 GB | `./scripts/download-osm.sh --region germany` |

### 2. Services starten

```bash
docker-compose up
```

GraphHopper verarbeitet die OSM-Daten beim ersten Start (Liechtenstein: ~1 Min,
DACH: ~10 Min). Der Backend-Service startet erst, wenn GraphHopper vollständig
bereit ist.

**DACH-Production** (erhöhter Speicher, längerer Start-Timeout):

```bash
docker-compose -f docker-compose.yml -f docker-compose.dach.yml up
```

### 3. Health-Check

```bash
curl http://localhost:8989/health
# {"status":"healthy"}

curl http://localhost:8000/health
# {"status":"ok"}
```

## Struktur

```
.
├── frontend/             React Vite PWA
├── backend/              FastAPI + Uvicorn
├── graphhopper/          Routing-Engine (Config + Datenpfad)
│   └── data/             OSM-Daten (gitignored: *.pbf)
├── scripts/              Hilfsskripte
├── docs/                 Dokumentation
├── docker-compose.yml
└── docker-compose.dach.yml  DACH-Production Override (höhere RAM-Limits)
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
