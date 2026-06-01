# Spec: React PWA Grundgerüst mit MapLibre GL JS

**Issue:** #4  
**Branch:** agent/issue-4  
**Datum:** 2026-05-31

## Problem

Das Frontend `fun-nav` benötigt eine interaktive Karte als zentrales UI-Element.
Aktuell zeigt die App nur einen Platzhalter-Text. Außerdem fehlt eine PWA-Konfiguration
(Manifest, Service Worker), um die App auf Mobilgeräten installierbar zu machen.

## Lösung

MapLibre GL JS als Kartenrenderer (GPU-beschleunigt, Open-Source, kein API-Key nötig).
PWA-Setup über `vite-plugin-pwa` (autoUpdate-Strategie, Manifest mit Icons).
Vollbild-Kartenlayout mit React-Hook für saubere Lifecycle-Verwaltung (init/cleanup).

## Akzeptanzkriterien

- `npm run dev` zeigt eine vollbildige interaktive Karte (MapLibre GL JS)
- `npm test` — alle Tests grün
- `npm run build` erzeugt ein valides PWA-Bundle (Manifest + Service Worker)
- Karteninitialisierung mit Standardparameter: Liechtenstein (Testdatensatz), Zoom 10
- Map-Komponente ist testbar (MapLibre wird gemockt)
- Sauberes Cleanup beim Unmount (map.remove())

## Out of Scope

- Routing-UI (kommt in späteren Issues)
- Echtes Kartenstil-Hosting (demotiles als Default)
- Produktionsreife PNG-Icons (SVG-Platzhalter genügt für Grundgerüst)
