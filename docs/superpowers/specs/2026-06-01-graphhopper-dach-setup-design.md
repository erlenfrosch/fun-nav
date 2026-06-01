# Spec: GraphHopper Docker-Setup für DACH

**Issue:** #2  
**Branch:** agent/issue-2  
**Datum:** 2026-06-01

## Ziel

GraphHopper self-hosted via Docker für die DACH-Region konfigurieren.

## Scope

1. `graphhopper/config.yml` — `auto`-Profil mit Custom-Model-Unterstützung (flexibles Routing)
2. `scripts/download-osm.sh` — DACH `.pbf` von Geofabrik (`dach-latest.osm.pbf`)
3. `docker-compose.yml` — Image auf `latest` aktualisieren, Healthcheck ergänzen

## Nicht im Scope

- Bike- oder Fußgänger-Profile (werden entfernt, da nicht im Issue)
- CI/CD-Integration

## Akzeptanzkriterium

`curl localhost:8989/health` → `{"status":"ready"}`

## Recherche-Quellen

- [Geofabrik DACH Download](https://download.geofabrik.de/europe/dach.html)
- [GraphHopper config-example.yml](https://github.com/graphhopper/graphhopper/blob/master/config-example.yml)
- [GraphHopper Custom Profiles Docs](https://docs.graphhopper.com/openapi/custom-profiles)
