import { describe, it, expect } from 'vitest'
import { formatDistance, formatDuration } from './format'

describe('formatDistance', () => {
  it('formats meters below 1000', () => {
    expect(formatDistance(750)).toBe('750 m')
  })

  it('formats kilometers', () => {
    expect(formatDistance(8750)).toBe('8.8 km')
  })

  it('formats exactly 1000 m as km', () => {
    expect(formatDistance(1000)).toBe('1.0 km')
  })
})

describe('formatDuration', () => {
  it('formats minutes under one hour', () => {
    expect(formatDuration(1050)).toBe('18 min')
  })

  it('formats hours and minutes', () => {
    expect(formatDuration(3900)).toBe('1 h 5 min')
  })

  it('formats exact hours without minutes', () => {
    expect(formatDuration(3600)).toBe('1 h')
  })
})
