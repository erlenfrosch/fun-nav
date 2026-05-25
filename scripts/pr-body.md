## Was wurde gemacht

Design-Spec und Backlog-Scripts für **Sub-Projekt 1: Runden-Modus** der Fun-Nav App — kurvenreiche Rundtouren für Auto und Motorrad.

## Enthaltene Änderungen

- **`docs/superpowers/specs/2026-05-22-fun-nav-runden-modus-design.md`**
  Vollständige Design-Spec: Architektur, Tech-Stack-Entscheidungen, Rundrouten-Algorithmus, User Flow, nicht-funktionale Anforderungen
- **`scripts/create-github-issues.sh`** / **`create-github-issues.ps1`** — Issue-Scripts für zukünftige Anpassungen des Backlogs
- **`scripts/issues/*.md`** — Body-Dateien für alle 15 GitHub Issues

## GitHub Backlog (bereits erstellt)

- ✅ 5 Milestones angelegt
- ✅ 6 Labels: `infra`, `backend`, `frontend`, `routing`, `navigation`, `pwa`
- ✅ 15 Issues erstellt → https://github.com/erlenfrosch/fun-nav/issues

## Tech-Stack-Entscheidungen

| Schicht | Technologie | Begründung |
|---|---|---|
| Frontend | React (Vite) + TypeScript + MapLibre GL JS | WebGL2, zero-cost, PWA-fähig |
| Backend | FastAPI (Python 3.12) | async, OpenAPI-Docs automatisch |
| Routing | GraphHopper self-hosted (Docker) | nativer `curvature`-Attribut-Support |
| Karten | OpenStreetMap / OpenFreeMap | kostenlos, kein API-Key |

**Warum GraphHopper:** Kurviger (führender Mitbewerber) basiert ebenfalls darauf. Nativer `curvature`-Wert pro Straßensegment + Custom Models API für Per-Request-Kurvigkeits-Gewichtung.

## Backlog-Übersicht

| Milestone | Issues |
|---|---|
| 1 – Infrastruktur | #1 Monorepo, #2 GraphHopper DACH, #3 FastAPI, #4 React PWA |
| 2 – Routing-Kern | #5 Custom Model, #6 Rundrouten-Algo, #7 REST Endpoint |
| 3 – Frontend | #8 RoutePanel, #9 Route-Anzeige, #10 GPS |
| 4 – Navigation | #11 Turn-by-Turn HUD, #12 Re-Routing |
| 5 – PWA & Mobile | #13 Service Worker, #14 Offline-Tiles, #15 Responsive |

## Nächste Schritte

Mit **Issue #1** (Monorepo-Struktur) auf einem neuen Feature-Branch beginnen. Sub-Projekt 2 (A→B Navigations-Modus) wird nach Milestone 1–2 separat geplant.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
