"""Bandeau du calendrier VEAF (docs/teaser-bandeau.jpg, 2400 × 432, rapport 5,55 comme l'affichage du calendrier)."""
from PIL import Image, ImageDraw

import teaser
from teaser import DOCS, font, tilted

W, H = 2400, 432


def main():
    teaser.W, teaser.H = W, H
    img = teaser.graded_background().convert("RGBA")
    carte, sh = tilted(Image.open(DOCS / "maps-hd" / "sitac-front.png"), 500, 4)
    img.alpha_composite(sh, (1580 + 14, 28 + 16))
    img.alpha_composite(carte, (1580, 28))
    reco, sh = tilted(Image.open(DOCS / "recon" / "02-sa6.jpg"), 400, -5)
    img.alpha_composite(sh, (1930 + 14, 40 + 16))
    img.alpha_composite(reco, (1930, 40))
    d = ImageDraw.Draw(img)
    x = 110
    d.text((x, 58), "VEAF  //  SYRIA  //  JEUDI 29 OCTOBRE  ·  21 H", fill=(235, 190, 110), font=font("bahnschrift.ttf", 40))
    d.text((x - 4, 105), "MARTEAU DU GOLAN", fill=(245, 242, 232), font=font("impact.ttf", 170))
    d.rectangle([x, 300, x + 120, 307], fill=(200, 25, 25))
    d.text((x, 325), "Percer le front. Briser la réserve. Rentrer avant la nuit.", fill=(240, 236, 226), font=font("segoeuib.ttf", 40))
    out = img.convert("RGB")
    out.save(DOCS / "teaser-bandeau.jpg", quality=92)
    print(out.size)


if __name__ == "__main__":
    main()
