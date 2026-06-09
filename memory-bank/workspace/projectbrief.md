# Project Brief: fun-nav

## Was ist dieses Projekt?
fun-nav ist ein Navigationsdienst, der GraphHopper (Routing-Engine), FastAPI (REST-API) und React PWA (Frontend) kombiniert. Nutzer können Routen berechnen lassen und das Ergebnis in einer Progressive Web App anzeigen.

## Ziele
- Routing-API via GraphHopper bereitstellen
- FastAPI-Backend als Proxy/Adapter zwischen Frontend und GraphHopper
- React PWA als interaktives Karteninterface
- Docker Compose für reproduzierbares Setup

## Nicht-Ziele
- Kein User-Management / Auth
- Keine persistente Datenhaltung (kein DB)
- Keine eigene Tile-Server-Infrastruktur (OSM-Rohdaten werden durch GraphHopper verarbeitet)
