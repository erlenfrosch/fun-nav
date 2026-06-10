import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

vi.mock('./components/Map', () => ({
  RouteMap: () => <div data-testid="route-map" />,
}))

vi.mock('./components/RoutePanel', () => ({
  RoutePanel: ({ onRoutesCalculated }: { onRoutesCalculated?: (r: unknown[]) => void }) => (
    <div data-testid="route-panel" onClick={() => onRoutesCalculated?.([])} />
  ),
}))

vi.mock('./components/RouteCard', () => ({
  RouteCard: () => <div data-testid="route-card" />,
}))

describe('App', () => {
  it('renders app title', () => {
    render(<App />)
    expect(screen.getByRole('heading', { name: 'fun-nav' })).toBeInTheDocument()
  })

  it('renders map and route panel', () => {
    render(<App />)
    expect(screen.getByTestId('route-map')).toBeInTheDocument()
    expect(screen.getByTestId('route-panel')).toBeInTheDocument()
  })
})
