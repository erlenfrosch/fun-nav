import { useEffect, useRef } from 'react'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'

const ROUTE_COLORS = ['#3B82F6', '#22C55E', '#F97316']
const VADUZ = [9.5209, 47.1410]

export default function Map({ routes, selectedRoute, onRouteSelect }) {
  const containerRef = useRef(null)
  const mapRef = useRef(null)
  const selectedRef = useRef(selectedRoute)

  useEffect(() => {
    selectedRef.current = selectedRoute
    applyRouteStyles(mapRef.current, routes.length, selectedRoute)
  }, [selectedRoute, routes.length])

  useEffect(() => {
    const map = new maplibregl.Map({
      container: containerRef.current,
      style: 'https://tiles.openfreemap.org/styles/bright',
      center: VADUZ,
      zoom: 12,
    })
    mapRef.current = map

    map.on('load', () => {
      routes.forEach((route, i) => {
        map.addSource(`route-${i}`, {
          type: 'geojson',
          data: { type: 'Feature', properties: {}, geometry: route.geometry },
        })

        map.addLayer({
          id: `route-${i}-line`,
          type: 'line',
          source: `route-${i}`,
          layout: { 'line-join': 'round', 'line-cap': 'round' },
          paint: {
            'line-color': ROUTE_COLORS[i],
            'line-width': i === selectedRef.current ? 6 : 4,
            'line-opacity': i === selectedRef.current ? 1 : 0.6,
          },
        })

        map.on('mousemove', `route-${i}-line`, () => {
          map.getCanvas().style.cursor = 'pointer'
          map.setPaintProperty(`route-${i}-line`, 'line-width', 8)
          map.setPaintProperty(`route-${i}-line`, 'line-opacity', 1)
        })

        map.on('mouseleave', `route-${i}-line`, () => {
          map.getCanvas().style.cursor = ''
          const hasSelection = selectedRef.current !== null && selectedRef.current !== undefined
          const isSelected = selectedRef.current === i
          map.setPaintProperty(`route-${i}-line`, 'line-width', isSelected ? 7 : 4)
          map.setPaintProperty(
            `route-${i}-line`,
            'line-opacity',
            hasSelection && !isSelected ? 0.25 : isSelected ? 1 : 0.8
          )
        })

        map.on('click', `route-${i}-line`, () => {
          onRouteSelect(i)
          zoomToRoute(map, route)
        })
      })

      applyRouteStyles(map, routes.length, selectedRef.current)
    })

    return () => {
      map.remove()
      mapRef.current = null
    }
  }, [])

  return <div ref={containerRef} style={{ width: '100%', height: '100%' }} />
}

function applyRouteStyles(map, routeCount, selectedRoute) {
  if (!map || !map.isStyleLoaded()) return
  const hasSelection = selectedRoute !== null && selectedRoute !== undefined
  for (let i = 0; i < routeCount; i++) {
    const layerId = `route-${i}-line`
    if (!map.getLayer(layerId)) continue
    const isSelected = i === selectedRoute
    map.setPaintProperty(layerId, 'line-width', isSelected ? 7 : 4)
    map.setPaintProperty(
      layerId,
      'line-opacity',
      hasSelection && !isSelected ? 0.25 : isSelected ? 1 : 0.8
    )
  }
}

function zoomToRoute(map, route) {
  const coords = route.geometry.coordinates
  const bounds = coords.reduce(
    (b, c) => b.extend(c),
    new maplibregl.LngLatBounds(coords[0], coords[0])
  )
  map.fitBounds(bounds, { padding: 60 })
}
