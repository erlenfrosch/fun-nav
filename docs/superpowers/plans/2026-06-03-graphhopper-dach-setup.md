# Plan: GraphHopper Docker-Setup für DACH

**Spec:** docs/superpowers/specs/2026-06-03-graphhopper-dach-setup.md  
**Datum:** 2026-06-03

## Recherche

- Geofabrik DACH-URL: `https://download.geofabrik.de/europe/dach-latest.osm.pbf` (5.7 GB)
- Einzelländer: germany (4.4 GB), austria (763 MB), switzerland (507 MB)
- GraphHopper-Heap für DACH: min. 8 GB für Import, 6 GB für Routing-Betrieb
- Docker Compose unterstützt `${VAR:-default}` Syntax nativ

## Änderungen

### 1. `scripts/download-osm.sh`

- Erstes Argument als Region akzeptieren: `liechtenstein` (default) oder `dach`
- URL-Mapping:
  - `liechtenstein` → `https://download.geofabrik.de/europe/liechtenstein-latest.osm.pbf`
  - `dach` → `https://download.geofabrik.de/europe/dach-latest.osm.pbf`
- Existenz-Check beibehalten (kein erneuter Download wenn Datei vorhanden)
- Fehlermeldung bei unbekannter Region

### 2. `docker-compose.yml`

- `JAVA_OPTS` aus Umgebung lesen: `${JAVA_OPTS:--Xmx1g -Xms256m}`
- Kein Breaking Change — Fallback-Wert entspricht aktuellem Wert

### 3. `.env.example` (neu)

Dokumentiert die zwei Betriebsmodi:
```
# Liechtenstein / Dev (~1 MB OSM, 1 GB Heap genug)
JAVA_OPTS=-Xmx1g -Xms256m

# DACH / Produktion (~5.7 GB OSM, mindestens 8 GB Heap empfohlen)
# JAVA_OPTS=-Xmx8g -Xms2g
```

### 4. `README.md`

- Bestehenden Quickstart um DACH-Variante ergänzen
- Ressourcenhinweis: mindestens 10 GB RAM empfohlen für DACH
- Import-Dauer: ca. 30–60 Minuten für DACH

## Reihenfolge

1. `scripts/download-osm.sh` anpassen
2. `docker-compose.yml` anpassen
3. `.env.example` erstellen
4. `README.md` ergänzen
5. Spec + Plan committen
6. Alles committen und PR öffnen
