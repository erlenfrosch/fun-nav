import { formatDistance, formatDuration } from '../utils/format'

const ROUTE_COLORS = ['#3B82F6', '#22C55E', '#F97316']
const ROUTE_LABELS = ['Route A', 'Route B', 'Route C']

function curvinessLabel(score) {
  if (score < 30) return 'flach'
  if (score < 60) return 'hügelig'
  return 'kurvig'
}

export default function RouteCard({ route, index, selected, onSelect }) {
  const color = ROUTE_COLORS[index]
  const curviness = route.curviness_score ?? null
  return (
    <button
      onClick={onSelect}
      style={{
        width: '100%',
        textAlign: 'left',
        border: `2px solid ${selected ? color : '#e5e7eb'}`,
        borderRadius: 8,
        padding: '12px 16px',
        cursor: 'pointer',
        background: selected ? `${color}18` : 'white',
        transition: 'border-color 0.15s, background 0.15s',
        fontFamily: 'inherit',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <span
          aria-hidden="true"
          style={{
            width: 12,
            height: 12,
            borderRadius: '50%',
            background: color,
            flexShrink: 0,
          }}
        />
        <strong style={{ color, fontSize: 14 }}>{ROUTE_LABELS[index]}</strong>
      </div>
      <div style={{ marginTop: 6, fontSize: 13, color: '#374151' }}>
        {formatDistance(route.distance)} · {formatDuration(route.duration)}
        {curviness !== null && (
          <span style={{ marginLeft: 6, color: '#6b7280' }}>
            · {curvinessLabel(curviness)} ({curviness})
          </span>
        )}
      </div>
    </button>
  )
}
