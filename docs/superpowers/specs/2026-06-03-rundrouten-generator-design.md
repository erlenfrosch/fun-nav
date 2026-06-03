# Spec: Rundrouten-Generator

**Issue:** #6
**Branch:** agent/issue-6
**Datum:** 2026-06-03

## Problem

fun-nav soll eine Route generieren, die am selben Punkt startet und endet (Rundroutenr).
GraphHopper bietet dafür den Algorithmus `round_trip` an.

## Lösung

Backend-Endpunkt `POST /api/round-trip`, der GraphHopper's `algorithm=round_trip` aufruft
und das Ergebnis normalisiert zurückgibt. Minimales React-Frontend-Formular für
Startkoordinaten, Zieldistanz und Verkehrsmittel.

## API-Design

### Request

```
POST /api/round-trip
Content-Type: application/json

{
  "lat": 47.1,
  "lng": 9.5,
  "distance": 10000,
  "profile": "bike",
  "seed": 0
}
```

### Response (200)

```json
{
  "distance": 10243.5,
  "time": 2345678,
  "points": {"type": "LineString", "coordinates": [...]},
  "bbox": [9.5, 47.1, 9.51, 47.11]
}
```

### Fehler

| Status | Ursache                        |
|--------|-------------------------------|
| 422    | Ungültige Eingabe (Pydantic)  |
| 502    | GraphHopper antwortet mit Fehler |
| 503    | GraphHopper nicht erreichbar  |

## Akzeptanzkriterien

- POST /api/round-trip gibt eine GeoJSON-LineString-Route zurück
- Start- und Endpunkt der Route liegen beim gegebenen Koordinatenpaar
- Tests decken Erfolgsfall, GH-Down (503) und GH-Fehler (502) ab
- Ungültige Eingaben liefern 422 (Pydantic-Validierung)
