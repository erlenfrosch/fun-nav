# Project Brief

## Was ist dieses Projekt?

fun-nav ist ein selbst-gehosteter Navigationsdienst für die DACH-Region, aufgebaut auf GraphHopper (Routing-Engine), FastAPI (REST-API) und React (PWA-Frontend). Alle Services laufen als Docker-Container.

## Ziele

- Routing-API für Auto, Fahrrad und Fußgänger auf OSM-Basisdaten
- REST-Backend als Proxy/Adapter zwischen Frontend und GraphHopper
- React PWA als Benutzeroberfläche
- Vollständig lokal/self-hosted betreibbar per `docker-compose up`

## Nicht-Ziele

- Kein Auth/User-Management
- Kein kommerzieller Kartendienst (kein Google Maps, keine Here-API)
- Keine Echtzeit-Verkehrsdaten
