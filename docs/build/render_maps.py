"""Rend toutes les cartes du briefing dans docs/maps-hd/ (deck, PDF, DCS) et docs/build/kneeboard/ (planchettes)."""
import math
from pathlib import Path

from maps import BLUE, DARK, ORANGE, RED, View, inset_map
from data import (BASES, BULLSEYE, COLONNE_ROUTE, FRIENDLIES, FRONT_LINE, HELOS, HELOS_FROM, JETS, JTAC,
                  OBJECTIVES, POUSSEE_ROUTE, QRA, RED_BASES, SAMS, SUPPORT)

OUT = Path(__file__).parent.parent / "maps-hd"
OUT.mkdir(exist_ok=True)
GREEN = (0, 130, 60)
SHORAD = [("SA-15", -202500, -5500, 12000), ("SA-8", -191200, 7600, 10300)]  # portées DCS (ThreatRange)


def common(v, detail):
    """Superpositions communes à la sitac générale et à la carte du front."""
    for name, x, y, rng in QRA:
        v.circle((x, y), rng, ORANGE, width=3, dash=(18, 14))
    for name, x, y, rng, det in SAMS:
        v.circle((x, y), rng, RED, width=5, fill=None if detail else (220, 0, 0, 14))
        if det:
            v.circle((x, y), det, RED, width=3, dash=(22, 16))
    if detail:
        for name, x, y, rng in SHORAD:
            v.circle((x, y), rng, RED, width=3, dash=(14, 10))
    v.line(FRONT_LINE, RED, width=7)
    helo = [HELOS_FROM[1:]] + [(h[1], h[2]) for h in HELOS[:4]]
    v.line(helo, GREEN, width=6, dash=(26, 14))
    if detail:
        v.line(COLONNE_ROUTE, RED, width=5, dash=(20, 12))
        v.line(POUSSEE_ROUTE, BLUE, width=5, dash=(20, 12))


def overview():
    v = View((-220000, -22000), 11, 3000, 1690, rot=36, up=1.25)
    common(v, detail=False)
    for name, a, b, lab in SUPPORT:
        v.line([a, b], BLUE, width=6)
        v.label(*b, lab, BLUE, size=22, dx=14, dy=10)
    v.line([JETS[0][1:3], JETS[1][1:3]], BLUE, width=4, dash=(16, 12))
    v.line([JETS[-2][1:3], (BASES["Ramat David"])], BLUE, width=4, dash=(16, 12))
    for name, p in BASES.items():
        v.marker(*p, BLUE, "square", 13)
        v.label(*p, name, BLUE, size=26)
    for name, p in RED_BASES.items():
        v.marker(*p, RED, "square", 11)
        v.label(*p, name, RED, size=22)
    for i, (name, x, y, *_rest) in enumerate(JETS[:-1], start=1):
        if name in ("PUSH", "EGRESS", "TELLHARA"):
            v.marker(x, y, BLUE, "dot", 9)
            v.label(x, y, f"W{i} {name}", BLUE, size=22, dx=14, dy=-12)
    offs = {"KHAN": (-16, -12), "SASA": (-16, -16), "SA6": (16, -16), "KANAKER": (16, 34),
            "KISWAH": (16, 30), "SA11": (16, -16), "TELLHARA": (16, -12)}
    for zone, title, wp, c, r, targets in OBJECTIVES:
        v.marker(*c, RED, "diamond", 12)
        dx, dy = offs[wp]
        v.label(*c, wp, RED, size=22, dx=dx, dy=dy)
    for name, x, y, rng in QRA:
        v.label(x + rng * 0.72, y - rng * 0.72, name, ORANGE, size=20, dx=0, dy=0)
    v.marker(*BULLSEYE, DARK, "cross", 9)
    v.label(*BULLSEYE, "Bullseye (Quneitra)", DARK, size=20, dx=-24, dy=30)
    v.marker(*HELOS[0][1:3], GREEN, "dot", 9)
    v.label(*HELOS[0][1:3], "MASADA (attente hélicos)", GREEN, size=20, dx=-16, dy=-14)
    legend = [(("square", BLUE), "Base de départ / alliée"), (("dot", BLUE), "Point du plan de vol"),
              (("line", BLUE), "Ravitailleurs et AWACS"), (("dash", GREEN), "Route des hélicoptères"),
              (("line", RED), "Ligne de contact"), (("ring", RED), "SAM : tir (plein), détection (tirets)"),
              (("dash", ORANGE), "Zone de réaction des QRA"), (("dot", RED), "Objectif")]
    img = v.render(scale_nm=10, legend=legend, title="Situation tactique générale", legend_right=True)
    img.save(OUT / "sitac-generale.png", optimize=True)
    return v


