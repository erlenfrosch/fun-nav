# Spec: Rundrouten-Generator Algorithmus

**Issue:** #6  
**Branch:** agent/issue-6  
**Datum:** 2026-06-02

## Problem

fun-nav soll Motorrad-/Auto-Fahrern Rundrouten auf Basis einer gewünschten Fahrtzeit
generieren. Ohne Algorithmus gibt es keine Routen.

## Lösung

Service `backend/app/services/circular_route.py` mit folgendem Algorithmus:

1. **Radius-Berechnung**  
   `radius = (fahrtzeit_min / 60 * avg_speed) / (2π)` km  
   avg_speed = 50 km/h (kurvenreich) / 40 km/h (sehr kurvenreich)

2. **8 Kandidaten-Waypoints** gleichmäßig auf dem Kreis (je 45°) via Haversine-Formel  
   (Inverse-Haversine: Zielpunkt aus Startpunkt, Kurs und Distanz)

3. **6 Routen-Varianten** via GraphHopper:  
   - 4 Paare mit genau gegenüberliegenden Waypoints (180°): (W0,W4), (W1,W5), (W2,W6), (W3,W7)  
   - 2 Paare mit nahezu gegenüberliegenden Waypoints (135°): (W0,W3), (W2,W5)  
   - Jede Route: Start → Wi → Wj → Start  
   - Parallelisiert via `asyncio.gather`

4. **Filtern:** Fahrtzeit-Abweichung ≤ 20% vom Ziel

5. **Sortieren** nach Kurvigkeits-Score (absteigende Reihenfolge)  
   Score = tatsächliche Streckenlänge / (2 × Radius) — Detour-Faktor

6. **Top 3 zurückgeben**

## Akzeptanzkriterium

München (48.137°N, 11.575°E), 60 min → 3 Routen mit 48–72 min Dauer.

## Nicht-Ziele

- Keine UI-Anbindung in diesem Issue
- Kein Profil-Auswahl (car als Default)
- Kein Caching
