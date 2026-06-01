import { useState } from 'react'
import Map from './Map.jsx'
import RouteCard from './RouteCard.jsx'
import { ROUTES } from './mockRoutes.js'

export default function App() {
  const [selectedRoute, setSelectedRoute] = useState(null)
  const [hoveredRoute, setHoveredRoute] = useState(null)

  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'system-ui, sans-serif' }}>
      <aside
        style={{
          width: '280px',
          flexShrink: 0,
          padding: '20px 16px',
          overflowY: 'auto',
          background: '#f8fafc',
          borderRight: '1px solid #e2e8f0',
        }}
      >
        <h1 style={{ margin: '0 0 4px', fontSize: '18px', color: '#1e293b' }}>fun-nav</h1>
        <p style={{ margin: '0 0 20px', fontSize: '13px', color: '#64748b' }}>
          3 Routen gefunden — wähle eine aus
        </p>

        {ROUTES.map((route) => (
          <RouteCard
            key={route.id}
            route={route}
            selected={selectedRoute === route.id}
            onClick={setSelectedRoute}
          />
        ))}

        {selectedRoute && (
          <button
            onClick={() => setSelectedRoute(null)}
            style={{
              marginTop: '8px',
              width: '100%',
              padding: '8px',
              border: '1px solid #cbd5e1',
              borderRadius: '6px',
              background: 'transparent',
              color: '#64748b',
              cursor: 'pointer',
              fontSize: '13px',
            }}
          >
            Auswahl aufheben
          </button>
        )}
      </aside>

      <main style={{ flex: 1, position: 'relative' }}>
        <Map
          routes={ROUTES}
          selectedRoute={selectedRoute}
          hoveredRoute={hoveredRoute}
          onSelectRoute={setSelectedRoute}
          onHoverRoute={setHoveredRoute}
        />
      </main>
    </div>
  )
}
