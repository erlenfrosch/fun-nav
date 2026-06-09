import { useState } from 'react'
import { useRouting } from '../hooks/useRouting'
import type { Curviness } from '../api/routes'
import styles from './RoutePanel.module.css'

const DURATION_MIN = 15
const DURATION_MAX = 180
const DURATION_STEP = 15
const DURATION_DEFAULT = 60

interface RoutePanelProps {
  lat: number
  lon: number
}

export function RoutePanel({ lat, lon }: RoutePanelProps) {
  const [duration, setDuration] = useState(DURATION_DEFAULT)
  const [curviness, setCurviness] = useState<Curviness>('kurvenreich')
  const { loading, error, calculateRoute } = useRouting()

  const handleCalculate = () => {
    void calculateRoute({ lat, lon, duration_min: duration, curviness })
  }

  return (
    <div className={styles.panel}>
      <h2 className={styles.title}>Route planen</h2>

      <div className={styles.field}>
        <label className={styles.label} htmlFor="duration-slider">
          Fahrtzeit: <strong>{duration} min</strong>
        </label>
        <input
          id="duration-slider"
          type="range"
          min={DURATION_MIN}
          max={DURATION_MAX}
          step={DURATION_STEP}
          value={duration}
          onChange={e => setDuration(Number(e.target.value))}
          className={styles.slider}
          aria-label={`Fahrtzeit ${duration} Minuten`}
          aria-valuemin={DURATION_MIN}
          aria-valuemax={DURATION_MAX}
          aria-valuenow={duration}
        />
        <div className={styles.sliderMarks} aria-hidden="true">
          <span>15 min</span>
          <span>180 min</span>
        </div>
      </div>

      <div className={styles.field}>
        <span className={styles.label}>Kurvigkeit</span>
        <div className={styles.toggle} role="group" aria-label="Kurvigkeit wählen">
          <button
            type="button"
            className={`${styles.toggleButton}${curviness === 'kurvenreich' ? ` ${styles.active}` : ''}`}
            onClick={() => setCurviness('kurvenreich')}
            aria-pressed={curviness === 'kurvenreich'}
          >
            Kurvenreich
          </button>
          <button
            type="button"
            className={`${styles.toggleButton}${curviness === 'sehr_kurvenreich' ? ` ${styles.active}` : ''}`}
            onClick={() => setCurviness('sehr_kurvenreich')}
            aria-pressed={curviness === 'sehr_kurvenreich'}
          >
            Sehr kurvenreich
          </button>
        </div>
      </div>

      {error && (
        <div className={styles.error} role="alert">
          {error}
        </div>
      )}

      <button
        type="button"
        className={styles.calculateButton}
        onClick={handleCalculate}
        disabled={loading}
        aria-busy={loading}
      >
        {loading ? (
          <>
            <span className={styles.spinner} aria-hidden="true" />
            Berechne...
          </>
        ) : (
          'Route berechnen'
        )}
      </button>
    </div>
  )
}
