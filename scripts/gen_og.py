"""Generate the Open Graph / Twitter share image (1200x630).

    pip install pillow
    python scripts/gen_og.py /path/to/Ubuntu-Bold.ttf /path/to/Ubuntu-Regular.ttf

Falls back to a default sans font if no TTF paths are given. Writes
docs/assets/og-image.png.
"""

import sys
from PIL import Image, ImageDraw, ImageFont

DARK = (21, 21, 21, 255)
RED = (238, 0, 0, 255)
WHITE = (242, 242, 242, 255)
MUTED = (163, 163, 163, 255)

W, H = 1200, 630
SHIELD = [
    (256, 84), (404, 140), (404, 276), (390, 340), (340, 400), (256, 448),
    (172, 400), (122, 340), (108, 276), (108, 140),
]
STEM = [(240, 262), (272, 262), (286, 344), (226, 344)]


def _poly(pts, cx, cy, s):
    return [(cx + (x - 256) * s, cy + (y - 256) * s) for x, y in pts]


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


bold = sys.argv[1] if len(sys.argv) > 1 else "arialbd.ttf"
regular = sys.argv[2] if len(sys.argv) > 2 else "arial.ttf"

img = Image.new("RGB", (W, H), DARK[:3])
d = ImageDraw.Draw(img)

# left keyline
d.rectangle([0, 0, 12, H], fill=RED[:3])

# shield mark, left third
cx, cy, s = 300, H // 2, 0.92
d.polygon(_poly(SHIELD, cx, cy, s), fill=RED[:3])
r = 34 * s
d.ellipse([cx - r, cy + (242 - 256) * s - r, cx + r, cy + (242 - 256) * s + r], fill=DARK[:3])
d.polygon(_poly(STEM, cx, cy, s), fill=DARK[:3])

# text block, right
tx = 500
d.text((tx, 232), "Security Basics", font=font(bold, 76), fill=WHITE[:3])
d.text((tx, 338), "A backend developer's mental model", font=font(regular, 34), fill=MUTED[:3])
d.text((tx, 386), "for web application security.", font=font(regular, 34), fill=MUTED[:3])

img.save("docs/assets/og-image.png")
print("wrote docs/assets/og-image.png")