def front():
    v = View((-194000, 10500), 12, 3000, 1690, rot=30, up=1.5)
    common(v, detail=True)
    for zone, title, wp, c, r, targets in OBJECTIVES:
        v.circle(c, r, RED, width=3, dash=(10, 8))
        for t in targets:
            v.marker(t[2], t[3], RED, "dot", 7)
        v.label(*c, title, RED, size=24, dx=-20 if zone in ("Kiswah", "SA11Kiswah") else 18,
                dy=40 if zone == "SA11Kiswah" else -20)
    for name, x, y in FRIENDLIES:
        v.marker(x, y, BLUE, "square", 9)
    v.label(*FRIENDLIES[0][1:], "Brigade alliée", BLUE, size=22, dx=-16, dy=-18)
    v.marker(*JTAC[1:], BLUE, "triangle", 12)
    v.label(*JTAC[1:], "JTAC Abu Nada", BLUE, size=22, dx=16, dy=32)
    for i, (name, x, y, *_r) in enumerate(HELOS[:-1], start=1):
        if name in ("MASADA", "HADAR", "BEITJINN"):
            v.marker(x, y, GREEN, "dot", 9)
            v.label(x, y, f"H{i} {name}", GREEN, size=22, dx=-16, dy=-14)
    v.label(*COLONNE_ROUTE[1], "Route Quneitra - Sa'sa' : axe de la poussée alliée, et d'une contre-attaque probable", DARK, size=20, dx=18, dy=44)
    for name, x, y, rng, det in SAMS[:1]:
        v.label(x, y, "SA-6 (≈ 24 km)", RED, size=20, dx=18, dy=46)
    for name, x, y, rng in SHORAD:
        v.label(x, y, f"{name} ({rng / 1000:.0f} km)", RED, size=18, dx=-16, dy=46)
    v.marker(*BULLSEYE, DARK, "cross", 9)
    v.label(*BULLSEYE, "Bullseye", DARK, size=20, dx=-24, dy=30)
    legend = [(("square", BLUE), "Unités alliées"), (("dot", RED), "Cible connue"),
              (("dash", GREEN), "Route des hélicoptères"), (("dash", BLUE), "Axe de la poussée alliée"),
              (("dash", RED), "Axe probable d'une contre-attaque"), (("ring", RED), "SAM : portée de tir"),
              (("dash", ORANGE), "Zone de réaction des QRA")]
    img = v.render(scale_km=5, legend=legend, title="Zone des combats : du Golan à Kiswah", legend_right=True)
    img.save(OUT / "sitac-front.png", optimize=True)
    return v


def pick_zoom(width_m, w, lat_cos=0.838):
    """Le zoom le plus bas dont la tuile, suréchantillonnée au plus × 2, donne la résolution voulue."""
    target = width_m / w
    for z in range(9, 18):
        up = 156543.03392 * lat_cos / 2**z / target
        if up <= 2.0:
            return z, up
    return 17, 1.0


def objective(zone, title, wp, c, r, targets):
    w, h = 2400, 1350
    width_m = max(r * 3.4, 3200)
    z, up = pick_zoom(width_m, w)
    v = View(c, z, w, h, rot=0, up=up)
    v.circle(c, r, RED, width=4, fill=(220, 0, 0, 22))
    for name, kind, x, y, role in targets:
        v.marker(x, y, RED, "dot", 11)
        v.label(x, y, name, RED, size=26, dx=16, dy=-12)
    inset = inset_map(c, width_m / 2)
    scale = 1 if width_m < 6000 else 2
    img = v.render(scale_km=scale, inset=inset, title=f"{wp} — {title}")
    img.save(OUT / f"objectif-{zone.lower()}.png", optimize=True)
    # vignettes des cibles, recadrées dans la carte rendue
    for i, (name, kind, x, y, role) in enumerate(targets):
        px, py = v.out_xy(x, y)
        s = 260
        crop = img.crop((int(px - s), int(py - s), int(px + s), int(py + s)))
        crop.save(OUT / f"cible-{zone.lower()}-{i}.png", optimize=True)


if __name__ == "__main__":
    overview()
    print("sitac générale ok")
    front()
    print("front ok")
    for o in OBJECTIVES:
        objective(*o)
        print(o[0], "ok")
