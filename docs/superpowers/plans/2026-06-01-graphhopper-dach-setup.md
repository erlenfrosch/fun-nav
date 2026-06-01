# Plan: GraphHopper Docker-Setup für DACH

**Issue:** #2  
**Branch:** agent/issue-2  
**Spec:** docs/superpowers/specs/2026-06-01-graphhopper-dach-setup-design.md

## Aufgaben

### 1. Tests schreiben (TDD-First)
- `tests/test_infrastructure.py`
  - config.yml hat car-Profil und car_custom-Profil
  - docker-compose.yml hat healthcheck für graphhopper
  - docker-compose.yml image ist `graphhopper/graphhopper:latest`
  - download script enthält DACH-URL

### 2. `graphhopper/config.yml` aktualisieren
- Bestehende Profile (car, bike, foot) behalten
- Neues `car_custom`-Profil mit `weighting: custom` und `custom_model: {}`
- `profiles_lm` für car_custom hinzufügen (Landmark-Mode für Per-Request Custom Models)
- CH bleibt für `car` (schnelles Standard-Routing)

### 3. `scripts/download-osm.sh` aktualisieren
- Env-Variable `OSM_REGION` (default: `dach`)
- Unterstützte Werte: `dach`, `germany`, `austria`, `switzerland`, `test`
- `test` = Liechtenstein für schnelle lokale Entwicklung
- Bestehende Prüfung auf vorhandene Datei beibehalten

### 4. `docker-compose.yml` aktualisieren
- Image: `graphhopper/graphhopper:latest`
- Healthcheck: `curl -sf http://localhost:8989/health | grep -q ready`
  - interval: 30s, timeout: 10s, retries: 40, start_period: 120s
- Backend `depends_on`: `condition: service_healthy`
- JAVA_OPTS: `-Xmx4g -Xms512m` (für DACH ausreichend RAM)

### 5. Commit + PR
- Tests müssen grün sein
- Kommentar im Issue

## Reihenfolge

1. Tests (rot)
2. config.yml (Tests grün)
3. download-osm.sh (Tests grün)
4. docker-compose.yml (Tests grün)
5. Commit, Push, PR
