# Spec: GraphHopper Docker-Setup für DACH

**Issue:** #2  
**Datum:** 2026-05-31

## Ziel

Self-hosted GraphHopper via Docker für die deutschsprachige Region (DACH) produktionsbereit machen.

## Anforderungen

1. `graphhopper/config.yml` — Car-Profil mit Custom Model Unterstützung (API-basierte Anpassung von Routing-Gewichten)
2. `scripts/download-osm.sh` — DACH-Kartendaten (~800 MB) von Geofabrik herunterladen
3. Docker Compose Healthcheck — wartet bis GraphHopper den Graph vollständig aufgebaut hat
4. Acceptance: `curl localhost:8989/health` gibt `{"status":"healthy"}` zurück

## Nicht-Ziele

- Keine GUI/Frontend-Änderungen
- Kein Custom Model Editor im Frontend
- Kein Kubernetes/Production-Deployment

## Technische Entscheidungen

### Config

- Car-Profil mit `custom_model_files: []` → erlaubt API-basierte Custom Models ohne Pre-Build
- CH (Contraction Hierarchies) nur für `car` — sinnvoll für DACH-Größe
- MMAP-Datenzugriff deaktiviert (Standard: RAM) — schneller bei ausreichend RAM
- Admin-Connector auf Port 8990 bleibt erhalten

### Download-Skript

- Region über `REGION`-Umgebungsvariable oder `--region`-Argument steuerbar
- Unterstützte Regionen: `liechtenstein` (default, ~1 MB), `dach` (~800 MB), `austria`, `switzerland`, `germany`
- Geofabrik-URLs: `https://download.geofabrik.de/europe/<region>-latest.osm.pbf`
- Bestehende Datei wird nicht überschrieben (idempotent)

### Healthcheck

- Docker Compose Healthcheck für GraphHopper mit `wget`
- Endpoint: `localhost:8989/health`
- `start_period: 300s` für DACH-Import (Graph-Build dauert mehrere Minuten)
- Backend `depends_on: graphhopper: condition: service_healthy`

### Speicher

- Entwicklung: `-Xmx2g -Xms256m` (ausreichend für Liechtenstein + Austria)
- DACH-Production: `docker-compose.dach.yml` Override mit `-Xmx6g -Xms1g`

## Akzeptanzkriterium

```bash
./scripts/download-osm.sh
docker-compose up -d
curl localhost:8989/health  # → {"status":"healthy"}
```
