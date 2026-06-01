import Map from 'react-map-gl/maplibre'
import 'maplibre-gl/dist/maplibre-gl.css'

const DACH_CENTER = { longitude: 13.5, latitude: 47.5, zoom: 7 }
const TILE_STYLE = 'https://tiles.openfreemap.org/styles/liberty'

export default function MapView() {
  return (
    <Map
      initialViewState={DACH_CENTER}
      style={{ width: '100%', height: '100%' }}
      mapStyle={TILE_STYLE}
    />
  )
}
