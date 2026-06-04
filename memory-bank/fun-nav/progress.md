# Progress

## Fertig

- Issue #1: Monorepo-Struktur + Docker Compose Grundgerüst (gemergt via PR #18)
- Issue #5: GraphHopper Custom Model für Kurvigkeits-Modi (Branch `agent/issue-5`, PR pending)
  - `graphhopper/config.yml` um Motorcycle-Custom-Model-Profil erweitert
  - `backend/app/services/graphhopper.py` implementiert (CURVY_MODEL, VERY_CURVY_MODEL, get_route, average_curvature)
  - 7 Unit-Tests, alle grün

## Läuft

- PR für Issue #5 erstellen

## Als nächstes

- Frontend-Anbindung: Route-Endpunkt in FastAPI, UI-Auswahl der Modi
- OSM-Daten-Download-Skript fertigstellen
- Integration-Tests mit echtem GraphHopper
