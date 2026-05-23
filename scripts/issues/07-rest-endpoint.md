## Beschreibung
FastAPI Endpoint, der den Rundrouten-Algorithmus als REST API exponiert.

## Request Schema (Pydantic)
```json
{"lat": 48.137, "lon": 11.575, "duration_min": 60, "curviness": "high"}
```
`curviness`: `"high"` | `"very_high"`

## Response Schema
```json
{
  "routes": [{
    "id": "route_1",
    "duration_min": 58.3,
    "distance_km": 47.2,
    "geojson": { "type": "LineString", "coordinates": [...] },
    "instructions": [{"text": "Links abbiegen", "distance": 320}]
  }]
}
```

## Aufgaben
- [ ] `backend/routers/routes.py` mit dem Endpoint
- [ ] `backend/models/schemas.py` mit Pydantic-Modellen
- [ ] Fehlerbehandlung: GH nicht erreichbar → 503, keine Route gefunden → 404
- [ ] Integration-Tests gegen echten GraphHopper

## Akzeptanzkriterium
POST liefert 3 Routen mit korrektem GeoJSON in < 5 Sekunden.
