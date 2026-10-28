"""Projection DCS Syria (Mercator transverse) et Web Mercator, sans dépendance externe."""
import math
A = 6378137.0
F = 1 / 298.257223563
E2 = F * (2 - F)
K0, LON0, X0, Y0 = 0.9996, math.radians(39.0), 282801.00000003, -3879865.00000136


def _tm(lat, lon):
    """Forward TM (Snyder): renvoie (easting, northing)."""
    phi, lam = math.radians(lat), math.radians(lon)
    ep2 = E2 / (1 - E2)
    n = A / math.sqrt(1 - E2 * math.sin(phi) ** 2)
    t = math.tan(phi) ** 2
    c = ep2 * math.cos(phi) ** 2
    a = math.cos(phi) * (lam - LON0)
    m = A * ((1 - E2 / 4 - 3 * E2**2 / 64 - 5 * E2**3 / 256) * phi
             - (3 * E2 / 8 + 3 * E2**2 / 32 + 45 * E2**3 / 1024) * math.sin(2 * phi)
             + (15 * E2**2 / 256 + 45 * E2**3 / 1024) * math.sin(4 * phi)
             - (35 * E2**3 / 3072) * math.sin(6 * phi))
    east = K0 * n * (a + (1 - t + c) * a**3 / 6 + (5 - 18 * t + t * t + 72 * c - 58 * ep2) * a**5 / 120)
    north = K0 * (m + n * math.tan(phi) * (a * a / 2 + (5 - t + 9 * c + 4 * c * c) * a**4 / 24
                                           + (61 - 58 * t + t * t + 600 * c - 330 * ep2) * a**6 / 720))
    return east, north


def latlon_to_dcs(lat, lon):
    e, n = _tm(lat, lon)
    return n + Y0 - 1.0, e + X0  # DCS x (nord), y (est) ; constantes calées sur resolve_coordinates


def dcs_to_latlon(x, y):
    """Inverse numérique (Newton sur la projection directe)."""
    lat, lon = 33.0, 36.0
    for _ in range(30):
        x0, y0 = latlon_to_dcs(lat, lon)
        dx, dy = x - x0, y - y0
        if abs(dx) < 0.01 and abs(dy) < 0.01:
            break
        lat += dx / 111000.0
        lon += dy / (111000.0 * math.cos(math.radians(lat)))
    return lat, lon


def merc(lat, lon, z):
    """Pixel Web Mercator au zoom z (tuiles 256 px)."""
    s = 256 * 2**z
    px = (lon + 180) / 360 * s
    py = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * s
    return px, py


def to_dms(v, pos, neg):
    h = pos if v >= 0 else neg
    v = abs(v)
    d = int(v)
    m = int((v - d) * 60)
    s = ((v - d) * 60 - m) * 60
    return f"{h}{d:02d}°{m:02d}'{s:05.2f}\""
