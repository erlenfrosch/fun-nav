import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { RouteCard } from './RouteCard'

const mockRoute = {
  id: 'kurvenreich-60',
  duration_min: 60,
  distance_km: 50,
  geometry: { type: 'LineString' as const, coordinates: [] },
}

describe('RouteCard', () => {
  it('renders route label, distance and duration', () => {
    render(<RouteCard route={mockRoute} index={0} isSelected={false} onClick={vi.fn()} />)
    expect(screen.getByText('Route 1')).toBeInTheDocument()
    expect(screen.getByText('50 km')).toBeInTheDocument()
    expect(screen.getByText('60 min')).toBeInTheDocument()
  })

  it('shows second route label for index 1', () => {
    render(<RouteCard route={mockRoute} index={1} isSelected={false} onClick={vi.fn()} />)
    expect(screen.getByText('Route 2')).toBeInTheDocument()
  })

  it('calls onClick when clicked', async () => {
    const user = userEvent.setup()
    const onClick = vi.fn()
    render(<RouteCard route={mockRoute} index={0} isSelected={false} onClick={onClick} />)
    await user.click(screen.getByRole('button'))
    expect(onClick).toHaveBeenCalledOnce()
  })

  it('has aria-pressed=true when selected', () => {
    render(<RouteCard route={mockRoute} index={0} isSelected={true} onClick={vi.fn()} />)
    expect(screen.getByRole('button')).toHaveAttribute('aria-pressed', 'true')
  })

  it('has aria-pressed=false when not selected', () => {
    render(<RouteCard route={mockRoute} index={0} isSelected={false} onClick={vi.fn()} />)
    expect(screen.getByRole('button')).toHaveAttribute('aria-pressed', 'false')
  })
})
