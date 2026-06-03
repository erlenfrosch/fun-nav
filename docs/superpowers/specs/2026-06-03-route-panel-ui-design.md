# Spec: RoutePanel UI – Fahrtzeit-Slider und Kurvigkeits-Toggle

**Datum:** 2026-06-03  
**Issue:** #8  
**Branch:** agent/issue-8

## Ziel

React-Komponente `RoutePanel` für die Rundrouten-Konfiguration. Eingebettet in die
App-Oberfläche als Maps-ähnliche weiße Card mit Schatten.

## UI-Elemente

| Element | Verhalten |
|---|---|
| Range-Slider | Fahrtzeit 15–180 min, Schrittweite 15 min; zeigt aktuellen Wert |
| Kurvigkeits-Toggle | Button-Gruppe: „kurvenreich" / „sehr kurvenreich" |
| Berechnen-Button | Disabled während Ladevorgang; zeigt Spinner-Text |
| Ladeindikator | Sichtbar solange `loading === true` im Hook |
| Fehlermeldung | Sichtbar wenn `error` gesetzt |

## API-Vertrag

POST `/api/route`  
Body: `{ durationMinutes: number, curviness: "kurvenreich" | "sehr-kurvenreich" }`  
Response: Route-Objekt (Format noch offen – wird in separatem Issue definiert)

## Technische Entscheidungen

- Implementierung in **JSX/JS** (kein TypeScript) – passt zum bestehenden Stack (Vite + React 18)
- Styling via dediziertem CSS-Modul `RoutePanel.css`
- Touch-freundlich: alle Interaktionsflächen ≥ 48×48 px
- `useRouting`-Hook kapselt fetch-Logik + loading/error-State

## Quellen

- React custom hooks: https://react.dev/learn/reusing-logic-with-custom-hooks
- useCallback für stabile Funktion: https://react.dev/reference/react/useCallback
