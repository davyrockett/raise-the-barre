"""Draws the app icons into ../icons. Run: python3 tools/make-icons.py (needs Pillow)."""
from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent.parent / "icons"
BG = (21, 19, 16)          # dark brown page background
ACCENT = (255, 148, 51)    # the app's orange (dark-mode shade, same as Page Fright)
CREAM = (240, 235, 227)


def draw(size: int) -> Image.Image:
    s = 1024  # draw large, then shrink for smooth edges
    img = Image.new("RGB", (s, s), BG)
    d = ImageDraw.Draw(img)
    # A chord box with an orange barre across it (kept inside the safe zone iOS/Android won't crop)
    left, right, top, rows, dy = 292, 732, 250, 4, 130
    for r in range(rows + 1):
        y = top + r * dy
        d.line([left, y, right, y], fill=CREAM, width=14)
    for i in range(6):
        x = left + i * (right - left) / 5
        d.line([x, top, x, top + rows * dy], fill=CREAM, width=14)
    y = top + dy / 2
    d.rounded_rectangle([left - 50, y - 50, right + 50, y + 50], radius=50, fill=ACCENT)
    for i, row in ((1, 2), (2, 2), (3, 1)):  # the rest of the E shape
        x, cy = left + i * (right - left) / 5, top + (row + 0.5) * dy
        d.ellipse([x - 50, cy - 50, x + 50, cy + 50], fill=ACCENT)
    return img.resize((size, size), Image.LANCZOS)


OUT.mkdir(exist_ok=True)
for name, size in [("icon-192.png", 192), ("icon-512.png", 512), ("apple-touch-icon.png", 180)]:
    draw(size).save(OUT / name, optimize=True)
    print("wrote", OUT / name)
