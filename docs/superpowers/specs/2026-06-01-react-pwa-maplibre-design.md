# Spec: React PWA Grundgerüst mit MapLibre GL JS

**Issue:** #4  
**Branch:** agent/issue-4  
**Datum:** 2026-06-01

## Ziel

React PWA mit Vite und MapLibre GL JS — leere Karte zentriert auf DACH-Region, kein API-Key erforderlich.

## Akzeptanzkriterium

`http://localhost:5173` zeigt eine vollbildige Karte mit DACH-Gebiet (Deutschland, Österreich, Schweiz).

## Technische Entscheidungen

- **Karten-Library:** `react-map-gl/maplibre` (Wrapper über `maplibre-gl`)
- **Tile-Quelle:** OpenFreeMap Liberty Style — `https://tiles.openfreemap.org/styles/liberty`  
  Kostenlos, kein API-Key, kein Rate-Limit
- **PWA:** `vite-plugin-pwa` mit `registerType: 'autoUpdate'`
- **TypeScript:** Migration von JSX auf TSX (react-ts Pattern)
- **HMR in Docker:** `server.watch.usePolling: true` in Vite-Config

## Komponenten

| Datei | Beschreibung |
|---|---|
| `src/Map.tsx` | MapLibre-Karte, vollbild, zentriert auf DACH (lon 13.5, lat 47.5, zoom 7) |
| `src/App.tsx` | Hauptkomponente, rendert Map vollbild |
| `src/main.tsx` | React-Einstiegspunkt |
| `vite.config.ts` | Vite + PWA-Plugin-Konfiguration |
| `tsconfig.json` | TypeScript-Konfiguration |

## Quellen

- [react-map-gl/maplibre Docs](https://github.com/visgl/react-map-gl/blob/master/docs/api-reference/maplibre/map.md)
- [OpenFreeMap Quick Start](https://openfreemap.org/quick_start/)
- [vite-plugin-pwa Konfiguration](https://github.com/vite-pwa/vite-plugin-pwa/blob/main/docs/guide/index.md)
