## Beschreibung
UI-Panel für die Rundrouten-Konfiguration als React-Komponente.

## UI-Elemente
- Slider: Fahrtzeit 15–180 Minuten (Schritte: 15 min)
- Toggle: kurvenreich / sehr kurvenreich
- Button: „Route berechnen"
- Ladeindikator während Berechnung

## Aufgaben
- [ ] `RoutePanel.tsx` implementieren
- [ ] Maps-ähnliches Styling (weiße Card, Schatten, abgerundete Ecken)
- [ ] `useRouting.ts` Hook: API-Call + Loading/Error-State
- [ ] Touch-freundliche Controls (min. 48×48px Tap-Targets)

## Akzeptanzkriterium
Panel auf Karte sichtbar, Slider bewegt sich flüssig, Button löst API-Call aus.
