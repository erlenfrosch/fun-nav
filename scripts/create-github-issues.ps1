# Fun-Nav GitHub Backlog erstellen
# Erstellt alle Milestones, Labels und Issues für fun-nav (Runden-Modus)
#
# Ausführen:
#   $env:GITHUB_TOKEN="ghp_dein_token_hier"
#   .\scripts\create-github-issues.ps1
#
# Token erstellen: https://github.com/settings/tokens/new
# Benötigte Scopes: repo (damit Issues und Milestones erstellt werden können)

param(
    [string]$Token = $env:GITHUB_TOKEN,
    [string]$Repo = "erlenfrosch/fun-nav"
)

if (-not $Token) {
    Write-Host "GITHUB_TOKEN nicht gesetzt." -ForegroundColor Red
    Write-Host "Erstelle einen Token unter: https://github.com/settings/tokens/new" -ForegroundColor Yellow
    Write-Host "Benötigte Scopes: repo" -ForegroundColor Yellow
    Write-Host ""
    $Token = Read-Host "GitHub Token eingeben"
}

$Headers = @{
    Authorization = "Bearer $Token"
    Accept        = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
}

$Base = "https://api.github.com/repos/$Repo"

function New-Milestone($Title, $Desc) {
    $Body = @{ title = $Title; description = $Desc } | ConvertTo-Json
    $r = Invoke-RestMethod -Uri "$Base/milestones" -Method POST -Headers $Headers -Body $Body -ContentType "application/json"
    Write-Host "  ✓ Milestone: $Title (#$($r.number))" -ForegroundColor Green
    return $r.number
}

function New-Label($Name, $Color, $Desc) {
    try {
        $Body = @{ name = $Name; color = $Color; description = $Desc } | ConvertTo-Json
        Invoke-RestMethod -Uri "$Base/labels" -Method POST -Headers $Headers -Body $Body -ContentType "application/json" | Out-Null
        Write-Host "  ✓ Label: $Name" -ForegroundColor Green
    } catch {
        Write-Host "  ~ Label '$Name' existiert bereits" -ForegroundColor Yellow
    }
}

function New-Issue($Title, $Body, $Labels, $Milestone) {
    $Payload = @{
        title     = $Title
        body      = $Body
        labels    = $Labels
        milestone = $Milestone
    } | ConvertTo-Json
    $r = Invoke-RestMethod -Uri "$Base/issues" -Method POST -Headers $Headers -Body $Payload -ContentType "application/json"
    Write-Host "  ✓ Issue #$($r.number): $Title" -ForegroundColor Green
    return $r.number
}

Write-Host "=== Fun-Nav GitHub Backlog Setup ===" -ForegroundColor Cyan
Write-Host "Repository: $Repo" -ForegroundColor Cyan
Write-Host ""

