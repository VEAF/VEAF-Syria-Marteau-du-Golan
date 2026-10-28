"""Place la caméra libre DCS (F11) en vue oblique sur une cible, puis capture la fenêtre DCS en pleine résolution."""
import ctypes, math, sys, time
from ctypes import wintypes
from pathlib import Path
from PIL import ImageGrab
from fiddle import run

OUT = Path(__file__).parent / "raw"
OUT.mkdir(exist_ok=True)
ctypes.windll.user32.SetProcessDPIAware()


def dcs_rect():
    hwnd = ctypes.windll.user32.FindWindowW(None, "Digital Combat Simulator")
    if not hwnd:
        raise SystemExit("fenêtre DCS introuvable")
    r = wintypes.RECT()
    ctypes.windll.user32.GetClientRect(hwnd, ctypes.byref(r))
    pt = wintypes.POINT(0, 0)
    ctypes.windll.user32.ClientToScreen(hwnd, ctypes.byref(pt))
    return pt.x, pt.y, pt.x + r.right, pt.y + r.bottom


LAST = {}


def place(x, y, ground, slant=1100, pitch=35, heading=0):
    """Caméra à `slant` m de la cible (x, y DCS, sol en m), regard au cap `heading`, incliné de `pitch` vers le bas."""
    p, h = math.radians(pitch), math.radians(heading)
    fwd = (math.cos(p) * math.cos(h), -math.sin(p), math.cos(p) * math.sin(h))
    up = (math.sin(p) * math.cos(h), math.cos(p), math.sin(p) * math.sin(h))
    right = (-math.sin(h), 0.0, math.cos(h))
    cx, cy, cz = x - fwd[0] * slant, ground - fwd[1] * slant, y - fwd[2] * slant
    lua = ("LoSetCameraPosition({x={x=%f,y=%f,z=%f},y={x=%f,y=%f,z=%f},z={x=%f,y=%f,z=%f},p={x=%f,y=%f,z=%f}}) return 'ok'"
           % (*fwd, *up, *right, cx, cy, cz))
    LAST.update(cam=(cx, cy, cz), fwd=fwd, up=up, right=right, heading=heading, pitch=pitch, target=(x, y, ground))
    return run(lua, "export")


def shoot(name, x, y, ground, **kw):
    place(x, y, ground, **kw)
    time.sleep(2.5)  # laisse DCS charger le décor
    place(x, y, ground, **kw)
    time.sleep(1.0)
    l, t, r, b = dcs_rect()
    for attempt in range(8):
        img = ImageGrab.grab().crop((l, t, r, b - 24))  # écran principal ; sans la barre d'infos F11
        if img.getextrema()[0][1] > 0:
            break
        time.sleep(2.0)
        place(x, y, ground, **kw)
    else:
        raise SystemExit("capture noire : la fenêtre DCS est-elle visible ?")
    img.save(OUT / f"{name}.png")
    import json
    (OUT / f"{name}.json").write_text(json.dumps(dict(LAST, size=img.size)), encoding="utf-8")
    return img.size


if __name__ == "__main__":
    name, x, y, g = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
    kw = {}
    for a in sys.argv[5:]:
        k, v = a.split("=")
        kw[k] = float(v)
    print(shoot(name, x, y, g, **kw))
