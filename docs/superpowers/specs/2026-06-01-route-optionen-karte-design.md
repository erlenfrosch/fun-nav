# Spec: 3 Route-Optionen auf Karte anzeigen

**Issue:** #9
**Branch:** agent/issue-9
**Datum:** 2026-06-01

## Problem

Das Frontend zeigt bisher nur einen Platzhalter-Text. Nutzer können keine Route
berechnen und keine Karte sehen. Ziel ist es, Start- und Zielpunkt eingeben zu
können und bis zu 3 alternative Routen auf einer interaktiven Karte anzuzeigen.

## Lösung

### Backend

Neuer Endpunkt `GET /routes` im FastAPI-Backend:
- Parameter: `from_lat`, `from_lon`, `to_lat`, `to_lon` (float)
- Ruft GraphHopper mit `algorithm=alternative_route&alternative_route.max_paths=3&ch.disable=true` auf
- Gibt eine Liste von bis zu 3 Routen zurück: je GeoJSON-Koordinaten, Distanz (m), Dauer (ms)

### Frontend

React-App mit:
- Interaktiver Leaflet-Karte (OpenStreetMap-Tiles)
- Formular für Start- und Zielkoordinaten
- Button "Route berechnen"
- Bis zu 3 Routen als farbige Polylines (blau, orange, grün)
- Info-Box je Route: Distanz in km, Dauer in Minuten

## Akzeptanzkriterien

- [ ] `GET /routes?from_lat=...&from_lon=...&to_lat=...&to_lon=...` liefert JSON mit `routes`-Array
- [ ] Frontend zeigt Leaflet-Karte
- [ ] Nutzer kann Koordinaten eingeben und Route abrufen
- [ ] Bis zu 3 Alternativrouten werden farbig auf der Karte angezeigt
- [ ] Jede Route zeigt Distanz und Dauer an
