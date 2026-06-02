# Spec: Rundrouten-Generator Algorithmus

**Datum:** 2026-06-02  
**Issue:** #6  
**Branch:** agent/issue-6

## Problem

Nutzer möchten Rundrouten (Ausfahrten) generieren, bei denen Start = Ziel ist und die
Fahrzeit einem gewünschten Zielwert entspricht.

## Lösung

### Algorithmus

1. **Radius berechnen** — `r = (fahrtzeit_min / 60 × 40 km/h) / (2π)` km
2. **8 Wegpunkte generieren** — gleichmäßig auf Kreis (45°-Schritte) via Haversine
3. **6 Routen-Varianten anfragen** — parallele asyncio-Requests an GraphHopper
   (start → waypoint → start, je eine Route pro Wegpunkt)
4. **Filtern** — Abweichung der Fahrzeit ≤ 20% vom Zielwert
5. **Ranken** — nach Curviness-Score absteigend (Strecke / (2 × Radius))

### API

`POST /api/circular-routes`

Request:
```json
{"lat": 48.137, "lng": 11.575, "duration_min": 60}
```

Response:
```json
[{"duration_min": 57.3, "distance_km": 42.1, "waypoint": {"lat": ..., "lng": ...}, "curviness_score": 3.2}]
```

## Akzeptanzkriterium

München (48.137°N, 11.575°E), 60 min → mind. 3 Routen mit 48–72 min Dauer.

## Nicht-Ziele

- Keine Echtzeit-Verkehrsdaten
- Kein Caching der GraphHopper-Ergebnisse
- Keine Profil-Auswahl (nur `car`)
