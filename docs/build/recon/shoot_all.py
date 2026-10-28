"""Enchaîne toutes les prises : vise le centre des unités de chaque cible, à son cap d'engagement."""
import json
import sys
from shoot import OUT, shoot
from shots import SHOTS, STATICS

units = [l.split(";") for l in open("live_units.txt", encoding="utf-8").read().splitlines()]
for name, prefixes, title, hdg, slant, pitch in SHOTS:
    if len(sys.argv) > 1 and name not in sys.argv[1:]:
        continue
    sel = [u for u in units if any(u[0].startswith(p) for p in prefixes)]
    pts = [(float(u[2]), float(u[3]), float(u[4])) for u in sel]
    pts += [(x, y, None) for _, x, y in STATICS.get(name, [])]
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    g = sum(p[2] for p in pts if p[2] is not None) / max(1, sum(1 for p in pts if p[2] is not None))
    size = shoot(name, cx, cy, g, slant=slant, pitch=pitch, heading=hdg)
    meta = json.loads((OUT / f"{name}.json").read_text(encoding="utf-8"))
    meta["title"] = title
    meta["units"] = [[u[0], u[1], float(u[2]), float(u[3]), float(u[4])] for u in sel]
    meta["statics"] = [[n, x, y, g] for n, x, y in STATICS.get(name, [])]
    (OUT / f"{name}.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    print(name, size, len(sel), "unités")
