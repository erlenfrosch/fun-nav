import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useRouting } from './useRouting'
import * as routesApi from '../api/routes'

vi.mock('../api/routes', () => ({
  fetchCircularRoute: vi.fn(),
}))

const request = {
  lat: 48.1,
  lon: 11.6,
  duration_min: 60,
  curviness: 'kurvenreich' as const,
}

const mockRoute = {
  id: '1',
  duration_min: 60,
  distance_km: 50,
  geometry: { type: 'LineString' as const, coordinates: [] },
}

describe('useRouting', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('initializes with empty routes, not loading, no error', () => {
    const { result } = renderHook(() => useRouting())
    expect(result.current.routes).toEqual([])
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBeNull()
  })

  it('sets loading=true while fetching', async () => {
    let resolve!: (val: routesApi.CircularRouteResponse) => void
    vi.mocked(routesApi.fetchCircularRoute).mockReturnValueOnce(
      new Promise(r => { resolve = r })
    )
    const { result } = renderHook(() => useRouting())
    act(() => { void result.current.calculateRoute(request) })
    expect(result.current.loading).toBe(true)
    await act(async () => { resolve({ routes: [] }) })
    expect(result.current.loading).toBe(false)
  })

  it('populates routes on success', async () => {
    vi.mocked(routesApi.fetchCircularRoute).mockResolvedValueOnce({ routes: [mockRoute] })
    const { result } = renderHook(() => useRouting())
    await act(async () => { await result.current.calculateRoute(request) })
    expect(result.current.routes).toEqual([mockRoute])
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBeNull()
  })

  it('clears previous routes before new fetch', async () => {
    vi.mocked(routesApi.fetchCircularRoute)
      .mockResolvedValueOnce({ routes: [mockRoute] })
      .mockReturnValueOnce(new Promise(() => {}))
    const { result } = renderHook(() => useRouting())
    await act(async () => { await result.current.calculateRoute(request) })
    expect(result.current.routes).toHaveLength(1)
    act(() => { void result.current.calculateRoute(request) })
    expect(result.current.routes).toEqual([])
  })

  it('sets error message on API failure', async () => {
    vi.mocked(routesApi.fetchCircularRoute).mockRejectedValueOnce(new Error('Netzwerkfehler'))
    const { result } = renderHook(() => useRouting())
    await act(async () => { await result.current.calculateRoute(request) })
    expect(result.current.error).toBe('Netzwerkfehler')
    expect(result.current.loading).toBe(false)
    expect(result.current.routes).toEqual([])
  })

  it('handles non-Error throws gracefully', async () => {
    vi.mocked(routesApi.fetchCircularRoute).mockRejectedValueOnce('string error')
    const { result } = renderHook(() => useRouting())
    await act(async () => { await result.current.calculateRoute(request) })
    expect(result.current.error).toBe('Unbekannter Fehler')
  })

  it('clearError resets error to null', async () => {
    vi.mocked(routesApi.fetchCircularRoute).mockRejectedValueOnce(new Error('Fehler'))
    const { result } = renderHook(() => useRouting())
    await act(async () => { await result.current.calculateRoute(request) })
    expect(result.current.error).toBeTruthy()
    act(() => { result.current.clearError() })
    expect(result.current.error).toBeNull()
  })
})
