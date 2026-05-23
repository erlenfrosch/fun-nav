## Beschreibung
React PWA mit Vite und MapLibre GL JS — leere Karte zentriert auf DACH.

## Aufgaben
- [ ] `npm create vite@latest frontend -- --template react-ts`
- [ ] MapLibre GL JS + react-map-gl installieren
- [ ] `Map.tsx`: Karte zentriert auf DACH (zoom ~7), Tile-Quelle OpenFreeMap (kostenlos, kein API-Key)
- [ ] vite-plugin-pwa Basis-Konfiguration
- [ ] `Dockerfile` für Docker Compose (dev + HMR)

## Akzeptanzkriterium
`http://localhost:5173` → Karte mit DACH-Gebiet sichtbar.
