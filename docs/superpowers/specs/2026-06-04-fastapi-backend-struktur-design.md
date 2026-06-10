# Spec: FastAPI Backend Grundstruktur

**Issue:** #3  
**Branch:** agent/issue-3  
**Datum:** 2026-06-04

## Problem

Das Backend hat nur einen simplen Health-Endpoint. Es fehlt die eigentliche
Routing-Logik, die Anfragen an GraphHopper weiterleitet, sowie eine saubere
Projektstruktur (Config, Schemas, Router).

## Lösung

Erweiterung des FastAPI-Backends um:
- Strukturierte Aufteilung: `config`, `schemas`, `graphhopper`-Client, `routers/`
- `POST /route`-Endpoint: nimmt Start-/Zielkoordinaten, fragt GraphHopper an,
  gibt Distanz, Dauer und Polyline zurück
- Tests mit gemocktem GraphHopper-Client (respx)

## API-Design

### `POST /route`

**Request:**
```json
{
  "start": {"lat": 47.1415, "lng": 9.5215},
  "end":   {"lat": 47.1700, "lng": 9.5100},
  "profile": "car"
}
```

**Response (200):**
```json
{
  "distance": 5432.1,
  "duration": 432000,
  "points": "_p~iF~ps|U_ulLnnqC"
}
```

**Fehler:**
- `502` — GraphHopper nicht erreichbar oder HTTP-Fehler
- `404` — Keine Route gefunden (leeres `paths`-Array)

## Akzeptanzkriterium

- `GET /health` → `{"status": "ok"}`
- `POST /route` mit gültigen Koordinaten → `200` mit Routendaten
- `POST /route` wenn GraphHopper `5xx` → `502`
- Alle Tests grün (`pytest`)
