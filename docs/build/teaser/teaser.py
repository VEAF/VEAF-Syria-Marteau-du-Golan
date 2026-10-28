"""Image teaser de la mission (docs/teaser.jpg, 1920 × 1080) : paysage DCS étalonné, carte, photo de reco, titre."""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

HERE = Path(__file__).parent
DOCS = HERE.parent.parent
W, H = 1920, 1080
F = "C:/Windows/Fonts/"


def font(name, size):
    return ImageFont.truetype(F + name, size)


def graded_background():
    bg = Image.open(HERE.parent / "recon" / "raw" / "03-sa11.png").convert("RGB")
    s = max(W / bg.width, H / bg.height)
    bg = bg.resize((int(bg.width * s) + 1, int(bg.height * s) + 1), Image.LANCZOS).crop((0, 0, W, H))
    bg = ImageEnhance.Contrast(bg).enhance(1.25)
    # étalonnage soir : ombres froides, hautes lumières chaudes
    g = ImageOps.grayscale(bg)
    warm = ImageOps.colorize(g, black=(10, 22, 34), mid=(120, 92, 60), white=(255, 214, 150))
    bg = Image.blend(bg, warm, 0.55)
    # assombrir la gauche pour le texte, et le haut comme un ciel lourd
    shade = Image.new("L", (W, H))
    d = ImageDraw.Draw(shade)
    for x in range(W):
        d.line([(x, 0), (x, H)], fill=int(235 * max(0.0, 1 - x / (W * 0.72)) ** 1.4))
    bg = Image.composite(Image.new("RGB", (W, H), (6, 8, 12)), bg, shade)
    vig = Image.radial_gradient("L").resize((W, H)).point(lambda v: int(v * 0.8))
    bg = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), bg, vig)
    random.seed(3)
    noise = Image.effect_noise((W, H), 18).convert("RGB")
    return Image.blend(bg, noise, 0.05)


def tilted(img, width, angle, border=14, caption=None):
    im = img.convert("RGB")
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    bottom = 70 if caption else 40
    framed = Image.new("RGB", (im.width + 2 * border, im.height + 2 * border + bottom), (238, 234, 222))
    framed.paste(im, (border, border))
    if caption:
        ImageDraw.Draw(framed).text((border + 10, im.height + border + 14), caption, fill=(200, 25, 25), font=font("Inkfree.ttf", 34))
    rot = framed.convert("RGBA").rotate(angle, expand=True, resample=Image.BICUBIC)
    shadow = Image.new("RGBA", rot.size, (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 150), mask=rot.split()[3])
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    return rot, shadow


def main():
    img = graded_background().convert("RGBA")
    # la carte de la zone des combats, puis la photo de reco du SA-6 par-dessus
    carte, sh = tilted(Image.open(DOCS / "maps-hd" / "sitac-front.png"), 760, 5)
    img.alpha_composite(sh, (1080 + 18, 120 + 22))
    img.alpha_composite(carte, (1080, 120))
    reco, sh = tilted(Image.open(DOCS / "recon" / "02-sa6.jpg"), 640, -6, caption="SA-6 de Sa'sa' : à faire tomber avant le col")
    img.alpha_composite(sh, (1170 + 18, 515 + 22))
    img.alpha_composite(reco, (1170, 515))
    d = ImageDraw.Draw(img)

    x = 90
    d.text((x, 150), "VEAF  //  SYRIA  //  JEUDI 29 OCTOBRE  ·  21 H", fill=(235, 190, 110), font=font("bahnschrift.ttf", 38))
    d.text((x - 4, 205), "MARTEAU", fill=(245, 242, 232), font=font("impact.ttf", 190))
    d.text((x - 4, 395), "DU GOLAN", fill=(245, 242, 232), font=font("impact.ttf", 190))
    d.rectangle([x, 610, x + 140, 618], fill=(200, 25, 25))
    tag = font("segoeuib.ttf", 42)
    for i, line in enumerate(("Percer le front.", "Briser la réserve.", "Rentrer avant la nuit.")):
        d.text((x, 650 + i * 58), line, fill=(240, 236, 226), font=tag)
    small = font("bahnschrift.ttf", 32)
    d.text((x, 860), "AH-64D · OH-58D · Mi-24P · A-10C · AV-8B · F-16C · F/A-18C", fill=(235, 190, 110), font=small)
    d.text((x, 910), "Attaque en profondeur · 6 à 12 pilotes · slots dynamiques", fill=(210, 206, 196), font=small)
    out = img.convert("RGB")
    out.save(DOCS / "teaser.jpg", quality=92)
    out.save(DOCS / "teaser.png")
    print(out.size)


if __name__ == "__main__":
    main()
