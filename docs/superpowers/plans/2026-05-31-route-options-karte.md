# Plan: 3 Route-Optionen auf Karte anzeigen

**Issue:** #9  
**Spec:** docs/superpowers/specs/2026-05-31-route-options-karte-design.md  
**Datum:** 2026-05-31

## Recherche-Quellen

- MapLibre GL JS – GeoJSON Line Layer: https://maplibre.org/maplibre-gl-js/docs/examples/add-a-geojson-line/
- MapLibre GL JS – Hover-Effekt: https://maplibre.org/maplibre-gl-js/docs/examples/create-a-hover-effect/
- MapLibre GL JS – fitBounds: https://maplibre.org/maplibre-gl-js/docs/examples/fit-to-the-bounds-of-a-linestring/

## Aufgaben

- [x] Spec schreiben
- [x] Plan schreiben
- [ ] `backend/app/main.py` – `/api/routes` Endpoint (Mock + optionaler GraphHopper-Call)
- [ ] `backend/requirements.txt` – pytest hinzufügen
- [ ] `backend/tests/test_routes.py` – Pytest-Tests
- [ ] `frontend/package.json` – maplibre-gl, vitest, @testing-library/react
- [ ] `frontend/vite.config.js` – Proxy + Vitest-Konfiguration
- [ ] `frontend/src/utils/format.js` – formatDistance, formatDuration
- [ ] `frontend/src/utils/format.test.js` – Unit-Tests
- [ ] `frontend/src/components/Map.jsx` – MapLibre-Kartenkomponente
- [ ] `frontend/src/components/RouteCard.jsx` – Info-Karte
- [ ] `frontend/src/components/RouteCard.test.jsx` – Komponenten-Tests
- [ ] `frontend/src/App.jsx` – Layout Sidebar + Karte verdrahten
- [ ] `docker-compose.yml` – BACKEND_URL für Proxy ergänzen
- [ ] Commit + Push + PR

## Entscheidungen

- Keine externen React-Wrapper für MapLibre (react-map-gl etc.) — minimale Deps
- Proxy-Target via `BACKEND_URL` Env-Var; Fallback `http://localhost:8000`
- Mock-Routen liegen in Liechtenstein (Vaduz → Schaan) für Konsistenz mit OSM-Datensatz
- Feature-State-Hover nur für Fill-Layer geeignet; bei Lines `setPaintProperty` direkt
