import { useState } from 'react'
import { RoutePanel } from './components/RoutePanel'
import { RouteCard } from './components/RouteCard'
import { RouteMap } from './components/Map'
import type { RouteOption } from './api/routes'

const DEFAULT_LAT = 47.5
const DEFAULT_LON = 13.5

export default function App() {
  const [routes, setRoutes] = useState<RouteOption[]>([])
  const [selectedIndex, setSelectedIndex] = useState(0)

  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'system-ui, sans-serif' }}>
      <aside style={{
        width: '320px',
        display: 'flex',
        flexDirection: 'column',
        overflowY: 'auto',
        background: '#f9fafb',
        borderRight: '1px solid #e5e7eb',
      }}>
        <header style={{ padding: '1rem 1.25rem', borderBottom: '1px solid #e5e7eb' }}>
          <h1 style={{ margin: 0, fontSize: '1.25rem', fontWeight: 700 }}>fun-nav</h1>
        </header>
        <RoutePanel
          lat={DEFAULT_LAT}
          lon={DEFAULT_LON}
          onRoutesCalculated={(r) => { setRoutes(r); setSelectedIndex(0) }}
        />
        {routes.map((route, i) => (
          <RouteCard
            key={route.id}
            route={route}
            index={i}
            isSelected={i === selectedIndex}
            onClick={() => setSelectedIndex(i)}
          />
        ))}
      </aside>
      <main style={{ flex: 1, position: 'relative' }}>
        <RouteMap
          routes={routes}
          selectedIndex={selectedIndex}
          onRouteSelect={setSelectedIndex}
        />
      </main>
    </div>
  )
}
