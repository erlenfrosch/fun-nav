export type Curviness = 'kurvenreich' | 'sehr_kurvenreich'

export interface CircularRouteRequest {
  lat: number
  lon: number
  duration_min: number
  curviness: Curviness
}

export interface RouteGeometry {
  type: 'LineString'
  coordinates: number[][]
}

export interface RouteOption {
  id: string
  duration_min: number
  distance_km: number
  geometry: RouteGeometry
}

export interface CircularRouteResponse {
  routes: RouteOption[]
}

const BASE_URL = typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_URL
  ? import.meta.env.VITE_API_URL
  : 'http://localhost:8000'

export async function fetchCircularRoute(
  request: CircularRouteRequest
): Promise<CircularRouteResponse> {
  const response = await fetch(`${BASE_URL}/api/routes/circular`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  })

  if (!response.ok) {
    throw new Error(`API-Fehler: ${response.status}`)
  }

  return response.json() as Promise<CircularRouteResponse>
}
