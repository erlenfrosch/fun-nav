import { useState, useCallback } from 'react'
import { fetchCircularRoute, type CircularRouteRequest, type RouteOption } from '../api/routes'

interface RoutingState {
  routes: RouteOption[]
  loading: boolean
  error: string | null
}

interface UseRoutingReturn extends RoutingState {
  calculateRoute: (request: CircularRouteRequest) => Promise<void>
  clearError: () => void
}

export function useRouting(): UseRoutingReturn {
  const [state, setState] = useState<RoutingState>({
    routes: [],
    loading: false,
    error: null,
  })

  const calculateRoute = useCallback(async (request: CircularRouteRequest) => {
    setState({ routes: [], loading: true, error: null })
    try {
      const result = await fetchCircularRoute(request)
      setState({ routes: result.routes, loading: false, error: null })
    } catch (err) {
      setState({
        routes: [],
        loading: false,
        error: err instanceof Error ? err.message : 'Unbekannter Fehler',
      })
    }
  }, [])

  const clearError = useCallback(() => {
    setState(prev => ({ ...prev, error: null }))
  }, [])

  return { ...state, calculateRoute, clearError }
}
