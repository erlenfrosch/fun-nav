# Spec: 3 Route-Optionen auf Karte anzeigen

**Issue:** #9  
**Branch:** agent/issue-9  
**Datum:** 2026-05-31

## Problem

Der Nutzer soll zwischen drei generierten Routenalternativen wählen können. Derzeit
existiert kein Karteninterface — `App.jsx` ist ein Platzhalter.

## Lösung

MapLibre GL JS rendert drei GeoJSON-Linien-Layer mit je einer Farbe. Pro Route gibt
es einen `RouteCard`-Eintrag in einer Seitenleiste. Hover-Effekt und Klick sind über
MapLibre-Events umgesetzt. Der Backend-Endpoint `/api/routes` liefert Geometrie +
Metadaten; er versucht GraphHopper, fällt andernfalls auf Mock-Daten zurück.

## Farben

| Route | Farbe   | Hex       |
|---|---|---|
| A    | Blau    | `#3B82F6` |
| B    | Grün    | `#22C55E` |
| C    | Orange  | `#F97316` |

## Akzeptanzkriterien

- 3 Routen auf Karte sichtbar, farblich unterschieden
- Hover verdickt die Route (4 px → 8 px)
- Klick selektiert Route, zoomt auf Bounds, hebt RouteCard hervor
- RouteCard zeigt Distanz (km) und Fahrzeit (min)
- Andere Routen werden bei Selektion abgedunkelt (opacity 0.6)

## Stack-Entscheidungen

- MapLibre GL JS (open-source, kein API-Key nötig)
- Tiles: `https://tiles.openfreemap.org/styles/bright` (kostenlos, kein Key)
- Karte in React via `useRef`/`useEffect` (kein separates Wrapper-Paket)
- Backend: FastAPI-Endpoint, der erst GraphHopper anfragt, sonst Mock
- Tests: vitest + @testing-library/react (Frontend), pytest (Backend)
