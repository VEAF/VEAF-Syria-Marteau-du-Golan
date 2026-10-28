"""Transforme les captures DCS en photos de reconnaissance annotées : docs/recon/<prise>.jpg."""
import json
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

sys.path.insert(0, str(Path(__file__).parent.parent))
from geo import dcs_to_latlon, to_dms  # noqa: E402
from proj import project  # noqa: E402
from shots import SHOTS  # noqa: E402

RAW = Path(__file__).parent / "raw"
OUT = Path(__file__).parent.parent.parent / "recon"
OUT.mkdir(exist_ok=True)
HFOV = 80  # calé sur la prise du SA-11 : six véhicules à quelques pixels de leur projection
F = "C:/Windows/Fonts/consola.ttf"
FB = "C:/Windows/Fonts/consolab.ttf"
YEL = (255, 220, 40)

UNIT_LABEL = {"Kub 1S91 str": "RADAR 1S91", "Kub 2P25 ln": "TEL", "SA-11 Buk SR 9S18M1": "RADAR 9S18",
              "SA-11 Buk CC 9S470M1": "PC", "SA-11 Buk LN 9A310M1": "TEL", "55G6 EWR": "RADAR 55G6"}
GROUP_LABEL = [("SA15", "SA-15"), ("SA13", "SA-13"), ("SA8", "SA-8"), ("SA19", "SA-19"), ("Air Defense", "AAA"),
               ("Armored Platoon", "BLINDÉS"), ("bmp", "BMP-2"), ("t72", "T-72"), ("2s1", "OBUSIERS 2S1"),
               ("grad", "BM-21"), ("SA6Sasa", None), ("SA11Kiswah", None), ("EWRTellHara-radar", None)]


def font(size, bold=False):
    return ImageFont.truetype(FB if bold else F, size)


def recce_look(img):
    g = ImageOps.grayscale(img)
    g = ImageOps.autocontrast(g, cutoff=1)
    g = g.filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))
    w, h = g.size
    random.seed(7)
    noise = Image.effect_noise((w, h), 22).filter(ImageFilter.GaussianBlur(0.6))
    g = Image.blend(g, noise, 0.10)
    # vignettage
    vig = Image.radial_gradient("L").resize((w, h)).point(lambda v: 255 - int(v * 0.55))
    g = Image.composite(g, Image.new("L", (w, h), 0), vig)
    tint = ImageOps.colorize(g, black=(12, 14, 10), white=(236, 232, 214))
    return tint


def label_for(group):
    for key, lab in GROUP_LABEL:
        if key in group:
            return lab
    return "CIBLE"


HAND = "C:/Windows/Fonts/Inkfree.ttf"
RED = (205, 22, 22)


def felt_ring(d, cx, cy, r, rng):
    """Une boucle au feutre : ellipse irrégulière, qui déborde un peu de son point de départ."""
    rx, ry = r * rng.uniform(1.05, 1.3), r * rng.uniform(0.75, 0.95)
    rot = rng.uniform(-0.5, 0.5)
    p1, p2 = rng.uniform(0, 6.3), rng.uniform(0, 6.3)
    start = rng.uniform(0, 6.3)
    pts = []
    n = 90
    for i in range(n + 1):
        a = start + (2 * math.pi + rng.uniform(0.25, 0.55)) * i / n
        k = 1 + 0.07 * math.sin(2 * a + p1) + 0.04 * math.sin(3 * a + p2) + 0.06 * i / n
        x, y = rx * k * math.cos(a), ry * k * math.sin(a)
        pts.append((cx + x * math.cos(rot) - y * math.sin(rot) + rng.uniform(-1, 1),
                    cy + x * math.sin(rot) + y * math.cos(rot) + rng.uniform(-1, 1)))
    for i in range(len(pts) - 1):
        wdt = int(5 + 3 * math.sin(math.pi * i / len(pts)))  # le feutre appuie au milieu du geste
        d.line([pts[i], pts[i + 1]], fill=RED, width=wdt)
    return rx, ry


def felt_label(d, x0, y0, x1, y1, text, rng, fnt):
    """Un trait tremblé vers l'étiquette, puis le texte manuscrit."""
    steps = 12
    prev = (x0, y0)
    for i in range(1, steps + 1):
        t_ = i / steps
        bend = math.sin(math.pi * t_) * rng.uniform(-14, 14)
        cur = (x0 + (x1 - x0) * t_ + bend, y0 + (y1 - y0) * t_ + rng.uniform(-2, 2))
        d.line([prev, cur], fill=RED, width=5)
        prev = cur
    tw = d.textlength(text, font=fnt)
    tx = x1 + 8 if x1 >= x0 else x1 - tw - 8
    d.text((tx + 2, y1 - 30 + 2), text, fill=(255, 255, 255), font=fnt)  # léger halo pour la lisibilité
    d.text((tx, y1 - 30), text, fill=RED, font=fnt)


