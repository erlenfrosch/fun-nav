import { MapContainer, TileLayer, Polyline, useMap } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'

const ROUTE_COLORS = ['#2563eb', '#ea580c', '#16a34a']

function FitBounds({ routes }) {
  const map = useMap()

  if (routes.length === 0) return null

  const allCoords = routes.flatMap((r) => r.coordinates)
  if (allCoords.length === 0) return null

  const lats = allCoords.map(([lat]) => lat)
  const lons = allCoords.map(([, lon]) => lon)
  map.fitBounds([
    [Math.min(...lats), Math.min(...lons)],
    [Math.max(...lats), Math.max(...lons)],
  ])

  return null
}

export default function RouteMap({ routes }) {
  return (
    <MapContainer
      center={[47.14, 9.52]}
      zoom={11}
      style={{ height: '500px', width: '100%' }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {routes.map((route, i) => (
        <Polyline
          key={i}
          positions={route.coordinates}
          pathOptions={{ color: ROUTE_COLORS[i] ?? '#6b7280', weight: i === 0 ? 5 : 3 }}
        />
      ))}
      {routes.length > 0 && <FitBounds routes={routes} />}
    </MapContainer>
  )
}
