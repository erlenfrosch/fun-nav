import { describe, it, expect, vi } from 'vitest'
import { render } from '@testing-library/react'
import { RouteMap } from './Map'

vi.mock('react-map-gl/maplibre', () => ({
  default: ({ children, ...props }: React.PropsWithChildren<object>) => (
    <div data-testid="maplibre-map" {...(props as object)}>{children}</div>
  ),
  Source: ({ children }: React.PropsWithChildren<object>) => <>{children}</>,
  Layer: () => null,
}))

vi.mock('maplibre-gl/dist/maplibre-gl.css', () => ({}))

const mockRoutes = [
  {
    id: 'route-1',
    duration_min: 60,
    distance_km: 50,
    geometry: { type: 'LineString' as const, coordinates: [[9.5, 47.1], [9.6, 47.2]] },
  },
  {
    id: 'route-2',
    duration_min: 55,
    distance_km: 45,
    geometry: { type: 'LineString' as const, coordinates: [[9.5, 47.1], [9.55, 47.25]] },
  },
]

describe('RouteMap', () => {
  it('renders the map container', () => {
    const { getByTestId } = render(
      <RouteMap routes={[]} selectedIndex={0} onRouteSelect={vi.fn()} />
    )
    expect(getByTestId('maplibre-map')).toBeInTheDocument()
  })

  it('renders without errors when routes provided', () => {
    expect(() =>
      render(<RouteMap routes={mockRoutes} selectedIndex={0} onRouteSelect={vi.fn()} />)
    ).not.toThrow()
  })

  it('renders without errors when selectedIndex changes', () => {
    const { rerender } = render(
      <RouteMap routes={mockRoutes} selectedIndex={0} onRouteSelect={vi.fn()} />
    )
    expect(() =>
      rerender(<RouteMap routes={mockRoutes} selectedIndex={1} onRouteSelect={vi.fn()} />)
    ).not.toThrow()
  })
})
