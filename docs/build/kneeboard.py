"""Planchettes 2:3 (1024 × 1536) : cartes, cartes de vol sans plan radio, cibles, coordination."""
import math
from pathlib import Path

from PIL import Image, ImageDraw

from alts import TARGET_FT, WP_M
from data import BASES, BULLSEYE, HELOS, HELOS_FROM, JETS, JETS_FROM, OBJECTIVES
from geo import dcs_to_latlon, to_dms
from maps import BLUE, DARK, RED, View, font
from render_maps import GREEN, OUT as MAPS, common

KB = Path(__file__).parent / "kneeboard"
KB.mkdir(exist_ok=True)
W, H = 1024, 1536


def be(x, y):
    dx, dy = x - BULLSEYE[0], y - BULLSEYE[1]
    return f"{(math.degrees(math.atan2(dy, dx)) + 360) % 360:03.0f}/{math.hypot(dx, dy) / 1852:.0f}"


def save(img, name):
    img.convert("RGB").save(KB / name, quality=88)


def map_pages():
    v = View((-222000, -25000), 11, W, H, rot=-54, up=1.0)
    common(v, detail=False)
    for name, p in BASES.items():
        v.marker(*p, BLUE, "square", 10)
        v.label(*p, name, BLUE, size=22)
    for zone, title, wp, c, r, t in OBJECTIVES:
        v.marker(*c, RED, "diamond", 9)
        v.label(*c, wp, RED, size=18, dx=12, dy=-8)
    for name in ("PUSH", "EGRESS"):
        p = next(j for j in JETS if j[0] == name)
        v.marker(p[1], p[2], BLUE, "dot", 7)
        v.label(p[1], p[2], name, BLUE, size=18)
    v.marker(*BULLSEYE, DARK, "cross", 7)
    save(v.render(scale_nm=10, title="Sitac générale"), "01-sitac-generale.jpg")

    v = View((-196000, 5000), 12, W, H, rot=-60, up=1.0)
    common(v, detail=True)
    for zone, title, wp, c, r, t in OBJECTIVES:
        for tt in t:
            v.marker(tt[2], tt[3], RED, "dot", 5)
        v.label(*c, wp, RED, size=20, dx=14, dy=-10)
    for name, x, y, *_r in HELOS[:3]:
        v.marker(x, y, GREEN, "dot", 7)
        v.label(x, y, name, GREEN, size=18, dx=-12, dy=-8)
    v.marker(*BULLSEYE, DARK, "cross", 7)
    save(v.render(scale_km=5, title="Zone des combats"), "02-zone-des-combats.jpg")

    for i, (zone, title, wp, c, r, t) in enumerate(OBJECTIVES, start=3):
        im = Image.open(MAPS / f"objectif-{zone.lower()}.png")
        cw = int(im.height * 2 / 3)
        x0 = (im.width - cw) // 2
        page = im.crop((x0, 0, x0 + cw, im.height)).resize((W, H), Image.LANCZOS)
        d = ImageDraw.Draw(page)
        d.rectangle([0, 0, W, 60], fill=(255, 255, 255))
        d.text((16, 12), f"{wp} — {title}", fill=DARK, font=font(30, True))
        save(page, f"{i:02d}-{zone.lower()}.jpg")


def table_page(title, header, rows, widths, name, note=None, size=21):
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((24, 20), title, fill=DARK, font=font(36, True))
    y = 90
    f, fb = font(size), font(size, True)

    def wrap(text, width, fnt):
        words, lines, cur = text.split(), [], ""
        for w_ in words:
            test = (cur + " " + w_).strip()
            if d.textlength(test, font=fnt) > width and cur:
                lines.append(cur)
                cur = w_
            else:
                cur = test
        lines.append(cur)
        return lines

    for k, row in enumerate([header] + rows):
        fnt = fb if k == 0 else f
        cells = [wrap(str(c), widths[j] - 12, fnt) for j, c in enumerate(row)]
        h = max(len(c) for c in cells) * (size + 6) + 10
        x = 24
        for j, c in enumerate(cells):
            d.rectangle([x, y, x + widths[j], y + h], fill=(31, 78, 160) if k == 0 else ((255, 255, 255) if k % 2 else (238, 242, 248)),
                        outline=(190, 190, 190))
            for li, line in enumerate(c):
                d.text((x + 6, y + 5 + li * (size + 6)), line, fill=(255, 255, 255) if k == 0 else DARK, font=fnt)
            x += widths[j]
        y += h
    if note:
        for li, line in enumerate(wrap(note, W - 48, font(18))):
            d.text((24, y + 16 + li * 24), line, fill=(100, 100, 100), font=font(18))
    save(img, name)


