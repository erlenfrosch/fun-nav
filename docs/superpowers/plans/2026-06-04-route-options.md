# Plan: 3 Route-Optionen auf Karte anzeigen

**Issue:** #9  
**Spec:** docs/superpowers/specs/2026-06-04-route-options-design.md  
**Datum:** 2026-06-04 (aktualisiert: 2026-06-10)

## Recherche-Quellen

- react-map-gl v7 Doku: https://visgl.github.io/react-map-gl/
- MapLibre GL JS Source/Layer API: https://maplibre.org/maplibre-gl-js/docs/API/
- OpenFreeMap Tiles: https://openfreemap.org/
- Issue #9: GeoJSON-Layer, Hover, Auswahl, Auto-Zoom

## Aufgaben

### Backend
- [x] `POST /api/routes/circular` Endpoint bereits vorhanden (Issue #7/#8)
- [x] Response-Format: `routes[].geometry` (GeoJSON LineString) + `duration_min`, `distance_km`
- [x] `pytest.ini` + `backend/tests/__init__.py` für Backend-Tests ergänzt
- [x] `pytest`, `pytest-asyncio` zu `requirements.txt` hinzugefügt

### Frontend
- [x] `maplibre-gl`, `react-map-gl` zu `package.json` hinzufügen
- [x] `Map.tsx` — MapLibre GL JS Karte mit GeoJSON Source/Layer pro Route
- [x] `RouteCard.tsx` — Info-Card mit Distanz und Dauer
- [x] `RoutePanel.tsx` — `onRoutesCalculated` Callback ergänzt
- [x] `App.jsx` — Map + RouteCard + RoutePanel zusammenführen, State verwalten
- [x] Tests: `RouteCard.test.tsx`, `Map.test.tsx`

## Entscheidungen

- **MapLibre GL JS statt Leaflet** — laut Haupt-Spec (WebGL2, kein Token, PWA-fähig)
- **react-map-gl v7** — idiomatisches React-Binding für MapLibre
- **OpenFreeMap** als Tile-Quelle — kostenlos, kein API-Key, DACH-Abdeckung
- **GeoJSON Source/Layer** statt Polyline — native MapLibre GL JS Methode
- **`onRoutesCalculated` Callback** in RoutePanel — hebt State zu App.jsx ohne Tests zu brechen
- Hover und Klick via `queryRenderedFeatures` + `onMouseMove`/`onClick` auf Map-Ebene
- Auto-Zoom via `mapRef.fitBounds` wenn `selectedIndex` oder `routes` sich ändert
