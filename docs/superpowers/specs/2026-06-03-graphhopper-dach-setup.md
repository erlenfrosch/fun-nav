# Spec: GraphHopper Docker-Setup für DACH

**Issue:** #2  
**Branch:** agent/issue-2  
**Datum:** 2026-06-03

## Problem

Das aktuelle Setup lädt nur Liechtenstein (~1 MB) als OSM-Testdatensatz. Für produktive
Nutzung im DACH-Raum (Deutschland, Österreich, Schweiz) ist ein erweitertes Setup nötig:
- Geofabrik bietet `dach-latest.osm.pbf` (~5.7 GB) als kombinierten Datensatz an
- GraphHopper benötigt für DACH wesentlich mehr Java-Heap-Speicher (8–12 GB)
- Der aktuelle Docker-Compose-JAVA_OPTS-Wert (`-Xmx1g`) reicht für DACH nicht aus

## Lösung

1. **Download-Skript parametrisieren**: `scripts/download-osm.sh [region]` mit den
   Optionen `liechtenstein` (Standard, Dev) und `dach` (Produktion)
2. **Memory via Env-Variable**: `docker-compose.yml` liest `JAVA_OPTS` aus der
   Umgebung, Fallback auf Liechtenstein-taugliche Werte
3. **`.env.example`**: Dokumentiert die empfohlenen Werte für beide Szenarien
4. **README.md**: Ergänzt DACH-Quickstart-Anleitung

## Akzeptanzkriterien

- `./scripts/download-osm.sh dach` lädt `dach-latest.osm.pbf` von Geofabrik
- `./scripts/download-osm.sh` (ohne Argument) lädt weiterhin Liechtenstein
- `docker-compose up` funktioniert mit beiden Datensätzen, wenn `JAVA_OPTS` gesetzt ist
- `.env.example` zeigt korrekte JAVA_OPTS für Liechtenstein und DACH
- README enthält DACH-Anleitung mit Ressourcenhinweis

## Quellen

- [Geofabrik DACH Download](https://download.geofabrik.de/europe/dach.html)
- [GraphHopper Memory Forum](https://discuss.graphhopper.com/t/memory-errors-and-requirements/9071)
