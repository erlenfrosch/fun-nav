## Beschreibung
Erkennen wenn der Nutzer von der Route abkommt, und automatisch neu berechnen.

## Aufgaben
- [ ] Off-Route-Erkennung: Abstand GPS → Polyline > 50m = Off-Route
- [ ] Re-Routing: Neuer GraphHopper-Call von aktueller Position zum nächsten Waypoint
- [ ] Debounce: Re-Routing max. alle 10 Sekunden auslösen (verhindert Flapping)
- [ ] UI-Feedback: „Berechne Route neu…" Toast-Nachricht
- [ ] Bestehende Route ausblenden, neue Route einblenden

## Akzeptanzkriterium
Nach 50m Abweichung erscheint Toast, neue Route wird berechnet und auf Karte angezeigt.
