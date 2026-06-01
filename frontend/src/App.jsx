import { useState } from 'react'
import RouteForm from './RouteForm'
import RouteInfo from './RouteInfo'
import RouteMap from './RouteMap'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export default function App() {
  const [routes, setRoutes] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(params) {
    setLoading(true)
    setError(null)
    try {
      const query = new URLSearchParams(params).toString()
      const res = await fetch(`${API_URL}/routes?${query}`)
      if (!res.ok) {
        const body = await res.json().catch(() => ({}))
        throw new Error(body.detail ?? `HTTP ${res.status}`)
      }
      const data = await res.json()
      setRoutes(data.routes)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main style={{ fontFamily: 'sans-serif', maxWidth: '900px', margin: '0 auto', padding: '1rem' }}>
      <h1 style={{ marginBottom: '0.75rem' }}>fun-nav</h1>
      <RouteForm onSubmit={handleSubmit} loading={loading} />
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <RouteInfo routes={routes} />
      <RouteMap routes={routes} />
    </main>
  )
}
