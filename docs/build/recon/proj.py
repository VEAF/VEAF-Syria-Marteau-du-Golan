"""Projection d'un point DCS (x nord, y est, alt) dans une prise, d'après les métadonnées de la caméra."""
import json, math


def project(meta, x, z, alt, hfov):
    cx, cy, cz = meta["cam"]
    d = (x - cx, alt - cy, z - cz)
    dot = lambda a, b: sum(i * j for i, j in zip(a, b))
    xc, yc, zc = dot(d, meta["right"]), dot(d, meta["up"]), dot(d, meta["fwd"])
    w, h = meta["size"][0], meta["size"][1] + 24  # la barre F11 retirée était en bas : le centre optique est celui de la fenêtre entière
    f = (w / 2) / math.tan(math.radians(hfov) / 2)
    return w / 2 + f * xc / zc, h / 2 - f * yc / zc
