import math

import pytest

from app.services.circular_route import _waypoints_on_circle, EARTH_RADIUS_KM


def test_waypoints_count():
    wps = _waypoints_on_circle(48.137, 11.575, radius_km=10.0, n=8)
    assert len(wps) == 8


def test_waypoints_approximately_on_circle():
    lat, lon, radius_km = 48.137, 11.575, 20.0
    wps = _waypoints_on_circle(lat, lon, radius_km, n=8)
    lat_rad = math.radians(lat)
    for wp_lat, wp_lon in wps:
        dlat = math.radians(wp_lat - lat) * EARTH_RADIUS_KM
        dlon = math.radians(wp_lon - lon) * EARTH_RADIUS_KM * math.cos(lat_rad)
        dist = math.sqrt(dlat**2 + dlon**2)
        assert abs(dist - radius_km) < 0.5, f"Waypoint distance {dist:.2f} km deviates from {radius_km} km"


def test_opposing_waypoints_are_symmetric():
    wps = _waypoints_on_circle(48.137, 11.575, radius_km=15.0, n=8)
    lat, lon = 48.137, 11.575
    for i in range(4):
        wp_a = wps[i]
        wp_b = wps[i + 4]
        mid_lat = (wp_a[0] + wp_b[0]) / 2
        mid_lon = (wp_a[1] + wp_b[1]) / 2
        assert abs(mid_lat - lat) < 0.01
        assert abs(mid_lon - lon) < 0.01
