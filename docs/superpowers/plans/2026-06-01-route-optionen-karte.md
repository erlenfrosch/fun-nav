# Plan: 3 Route-Optionen auf Karte anzeigen

**Issue:** #9
**Spec:** docs/superpowers/specs/2026-06-01-route-optionen-karte-design.md
**Datum:** 2026-06-01

## Recherche-Quellen

- react-leaflet Polyline API: https://react-leaflet.js.org/docs/api-components
- react-leaflet vector layers Beispiel: https://react-leaflet.js.org/docs/example-vector-layers
- GraphHopper Alternative Routes: `algorithm=alternative_route&ch.disable=true&alternative_route.max_paths=3`

## Aufgaben

### Backend
- [ ] Test: `test_routes_endpoint` schreiben (pytest, httpx mock)
- [ ] `GET /routes` Endpunkt in `backend/app/main.py`
- [ ] GraphHopper-Aufruf mit `algorithm=alternative_route&ch.disable=true&alternative_route.max_paths=3&points_encoded=false`
- [ ] Response-Schema: `{ routes: [{ coordinates: [[lat,lon],...], distance_m: float, duration_ms: int }] }`
- [ ] `pytest` und `pytest-asyncio` in `requirements.txt` hinzufügen

### Frontend
- [ ] `leaflet` und `react-leaflet` in `package.json` hinzufügen
- [ ] `RouteForm`-Komponente: Eingabe für from/to Koordinaten + Submit-Button
- [ ] `RouteMap`-Komponente: MapContainer + TileLayer + Polylines
- [ ] `App.jsx` zusammenbauen

## Entscheidungen

- Kartenbibliothek: `react-leaflet` (High reputation, 157 Snippets, gut dokumentiert)
- CH deaktivieren für Alternativrouten (GraphHopper-Limitation: CH unterstützt keine Alternativen)
- Routenfarben: Blau (primär), Orange (alternativ 1), Grün (alternativ 2)
- Koordinaten-Eingabe: Dezimalgrad als Text-Input (einfachste Lösung, kein Geocoding nötig)
- Kein Geocoder in diesem Issue (YAGNI)
