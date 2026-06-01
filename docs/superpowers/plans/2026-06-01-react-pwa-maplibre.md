# Plan: React PWA Grundgerüst mit MapLibre GL JS

**Issue:** #4  
**Branch:** agent/issue-4  
**Spec:** `docs/superpowers/specs/2026-06-01-react-pwa-maplibre-design.md`

## Aufgaben

1. `package.json` — neue Abhängigkeiten: `maplibre-gl`, `react-map-gl`, `vite-plugin-pwa`, TypeScript-Devdeps
2. `tsconfig.json` + `tsconfig.node.json` — TypeScript-Konfiguration für Vite
3. `src/Map.tsx` — MapLibre-Karte, OpenFreeMap-Tiles, DACH-Zentrierung
4. `src/App.tsx` — vollbildige Karte, ersetzt App.jsx
5. `src/main.tsx` — TypeScript-Version von main.jsx
6. `vite.config.ts` — React-Plugin + VitePWA + HMR-Polling
7. `index.html` — Script-Referenz auf `main.tsx` aktualisieren
8. `Dockerfile` — bereits korrekt, kein Update nötig
9. Alte JSX-Dateien entfernen (App.jsx, main.jsx)
