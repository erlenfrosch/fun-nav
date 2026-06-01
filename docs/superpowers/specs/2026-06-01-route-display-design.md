# Spec: 3 Route-Optionen auf Karte anzeigen

**Issue:** #9  
**Branch:** agent/issue-9  
**Datum:** 2026-06-01

## Problem

Der Nutzer erhält nach der Runden-Berechnung 3 Route-Optionen, sieht diese aber
noch nicht auf der Karte. Es fehlen Visualisierung, Interaktion und Info-Karten.

## Lösung

MapLibre GL JS in das Frontend integrieren. Drei Routes als GeoJSON-LineStrings
auf der Karte darstellen. Jede Route hat eine eigene Farbe und ist interaktiv
(Hover → verdickt, Klick → ausgewählt/blasse Alternativrouten).

## Komponenten

| Komponente       | Datei                     | Aufgabe |
|---|---|---|
| Karte            | `src/Map.jsx`             | MapLibre-Instanz, Routen-Layer, Events |
| Route-Karte      | `src/RouteCard.jsx`       | Dauer, Distanz, Kurvig­keits-Score |
| Mock-Daten       | `src/mockRoutes.js`       | 3 GeoJSON-Routen um Vaduz (LI) |
| App-Layout       | `src/App.jsx`             | Karte + Sidebar nebeneinander |

## Farbschema

| Route | Farbe aktiv | Farbe verblasst |
|---|---|---|
| A (kurz, flach) | `#3b82f6` (blau) | `#93c5fd` |
| B (mittel, hügelig) | `#22c55e` (grün) | `#86efac` |
| C (lang, kurvig) | `#f97316` (orange) | `#fdba74` |

## Interaktion

- **Hover:** `line-width` von 4 → 6, Cursor = pointer
- **Auswahl:** ausgewählte Route `line-width` 7, andere `line-opacity` 0.3
- **Auto-Zoom:** `fitBounds` auf Bounding-Box der ausgewählten Route

## Akzeptanzkriterium

3 Routen auf Karte sichtbar, auswählbar, zugehörige Info-Cards werden angezeigt.
