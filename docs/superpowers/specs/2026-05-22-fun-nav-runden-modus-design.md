# Design Spec: Fun-Nav Runden-Modus

**Datum:** 2026-05-22
**Status:** Genehmigt
**Projekt:** fun-nav — Sub-Projekt 1 von 2

---

## Problemstellung

Motorrad- und Autofahrer wollen Touren nicht nach Ankunftszeit, sondern nach Fahrspaß planen.
Klassische Navigations-Apps (Google Maps, Apple Maps) optimieren auf Schnelligkeit und kennen
kein Konzept für kurvenreiche Strecken oder Rundkurse.

## Ziel

Eine Web-App / PWA, bei der der Nutzer eine **Wunsch-Fahrtzeit** eingibt, und die App automatisch
eine **kurvenreiche Rundroute** (Start = Ziel) berechnet und navigiert. Ankunftszeit ist
nebensächlich — Fahrspaß ist das Ziel.

---

## Scope (Sub-Projekt 1)

**In Scope:**
- Runden-Modus: Rundrouten-Generierung basierend auf Fahrtzeit
- Kurvigkeits-Auswahl: kurvenreich / sehr kurvenreich
- Karten-UI im Maps-Stil
- Echtzeit GPS-Navigation (Turn-by-Turn)
- PWA (installierbar, Offline-Tiles für DACH)

**Out of Scope (→ Sub-Projekt 2):**
- Navigations-Modus (A→B mit Kurvenpräferenz)
- Benutzerkonten und gespeicherte Routen
- Social Features (Routen teilen)

---

## Technologie-Entscheidungen

| Schicht | Technologie | Begründung |
|---|---|---|
| Frontend | React (Vite) + TypeScript + MapLibre GL JS | WebGL2, zero-cost Lizenz, PWA-fähig |
| Karten-Binding | react-map-gl | idiomatische React-Integration |
| Offline-Tiles | map-gl-offline (IndexedDB) | vollständiges Offline-Caching |
| Backend | FastAPI (Python 3.12) | async, automatische OpenAPI-Docs |
| Routing-Engine | GraphHopper self-hosted (Docker) | nativer `curvature`-Support + Custom Models API |
| OSM-Daten | DACH .pbf von Geofabrik | kostenlos, aktuell |
| Tile-Quelle | OpenFreeMap / MapTiler Free | DACH-Karten kostenfrei |

**Warum GraphHopper statt Valhalla:**
GraphHopper hat ein natives `curvature`-Attribut (0..1, niedrig = kurvig) und eine Custom Models API
für Per-Request-Kurvigkeits-Gewichtung. Kurviger — der führende Mitbewerber — basiert ebenfalls
auf GraphHopper. Quelle: [GraphHopper Curvature Forum](https://discuss.graphhopper.com/t/setting-curvature-in-v5/7360),
[Kurviger OSM Wiki](https://wiki.openstreetmap.org/wiki/Kurviger)

---

## Kurvigkeits-Modi

GraphHopper Custom Model per Request:

```json
// "kurvenreich" — mäßige Bevorzugung kurvenreicher Landstraßen
{
  "priority": [
    {"if": "curvature < 0.7", "multiply_by": 1.5},
    {"if": "road_class == MOTORWAY", "multiply_by": 0.1}
  ]
}

// "sehr kurvenreich" — starke Bevorzugung, Autobahnen fast ausgeschlossen
{
  "priority": [
    {"if": "curvature < 0.4", "multiply_by": 3.0},
    {"if": "road_class == MOTORWAY || road_class == TRUNK", "multiply_by": 0.05}
  ]
}
```

---

## Rundrouten-Generator-Algorithmus

GraphHopper bietet keinen nativen Circular-Route-Endpunkt. Das Backend implementiert:

```
Eingabe: (lat, lon, fahrtzeit_min, kurvigkeit)

1. Ø-Geschwindigkeit:
   - kurvenreich:      50 km/h
   - sehr kurvenreich: 40 km/h

2. Radius berechnen:
   total_km = (fahrtzeit_min / 60) * avg_speed_kmh
   radius_km = total_km / (2 * π)

3. 8 Kandidaten-Waypoints auf Kreis (je 45°):
   lat_wp = lat + (radius_km / 111) * cos(angle)
   lon_wp = lon + (radius_km / 111) * sin(angle) / cos(lat_rad)

4. 6 Route-Varianten anfragen:
   - 2 Waypoints gegenüber (0°+180°, 45°+225°, 90°+270°)

5. Routen filtern und sortieren:
   - Fahrtzeit-Abweichung ≤ 20% vom Ziel
   - Score = curvature_score * duration_match_score

6. Top 3 zurückgeben
```

---

## Architektur

```
Browser (PWA)
  └── React + MapLibre GL JS
        ├── Karte + Route-Visualisierung (MapLibre)
        ├── GPS via Web Geolocation API
        └── REST → FastAPI :8000
                    ├── POST /api/routes/circular
                    └── HTTP → GraphHopper :8989 (Docker)
                                  └── DACH OSM .pbf (Geofabrik)
```

---

## Projektstruktur

```
fun-nav/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Map.tsx              # MapLibre GL JS Wrapper
│   │   │   ├── RoutePanel.tsx       # Fahrtzeit-Slider + Kurvigkeits-Toggle
│   │   │   ├── RouteCard.tsx        # Einzelne Route-Option
│   │   │   └── NavigationHUD.tsx    # Turn-by-Turn Overlay
│   │   ├── hooks/
│   │   │   ├── useGeolocation.ts    # GPS-Position
│   │   │   └── useRouting.ts        # API-Calls + Route-State
│   │   └── api/
│   │       └── routes.ts            # Backend API Client
│   ├── vite.config.ts               # Vite + PWA Plugin
│   └── package.json
├── backend/
│   ├── main.py
│   ├── routers/routes.py            # /api/routes/circular
│   ├── services/
│   │   ├── graphhopper.py           # GraphHopper HTTP Client
│   │   └── circular_route.py        # Rundrouten-Algorithmus
│   └── models/schemas.py            # Pydantic-Modelle
├── graphhopper/
│   ├── config.yml                   # GH Custom Profile
│   └── data/                        # OSM .pbf (gitignored)
└── docker-compose.yml
```

---

## User Flow

```
1. App öffnen
   → Karte lädt, zentriert auf DACH
   → GPS-Position wird ermittelt

2. Fahrtzeit wählen (Slider: 15–180 min)
   + Kurvigkeit wählen (kurvenreich / sehr kurvenreich)
   → "Route berechnen" drücken

3. 3 Route-Optionen erscheinen auf der Karte
   (verschiedene Farben, Karte zeigt Dauer + Distanz)
   → Nutzer wählt eine Route

4. Navigation starten
   → HUD zeigt: nächste Abbiegung, Distanz, Straßenname
   → Bei Off-Route: automatisches Re-Routing
```

---

## Nicht-funktionale Anforderungen

- PWA installierbar auf iOS und Android
- Offline-Nutzung für DACH-Gebiet (vorher gecachte Tiles)
- Routing-Antwort < 5 Sekunden (GH lokal, DACH-Daten)
- Mobile-first Responsive Design (Touch-Gesten, große Tap-Targets)
