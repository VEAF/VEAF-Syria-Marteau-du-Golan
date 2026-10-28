"""Cartes du briefing : tuiles OpenTopoMap en cache, rotation libre, superpositions nettes."""
import math
import time
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

from geo import dcs_to_latlon, merc

HERE = Path(__file__).parent
CACHE = HERE / "tiles"
ATTRIB = "© OpenStreetMap contributors, SRTM | style © OpenTopoMap (CC-BY-SA)"
UA = {"User-Agent": "VEAF-mission-briefing/1.0 (DCS mission maker, offline cache)"}

FONT = "C:/Windows/Fonts/arial.ttf"
FONT_B = "C:/Windows/Fonts/arialbd.ttf"

RED = (200, 20, 20)
BLUE = (20, 70, 200)
ORANGE = (230, 120, 0)
DARK = (25, 25, 25)
WHITE = (255, 255, 255)


def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def tile(z, tx, ty):
    p = CACHE / f"{z}/{tx}/{ty}.png"
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://{'abc'[(tx + ty) % 3]}.tile.opentopomap.org/{z}/{tx}/{ty}.png"
        for attempt in range(4):
            r = requests.get(url, headers=UA, timeout=30)
            if r.status_code == 200:
                p.write_bytes(r.content)
                break
            time.sleep(2 + attempt * 3)
        else:
            raise RuntimeError(f"tuile {z}/{tx}/{ty} : HTTP {r.status_code}")
        time.sleep(0.25)
    return Image.open(p).convert("RGB")


