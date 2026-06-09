import type { RouteOption } from '../api/routes'
import styles from './RouteCard.module.css'

const ROUTE_LABELS = ['Route 1', 'Route 2', 'Route 3']
const ROUTE_COLORS = ['#2563eb', '#22c55e', '#f97316']

interface RouteCardProps {
  route: RouteOption
  index: number
  isSelected: boolean
  onClick: () => void
}

export function RouteCard({ route, index, isSelected, onClick }: RouteCardProps) {
  const label = ROUTE_LABELS[index] ?? `Route ${index + 1}`
  const color = ROUTE_COLORS[index] ?? '#6b7280'

  return (
    <button
      type="button"
      className={`${styles.card} ${isSelected ? styles.selected : ''}`}
      style={{ borderLeftColor: color }}
      onClick={onClick}
      aria-pressed={isSelected}
      aria-label={`${label} auswählen`}
    >
      <span className={styles.label}>{label}</span>
      <span className={styles.stat}>{route.distance_km} km</span>
      <span className={styles.stat}>{route.duration_min} min</span>
    </button>
  )
}
