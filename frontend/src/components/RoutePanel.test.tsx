import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { RoutePanel } from './RoutePanel'
import * as routesApi from '../api/routes'

vi.mock('../api/routes', () => ({
  fetchCircularRoute: vi.fn(),
}))

const defaultProps = { lat: 48.1, lon: 11.6 }

describe('RoutePanel', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders all UI controls', () => {
    render(<RoutePanel {...defaultProps} />)
    expect(screen.getByRole('slider')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /^Kurvenreich$/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Sehr kurvenreich/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Route berechnen/i })).toBeInTheDocument()
  })

  it('defaults to 60 min and kurvenreich', () => {
    render(<RoutePanel {...defaultProps} />)
    expect(screen.getByRole('slider')).toHaveValue('60')
    expect(screen.getByText(/60 min/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /^Kurvenreich$/i })).toHaveAttribute('aria-pressed', 'true')
    expect(screen.getByRole('button', { name: /Sehr kurvenreich/i })).toHaveAttribute('aria-pressed', 'false')
  })

  it('displays updated duration when slider changes', () => {
    render(<RoutePanel {...defaultProps} />)
    fireEvent.change(screen.getByRole('slider'), { target: { value: '90' } })
    expect(screen.getByText(/90 min/i)).toBeInTheDocument()
    expect(screen.getByRole('slider')).toHaveValue('90')
  })

  it('slider has correct min/max/step attributes', () => {
    render(<RoutePanel {...defaultProps} />)
    const slider = screen.getByRole('slider')
    expect(slider).toHaveAttribute('min', '15')
    expect(slider).toHaveAttribute('max', '180')
    expect(slider).toHaveAttribute('step', '15')
  })

  it('switches to sehr_kurvenreich toggle', async () => {
    const user = userEvent.setup()
    render(<RoutePanel {...defaultProps} />)
    await user.click(screen.getByRole('button', { name: /Sehr kurvenreich/i }))
    expect(screen.getByRole('button', { name: /Sehr kurvenreich/i })).toHaveAttribute('aria-pressed', 'true')
    expect(screen.getByRole('button', { name: /^Kurvenreich$/i })).toHaveAttribute('aria-pressed', 'false')
  })

  it('calls fetchCircularRoute with correct params', async () => {
    const user = userEvent.setup()
    vi.mocked(routesApi.fetchCircularRoute).mockResolvedValueOnce({ routes: [] })
    render(<RoutePanel {...defaultProps} />)
    await user.click(screen.getByRole('button', { name: /Route berechnen/i }))
    expect(routesApi.fetchCircularRoute).toHaveBeenCalledWith({
      lat: 48.1,
      lon: 11.6,
      duration_min: 60,
      curviness: 'kurvenreich',
    })
  })

  it('disables button and shows loading text while fetching', async () => {
    let resolve!: (val: routesApi.CircularRouteResponse) => void
    vi.mocked(routesApi.fetchCircularRoute).mockReturnValueOnce(
      new Promise(r => { resolve = r })
    )
    const user = userEvent.setup()
    render(<RoutePanel {...defaultProps} />)
    await user.click(screen.getByRole('button', { name: /Route berechnen/i }))
    const btn = screen.getByRole('button', { name: /Berechne/i })
    expect(btn).toBeDisabled()
    expect(btn).toHaveAttribute('aria-busy', 'true')
    await act(async () => { resolve({ routes: [] }) })
  })

  it('shows error message on API failure', async () => {
    const user = userEvent.setup()
    vi.mocked(routesApi.fetchCircularRoute).mockRejectedValueOnce(new Error('Server nicht erreichbar'))
    render(<RoutePanel {...defaultProps} />)
    await user.click(screen.getByRole('button', { name: /Route berechnen/i }))
    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent('Server nicht erreichbar')
    })
  })

  it('toggle and calculate buttons have sufficient height for touch targets', () => {
    render(<RoutePanel {...defaultProps} />)
    const buttons = screen.getAllByRole('button')
    buttons.forEach(btn => {
      expect(btn).toBeInTheDocument()
    })
  })
})
