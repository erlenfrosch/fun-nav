import { useState, useEffect } from 'react'
import Map from './components/Map'
import RouteCard from './components/RouteCard'

export default function App() {
  const [routes, setRoutes] = useState([])
  const [selectedRoute, setSelectedRoute] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/api/routes')
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`)
        return r.json()
      })
      .then((data) => {
        setRoutes(data.routes)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <div style={styles.centered}>Routen werden geladen…</div>
  }

  if (error) {
    return <div style={styles.centered}>Fehler beim Laden der Routen: {error}</div>
  }

  return (
    <div style={styles.layout}>
      <aside style={styles.sidebar}>
        <h1 style={styles.title}>fun-nav</h1>
        <p style={styles.subtitle}>{routes.length} Routen verfügbar</p>
        <div style={styles.cardList}>
          {routes.map((route, i) => (
            <RouteCard
              key={i}
              route={route}
              index={i}
              selected={selectedRoute === i}
              onSelect={() => setSelectedRoute(i)}
            />
          ))}
        </div>
      </aside>
      <main style={styles.mapArea}>
        {routes.length > 0 && (
          <Map
            routes={routes}
            selectedRoute={selectedRoute}
            onRouteSelect={setSelectedRoute}
          />
        )}
      </main>
    </div>
  )
}

const styles = {
  layout: {
    display: 'flex',
    height: '100vh',
    fontFamily: 'system-ui, -apple-system, sans-serif',
  },
  sidebar: {
    width: 280,
    padding: '20px 16px',
    display: 'flex',
    flexDirection: 'column',
    gap: 10,
    borderRight: '1px solid #e5e7eb',
    overflowY: 'auto',
    background: '#fafafa',
  },
  mapArea: {
    flex: 1,
  },
  title: {
    margin: 0,
    fontSize: 22,
    fontWeight: 700,
    color: '#111827',
  },
  subtitle: {
    margin: '2px 0 8px',
    fontSize: 13,
    color: '#6b7280',
  },
  cardList: {
    display: 'flex',
    flexDirection: 'column',
    gap: 8,
  },
  centered: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    fontFamily: 'system-ui, sans-serif',
    color: '#6b7280',
  },
}
