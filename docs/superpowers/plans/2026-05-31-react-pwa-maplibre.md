# Plan: React PWA Grundgerüst mit MapLibre GL JS

**Issue:** #4  
**Spec:** docs/superpowers/specs/2026-05-31-react-pwa-maplibre-design.md  
**Datum:** 2026-05-31

## Recherche-Quellen

- MapLibre GL JS Docs (context7): npm-Import, Map-Initialisierung, CSS-Import
- vite-plugin-pwa Docs (context7): VitePWA-Plugin, registerType, manifest config

## Aufgaben

- [x] Branch `agent/issue-4` erstellen
- [x] Spec schreiben
- [x] Plan schreiben
- [ ] `package.json` — maplibre-gl, vite-plugin-pwa, vitest, @testing-library/react
- [ ] `src/components/Map.test.jsx` — Tests zuerst (TDD)
- [ ] `src/components/Map.jsx` — MapLibre-Komponente
- [ ] `src/app.css` — Vollbild-Layout
- [ ] `src/App.jsx` — Map-Komponente einbinden
- [ ] `vite.config.js` — VitePWA + vitest-Konfiguration
- [ ] `src/test-setup.js` — @testing-library/jest-dom
- [ ] `index.html` — PWA-Meta-Tags, theme-color
- [ ] `public/icon.svg` — Platzhalter-Icon
- [ ] `npm install && npm test` — grüne Tests
- [ ] Commit + PR

## Entscheidungen

- MapLibre `^5.0.0` — aktuelle Stable-Version mit GPU-Rendering
- vite-plugin-pwa `registerType: 'autoUpdate'` — Service Worker ohne Nutzerprompt
- Default-Style: `https://demotiles.maplibre.org/style.json` (kein API-Key)
- Default-Center: `[9.5, 47.14]` (Liechtenstein, passend zum OSM-Testdatensatz)
- vitest + jsdom — Map-Klasse wird gemockt, kein WebGL-Kontext nötig
- SVG-Icons als Platzhalter — PNG-Generierung ist eigenständiges TODO
