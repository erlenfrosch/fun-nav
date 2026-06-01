# Project Brief

## Was ist dieses Projekt?

fun-nav ist ein Navigationsdienst, der GraphHopper als Routing-Engine, FastAPI als REST-Backend und React als PWA-Frontend kombiniert. Ziel ist eine selbst gehostete Routing-Lösung auf Basis von OpenStreetMap-Daten.

## Ziele

- Routen berechnen via GraphHopper (OSM-Daten)
- REST-API (FastAPI) als Schicht zwischen Frontend und Routing-Engine
- React PWA für mobile und Desktop-Nutzung
- Vollständig dockerisiertes Setup via Docker Compose

## Nicht-Ziele

- Kein eigener Kartendienst (Tiles kommen von extern)
- Keine Benutzerverwaltung / Auth in Milestone 1
- Keine Produktiv-Deployment-Konfiguration in Milestone 1
