## Beschreibung
Kernalgorithmus zur Generierung von Rundrouten in `backend/services/circular_route.py`.

## Algorithmus
1. Ø-Geschwindigkeit: 50 km/h (kurvenreich) / 40 km/h (sehr kurvenreich)
2. Radius = `(fahrtzeit_min / 60 * avg_speed) / (2π)` km
3. 8 Kandidaten-Waypoints gleichmäßig auf Kreis (alle 45°) via Haversine-Formel
4. 6 Routen-Varianten via GraphHopper (je 2 gegenüberliegende Waypoints)
5. Filtern: Fahrtzeit-Abweichung ≤ 20% vom Ziel
6. Sortieren nach Kurvigkeits-Score
7. Top 3 zurückgeben

## Aufgaben
- [ ] `circular_route.py` implementieren
- [ ] Waypoint-Berechnung mit Haversine-Formel für korrekte Geo-Koordinaten
- [ ] Parallelisierte GH-Anfragen (asyncio.gather)
- [ ] Unit-Tests mit Mock-GH-Responses

## Akzeptanzkriterium
München (48.137°N, 11.575°E), 60 min → 3 Routen mit 48–72 min Dauer zurück.
