#!/usr/bin/env bash
# Erstellt alle GitHub Milestones und Issues für fun-nav (Runden-Modus)
# Voraussetzung: gh CLI installiert und authentifiziert (gh auth login)
# Ausführen: bash scripts/create-github-issues.sh

set -euo pipefail

REPO="erlenfrosch/fun-nav"

echo "=== Fun-Nav GitHub Backlog Setup ==="
echo "Repository: $REPO"
echo ""

# --- Milestones ---
echo "Erstelle Milestones..."

M1=$(gh api repos/$REPO/milestones -X POST \
  -f title="Milestone 1 – Infrastruktur & Setup" \
  -f description="Monorepo, GraphHopper Docker, FastAPI Grundstruktur, React PWA Grundgerüst" \
  --jq '.number')
echo "  ✓ Milestone 1 (#$M1)"

M2=$(gh api repos/$REPO/milestones -X POST \
  -f title="Milestone 2 – Routing-Kern" \
  -f description="GraphHopper Custom Model für Kurvigkeit, Rundrouten-Algorithmus, REST Endpoint" \
  --jq '.number')
echo "  ✓ Milestone 2 (#$M2)"

M3=$(gh api repos/$REPO/milestones -X POST \
  -f title="Milestone 3 – Frontend Runden-Modus" \
  -f description="RoutePanel UI, Karten-Anzeige, GPS-Position" \
  --jq '.number')
echo "  ✓ Milestone 3 (#$M3)"

M4=$(gh api repos/$REPO/milestones -X POST \
  -f title="Milestone 4 – Navigation" \
  -f description="Turn-by-Turn HUD, Off-Route-Erkennung, Re-Routing" \
  --jq '.number')
echo "  ✓ Milestone 4 (#$M4)"

M5=$(gh api repos/$REPO/milestones -X POST \
  -f title="Milestone 5 – PWA & Mobile" \
  -f description="Service Worker, Offline-Tiles, Responsive Layout" \
  --jq '.number')
echo "  ✓ Milestone 5 (#$M5)"

echo ""

# --- Labels ---
echo "Erstelle Labels..."
gh api repos/$REPO/labels -X POST -f name="infra" -f color="0075ca" -f description="Infrastruktur & Setup" 2>/dev/null || true
gh api repos/$REPO/labels -X POST -f name="backend" -f color="e4e669" -f description="FastAPI / Python Backend" 2>/dev/null || true
gh api repos/$REPO/labels -X POST -f name="frontend" -f color="7057ff" -f description="React / MapLibre Frontend" 2>/dev/null || true
gh api repos/$REPO/labels -X POST -f name="routing" -f color="d93f0b" -f description="GraphHopper / Routing-Algorithmus" 2>/dev/null || true
gh api repos/$REPO/labels -X POST -f name="navigation" -f color="0e8a16" -f description="GPS / Turn-by-Turn Navigation" 2>/dev/null || true
gh api repos/$REPO/labels -X POST -f name="pwa" -f color="f9d0c4" -f description="PWA / Offline / Mobile" 2>/dev/null || true
echo "  ✓ Labels erstellt"

echo ""

# --- Issues: Milestone 1 ---
echo "Erstelle Issues – Milestone 1..."

gh issue create --repo $REPO \
  --title "Monorepo-Struktur anlegen + Docker Compose Grundgerüst" \
  --label "infra" \
  --milestone "$M1" \
  --body "## Beschreibung
Projektstruktur anlegen und Docker Compose für Entwicklung vorbereiten.