# Verbindung testen
try {
    $repoInfo = Invoke-RestMethod -Uri $Base -Headers $Headers
    Write-Host "✓ Verbunden mit: $($repoInfo.full_name)" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "✗ Fehler: Kann Repo nicht erreichen. Token korrekt?" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# ── Milestones ──────────────────────────────────────────────────────────────
Write-Host "Erstelle Milestones..." -ForegroundColor Cyan
$M1 = New-Milestone "Milestone 1 – Infrastruktur & Setup" "Monorepo, GraphHopper Docker, FastAPI, React PWA Grundgerüst"
$M2 = New-Milestone "Milestone 2 – Routing-Kern" "GraphHopper Custom Model, Rundrouten-Algorithmus, REST Endpoint"
$M3 = New-Milestone "Milestone 3 – Frontend Runden-Modus" "RoutePanel UI, Karten-Anzeige, GPS Live-Position"
$M4 = New-Milestone "Milestone 4 – Navigation" "Turn-by-Turn HUD, Off-Route-Erkennung, Re-Routing"
$M5 = New-Milestone "Milestone 5 – PWA & Mobile" "Service Worker, Offline-Tiles, Responsive Layout"
Write-Host ""

# ── Labels ───────────────────────────────────────────────────────────────────
Write-Host "Erstelle Labels..." -ForegroundColor Cyan
New-Label "infra"       "0075ca" "Infrastruktur & Setup"
New-Label "backend"     "e4e669" "FastAPI / Python Backend"
New-Label "frontend"    "7057ff" "React / MapLibre Frontend"
New-Label "routing"     "d93f0b" "GraphHopper / Routing-Algorithmus"
New-Label "navigation"  "0e8a16" "GPS / Turn-by-Turn Navigation"
New-Label "pwa"         "f9d0c4" "PWA / Offline / Mobile"
Write-Host ""

# ── Issues: Milestone 1 ──────────────────────────────────────────────────────
Write-Host "Erstelle Issues – Milestone 1..." -ForegroundColor Cyan

New-Issue `
    "Monorepo-Struktur anlegen + Docker Compose Grundgerüst" `
    "## Beschreibung
Projektstruktur anlegen und Docker Compose für Entwicklung vorbereiten.

## Aufgaben
- [ ] Verzeichnisstruktur: ``frontend/``, ``backend/``, ``graphhopper/``, ``scripts/``, ``docs/``
- [ ] ``.gitignore`` mit OSM-Daten (``graphhopper/data/*.pbf``), Node-Modules, Python venvs
- [ ] ``docker-compose.yml`` mit Services: ``graphhopper``, ``backend``, ``frontend``
- [ ] ``README.md`` mit Quickstart-Anleitung

## Akzeptanzkriterium
``docker-compose up`` startet alle Services ohne Fehler." `
    @("infra") $M1

New-Issue `
    "GraphHopper Docker-Setup für DACH" `
    "## Beschreibung
GraphHopper self-hosted via Docker für die DACH-Region konfigurieren.

## Aufgaben
- [ ] ``graphhopper/config.yml`` mit Auto-Profil und Custom Model Unterstützung
- [ ] Download-Script ``scripts/download-osm.sh`` für DACH .pbf (Geofabrik)
- [ ] Docker Compose Service mit Volume-Mount für ``graphhopper/data/``
- [ ] Startup-Healthcheck

## Technische Details
- OSM-Quelle: https://download.geofabrik.de/europe/dach-latest.osm.pbf (~800 MB)
- GH Image: ``graphhopper/graphhopper:latest``
- Port: 8989

## Akzeptanzkriterium
``curl localhost:8989/health`` → ``{""status"":""ready""``}" `
    @("infra", "routing") $M1

New-Issue `
    "FastAPI Backend Grundstruktur" `
    "## Beschreibung
FastAPI Backend mit Health-Endpoint und CORS einrichten.

## Aufgaben
- [ ] ``backend/main.py`` mit FastAPI App
- [ ] ``GET /health`` → ``{""status"":""ok""}``
- [ ] CORS für Frontend (localhost:5173)
- [ ] ``requirements.txt``: fastapi, uvicorn, httpx, pydantic
- [ ] ``Dockerfile`` für Docker Compose
- [ ] Ordnerstruktur: ``routers/``, ``services/``, ``models/``

## Akzeptanzkriterium
``curl localhost:8000/health`` → ``{""status"":""ok""}``" `
    @("backend", "infra") $M1

New-Issue `
    "React PWA Grundgerüst mit MapLibre GL JS" `
    "## Beschreibung
React PWA mit Vite und MapLibre GL JS — leere Karte zentriert auf DACH.

## Aufgaben
- [ ] ``npm create vite@latest frontend -- --template react-ts``
- [ ] MapLibre GL JS + react-map-gl installieren
- [ ] ``Map.tsx``: Karte zentriert auf DACH (zoom ~7), Tile-Quelle OpenFreeMap
- [ ] vite-plugin-pwa Basis-Konfiguration
- [ ] ``Dockerfile`` für Docker Compose (dev + HMR)

## Akzeptanzkriterium
``http://localhost:5173`` zeigt Karte mit DACH-Gebiet." `
    @("frontend", "infra") $M1

Write-Host ""

# ── Issues: Milestone 2 ──────────────────────────────────────────────────────
Write-Host "Erstelle Issues – Milestone 2..." -ForegroundColor Cyan

New-Issue `
    "GraphHopper Custom Model für Kurvigkeits-Modi" `
    "## Beschreibung
GraphHopper Custom Models für beide Kurvigkeits-Modi implementieren.

## Modi
**kurvenreich:**
``````json
{""priority"": [{""if"": ""curvature < 0.7"", ""multiply_by"": 1.5}, {""if"": ""road_class == MOTORWAY"", ""multiply_by"": 0.1}]}
``````
**sehr kurvenreich:**
``````json
{""priority"": [{""if"": ""curvature < 0.4"", ""multiply_by"": 3.0}, {""if"": ""road_class == MOTORWAY || road_class == TRUNK"", ""multiply_by"": 0.05}]}
``````

## Aufgaben
- [ ] ``graphhopper/config.yml`` um Custom Model Support erweitern
- [ ] ``backend/services/graphhopper.py``: HTTP Client für GH Routing API
- [ ] Unit-Tests: Route kurvenreich vs. sehr kurvenreich vergleichen

## Akzeptanzkriterium
Test zeigt: sehr-kurvenreich hat höheren Kurvenanteil als kurvenreich." `
    @("routing", "backend") $M2

New-Issue `
    "Rundrouten-Generator Algorithmus" `
    "## Beschreibung
Kernalgorithmus für Rundrouten-Generierung in ``backend/services/circular_route.py``.

## Algorithmus
1. Ø-Geschwindigkeit: 50 km/h (kurvenreich) / 40 km/h (sehr kurvenreich)
2. Radius = ``(fahrtzeit_min/60 * avg_speed) / (2π)`` km
3. 8 Kandidaten-Waypoints auf Kreis (alle 45°) via Haversine
4. 6 Routen-Varianten via GraphHopper (je 2 gegenüberliegende Waypoints)
5. Filtern: Fahrtzeit-Abweichung ≤ 20%
6. Sortieren nach Kurvigkeits-Score
7. Top 3 zurückgeben

## Aufgaben
- [ ] ``circular_route.py`` implementieren
- [ ] Parallelisierte GH-Anfragen (asyncio.gather)
- [ ] Unit-Tests mit Mock-GH-Responses

## Akzeptanzkriterium
München (48.137°N, 11.575°E), 60 min → 3 Routen mit 48–72 min Dauer." `
    @("routing", "backend") $M2

New-Issue `
    "REST Endpoint POST /api/routes/circular" `
    "## Beschreibung
FastAPI Endpoint für den Rundrouten-Algorithmus.

## Request (Pydantic)
``````json
{""lat"": 48.137, ""lon"": 11.575, ""duration_min"": 60, ""curviness"": ""high""}
``````
``curviness``: ``high`` | ``very_high``

## Response
``````json
{""routes"": [{""id"": ""route_1"", ""duration_min"": 58.3, ""distance_km"": 47.2, ""geojson"": {...}, ""instructions"": [...]}]}
``````

## Aufgaben
- [ ] ``backend/routers/routes.py`` mit Endpoint
- [ ] ``backend/models/schemas.py`` mit Pydantic-Modellen
- [ ] Fehlerbehandlung (GH nicht erreichbar, keine Route gefunden)
- [ ] Integration-Tests gegen echten GH

## Akzeptanzkriterium
POST liefert 3 Routen in < 5 Sekunden." `
    @("backend") $M2

Write-Host ""

# ── Issues: Milestone 3 ──────────────────────────────────────────────────────
Write-Host "Erstelle Issues – Milestone 3..." -ForegroundColor Cyan

New-Issue `
    "RoutePanel UI – Fahrtzeit-Slider und Kurvigkeits-Toggle" `
    "## Beschreibung
UI-Panel für Rundrouten-Konfiguration.

## UI-Elemente
- Slider: Fahrtzeit 15–180 Minuten (Schritte: 15 min)
- Toggle: kurvenreich / sehr kurvenreich
- Button: »Route berechnen«
- Ladeindikator während Berechnung

## Aufgaben
- [ ] ``RoutePanel.tsx`` implementieren
- [ ] Maps-ähnliches Styling (weiße Card, Schatten)
- [ ] ``useRouting.ts`` Hook: API-Call + Loading/Error-State
- [ ] Touch-freundliche Controls (min. 48×48px)

## Akzeptanzkriterium
Panel auf Karte sichtbar, Slider flüssig, Button löst API-Call aus." `
    @("frontend") $M3

New-Issue `
    "3 Route-Optionen auf Karte anzeigen" `
    "## Beschreibung
Generierte Routen auf der MapLibre-Karte visualisieren und auswählbar machen.

## Aufgaben
- [ ] GeoJSON-Layer für jede Route (Farben: blau, grün, orange)
- [ ] Hover: Route wird dicker
- [ ] Click/Tap: Route auswählen (ausgewählt = fett, andere blass)
- [ ] ``RouteCard.tsx``: Info-Card mit Dauer, Distanz, Kurvigkeits-Score
- [ ] Karte zoomt automatisch auf gewählte Route

## Akzeptanzkriterium
3 Routen auf Karte, auswählbar, Info-Cards sichtbar." `
    @("frontend") $M3

New-Issue `
    "GPS-Position live auf Karte" `
    "## Beschreibung
Echtzeit-GPS-Position des Nutzers auf der Karte anzeigen.

## Aufgaben
- [ ] ``useGeolocation.ts`` Hook: ``navigator.geolocation.watchPosition``
- [ ] Blauer Punkt mit Genauigkeits-Kreis
- [ ] »Mein Standort«-Button: Karte auf aktuelle Position zentrieren
- [ ] Fallback: Manuelle Standort-Eingabe wenn GPS verweigert
- [ ] Letzter Standort in localStorage speichern

## Akzeptanzkriterium
Blauer GPS-Punkt erscheint und aktualisiert sich beim Bewegen." `
    @("frontend", "navigation") $M3

Write-Host ""

# ── Issues: Milestone 4 ──────────────────────────────────────────────────────
Write-Host "Erstelle Issues – Milestone 4..." -ForegroundColor Cyan

New-Issue `
    "Turn-by-Turn Navigation HUD" `
    "## Beschreibung
Echtzeit-Navigation HUD während der Fahrt.

## UI-Elemente
- Großes Abbiegesymbol (Pfeil) oben auf der Karte
- Distanz zur nächsten Abbiegung (»in 300 m«)
- Straßenname der nächsten Straße
- Restzeit und Restdistanz
- »Navigation beenden«-Button

## Aufgaben
- [ ] ``NavigationHUD.tsx`` Komponente
- [ ] GPS-Position gegen Route-Polyline projizieren
- [ ] Nächste Anweisung aus GH ``instructions``-Array ermitteln
- [ ] Karte folgt GPS-Position (Track-Up-Modus optional)

## Akzeptanzkriterium
HUD zeigt korrekte Abbiegung für aktuelle GPS-Position." `
    @("navigation", "frontend") $M4

New-Issue `
    "Off-Route-Erkennung und automatisches Re-Routing" `
    "## Beschreibung
Erkennung wenn der Nutzer von der Route abkommt, automatisch neu berechnen.

## Aufgaben
- [ ] Off-Route: Abstand GPS → Polyline > 50m = Off-Route
- [ ] Re-Routing: Neuer GH-Call von aktueller Position zum nächsten Waypoint
- [ ] Debounce: Max. alle 10 Sekunden auslösen
- [ ] Toast-Nachricht: »Berechne Route neu…«
- [ ] Alte Route ausblenden, neue einblenden

## Akzeptanzkriterium
Nach 50m Abweichung: Toast erscheint, neue Route wird berechnet." `
    @("navigation", "backend") $M4

Write-Host ""

# ── Issues: Milestone 5 ──────────────────────────────────────────────────────
Write-Host "Erstelle Issues – Milestone 5..." -ForegroundColor Cyan

New-Issue `
    "PWA Service Worker (installierbar)" `
    "## Beschreibung
App als installierbare PWA konfigurieren.

## Aufgaben
- [ ] vite-plugin-pwa vollständig konfigurieren
- [ ] ``manifest.json``: Name, Icons (512px, 192px), Theme-Farbe
- [ ] Service Worker: App-Shell cachen (HTML, JS, CSS)
- [ ] Install-Prompt-Banner
- [ ] iOS Safari: ``apple-touch-icon``, ``apple-mobile-web-app-capable``

## Akzeptanzkriterium
Chrome/Safari zeigen Install-Prompt, App startet offline (Shell sichtbar)." `
    @("pwa") $M5

New-Issue `
    "Offline-Tile-Caching für DACH via map-gl-offline" `
    "## Beschreibung
Karten-Tiles für DACH offline speichern.

## Aufgaben
- [ ] ``map-gl-offline`` (npm) installieren und konfigurieren
- [ ] »Offline speichern«-Button: Tiles für aktuellen Ausschnitt in IndexedDB
- [ ] Fortschrittsbalken während Download
- [ ] Tile-Fallback: gecachte Tiles wenn offline
- [ ] Storage-Info: »X MB gespeichert«

## Akzeptanzkriterium
Nach Tile-Download: Airplane-Modus → Karte bleibt sichtbar." `
    @("pwa", "frontend") $M5

New-Issue `
    "Mobile-optimiertes Responsive Layout" `
    "## Beschreibung
Layout für Smartphone-Nutzung optimieren (Motorrad-Halterung, Handschuhe).

## Aufgaben
- [ ] Große Tap-Targets: Buttons min. 48×48px
- [ ] Bottom Sheet auf Mobile, Sidebar auf Desktop
- [ ] Landscape-Modus: HUD für Querformat optimiert
- [ ] Wake Lock API: Bildschirm-Schlaf während Navigation verhindern
- [ ] Overscroll-Verhalten deaktivieren (verhindert Browser-Pull-to-Refresh)

## Akzeptanzkriterium
iPhone/Android: Alle Buttons tappbar, HUD in Landscape gut lesbar." `
    @("pwa", "frontend") $M5

Write-Host ""
Write-Host "=== Fertig! ===" -ForegroundColor Green
Write-Host "Alle 5 Milestones und 15 Issues wurden erstellt." -ForegroundColor Green
Write-Host "Issues: https://github.com/$Repo/issues" -ForegroundColor Cyan
Write-Host "Milestones: https://github.com/$Repo/milestones" -ForegroundColor Cyan
