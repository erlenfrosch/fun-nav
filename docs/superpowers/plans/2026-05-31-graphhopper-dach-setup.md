# Plan: GraphHopper Docker-Setup für DACH

**Issue:** #2  
**Spec:** docs/superpowers/specs/2026-05-31-graphhopper-dach-setup-design.md  
**Datum:** 2026-05-31

## Recherche-Quellen

- Geofabrik DACH: https://download.geofabrik.de/europe/dach.html
- GraphHopper Custom Models: https://github.com/graphhopper/graphhopper/blob/master/docs/custom-models.md
- GraphHopper Health Endpoint: https://discuss.graphhopper.com/t/modifying-dockerfile-config-example-yml-and-setting-up-graphhopper-via-docker-with-your-own-data/5445
- GraphHopper Memory: https://discuss.graphhopper.com/t/memory-errors-and-requirements/9071

## Aufgaben

- [x] Spec schreiben
- [x] `graphhopper/config.yml` — car-Profil auf `custom_model_files: []` umstellen
- [x] `scripts/download-osm.sh` — DACH-Unterstützung via REGION-Variable
- [x] `docker-compose.yml` — Healthcheck für GraphHopper, Backend depends_on service_healthy, Speicher auf 2g
- [x] `docker-compose.dach.yml` — Override-Datei für DACH-Production (6g RAM)
- [x] `README.md` — DACH-Abschnitt + Healthcheck-Hinweis
- [ ] Commit + Push + PR

## Entscheidungen

- `wget` statt `curl` im Healthcheck (ist in GraphHopper-Image verfügbar)
- `start_period: 300s` — DACH-Import dauert 3–10 min je nach Hardware
- `custom_model_files: []` — leere Liste = Custom Models nur via API, kein Pre-Build nötig
- Separate `docker-compose.dach.yml` statt Anpassung der Basis-Compose (YAGNI für Dev-Setups)
