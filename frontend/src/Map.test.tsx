import { describe, it, expect, vi } from 'vitest'
import { render } from '@testing-library/react'
import MapView from './Map'

vi.mock('react-map-gl/maplibre', () => ({
  default: ({ style }: { style: React.CSSProperties }) => (
    <div data-testid="map-container" style={style} />
  ),
}))

vi.mock('maplibre-gl/dist/maplibre-gl.css', () => ({}))

describe('MapView', () => {
  it('rendert einen Map-Container', () => {
    const { getByTestId } = render(<MapView />)
    expect(getByTestId('map-container')).toBeTruthy()
  })

  it('setzt vollbild-Styles', () => {
    const { getByTestId } = render(<MapView />)
    const el = getByTestId('map-container')
    expect(el.style.width).toBe('100%')
    expect(el.style.height).toBe('100%')
  })
})
