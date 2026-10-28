"""Une vignette par étape du plan de vol : la branche en surbrillance sur la sitac générale ou la carte du front."""
from PIL import Image, ImageDraw

from data import HELOS, HELOS_FROM, JETS, JETS_FROM
from render_maps import OUT, front, overview

YELLOW = (255, 200, 0)


def crop_leg(v, img, a, b, name, path, cw=1300, ch=900):
    im = img.copy()
    d = ImageDraw.Draw(im, "RGBA")
    pa, pb = v.out_xy(*a), v.out_xy(*b)
    d.line([pa, pb], fill=(0, 0, 0, 200), width=16)
    d.line([pa, pb], fill=YELLOW, width=10)
    r = 16
    d.ellipse([pb[0] - r, pb[1] - r, pb[0] + r, pb[1] + r], fill=YELLOW, outline=(0, 0, 0), width=4)
    mx, my = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2
    # agrandit le cadre si la branche est plus longue que lui
    span = max(abs(pa[0] - pb[0]) + 240, (abs(pa[1] - pb[1]) + 240) * cw / ch, cw)
    cw2, ch2 = span, span * ch / cw
    x0 = min(max(mx - cw2 / 2, 0), im.width - cw2)
    y0 = min(max(my - ch2 / 2, 0), im.height - ch2)
    im.crop((int(x0), int(y0), int(x0 + cw2), int(y0 + ch2))).resize((cw, ch), Image.LANCZOS).save(path, optimize=True)


def inside(v, p, margin=80):
    x, y = v.out_xy(*p)
    return margin < x < v.w - margin and margin < y < v.h - margin


if __name__ == "__main__":
    vo = overview()
    io = Image.open(OUT / "sitac-generale.png")
    vf = front()
    fr = Image.open(OUT / "sitac-front.png")
    for plan, start, pts in (("jets", JETS_FROM, JETS), ("helos", HELOS_FROM, HELOS)):
        prev = start[1:]
        for i, (name, x, y, *_r) in enumerate(pts, start=1):
            use_front = inside(vf, prev) and inside(vf, (x, y))
            v, im = (vf, fr) if use_front else (vo, io)
            crop_leg(v, im, prev, (x, y), name, OUT / f"etape-{plan}-{i:02d}.png")
            prev = (x, y)
    print("étapes ok")
