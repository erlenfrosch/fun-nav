# Spec: Monorepo-Struktur + Docker Compose Grundgerüst

**Issue:** #1  
**Branch:** agent/issue-1  
**Datum:** 2026-05-31

## Problem

Das Projekt `fun-nav` benötigt eine reproduzierbare Entwicklungsumgebung mit drei
Services: GraphHopper (Routing-Engine), FastAPI (Backend) und React PWA (Frontend).

## Lösung

Monorepo mit einem `docker-compose.yml` an der Wurzel. Jeder Service hat sein eigenes
Unterverzeichnis mit eigenem `Dockerfile`. GraphHopper nutzt das offizielle
`graphhopper/graphhopper`-Image mit externem Volume für OSM-Daten.

## Struktur

```
/
├── frontend/          React Vite PWA
├── backend/           FastAPI + Uvicorn
├── graphhopper/       Config + Datenpfad (OSM-Dateien gitignored)
├── scripts/           Hilfsskripte (OSM-Download, etc.)
├── docs/              Dokumentation
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Services

| Service      | Image/Build       | Port | Abhängigkeiten |
|---|---|---|---|
| graphhopper  | graphhopper/graphhopper:7 | 8989 | – |
| backend      | ./backend         | 8000 | graphhopper |
| frontend     | ./frontend        | 5173 | backend |

## Akzeptanzkriterium

`docker-compose up` startet alle Services ohne Fehler (nach `scripts/download-osm.sh`).
