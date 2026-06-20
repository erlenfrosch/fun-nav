## Beschreibung
GraphHopper self-hosted via Docker für die DACH-Region konfigurieren.

## Aufgaben
- [ ] `graphhopper/config.yml` mit Auto-Profil und Custom Model Unterstützung
- [ ] Download-Script `scripts/download-osm.sh` für DACH .pbf von Geofabrik (~800 MB)
- [ ] Docker Compose Service mit Volume-Mount für `graphhopper/data/`
- [ ] Startup-Healthcheck bis Graph fertig gebaut ist
- [ ] GH Image: `graphhopper/graphhopper:latest`, Port: 8989

## Akzeptanzkriterium
`curl localhost:8989/health` → `{"status":"ready"}`
