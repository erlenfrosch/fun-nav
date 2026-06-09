# Spec: 3 Route-Optionen auf Karte anzeigen

**Issue:** #9  
**Branch:** agent/issue-9  
**Datum:** 2026-06-04 (aktualisiert: 2026-06-10)

## Problem

Das Frontend zeigt noch keine Karte und keine Routenanzeige. Nutzer können
keine der berechneten Rundrouten sehen oder auswählen.

## Lösung

MapLibre GL JS Karte (`Map.tsx`) mit GeoJSON-Layern pro Route. Routen kommen
vom bestehenden `POST /api/routes/circular` Endpoint. Jede Route ist farblich
unterschieden; Hover macht die Linie dicker; Klick wählt eine Route aus
(hervorgehoben, andere blass). `RouteCard.tsx` zeigt Distanz und Dauer als
auswählbare Info-Karte. Bei Auswahl zoomt die Karte automatisch auf die
Bounding-Box der gewählten Route.

## Scope

### Backend (keine Änderungen am Endpoint)
- `POST /api/routes/circular` bereits vorhanden
- Response: `routes[].{id, duration_min, distance_km, geometry}`
- Neu: `pytest.ini` + `backend/tests/` Scaffold

### Frontend
- `Map.tsx` — MapLibre GL JS via react-map-gl, OpenFreeMap Tiles
- GeoJSON Source + Line-Layer pro Route (blau, grün, orange)
- Hover: `line-width` erhöht via `queryRenderedFeatures` + `onMouseMove`
- Klick: Route wählen via `queryRenderedFeatures` + `onClick`
- Ausgewählt = `line-opacity: 1`, andere = `0.45`
- Auto-Zoom: `mapRef.fitBounds` auf Koordinaten-BoundingBox bei `selectedIndex`-Änderung
- `RouteCard.tsx` — Button mit Farb-Akzent (border-left), Distanz und Dauer
- `RoutePanel.tsx` — `onRoutesCalculated` Callback ergänzt (state lift zu App.jsx)
- `App.jsx` — Sidebar (RoutePanel + RouteCards) + Karte nebeneinander

## Akzeptanzkriterien

1. 3 Routen als farbige Polylines auf der MapLibre-Karte sichtbar
2. Hover über Route → Linie wird dicker
3. Klick auf Route → ausgewählt (fett + volle Deckkraft), andere blass
4. Klick auf RouteCard → gleiche Auswahl wie Klick auf Karte
5. Karte zoomt automatisch auf gewählte Route
6. Frontend-Tests für RouteCard und Map grün
