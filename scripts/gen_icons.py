"""Generate the PWA icon PNGs from the shield mark.

    pip install pillow
    python scripts/gen_icons.py

Writes icon-192/512(.png), icon-192/512-maskable.png and apple-touch-icon.png
into docs/assets/icons/. icon.svg in that folder is the scalable source of truth;
keep this mark in sync with it.
"""

from PIL import Image, ImageDraw

DARK = (21, 21, 21, 255)   # #151515
RED = (238, 0, 0, 255)     # #ee0000

SHIELD = [
    (256, 84), (404, 140), (404, 276), (390, 340), (340, 400), (256, 448),
    (172, 400), (122, 340), (108, 276), (108, 140),
]
STEM = [(240, 262), (272, 262), (286, 344), (226, 344)]


def _poly(pts, cx, cy, s):
    return [(cx + (x - 256) * s, cy + (y - 256) * s) for x, y in pts]


def render(size, maskable):
    ss = 4  # supersample then downscale for clean edges
    w = size * ss
    img = Image.new("RGBA", (w, w), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if maskable:
        d.rectangle([0, 0, w, w], fill=DARK)
        s = (w / 512) * 0.80
    else:
        d.rounded_rectangle([0, 0, w - 1, w - 1], radius=int(w * 96 / 512), fill=DARK)
        s = w / 512
    cx = cy = w / 2
    d.polygon(_poly(SHIELD, cx, cy, s), fill=RED)
    r = 34 * s
    hole = (cx, cy + (242 - 256) * s)
    d.ellipse([hole[0] - r, hole[1] - r, hole[0] + r, hole[1] + r], fill=DARK)
    d.polygon(_poly(STEM, cx, cy, s), fill=DARK)
    return img.resize((size, size), Image.LANCZOS)


OUT = "docs/assets/icons/"
render(192, False).save(OUT + "icon-192.png")
render(512, False).save(OUT + "icon-512.png")
render(192, True).save(OUT + "icon-192-maskable.png")
render(512, True).save(OUT + "icon-512-maskable.png")
render(180, False).save(OUT + "apple-touch-icon.png")
print("icons written to", OUT)