def annotate(img, meta):
    d = ImageDraw.Draw(img)
    w, h = img.size
    rng = random.Random(meta["title"])
    fnt = ImageFont.truetype(HAND, 50)
    marks = []  # (x, y, r, texte)
    groups = {}
    for gname, typ, x, z, alt in meta["units"]:
        groups.setdefault(gname, []).append((typ, project(meta, x, z, alt, HFOV)))
    for gname, us in groups.items():
        glab = label_for(gname)
        pts = [p for _, p in us if 0 <= p[0] < w and 0 <= p[1] < h]
        if not pts:
            continue
        if glab is None:
            for typ, (px, py) in us:
                if 0 <= px < w and 0 <= py < h:
                    marks.append((px, py, 30, UNIT_LABEL.get(typ, "véhicule")))
        else:
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            marks.append(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2,
                          max(max(xs) - min(xs), max(ys) - min(ys)) / 2 + 36, glab))
    for name, x, z, alt in meta.get("statics", []):
        px, py = project(meta, x, z, alt, HFOV)
        if 0 <= px < w and 0 <= py < h:
            marks.append((px, py, 34, name))
    placed = []
    for i, (px, py, r, text) in enumerate(sorted(marks, key=lambda m: m[1])):
        rx, ry = felt_ring(d, px, py, r, rng)
        side = 1 if px < w * 0.7 else -1
        lx, ly = px + side * (rx + 90), py - ry - 60
        while any(abs(ly - q) < 60 and abs(lx - p_) < 420 for p_, q in placed):
            ly -= 64
        placed.append((lx, ly))
        felt_label(d, px + side * rx * 0.7, py - ry * 0.7, lx, ly, text, rng, fnt)


def frame(img, meta, index, total):
    w, h = img.size
    top, bot = 70, 130
    out = Image.new("RGB", (w, h + top + bot), (8, 8, 8))
    out.paste(img, (0, top))
    d = ImageDraw.Draw(out)
    f, fb = font(30), font(34, True)
    d.text((24, 18), "RECCE  //  OPÉRATION MARTEAU DU GOLAN  //  DIFFUSION RESTREINTE", fill=(230, 230, 220), font=fb)
    d.text((w - 330, 18), f"FRAME {index:02d}/{total:02d}", fill=(230, 230, 220), font=fb)
    tx, ty, alt = meta["target"]
    lat, lon = dcs_to_latlon(tx, ty)
    d.text((24, h + top + 14), meta["title"].upper(), fill=YEL, font=font(40, True))
    line = (f"CAP {meta['heading']:03.0f}°   OBLIQUE {meta['pitch']:.0f}°   "
            f"{to_dms(lat, 'N', 'S')} {to_dms(lon, 'E', 'W')}   SOL {round(alt * 3.281)} FT   16 AVR 11:31L")
    d.text((24, h + top + 70), line, fill=(230, 230, 220), font=f)
    # repères de cadre
    for (x0, y0, sx, sy) in ((40, top + 40, 1, 1), (w - 40, top + 40, -1, 1), (40, top + h - 40, 1, -1), (w - 40, top + h - 40, -1, -1)):
        d.line([(x0, y0), (x0 + 70 * sx, y0)], fill=(230, 230, 220), width=4)
        d.line([(x0, y0), (x0, y0 + 70 * sy)], fill=(230, 230, 220), width=4)
    # flèche de cap : vers le haut de l'image = cap de la prise ; le nord est tourné d'autant
    cx, cy, L = w - 110, top + 130, 60
    d.ellipse([cx - 75, cy - 75, cx + 75, cy + 75], outline=(230, 230, 220), width=3)
    a = math.radians(-meta["heading"])
    nx, ny = cx + L * math.sin(a), cy - L * math.cos(a)
    d.line([(cx, cy), (nx, ny)], fill=YEL, width=6)
    d.text((nx - 10, ny - 20), "N", fill=YEL, font=font(34, True))
    d.text((cx - 60, cy + 82), f"CAP {meta['heading']:03.0f}", fill=(230, 230, 220), font=font(26, True))
    return out


if __name__ == "__main__":
    names = [s[0] for s in SHOTS]
    for i, name in enumerate(names, start=1):
        meta = json.loads((RAW / f"{name}.json").read_text(encoding="utf-8"))
        raw = Image.open(RAW / f"{name}.png").convert("RGB")
        raw = raw.crop((0, 0, raw.width, raw.height - 26))  # reste de la barre d'infos F11
        img = recce_look(raw)
        annotate(img, meta)
        out = frame(img, meta, i, len(names))
        out.save(OUT / f"{name}.jpg", quality=88)
        print(name, out.size)
