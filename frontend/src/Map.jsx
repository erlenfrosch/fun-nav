import { useEffect, useRef } from 'react'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'

const MAP_STYLE = 'https://tiles.openfreemap.org/styles/bright'

export default function Map({ routes, selectedRoute, hoveredRoute, onSelectRoute, onHoverRoute }) {
  const containerRef = useRef(null)
  const mapRef = useRef(null)
  const loadedRef = useRef(false)

  useEffect(() => {
    const map = new maplibregl.Map({
      container: containerRef.current,
      style: MAP_STYLE,
      center: [9.521, 47.141],
      zoom: 11.5,
    })

    map.addControl(new maplibregl.NavigationControl(), 'top-right')

    map.on('load', () => {
      routes.forEach((route) => {
        map.addSource(route.id, { type: 'geojson', data: route.geojson })

        map.addLayer({
          id: route.id,
          type: 'line',
          source: route.id,
          layout: { 'line-join': 'round', 'line-cap': 'round' },
          paint: {
            'line-color': route.color,
            'line-width': 4,
            'line-opacity': 0.9,
          },
        })

        map.on('click', route.id, () => onSelectRoute(route.id))
        map.on('mouseenter', route.id, () => {
          map.getCanvas().style.cursor = 'pointer'
          onHoverRoute(route.id)
        })
        map.on('mouseleave', route.id, () => {
          map.getCanvas().style.cursor = ''
          onHoverRoute(null)
        })
      })

      loadedRef.current = true
    })

    mapRef.current = map
    return () => {
      map.remove()
      loadedRef.current = false
    }
  }, [])

  useEffect(() => {
    const map = mapRef.current
    if (!map || !loadedRef.current) return

    routes.forEach((route) => {
      if (!map.getLayer(route.id)) return

      let width = 4
      let opacity = 0.9
      let color = route.color

      if (selectedRoute) {
        if (route.id === selectedRoute) {
          width = 7
          opacity = 1
        } else {
          opacity = 0.3
          color = route.colorFaded
          width = 3
        }
      } else if (hoveredRoute) {
        if (route.id === hoveredRoute) {
          width = 6
        } else {
          opacity = 0.55
        }
      }

      map.setPaintProperty(route.id, 'line-width', width)
      map.setPaintProperty(route.id, 'line-opacity', opacity)
      map.setPaintProperty(route.id, 'line-color', color)
    })
  }, [selectedRoute, hoveredRoute, routes])

  useEffect(() => {
    const map = mapRef.current
    if (!map || !selectedRoute || !loadedRef.current) return

    const route = routes.find((r) => r.id === selectedRoute)
    if (!route) return

    const coords = route.geojson.geometry.coordinates
    const bounds = coords.reduce(
      (b, c) => b.extend(c),
      new maplibregl.LngLatBounds(coords[0], coords[0])
    )
    map.fitBounds(bounds, { padding: 80, duration: 600 })
  }, [selectedRoute, routes])

  return <div ref={containerRef} style={{ width: '100%', height: '100%' }} />
}
