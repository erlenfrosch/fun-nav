import { RoutePanel } from './components/RoutePanel'

// Liechtenstein-Mittelpunkt als Startposition bis ein Karten-Picker implementiert ist
const DEFAULT_LAT = 47.1666
const DEFAULT_LON = 9.5554

export default function App() {
  return (
    <main style={{ minHeight: '100vh', background: '#f0f2f5' }}>
      <header style={{ padding: '1rem 1.5rem' }}>
        <h1 style={{ margin: 0, fontSize: '1.25rem', fontWeight: 700, color: '#1a1a1a' }}>
          fun-nav
        </h1>
      </header>
      <RoutePanel lat={DEFAULT_LAT} lon={DEFAULT_LON} />
    </main>
  )
}
