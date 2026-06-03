import { useState } from 'react'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function RoundTripForm() {
  const [form, setForm] = useState({
    lat: '',
    lng: '',
    distance: 10000,
    profile: 'bike',
    seed: 0,
  })
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  function set(key) {
    return e => setForm(f => ({ ...f, [key]: e.target.value }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const resp = await fetch(`${API}/api/round-trip`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          lat: parseFloat(form.lat),
          lng: parseFloat(form.lng),
          distance: parseInt(form.distance),
          profile: form.profile,
          seed: parseInt(form.seed),
        }),
      })
      if (!resp.ok) {
        const err = await resp.json()
        throw new Error(err.detail || `HTTP ${resp.status}`)
      }
      setResult(await resp.json())
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section>
      <h2>Rundrouten-Generator</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Breitengrad
          <input type="number" step="any" value={form.lat} onChange={set('lat')} required />
        </label>
        <label>
          Längengrad
          <input type="number" step="any" value={form.lng} onChange={set('lng')} required />
        </label>
        <label>
          Distanz (m)
          <input type="number" min="1000" max="100000" value={form.distance} onChange={set('distance')} />
        </label>
        <label>
          Profil
          <select value={form.profile} onChange={set('profile')}>
            <option value="bike">Fahrrad</option>
            <option value="foot">Zu Fuß</option>
            <option value="car">Auto</option>
          </select>
        </label>
        <label>
          Zufallssamen
          <input type="number" value={form.seed} onChange={set('seed')} />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? 'Berechne…' : 'Route generieren'}
        </button>
      </form>
      {error && <p role="alert" style={{ color: 'red' }}>{error}</p>}
      {result && (
        <div>
          <p>Distanz: {(result.distance / 1000).toFixed(1)} km</p>
          <p>Dauer: {Math.round(result.time / 60000)} min</p>
          <p>Wegpunkte: {result.points.coordinates.length}</p>
        </div>
      )}
    </section>
  )
}