## Aufgaben
- [ ] Verzeichnisstruktur anlegen: \`frontend/\`, \`backend/\`, \`graphhopper/\`, \`scripts/\`, \`docs/\`
- [ ] \`.gitignore\` mit OSM-Daten (\`graphhopper/data/*.pbf\`), Node-Modules, Python venvs
- [ ] \`docker-compose.yml\` mit Services: \`graphhopper\`, \`backend\`, \`frontend\`
- [ ] \`README.md\` mit Quickstart-Anleitung

## Akzeptanzkriterium
\`docker-compose up\` startet alle Services ohne Fehler (auch wenn GH noch leer ist)."

gh issue create --repo $REPO \
  --title "GraphHopper Docker-Setup für DACH" \
  --label "infra,routing" \
  --milestone "$M1" \
  --body "## Beschreibung
GraphHopper self-hosted via Docker für die DACH-Region konfigurieren.

## Aufgaben
- [ ] \`graphhopper/config.yml\` erstellen (Auto-Profil, Custom Model aktivieren)
- [ ] Download-Script \`scripts/download-osm.sh\` für DACH .pbf von Geofabrik
- [ ] Docker Compose Service \`graphhopper\` mit Volume-Mount für \`graphhopper/data/\`
- [ ] Startup-Healthcheck bis GH-Graphen fertig gebaut ist

## Technische Details
- OSM-Quelle: https://download.geofabrik.de/europe/dach-latest.osm.pbf (~800 MB)
- GH Image: \`graphhopper/graphhopper:latest\`
- Port: 8989

## Akzeptanzkriterium
\`curl localhost:8989/health\` gibt \`{\"status\":\"ready\"}\` zurück."

gh issue create --repo $REPO \
  --title "FastAPI Backend Grundstruktur" \
  --label "backend,infra" \
  --milestone "$M1" \
  --body "## Beschreibung
FastAPI Backend mit Grundstruktur, Health-Endpoint und CORS konfigurieren.

## Aufgaben
- [ ] \`backend/main.py\` mit FastAPI App
- [ ] \`GET /health\` Endpoint → \`{\"status\":\"ok\"}\`
- [ ] CORS für Frontend (localhost:5173)
- [ ] \`backend/requirements.txt\` (fastapi, uvicorn, httpx, pydantic)
- [ ] \`backend/Dockerfile\` für Docker Compose
- [ ] Grundlegende Ordnerstruktur: \`routers/\`, \`services/\`, \`models/\`

## Akzeptanzkriterium
\`curl localhost:8000/health\` gibt \`{\"status\":\"ok\"}\` zurück."

gh issue create --repo $REPO \
  --title "React PWA Grundgerüst mit MapLibre GL JS" \
  --label "frontend,infra" \
  --milestone "$M1" \
  --body "## Beschreibung
React PWA mit Vite und MapLibre GL JS aufsetzen — zeigt eine leere Karte zentriert auf DACH.

## Aufgaben
- [ ] \`npm create vite@latest frontend -- --template react-ts\`
- [ ] MapLibre GL JS + react-map-gl installieren
- [ ] \`Map.tsx\` Komponente: Karte zentriert auf DACH (Wien/München Bereich, zoom ~7)
- [ ] Tile-Quelle: OpenFreeMap (kostenlos, keine API-Key)
- [ ] vite-plugin-pwa installieren + Basis-Konfiguration
- [ ] \`frontend/Dockerfile\` für Docker Compose (dev mode mit HMR)

## Akzeptanzkriterium
Browser öffnet \`http://localhost:5173\` → Karte mit DACH-Gebiet sichtbar."

echo "  ✓ Milestone 1 Issues erstellt"
echo ""

# --- Issues: Milestone 2 ---
echo "Erstelle Issues – Milestone 2..."

gh issue create --repo $REPO \
  --title "GraphHopper Custom Model für Kurvigkeits-Modi" \
  --label "routing,backend" \
  --milestone "$M2" \
  --body "## Beschreibung
GraphHopper Custom Models für beide Kurvigkeits-Modi implementieren und testen.

## Aufgaben
- [ ] \`graphhopper/config.yml\` um Custom Model Support erweitern
- [ ] Modus \"kurvenreich\": \`curvature < 0.7 → multiply_by: 1.5\`, Autobahnen meiden
- [ ] Modus \"sehr kurvenreich\": \`curvature < 0.4 → multiply_by: 3.0\`, Autobahnen/Bundesstraßen stark meiden
- [ ] \`backend/services/graphhopper.py\`: HTTP Client für GH Routing API
- [ ] Unit-Tests: Route kurvenreich vs. sehr kurvenreich vergleichen (gleicher Start/Ziel)

## Technische Details
GraphHopper Custom Model Syntax (per-request):
\`\`\`json
{\"priority\": [{\"if\": \"curvature < 0.7\", \"multiply_by\": 1.5}]}
\`\`\`

## Akzeptanzkriterium
Test zeigt: sehr-kurvenreich Route hat höheren Kurvenanteil als kurvenreich Route."

gh issue create --repo $REPO \
  --title "Rundrouten-Generator Algorithmus" \
  --label "routing,backend" \
  --milestone "$M2" \
  --body "## Beschreibung
Kernalgorithmus zur Generierung von Rundrouten in \`backend/services/circular_route.py\`.

## Algorithmus
1. Ø-Geschwindigkeit: 50 km/h (kurvenreich) / 40 km/h (sehr kurvenreich)
2. Radius = \`(fahrtzeit_min/60 * avg_speed) / (2π)\` km
3. 8 Kandidaten-Waypoints gleichmäßig auf Kreis (alle 45°)
4. 6 Routen-Varianten via GraphHopper (je 2 gegenüberliegende Waypoints)
5. Filtern: Fahrtzeit-Abweichung ≤ 20%
6. Sortieren nach Kurvigkeits-Score
7. Top 3 zurückgeben

## Aufgaben
- [ ] \`circular_route.py\` implementieren
- [ ] Waypoint-Berechnung (Haversine-Formel für korrekte Geo-Koordinaten)
- [ ] Parallelisierte GH-Anfragen (asyncio.gather)
- [ ] Unit-Tests mit Mock-GH-Responses

## Akzeptanzkriterium
Für München (48.137°N, 11.575°E), 60 min: 3 Routen mit 48–72 min Dauer."

gh issue create --repo $REPO \
  --title "REST Endpoint POST /api/routes/circular" \
  --label "backend" \
  --milestone "$M2" \
  --body "## Beschreibung
FastAPI Endpoint, der den Rundrouten-Algorithmus als REST API exponiert.

## Request Schema (Pydantic)
\`\`\`json
{
  \"lat\": 48.137,
  \"lon\": 11.575,
  \"duration_min\": 60,
  \"curviness\": \"high\" | \"very_high\"
}
\`\`\`

## Response Schema
\`\`\`json
{
  \"routes\": [{
    \"id\": \"route_1\",
    \"duration_min\": 58.3,
    \"distance_km\": 47.2,
    \"geojson\": { ... },
    \"instructions\": [...]
  }]
}
\`\`\`

## Aufgaben
- [ ] \`backend/routers/routes.py\` mit dem Endpoint
- [ ] \`backend/models/schemas.py\` mit Pydantic-Modellen
- [ ] Fehlerbehandlung (GH nicht erreichbar, keine Route gefunden)
- [ ] Integration-Tests gegen echten GH

## Akzeptanzkriterium
POST liefert 3 Routen in < 5 Sekunden."

echo "  ✓ Milestone 2 Issues erstellt"
echo ""

# --- Issues: Milestone 3 ---
echo "Erstelle Issues – Milestone 3..."

gh issue create --repo $REPO \
  --title "RoutePanel UI – Fahrtzeit-Slider und Kurvigkeits-Toggle" \
  --label "frontend" \
  --milestone "$M3" \
  --body "## Beschreibung
UI-Panel für die Rundrouten-Konfiguration als React-Komponente.

## UI-Elemente
- Slider: Fahrtzeit 15–180 Minuten (Schritte: 15 min)
- Toggle: kurvenreich / sehr kurvenreich
- Button: \"Route berechnen\"
- Ladeindikator während Berechnung

## Aufgaben
- [ ] \`RoutePanel.tsx\` implementieren
- [ ] Styling: Maps-ähnliches UI (weiße Card, Schatten, abgerundete Ecken)
- [ ] \`useRouting.ts\` Hook: API-Call + Loading/Error-State
- [ ] Keyboard-Navigation und Touch-freundliche Controls

## Akzeptanzkriterium
Panel auf Karte, Slider bewegt sich flüssig, Button löst API-Call aus."

gh issue create --repo $REPO \
  --title "3 Route-Optionen auf Karte anzeigen" \
  --label "frontend" \
  --milestone "$M3" \
  --body "## Beschreibung
Die 3 generierten Routen auf der MapLibre-Karte visualisieren und auswählbar machen.

## Aufgaben
- [ ] GeoJSON-Layer für jede Route (Farben: blau, grün, orange)
- [ ] Hover-Effekt: Route wird dicker
- [ ] Click/Tap: Route auswählen (ausgewählt = fetter + andere blass)
- [ ] \`RouteCard.tsx\`: Info-Card unter der Karte (Dauer, Distanz, Kurvigkeits-Score)
- [ ] Karte zoomt automatisch auf gewählte Route

## Akzeptanzkriterium
3 Routen auf Karte, auswählbar, zugehörige Info-Cards sichtbar."

gh issue create --repo $REPO \
  --title "GPS-Position live auf Karte" \
  --label "frontend,navigation" \
  --milestone "$M3" \
  --body "## Beschreibung
Echtzeit-GPS-Position des Nutzers auf der Karte anzeigen.

## Aufgaben
- [ ] \`useGeolocation.ts\` Hook: \`navigator.geolocation.watchPosition\`
- [ ] Blauer Punkt mit Genauigkeits-Kreis auf Karte
- [ ] \"Mein Standort\"-Button: Karte auf aktuelle Position zentrieren
- [ ] Fallback: Manuelle Standort-Eingabe wenn GPS verweigert
- [ ] Karte startet zentriert auf letzten bekannten Standort (localStorage)

## Akzeptanzkriterium
Blauer GPS-Punkt erscheint, aktualisiert sich beim Bewegen."

echo "  ✓ Milestone 3 Issues erstellt"
echo ""

# --- Issues: Milestone 4 ---
echo "Erstelle Issues – Milestone 4..."

gh issue create --repo $REPO \
  --title "Turn-by-Turn Navigation HUD" \
  --label "navigation,frontend" \
  --milestone "$M4" \
  --body "## Beschreibung
Echtzeit-Navigation HUD (Heads-Up Display) während der Fahrt.

## UI-Elemente
- Großes Abbiegesymbol (Pfeil) oben auf der Karte
- Distanz zur nächsten Abbiegung (z.B. \"in 300 m\")
- Straßenname der nächsten Straße
- Restzeit und Restdistanz zur Route-Vollendung
- \"Navigation beenden\"-Button

## Aufgaben
- [ ] \`NavigationHUD.tsx\` Komponente
- [ ] Positionierung: GPS-Position gegen Route-Polyline projekzieren
- [ ] Nächste Anweisung aus GH \`instructions\`-Array ermitteln
- [ ] Distanz zur nächsten Abbiegung berechnen
- [ ] Karte folgt GPS-Position (\"Track Up\"-Modus optional)

## Akzeptanzkriterium
HUD zeigt korrekte Abbiegung für aktuelle GPS-Position."

gh issue create --repo $REPO \
  --title "Off-Route-Erkennung und automatisches Re-Routing" \
  --label "navigation,backend" \
  --milestone "$M4" \
  --body "## Beschreibung
Erkennen wenn der Nutzer von der Route abkommt, und automatisch neu berechnen.

## Aufgaben
- [ ] Off-Route-Erkennung: Abstand GPS → Route-Polyline > 50m = Off-Route
- [ ] Re-Routing: Neuer GraphHopper-Call von aktueller Position zum nächsten Waypoint
- [ ] Debounce: Re-Routing max. alle 10 Sekunden auslösen
- [ ] UI-Feedback: \"Neu berechne Route...\" Toast-Nachricht
- [ ] Bestehende Route ausblenden, neue einblenden

## Akzeptanzkriterium
Nach 50m Abweichung erscheint Toast, neue Route wird berechnet und angezeigt."

echo "  ✓ Milestone 4 Issues erstellt"
echo ""

# --- Issues: Milestone 5 ---
echo "Erstelle Issues – Milestone 5..."

gh issue create --repo $REPO \
  --title "PWA Service Worker (installierbar)" \
  --label "pwa" \
  --milestone "$M5" \
  --body "## Beschreibung
App als installierbare PWA konfigurieren.

## Aufgaben
- [ ] vite-plugin-pwa vollständig konfigurieren
- [ ] \`manifest.json\`: Name, Icons (512px, 192px), Theme-Farbe
- [ ] Service Worker: App-Shell cachen (HTML, JS, CSS)
- [ ] Install-Prompt: \"Zum Homescreen hinzufügen\" Banner
- [ ] iOS Safari: \`apple-touch-icon\`, \`apple-mobile-web-app-capable\`

## Akzeptanzkriterium
Chrome/Safari zeigen Install-Prompt, App startet offline (leere Karte)."

gh issue create --repo $REPO \
  --title "Offline-Tile-Caching für DACH via map-gl-offline" \
  --label "pwa,frontend" \
  --milestone "$M5" \
  --body "## Beschreibung
Karten-Tiles für die DACH-Region offline speichern damit Navigation auch ohne Internet funktioniert.

## Aufgaben
- [ ] \`map-gl-offline\` (npm) installieren und konfigurieren
- [ ] \"Offline speichern\"-Button: Tiles für aktuellen Karten-Ausschnitt in IndexedDB laden
- [ ] Fortschrittsbalken während Download
- [ ] Tile-Fallback: Gecachte Tiles verwenden wenn offline
- [ ] Storage-Info: \"X MB gespeichert\" anzeigen

## Akzeptanzkriterium
Nach Tile-Download: Airplane-Modus an → Karte bleibt sichtbar."

gh issue create --repo $REPO \
  --title "Mobile-optimiertes Responsive Layout" \
  --label "pwa,frontend" \
  --milestone "$M5" \
  --body "## Beschreibung
Layout für Smartphone-Nutzung optimieren (Motorrad-Halterung, Handschuhe).

## Aufgaben
- [ ] Touch-Gesten: Karte zoomen/schwenken nativ via MapLibre
- [ ] Große Tap-Targets: Buttons min. 48×48px
- [ ] Panel-Position: Bottom Sheet auf Mobile, Sidebar auf Desktop
- [ ] Landscape-Modus: HUD optimiert für Querformat
- [ ] Verhindert Bildschirm-Schlaf während Navigation (Wake Lock API)

## Akzeptanzkriterium
App auf iPhone/Android: Alle Buttons tappbar, HUD in Landscape gut lesbar."

echo "  ✓ Milestone 5 Issues erstellt"
echo ""
echo "=== Fertig! ==="
echo "Alle Milestones und Issues wurden in $REPO erstellt."
echo "Issues anzeigen: https://github.com/$REPO/issues"