def short(text):
    return text.split(".")[0]


def flight_cards():
    for n, (label, start, pts, num) in enumerate((("Jets", JETS_FROM, JETS, 10), ("Hélicoptères", HELOS_FROM, HELOS, 11))):
        rows = [["0", start[0], "—", "—", "—", "Départ"]]
        for i, (name, x, y, hdg, nm, role) in enumerate(pts, start=1):
            alt = WP_M.get(name)
            rows.append([str(i), name, f"{hdg:03d}", f"{nm:g}", f"{round(alt * 3.281)}" if alt else "—", short(role)])
        table_page(f"Carte de vol — {label}", ["W", "Point", "Cap", "nm", "Sol ft", "Rôle"], rows,
                   [50, 160, 70, 70, 90, 536], f"{num}-carte-de-vol-{'jets' if n == 0 else 'helos'}.jpg",
                   note="Sol : relief seul (sans arbres ni bâtiments). Les fréquences sont préréglées dans l'appareil.")


def targets_page():
    rows, k = [], 0
    for zone, title, wp, c, r, t in OBJECTIVES:
        for name, kind, x, y, role in t:
            lat, lon = dcs_to_latlon(x, y)
            rows.append([wp, name, f"{to_dms(lat, 'N', 'S')}\n{to_dms(lon, 'E', 'W')}".replace("\n", " "), str(TARGET_FT[k]), be(x, y)])
            k += 1
    half = (len(rows) + 1) // 2
    for p, chunk in enumerate((rows[:half], rows[half:]), start=0):
        table_page(f"Cibles ({p + 1}/2)", ["Pt", "Cible", "Coordonnées", "Sol ft", "BE"], chunk, [120, 220, 410, 100, 126],
                   f"{12 + p}-cibles-{p + 1}.jpg", size=18)


def coordination_page():
    table_page("Coordination", ["Mot-code", "Sens", "Qui réagit"], [
        ["PORTE OUVERTE", "SA-6 de Sa'sa' détruit", "Blade franchit le col"],
        ["MARTEAU", "Khan Arnabah tombé", "Le Mission Maker lance la poussée"],
        ["ENCLUME", "Contre-attaque en route", "Blade, Archer, Jedi la cassent"],
        ["PORTE FERMÉE", "SA-11 encore actif", "Arctic ne part pas sur Kiswah"],
        ["—", "JTAC Abu Nada", "Code 1511, FM 35.55, véhicules < 10 km"],
        ["—", "QRA ennemies", "Prêtes à H+15, ignorent les hélicos"],
        ["—", "SEAD (Ninja)", "SA-15 Khan, puis SA-6, puis radar, puis SA-11"],
    ], [230, 330, 416], "14-coordination.jpg", note="Mots-codes sur la fréquence Package.")


def recon_pages():
    names = sorted(p.stem for p in (Path(__file__).parent.parent / "recon").glob("*.jpg"))
    for k in range(0, len(names), 2):
        page = Image.new("RGB", (W, H), (10, 10, 10))
        for j, n in enumerate(names[k:k + 2]):
            im = Image.open(Path(__file__).parent.parent / "recon" / f"{n}.jpg")
            im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
            page.paste(im, (0, 20 + j * (im.height + 30)))
        save(page, f"{15 + k // 2:02d}-reco-{k // 2 + 1}.jpg")


if __name__ == "__main__":
    recon_pages()
    map_pages()
    flight_cards()
    targets_page()
    coordination_page()
    print(sorted(p.name for p in KB.iterdir()))
