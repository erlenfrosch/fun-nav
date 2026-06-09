# Plan: RoutePanel UI – Fahrtzeit-Slider und Kurvigkeits-Toggle

**Datum:** 2026-06-03  
**Spec:** docs/superpowers/specs/2026-06-03-route-panel-ui-design.md

## Aufgaben

1. `frontend/src/hooks/useRouting.js` – Hook mit `calculateRoute`, `loading`, `error`, `route`
2. `frontend/src/components/RoutePanel.jsx` – UI-Komponente mit Slider, Toggle, Button
3. `frontend/src/components/RoutePanel.css` – Maps-Stil: weiße Card, Schatten, Rundung
4. `frontend/src/App.jsx` – RoutePanel einbinden
5. `backend/app/main.py` – POST `/api/route` Stub-Endpunkt
6. Tests: `frontend/src/hooks/useRouting.test.js` mit Vitest

## Reihenfolge

Tests → Hook → Komponente → Styling → App → Backend → PR
