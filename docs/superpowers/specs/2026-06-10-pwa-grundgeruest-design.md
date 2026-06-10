# Spec: React PWA Grundgerüst mit MapLibre GL JS

**Datum:** 2026-06-10
**Issue:** #4

## Ziel

Das Frontend wird zu einer installierbaren Progressive Web App (PWA) ausgebaut.
Nutzer können die App auf dem Homescreen ihres Geräts installieren und grundlegende
Offline-Fähigkeit (App-Shell-Cache via Service Worker) nutzen.

## Ausgangszustand (dieser Branch)

- React 18 + Vite + TypeScript
- MapLibre GL JS via `react-map-gl/maplibre`
- `App.tsx`, `main.tsx` in TypeScript ✅
- `vite-plugin-pwa` installiert und konfiguriert ✅
- `index.html` mit `theme-color` Meta und Manifest-Link ✅
- SVG-Icon (`icon.svg`) für Manifest ✅
- PNG-Icons 192×192 und 512×512 für Lighthouse-Kompatibilität ✅

## Anforderungen

### Funktional
- App ist über den Browser installierbar (Web-App-Manifest vorhanden)
- Service Worker cached die App-Shell für Offline-Nutzung (Workbox GenerateSW)
- Seite lädt bei erneutem Besuch auch ohne Netz (zumindest die Shell)

### Technisch
- `registerType: 'autoUpdate'` — SW wird automatisch aktualisiert
- Manifest: name, short_name, theme_color, background_color, display standalone
- Icons: 192×192 PNG + 512×512 PNG (maskable) + SVG (any)
- TypeScript kompiliert ohne Fehler (`tsc --noEmit`)

### Nicht-Ziele
- Offline-Tile-Caching (Kacheln sind externe Ressource, zu groß)
- Push-Notifications
- Background-Sync

## Akzeptanzkriterien

- [x] `npm test` — alle Tests grün (27/27)
- [x] `tsc --noEmit` — keine TypeScript-Fehler
- [x] `npm run build` produziert `dist/manifest.webmanifest` und `dist/sw.js`
- [ ] Lighthouse-PWA-Audit meldet "Installable" (manuell, kein CI-Gate)
