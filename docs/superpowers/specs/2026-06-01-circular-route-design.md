# Spec: POST /api/routes/circular

## Kontext
GitHub Issue #7 — Rundrouten-Endpoint für fun-nav Backend.

## Request-Schema
```json
{
  "lat": 48.137,
  "lon": 11.575,
  "duration_min": 60,
  "curviness": "high"
}
```
- `lat`, `lon`: Startkoordinaten (float)
- `duration_min`: Gewünschte Fahrtdauer in Minuten (float)
- `curviness`: Kurvenreichtum — `"high"` | `"very_high"`

## Response-Schema (3 Routen)
```json
{
  "routes": [
    {
      "id": "route_1",
      "duration_min": 58.3,
      "distance_km": 47.2,
      "geojson": {
        "type": "LineString",
        "coordinates": [[11.575, 48.137], ...]
      },
      "instructions": [
        {"text": "Links abbiegen", "distance": 320}
      ]
    }
  ]
}
```

## Fehlerbehandlung
| Situation | HTTP-Status | Detail |
|---|---|---|
| GraphHopper nicht erreichbar (`ConnectError`) | 503 | "GraphHopper nicht erreichbar" |
| GraphHopper antwortet mit Nicht-200 | 503 | "GraphHopper-Fehler: <status>" |
| Keine Route gefunden (`paths` leer) | 404 | "Keine Route gefunden" |
| Ungültiger `curviness`-Wert | 422 | Pydantic-Validierungsfehler |

## GraphHopper-Mapping: curviness → distance_m

GraphHopper Round-Trip-Algorithmus erwartet `round_trip.distance` in Metern.
Formel: `distance_m = duration_min * M_PER_MIN`

| curviness | m/min | Begründung |
|---|---|---|
| `high` | 250 | Ca. 15 km/h Durchschnitt (kurvenreiche Strecke) |
| `very_high` | 167 | Ca. 10 km/h (stark kurvenreiche Strecke, Bergpfade) |

## GraphHopper API-Aufruf
```
GET /route?point=<lat>,<lon>&profile=bike&algorithm=round_trip
         &round_trip.distance=<distance_m>&round_trip.seed=<0|1|2>
         &locale=de&calc_points=true&instructions=true&points_encoded=false
```
Seeds 0, 1, 2 erzeugen 3 verschiedene Routen vom selben Startpunkt.

## Akzeptanzkriterium
- POST `/api/routes/circular` liefert exakt 3 Routen
- Jede Route enthält GeoJSON `LineString` mit mindestens 2 Koordinaten
- Response in < 5 Sekunden