class View:
    """Une carte : centre (x, y DCS), zoom des tuiles, taille finale, rotation (degrés horaires), suréchantillonnage."""

    def __init__(self, center, z, w, h, rot=0.0, up=2.0):
        self.z, self.w, self.h, self.rot, self.up = z, w, h, rot, up
        self.lat0, self.lon0 = dcs_to_latlon(*center)
        self.cpx, self.cpy = merc(self.lat0, self.lon0, z)
        self.r = math.ceil(math.hypot(w, h) / 2 / up) + 8  # rayon en px de tuile
        x0, y0 = self.cpx - self.r, self.cpy - self.r
        mos = Image.new("RGB", (2 * self.r, 2 * self.r))
        for tx in range(int(x0 // 256), int((x0 + 2 * self.r) // 256) + 1):
            for ty in range(int(y0 // 256), int((y0 + 2 * self.r) // 256) + 1):
                mos.paste(tile(self.z, tx, ty), (int(tx * 256 - x0), int(ty * 256 - y0)))
        size = int(2 * self.r * up)
        self.big = mos.resize((size, size), Image.LANCZOS)
        # léger voile pour faire ressortir les superpositions
        self.big = Image.blend(self.big, Image.new("RGB", self.big.size, WHITE), 0.18)
        self.draw = ImageDraw.Draw(self.big, "RGBA")
        self.labels = []

    def m_per_px(self):
        return 156543.03392 * math.cos(math.radians(self.lat0)) / 2**self.z / self.up

    def big_xy(self, x, y):
        lat, lon = dcs_to_latlon(x, y)
        px, py = merc(lat, lon, self.z)
        return (px - self.cpx + self.r) * self.up, (py - self.cpy + self.r) * self.up

    def out_xy(self, x, y):
        bx, by = self.big_xy(x, y)
        c = self.r * self.up
        a = math.radians(self.rot)
        dx, dy = bx - c, by - c
        rx = dx * math.cos(a) - dy * math.sin(a)
        ry = dx * math.sin(a) + dy * math.cos(a)
        return rx + self.w / 2, ry + self.h / 2

    # --- superpositions dessinées avant rotation (traits, cercles) ---
    def line(self, pts, color, width=4, dash=None):
        ps = [self.big_xy(*p) for p in pts]
        if not dash:
            self.draw.line(ps, fill=color, width=width, joint="curve")
            return
        on, off = dash
        for (x1, y1), (x2, y2) in zip(ps, ps[1:]):
            d = math.hypot(x2 - x1, y2 - y1)
            n = max(1, int(d // (on + off)))
            for i in range(n + 1):
                a = i * (on + off) / d
                b = min(1, (i * (on + off) + on) / d)
                if a >= 1:
                    break
                self.draw.line([(x1 + (x2 - x1) * a, y1 + (y2 - y1) * a), (x1 + (x2 - x1) * b, y1 + (y2 - y1) * b)],
                               fill=color, width=width)

    def circle(self, center, radius_m, color, width=4, fill=None, dash=None):
        cx, cy = self.big_xy(*center)
        r = radius_m / self.m_per_px()
        if dash:
            n = max(24, int(2 * math.pi * r / sum(dash)))
            for i in range(n):
                a1 = 360 * i / n
                a2 = a1 + 360 / n * dash[0] / sum(dash)
                self.draw.arc([cx - r, cy - r, cx + r, cy + r], a1, a2, fill=color, width=width)
        else:
            self.draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=width, fill=fill)

    # --- étiquettes et symboles, dessinés après rotation (toujours droits) ---
    def label(self, x, y, text, color=DARK, size=22, bold=True, dx=14, dy=-14, box=True):
        self.labels.append(("label", x, y, text, color, size, bold, dx, dy, box))

    def marker(self, x, y, color, shape="dot", size=10):
        self.labels.append(("marker", x, y, color, shape, size))

    def render(self, north_arrow=True, scale_nm=None, scale_km=None, legend=None, inset=None, title=None, legend_right=False):
        img = self.big.rotate(-self.rot, resample=Image.BICUBIC, center=(self.r * self.up, self.r * self.up))
        c = self.r * self.up
        img = img.crop((int(c - self.w / 2), int(c - self.h / 2), int(c - self.w / 2) + self.w, int(c - self.h / 2) + self.h))
        d = ImageDraw.Draw(img, "RGBA")
        for item in self.labels:
            if item[0] == "marker":
                _, x, y, color, shape, s = item
                px, py = self.out_xy(x, y)
                if shape == "dot":
                    d.ellipse([px - s, py - s, px + s, py + s], fill=color, outline=WHITE, width=2)
                elif shape == "square":
                    d.rectangle([px - s, py - s, px + s, py + s], fill=color, outline=WHITE, width=2)
                elif shape == "diamond":
                    d.polygon([(px, py - s * 1.3), (px + s * 1.3, py), (px, py + s * 1.3), (px - s * 1.3, py)], fill=color, outline=WHITE)
                elif shape == "triangle":
                    d.polygon([(px, py - s * 1.3), (px + s * 1.2, py + s), (px - s * 1.2, py + s)], fill=color, outline=WHITE)
                elif shape == "cross":
                    d.ellipse([px - s * 1.6, py - s * 1.6, px + s * 1.6, py + s * 1.6], outline=DARK, width=3)
                    d.line([(px - s * 2.2, py), (px + s * 2.2, py)], fill=DARK, width=3)
                    d.line([(px, py - s * 2.2), (px, py + s * 2.2)], fill=DARK, width=3)
        for item in self.labels:
            if item[0] != "label":
                continue
            _, x, y, text, color, size, bold, dx, dy, box = item
            px, py = self.out_xy(x, y)
            f = font(size, bold)
            l, t, r, b = d.textbbox((0, 0), text, font=f)
            tx, ty = px + dx, py + dy - (b - t)
            if dx < 0:
                tx = px + dx - (r - l)
            if box:
                d.rounded_rectangle([tx - 6, ty - 4 + t, tx + r - l + 6, ty + b + 4], radius=5, fill=(255, 255, 255, 230), outline=color, width=2)
            d.text((tx - l, ty), text, fill=color, font=f)
        if north_arrow:
            self._north(d)
        if scale_nm or scale_km:
            self._scale(d, scale_nm, scale_km)
        if legend:
            self._legend(d, legend, legend_right)
        if inset:
            img.paste(inset, (self.w - inset.width - 20, 20))
            d.rectangle([self.w - inset.width - 20, 20, self.w - 20, 20 + inset.height], outline=DARK, width=3)
        if title:
            f = font(30, True)
            d.rounded_rectangle([16, 16, 30 + d.textlength(title, font=f), 64], radius=6, fill=(255, 255, 255, 235), outline=DARK, width=2)
            d.text((24, 22), title, fill=DARK, font=f)
        fa = font(15)
        tw = d.textlength(ATTRIB, font=fa)
        d.rectangle([self.w - tw - 16, self.h - 26, self.w, self.h], fill=(255, 255, 255, 220))
        d.text((self.w - tw - 8, self.h - 23), ATTRIB, fill=DARK, font=fa)
        return img

    def _north(self, d):
        cx, cy, L = 60, self.h - 120, 46
        a = math.radians(-self.rot)
        tipx, tipy = cx + L * math.sin(-a) * -1, cy - L * math.cos(a)
        tipx = cx + L * math.sin(math.radians(self.rot))
        tipy = cy - L * math.cos(math.radians(self.rot))
        basex = cx - L * 0.6 * math.sin(math.radians(self.rot))
        basey = cy + L * 0.6 * math.cos(math.radians(self.rot))
        d.ellipse([cx - 58, cy - 58, cx + 58, cy + 58], fill=(255, 255, 255, 220), outline=DARK, width=2)
        px, py = math.cos(math.radians(self.rot)) * 14, math.sin(math.radians(self.rot)) * 14
        d.polygon([(tipx, tipy), (basex + px, basey + py), (basex - px, basey - py)], fill=RED, outline=DARK)
        f = font(22, True)
        nx = cx + (L + 2) * math.sin(math.radians(self.rot)) * 0 + 0
        d.text((tipx - 8 + 14 * math.sin(math.radians(self.rot)), tipy - 30 - 4 * math.cos(math.radians(self.rot))), "N", fill=DARK, font=f)

    def _scale(self, d, nm, km):
        mpp = self.m_per_px()
        meters = nm * 1852 if nm else km * 1000
        L = meters / mpp
        x0, y0 = 130, self.h - 46
        d.rectangle([x0 - 10, y0 - 34, x0 + L + 90, y0 + 16], fill=(255, 255, 255, 220))
        d.rectangle([x0, y0 - 6, x0 + L, y0 + 4], fill=DARK)
        d.rectangle([x0 + L / 2, y0 - 6, x0 + L, y0 + 4], fill=WHITE, outline=DARK)
        d.text((x0 + L + 10, y0 - 16), f"{nm} nm" if nm else f"{km} km", fill=DARK, font=font(22, True))

    def _legend(self, d, items, right=False):
        f = font(18)
        w = max(d.textlength(t, font=f) for _, t in items) + 60
        h = 28 * len(items) + 14
        x0, y0 = (self.w - w - 16, 16) if right else (16, 80)
        d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=6, fill=(255, 255, 255, 225), outline=DARK, width=2)
        for i, (sym, text) in enumerate(items):
            yy = y0 + 10 + i * 28
            kind, color = sym
            if kind == "line":
                d.line([(x0 + 10, yy + 10), (x0 + 40, yy + 10)], fill=color, width=4)
            elif kind == "dash":
                d.line([(x0 + 10, yy + 10), (x0 + 20, yy + 10)], fill=color, width=4)
                d.line([(x0 + 28, yy + 10), (x0 + 40, yy + 10)], fill=color, width=4)
            elif kind == "ring":
                d.ellipse([x0 + 16, yy, x0 + 36, yy + 20], outline=color, width=3)
            elif kind == "dot":
                d.ellipse([x0 + 18, yy + 2, x0 + 34, yy + 18], fill=color, outline=WHITE)
            elif kind == "square":
                d.rectangle([x0 + 18, yy + 2, x0 + 34, yy + 18], fill=color, outline=WHITE)
            d.text((x0 + 50, yy), text, fill=DARK, font=f)


def inset_map(highlight_center, highlight_half_m, w=360, h=270):
    """Encart : la zone des combats au zoom 9, avec le cadre du zoom courant."""
    from data import BASES, OBJECTIVES, FRONT_LINE, BULLSEYE
    v = View((-205000, -5000), 9, w, h, rot=0, up=1.0)
    v.line(FRONT_LINE, RED, width=3)
    for _, _, _, c, _, _ in OBJECTIVES:
        v.marker(*c, RED, "dot", 4)
    for _, p in BASES.items():
        v.marker(*p, BLUE, "square", 5)
    v.marker(*BULLSEYE, DARK, "dot", 3)
    x, y = highlight_center
    hm = highlight_half_m
    img = v.render(north_arrow=False)
    d = ImageDraw.Draw(img, "RGBA")
    pts = [v.out_xy(x + hm, y - hm), v.out_xy(x + hm, y + hm), v.out_xy(x - hm, y + hm), v.out_xy(x - hm, y - hm)]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    if max(xs) - min(xs) < 14:
        cx, cy = sum(xs) / 4, sum(ys) / 4
        xs, ys = [cx - 7, cx + 7], [cy - 7, cy + 7]
    d.rectangle([min(xs), min(ys), max(xs), max(ys)], outline=(255, 0, 0, 255), width=4)
    d.rectangle([0, 0, w, 26], fill=(255, 255, 255, 220))
    d.text((8, 3), "Situation", fill=DARK, font=font(18, True))
    # cache l'attribution répétée : elle figure sur la carte principale
    d.rectangle([0, h - 26, w, h], fill=(255, 255, 255, 255))
    d.text((8, h - 23), "N en haut", fill=DARK, font=font(15))
    return img
