# Plan: 3 Route-Optionen auf Karte anzeigen

**Issue:** #9  
**Spec:** docs/superpowers/specs/2026-06-01-route-display-design.md  
**Datum:** 2026-06-01

## Recherche-Quellen

- MapLibre GL JS Docs: https://maplibre.org/maplibre-gl-js/docs/ (context7)
- GeoJSON Line Layer: map.addSource + map.addLayer(type: 'line')
- Hover-Effekt: map.on('mouseenter'/'mouseleave', layerId, handler)
- fitBounds: new maplibregl.LngLatBounds + coordinates.reduce
- Map-Tile-Style: https://tiles.openfreemap.org/styles/bright (kostenlos, kein API-Key)

## Aufgaben

- [x] Branch `agent/issue-9` anlegen
- [x] Spec schreiben
- [x] Plan schreiben
- [ ] `maplibre-gl` in `frontend/package.json` eintragen
- [ ] `frontend/src/mockRoutes.js` — 3 GeoJSON-Routen um Vaduz
- [ ] `frontend/src/RouteCard.jsx` — Info-Karte pro Route
- [ ] `frontend/src/Map.jsx` — MapLibre-Komponente
- [ ] `frontend/src/App.jsx` — Layout Karte + Sidebar
- [ ] Commit + PR

## Entscheidungen

- Vanilla MapLibre GL JS (kein React-Wrapper) — passt zur bestehenden Plain-JSX-Struktur
- `setPaintProperty` für dynamisches Umfärben bei Hover/Auswahl
- OpenFreeMap bright-Style — kein API-Key, quelloffen
- Mock-Daten (GeoJSON) statt echtem Routing — Backend-Routing-Endpunkt nicht Teil dieses Issues
