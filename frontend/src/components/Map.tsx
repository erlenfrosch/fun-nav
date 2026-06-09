import { useRef, useState, useEffect, useCallback } from 'react'
import MapGL, { Source, Layer } from 'react-map-gl/maplibre'
import type { MapRef, MapMouseEvent } from 'react-map-gl/maplibre'
import 'maplibre-gl/dist/maplibre-gl.css'
import type { RouteOption } from '../api/routes'

const MAP_STYLE = 'https://tiles.openfreemap.org/styles/liberty'
const ROUTE_COLORS = ['#2563eb', '#22c55e', '#f97316']

interface RouteMapProps {
  routes: RouteOption[]
  selectedIndex: number
  onRouteSelect: (index: number) => void
}

export function RouteMap({ routes, selectedIndex, onRouteSelect }: RouteMapProps) {
  const mapRef = useRef<MapRef>(null)
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null)

  useEffect(() => {
    if (!mapRef.current || routes.length === 0) return
    const route = routes[selectedIndex] ?? routes[0]
    if (!route?.geometry?.coordinates?.length) return
    const coords = route.geometry.coordinates
    const lngs = coords.map((c: number[]) => c[0])
    const lats = coords.map((c: number[]) => c[1])
    mapRef.current.fitBounds(
      [[Math.min(...lngs), Math.min(...lats)], [Math.max(...lngs), Math.max(...lats)]],
      { padding: 60, duration: 800 }
    )
  }, [selectedIndex, routes])

  const routeLayerIds = routes.map((_, i) => `route-line-${i}`)

  const handleClick = useCallback((e: MapMouseEvent) => {
    const features = e.target.queryRenderedFeatures(e.point, { layers: routeLayerIds })
    if (!features.length) return
    const idx = parseInt(features[0].layer.id.replace('route-line-', ''), 10)
    if (!isNaN(idx)) onRouteSelect(idx)
  }, [routeLayerIds, onRouteSelect])

  const handleMouseMove = useCallback((e: MapMouseEvent) => {
    const features = e.target.queryRenderedFeatures(e.point, { layers: routeLayerIds })
    if (features.length) {
      const idx = parseInt(features[0].layer.id.replace('route-line-', ''), 10)
      setHoveredIndex(isNaN(idx) ? null : idx)
      e.target.getCanvas().style.cursor = 'pointer'
    } else {
      setHoveredIndex(null)
      e.target.getCanvas().style.cursor = ''
    }
  }, [routeLayerIds])

  return (
    <MapGL
      ref={mapRef}
      mapStyle={MAP_STYLE}
      initialViewState={{ longitude: 9.5215, latitude: 47.1416, zoom: 9 }}
      style={{ width: '100%', height: '100%' }}
      onClick={handleClick}
      onMouseMove={handleMouseMove}
    >
      {routes.map((route, i) => (
        <Source
          key={route.id}
          id={`route-source-${i}`}
          type="geojson"
          data={{ type: 'Feature', geometry: route.geometry, properties: {} }}
        >
          <Layer
            id={`route-line-${i}`}
            type="line"
            layout={{ 'line-join': 'round', 'line-cap': 'round' }}
            paint={{
              'line-color': ROUTE_COLORS[i] ?? '#6b7280',
              'line-width': hoveredIndex === i ? 8 : i === selectedIndex ? 6 : 4,
              'line-opacity': i === selectedIndex ? 1 : hoveredIndex === i ? 0.85 : 0.45,
            }}
          />
        </Source>
      ))}
    </MapGL>
  )
}
