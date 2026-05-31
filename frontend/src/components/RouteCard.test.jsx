import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import RouteCard from './RouteCard'

const mockRoute = { distance: 8750, duration: 1050 }

describe('RouteCard', () => {
  it('renders route label', () => {
    render(<RouteCard route={mockRoute} index={0} selected={false} onSelect={() => {}} />)
    expect(screen.getByText('Route A')).toBeTruthy()
  })

  it('renders distance and duration', () => {
    render(<RouteCard route={mockRoute} index={0} selected={false} onSelect={() => {}} />)
    expect(screen.getByText(/8\.8 km/)).toBeTruthy()
    expect(screen.getByText(/18 min/)).toBeTruthy()
  })

  it('calls onSelect on click', () => {
    const onSelect = vi.fn()
    render(<RouteCard route={mockRoute} index={1} selected={false} onSelect={onSelect} />)
    fireEvent.click(screen.getByRole('button'))
    expect(onSelect).toHaveBeenCalledOnce()
  })

  it('highlights border when selected', () => {
    const { container } = render(
      <RouteCard route={mockRoute} index={1} selected={true} onSelect={() => {}} />
    )
    const btn = container.querySelector('button')
    // jsdom normalizes hex → rgb(34, 197, 94) for #22C55E
    expect(btn.style.border).toContain('rgb(34, 197, 94)')
  })
})
