const ROUTE_COLORS = ['#2563eb', '#ea580c', '#16a34a']
const ROUTE_LABELS = ['Hauptroute', 'Alternative 1', 'Alternative 2']

function formatDist(m) {
  return m >= 1000 ? `${(m / 1000).toFixed(1)} km` : `${Math.round(m)} m`
}

function formatDur(ms) {
  const min = Math.round(ms / 60000)
  return min >= 60 ? `${Math.floor(min / 60)} h ${min % 60} min` : `${min} min`
}

export default function RouteInfo({ routes }) {
  if (routes.length === 0) return null

  return (
    <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap', margin: '0.5rem 0' }}>
      {routes.map((route, i) => (
        <div
          key={i}
          style={{
            borderLeft: `4px solid ${ROUTE_COLORS[i] ?? '#6b7280'}`,
            paddingLeft: '0.5rem',
          }}
        >
          <strong>{ROUTE_LABELS[i] ?? `Route ${i + 1}`}</strong>
          <br />
          {formatDist(route.distance_m)} · {formatDur(route.duration_ms)}
        </div>
      ))}
    </div>
  )
}
