export default function RouteCard({ route, selected, onClick }) {
  const curvinessLabel = route.curviness < 30 ? 'flach' : route.curviness < 60 ? 'hügelig' : 'kurvig'

  return (
    <button
      onClick={() => onClick(route.id)}
      style={{
        width: '100%',
        padding: '12px 16px',
        marginBottom: '10px',
        border: `2px solid ${selected ? route.color : '#e2e8f0'}`,
        borderRadius: '8px',
        background: selected ? `${route.color}18` : '#fff',
        cursor: 'pointer',
        textAlign: 'left',
        transition: 'border-color 0.15s, background 0.15s',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
        <span
          style={{
            display: 'inline-block',
            width: '12px',
            height: '12px',
            borderRadius: '50%',
            background: route.color,
            flexShrink: 0,
          }}
        />
        <strong style={{ fontSize: '14px', color: '#1e293b' }}>{route.label}</strong>
      </div>
      <div style={{ display: 'flex', gap: '16px', fontSize: '13px', color: '#475569' }}>
        <span>⏱ {route.duration} min</span>
        <span>📏 {route.distance.toFixed(1)} km</span>
        <span>〰 {curvinessLabel}</span>
      </div>
    </button>
  )
}
