# Spec: GraphHopper Custom Model für Kurvigkeits-Modi

**Issue:** #5  
**Branch:** agent/issue-5  
**Datum:** 2026-05-31

## Problem

fun-nav soll kurvenreiche Motorradrouten berechnen. GraphHopper bietet dafür Custom Models,
die per API-Request übergeben werden können. Bisher hat `graphhopper/config.yml` keine
Custom-Model-fähigen Profile.

## Lösung

### 1. GraphHopper-Profil: `bike_custom`

Ein neues Profil mit `weighting: custom` und `custom_model_files: []` erlaubt es, bei
jedem Routing-Request ein individuelles Custom Model mitzuschicken. CH (Contraction
Hierarchies) entfällt für dieses Profil, da CH mit dynamischen Custom Models unverträglich ist.

### 2. Kurvigkeits-Modi (Custom Models gemäß Issue-Beschreibung)

**kurvenreich:**
```json
{"priority": [{"if": "curvature < 0.7", "multiply_by": 1.5}, {"if": "road_class == MOTORWAY", "multiply_by": 0.1}]}
```

**sehr_kurvenreich:**
```json
{"priority": [{"if": "curvature < 0.4", "multiply_by": 3.0}, {"if": "road_class == MOTORWAY || road_class == TRUNK", "multiply_by": 0.05}]}
```

Die `curvature`-Variable liegt im Bereich 0 (gerade) bis 1 (sehr kurvig). Ein niedrigerer
Threshold bedeutet, dass nur stärker kurvige Straßen bevorzugt werden.

### 3. Backend-Service: `backend/app/services/graphhopper.py`

Async-Funktion `route_curvy(start, end, mode, base_url)`:
- Nimmt Lat/Lon-Koordinaten und Modus-String entgegen
- Sendet POST `/route` an GraphHopper mit passendem Custom Model
- Gibt den GH-API-Response zurück

### 4. Tests

Unit-Tests mit gemocktem httpx-Client (kein laufender GH nötig):
- Prüfen, dass das korrekte Custom Model pro Modus gesendet wird
- Prüfen, dass `sehr_kurvenreich` strengere Schwellenwerte hat als `kurvenreich`
- Prüfen, dass ungültige Modi einen Fehler werfen

## Nicht-Ziele

- Kein neuer API-Endpoint im Backend (separates Issue)
- Kein Frontend-Change
- Kein Contraction Hierarchies für `bike_custom`

## Quellen

- GraphHopper Custom Models: https://docs.graphhopper.com/#section/Map-Data-and-Routing-Profiles/OpenStreetMap/Customized-Routing-Profiles
- Curvature-Diskussion: https://discuss.graphhopper.com/t/setting-curvature-in-v5/7360
