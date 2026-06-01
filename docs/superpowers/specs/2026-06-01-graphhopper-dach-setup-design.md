# Spec: GraphHopper Docker-Setup für DACH

**Issue:** #2  
**Branch:** agent/issue-2  
**Datum:** 2026-06-01

## Kontext

Das Projekt nutzt GraphHopper als self-hosted Routing-Engine via Docker.
Aktuell ist nur Liechtenstein (~1 MB) als Test-Datensatz konfiguriert.
Das Issue fordert ein vollständiges DACH-Setup.

## Anforderungen (aus Issue #2)

1. `graphhopper/config.yml` mit Auto-Profil und Custom Model Unterstützung
2. Download-Script `scripts/download-osm.sh` für DACH .pbf von Geofabrik
3. Docker Compose Service mit Volume-Mount für `graphhopper/data/`
4. Startup-Healthcheck bis Graph fertig gebaut ist
5. GH Image: `graphhopper/graphhopper:latest`, Port: 8989

## Akzeptanzkriterium

`curl localhost:8989/health` → `{"status":"ready"}`

## Recherche-Ergebnisse

- GraphHopper stellt seit v3.x einen `/health`-Endpunkt auf Port 8989 bereit
- Custom Models werden über `weighting: custom` + `custom_model: {}` aktiviert
- Für flexible Per-Request Custom Models braucht es Landmark (LM) Mode statt CH
- Geofabrik DACH-Datei: `https://download.geofabrik.de/europe/dach-latest.osm.pbf` (~3.6 GB)
- Gesundheitsprüfung im Docker Compose via `condition: service_healthy` im Backend

## Nicht-Scope

- Keine Implementierung von konkreten Custom Models (nur Infrastruktur)
- Kein Import anderer Kartenquellen
- Kein Multi-Region-Merge (osmium)

## Quellen

- GraphHopper config-example.yml: https://github.com/graphhopper/graphhopper/blob/master/config-example.yml
- GraphHopper Profiles Docs: https://github.com/graphhopper/graphhopper/blob/master/docs/core/profiles.md
- Geofabrik DACH: https://download.geofabrik.de/europe/
