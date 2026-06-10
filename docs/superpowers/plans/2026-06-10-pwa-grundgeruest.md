# Plan: React PWA Grundgerüst mit MapLibre GL JS

**Datum:** 2026-06-10
**Spec:** docs/superpowers/specs/2026-06-10-pwa-grundgeruest-design.md
**Issue:** #4

## Recherche

- vite-plugin-pwa Doku: https://vite-pwa-org.netlify.app/guide/
- Minimal Requirements: https://vite-pwa-org.netlify.app/guide/pwa-minimal-requirements.html
- Quelle: context7 /vite-pwa/vite-plugin-pwa

## Umgesetzte Aufgaben

1. ✅ `vite-plugin-pwa` installiert — `npm install -D vite-plugin-pwa`
2. ✅ `App.jsx` → `App.tsx` — vollständig typsicher, `RouteOption[]`-State
3. ✅ `main.jsx` → `main.tsx` — React-Root mit TypeScript
4. ✅ `index.html` — `main.tsx`, `theme-color` Meta, Manifest-Link
5. ✅ `vite.config.ts` — VitePWA mit autoUpdate, Workbox, Manifest
6. ✅ `public/icon.svg` — Vektor-Icon für Manifest (`sizes: any`)
7. ✅ `public/pwa-192x192.png` + `pwa-512x512.png` — PNG-Icons für Lighthouse
8. ✅ `App.test.tsx` — App-Rendering-Tests

## Vite-Plugin-Konfiguration

```ts
VitePWA({
  registerType: 'autoUpdate',
  includeAssets: ['icon.svg', 'pwa-192x192.png', 'pwa-512x512.png'],
  workbox: {
    globPatterns: ['**/*.{js,css,html,ico,png,svg}'],
  },
  manifest: {
    name: 'fun-nav',
    short_name: 'fun-nav',
    description: 'Self-hosted Navigation for DACH',
    theme_color: '#1976d2',
    background_color: '#ffffff',
    display: 'standalone',
    start_url: '/',
    icons: [
      { src: 'pwa-192x192.png', sizes: '192x192', type: 'image/png' },
      { src: 'pwa-512x512.png', sizes: '512x512', type: 'image/png', purpose: 'any maskable' },
      { src: 'icon.svg', sizes: 'any', type: 'image/svg+xml', purpose: 'any' },
    ],
  },
})
```
