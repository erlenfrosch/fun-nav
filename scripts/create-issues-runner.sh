#!/usr/bin/env bash
set -e
REPO='erlenfrosch/fun-nav'
D='/home/erlenfrosch/repos/fun-nav/scripts/issues'

gi() {
  local url
  url=$(gh issue create --repo "$REPO" --title "$1" --label "$2" --milestone "$3" --body-file "$D/$4" 2>&1)
  echo "  ✓ $1 → $url"
}

echo "=== Milestone 1 – Infrastruktur ==="
gi "Monorepo-Struktur anlegen + Docker Compose Grundgerüst" "infra" "Milestone 1 – Infrastruktur & Setup" "01-monorepo.md"
gi "GraphHopper Docker-Setup für DACH" "infra,routing" "Milestone 1 – Infrastruktur & Setup" "02-graphhopper.md"
gi "FastAPI Backend Grundstruktur" "backend,infra" "Milestone 1 – Infrastruktur & Setup" "03-fastapi.md"
gi "React PWA Grundgerüst mit MapLibre GL JS" "frontend,infra" "Milestone 1 – Infrastruktur & Setup" "04-react-pwa.md"

echo "=== Milestone 2 – Routing-Kern ==="
gi "GraphHopper Custom Model für Kurvigkeits-Modi" "routing,backend" "Milestone 2 - Routing-Kern" "05-gh-custom-model.md"
gi "Rundrouten-Generator Algorithmus" "routing,backend" "Milestone 2 - Routing-Kern" "06-circular-algorithm.md"
gi "REST Endpoint POST /api/routes/circular" "backend" "Milestone 2 - Routing-Kern" "07-rest-endpoint.md"

echo "=== Milestone 3 – Frontend ==="
gi "RoutePanel UI – Fahrtzeit-Slider und Kurvigkeits-Toggle" "frontend" "Milestone 3 - Frontend Runden-Modus" "08-route-panel.md"
gi "3 Route-Optionen auf Karte anzeigen" "frontend" "Milestone 3 - Frontend Runden-Modus" "09-route-display.md"
gi "GPS-Position live auf Karte" "frontend,navigation" "Milestone 3 - Frontend Runden-Modus" "10-gps.md"

echo "=== Milestone 4 – Navigation ==="
gi "Turn-by-Turn Navigation HUD" "navigation,frontend" "Milestone 4 - Navigation" "11-navigation-hud.md"
gi "Off-Route-Erkennung und automatisches Re-Routing" "navigation,backend" "Milestone 4 - Navigation" "12-rerouting.md"

echo "=== Milestone 5 – PWA ==="
gi "PWA Service Worker (installierbar)" "pwa" "Milestone 5 – PWA & Mobile" "13-service-worker.md"
gi "Offline-Tile-Caching für DACH via map-gl-offline" "pwa,frontend" "Milestone 5 – PWA & Mobile" "14-offline-tiles.md"
gi "Mobile-optimiertes Responsive Layout" "pwa,frontend" "Milestone 5 – PWA & Mobile" "15-responsive.md"

echo ""
echo "=== Fertig! 15 Issues erstellt. ==="
echo "Issues: https://github.com/$REPO/issues"
