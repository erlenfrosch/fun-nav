# Plan: GraphHopper Docker-Setup für DACH

**Issue:** #2  
**Spec:** docs/superpowers/specs/2026-06-01-graphhopper-dach-setup-design.md

## Umsetzungsschritte

### 1. `graphhopper/config.yml`
- `auto`-Profil mit `custom_model_files: []` (leeres Array = Custom Model API an jedem Request erlaubt)
- CH-Profile entfernen (inkompatibel mit Custom Model / flexiblem Routing)
- LM-Profil für `auto` hinzufügen (schnelles Routing trotz Flexibilität)
- `graph.encoded_values` mit relevanten Werten für DACH-Straßennetz

### 2. `scripts/download-osm.sh`
- URL auf `https://download.geofabrik.de/europe/dach-latest.osm.pbf` (~5.7 GB) ändern
- Dateiname bleibt `map.osm.pbf`

### 3. `docker-compose.yml`
- Image: `graphhopper/graphhopper:7` → `graphhopper/graphhopper:latest`
- Healthcheck hinzufügen: `curl -f http://localhost:8989/health`
  - `start_period: 600s` (Graph-Build dauert für DACH lange)
  - `interval: 30s`, `retries: 20`

## Abhängigkeiten

Keine externen Abhängigkeiten.
