## Beschreibung
Echtzeit-Navigation HUD (Heads-Up Display) während der Fahrt.

## UI-Elemente
- Großes Abbiegesymbol (Pfeil) oben auf der Karte
- Distanz zur nächsten Abbiegung (z.B. „in 300 m")
- Straßenname der nächsten Straße
- Restzeit und Restdistanz zur Route-Vollendung
- „Navigation beenden"-Button

## Aufgaben
- [ ] `NavigationHUD.tsx` Komponente
- [ ] GPS-Position gegen Route-Polyline projizieren (nächster Punkt auf Strecke)
- [ ] Nächste Anweisung aus GraphHopper `instructions`-Array ermitteln
- [ ] Distanz zur nächsten Abbiegung live berechnen
- [ ] Karte folgt GPS-Position (optional: Track-Up-Modus mit Kartenrotation)

## Akzeptanzkriterium
HUD zeigt korrekte Abbiegeanweisung für die aktuelle GPS-Position.
