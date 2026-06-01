import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render } from '@testing-library/react'
import Map from './Map'

const mockRemove = vi.fn()
const mockMapInstance = { remove: mockRemove, on: vi.fn() }

vi.mock('maplibre-gl', () => ({
  Map: vi.fn(() => mockMapInstance),
}))

vi.mock('maplibre-gl/dist/maplibre-gl.css', () => ({}))

describe('Map', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('rendert einen Container-div', () => {
    const { container } = render(<Map />)
    expect(container.querySelector('div')).toBeTruthy()
  })

  it('initialisiert MapLibre mit center und zoom', async () => {
    const { Map: MapLibreMock } = await import('maplibre-gl')
    render(<Map center={[9.5, 47.14]} zoom={10} />)
    expect(MapLibreMock).toHaveBeenCalledWith(
      expect.objectContaining({ center: [9.5, 47.14], zoom: 10 }),
    )
  })

  it('übergibt den style-Parameter', async () => {
    const { Map: MapLibreMock } = await import('maplibre-gl')
    const style = 'https://demotiles.maplibre.org/style.json'
    render(<Map style={style} />)
    expect(MapLibreMock).toHaveBeenCalledWith(
      expect.objectContaining({ style }),
    )
  })

  it('ruft map.remove() beim Unmount auf', () => {
    const { unmount } = render(<Map />)
    unmount()
    expect(mockRemove).toHaveBeenCalledOnce()
  })
})
