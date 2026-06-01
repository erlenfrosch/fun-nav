import { useEffect, useRef } from 'react'
import { Map as MapLibre } from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'

const DEFAULT_STYLE = 'https://demotiles.maplibre.org/style.json'
const DEFAULT_CENTER = [9.5, 47.14]
const DEFAULT_ZOOM = 10

export default function Map({
  style = DEFAULT_STYLE,
  center = DEFAULT_CENTER,
  zoom = DEFAULT_ZOOM,
}) {
  const containerRef = useRef(null)
  const mapRef = useRef(null)

  useEffect(() => {
    if (mapRef.current) return

    mapRef.current = new MapLibre({
      container: containerRef.current,
      style,
      center,
      zoom,
    })

    return () => {
      mapRef.current?.remove()
      mapRef.current = null
    }
  }, [])

  return <div ref={containerRef} style={{ width: '100%', height: '100%' }} />
}
