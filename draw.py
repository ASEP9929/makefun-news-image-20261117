# draw.py — draws entry.png: a newspaper front page summing up 17 November 2026.
# Run: python3 draw.py  (writes entry.png, 1024x1024, deterministic, no network)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (20, 20, 22)
NAVY = (20, 33, 61)
RED = (178, 34, 34)
GOLD = (232, 184, 75)
SKY_TOP = (250, 183, 120)
SKY_MID = (233, 150, 130)
SKY_BOT = (96, 110, 150)
SEA = (38, 68, 104)
SEA_DARK = (24, 48, 80)

CANDIDATES = {
    "serif_b": ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"],
    "sans_b": ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
               "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"],
    "sans": ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
             "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"],
    "serif": ["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"],
}


def font(kind, size):
    for p in CANDIDATES[kind]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    n = max(1, y1 - y0)
    for i in range(n):
        t = i / n
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def smoke_layer(img, blobs, blur=14):
    """blobs: list of (cx, cy, r, alpha) grey smoke puffs on a transparent layer."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for cx, cy, r, a in blobs:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 70, 78, a))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    img.alpha_composite(layer)


def flag_china(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.text((x + w * 0.16, y + h * 0.12), "\u2605", font=font("sans_b", int(h * 0.42)),
           fill=(255, 222, 0), anchor="la")
    for sx, sy in [(0.62, 0.16), (0.78, 0.30), (0.78, 0.52), (0.62, 0.66)]:
        d.text((x + w * sx, y + h * sy), "\u2605", font=font("sans_b", int(h * 0.16)),
               fill=(255, 222, 0), anchor="la")


def flag_usa(d, x, y, w, h):
    for i in range(7):
        d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + w * 0.42, y + h * 4 / 7], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            px = x + w * 0.05 + c * w * 0.075
            py = y + h * 0.06 + r * h * 0.085
            d.ellipse([px, py, px + 3, py + 3], fill=(255, 255, 255))


def flag_russia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=(255, 255, 255))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def headline_bar(d, x, y, w, h, lines, size=40, sub=None, sub_size=21):
    d.rectangle([x, y, x + w, y + h], fill=INK)
    cx = x + w / 2
    # shrink the headline until it fits the panel width
    s = size
    while s > 18 and d.textlength(lines[0], font=font("sans_b", s)) > w - 16:
        s -= 2
    if sub is None:
        d.text((cx, y + h / 2), lines[0], font=font("sans_b", s),
               fill=(255, 255, 255), anchor="mm")
    else:
        d.text((cx, y + h * 0.34), lines[0], font=font("sans_b", s),
               fill=(255, 255, 255), anchor="mm")
        ss = sub_size
        while ss > 14 and d.textlength(sub, font=font("sans", ss)) > w - 16:
            ss -= 1
        d.text((cx, y + h * 0.74), sub, font=font("sans", ss),
               fill=(210, 210, 210), anchor="mm")


def draw_bridge_panel(d, img, x, y, w, h):
    # dusk sky over the strait, bridge deck broken mid-span
    vgrad(d, (x, y, x + w, y + int(h * 0.62)), SKY_TOP, SKY_BOT)
    # low sun
    d.ellipse([x + w - 150, y + 42, x + w - 90, y + 102], fill=(255, 214, 130))
    # sea
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=SEA)
    for i in range(9):
        wy = y + int(h * 0.66) + i * 9
        d.line([(x + 12, wy), (x + w - 12, wy)], fill=SEA_DARK, width=2)
    deck_y = y + int(h * 0.52)
    # far shore
    d.rectangle([x, y + int(h * 0.60), x + w, y + int(h * 0.63)], fill=(52, 58, 64))
    # bridge towers + deck, broken in the middle
    gap_c = x + w // 2
    for tx in (x + 90, x + w - 150):
        d.rectangle([tx, deck_y - 92, tx + 16, deck_y + 4], fill=(30, 30, 34))
        d.rectangle([tx - 8, deck_y - 104, tx + 24, deck_y - 92], fill=(30, 30, 34))
    d.rectangle([x, deck_y, gap_c - 64, deck_y + 14], fill=(30, 30, 34))
    d.rectangle([gap_c + 64, deck_y, x + w, deck_y + 14], fill=(30, 30, 34))
    # fallen deck segment, tilted into the water
    d.polygon([(gap_c - 64, deck_y + 14), (gap_c + 30, deck_y + 44),
               (gap_c + 22, deck_y + 58), (gap_c - 70, deck_y + 30)], fill=(44, 44, 48))
    # blast glow at the break
    for r, col in [(46, (255, 120, 20)), (30, (255, 190, 60)), (16, (255, 240, 170))]:
        d.ellipse([gap_c - r, deck_y - r + 6, gap_c + r, deck_y + r + 6], fill=col)
    smoke_layer(img, [(gap_c - 30, deck_y - 70, 44, 135),
                      (gap_c + 40, deck_y - 96, 52, 125),
                      (gap_c + 90, deck_y - 130, 38, 105),
                      (gap_c - 80, deck_y - 110, 34, 100)])


def draw_hormuz_panel(d, img, x, y, w, h):
    # night sea in the Gulf: tanker burning, carrier on the horizon
    vgrad(d, (x, y, x + w, y + int(h * 0.55)), (24, 30, 52), (64, 78, 110))
    d.ellipse([x + w - 66, y + 26, x + w - 34, y + 58], fill=(235, 220, 180))
    d.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=(16, 34, 60))
    # distant carrier silhouette
    cx = x + w - 120
    d.rectangle([cx, y + int(h * 0.46), cx + 92, y + int(h * 0.55)], fill=(10, 14, 22))
    d.rectangle([cx + 52, y + int(h * 0.40), cx + 66, y + int(h * 0.46)], fill=(10, 14, 22))
    # tanker hull
    hy = y + int(h * 0.66)
    d.polygon([(x + 26, hy), (x + w - 30, hy), (x + w - 66, hy + 34),
               (x + 56, hy + 34)], fill=(12, 12, 14))
    d.rectangle([x + 60, hy - 34, x + 118, hy], fill=(26, 26, 30))
    d.rectangle([x + 130, hy - 22, x + 150, hy], fill=(150, 40, 30))
    # fire on deck + glow on water
    fx = x + 210
    for r, col in [(34, (255, 110, 16)), (22, (255, 180, 50)), (11, (255, 235, 160))]:
        d.ellipse([fx - r, hy - 44 - r, fx + r, hy - 44 + r], fill=col)
    d.ellipse([fx - 70, hy + 38, fx + 70, hy + 52], fill=(200, 90, 20))
    smoke_layer(img, [(fx - 10, hy - 110, 44, 150), (fx + 34, hy - 150, 52, 135),
                      (fx + 70, hy - 185, 38, 115)], blur=12)


def draw_shenzhen_panel(d, img, x, y, w, h):
    # dawn skyline + three flags on poles
    vgrad(d, (x, y, x + w, y + int(h * 0.62)), (126, 150, 196), (238, 214, 170))
    d.ellipse([x + 36, y + 30, x + 84, y + 78], fill=(255, 226, 150))
    base = y + int(h * 0.62)
    skyline = [(0, 96), (34, 150), (72, 84), (108, 170), (148, 120), (186, 190),
               (224, 100), (258, 150), (292, 88), (330, 168), (368, 130), (404, 176),
               (440, 110)]
    for sx, sh in skyline:
        d.rectangle([x + sx, base - sh, x + sx + 30, base], fill=(28, 34, 52))
        for wy in range(base - sh + 12, base - 8, 16):
            for wx in range(x + sx + 6, x + sx + 26, 10):
                if (wx * 7 + wy * 13) % 5 == 0:
                    d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 214, 110))
    d.rectangle([x, base, x + w, y + h], fill=(52, 56, 66))
    # flag poles
    fy = y + h - 108
    for i, (fx, fn) in enumerate([(x + 56, "cn"), (x + 196, "us"), (x + 336, "ru")]):
        d.rectangle([fx, fy - 66, fx + 5, fy + 8], fill=(210, 210, 210))
        if fn == "cn":
            flag_china(d, fx + 5, fy - 66, 84, 52)
        elif fn == "us":
            flag_usa(d, fx + 5, fy - 66, 84, 52)
        else:
            flag_russia(d, fx + 5, fy - 66, 84, 52)


def main():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((W // 2, 46), "THE WORLD IN ONE DAY", font=font("serif_b", 62),
           fill=(255, 255, 255), anchor="mm")
    d.text((W // 2, 96), "TUESDAY  \u2022  17 NOVEMBER 2026", font=font("sans_b", 26),
           fill=GOLD, anchor="mm")
    d.rectangle([0, 118, W, 124], fill=RED)

    # ---- lead story: Crimea bridge ----
    px, py, pw, ph = 14, 134, 996, 330
    draw_bridge_panel(d, img, px, py, pw, ph)
    headline_bar(d, px, py + ph - 2, pw, 92,
                 ["UKRAINE STRIKES CRIMEA BRIDGE AGAIN"],
                 size=42,
                 sub="Second day in a row \u2014 Kyiv hails an \u2018unprecedented operation\u2019",
                 sub_size=21)

    # ---- two panels ----
    y2, h2 = 574, 250
    draw_hormuz_panel(d, img, 14, y2, 488, h2)
    headline_bar(d, 14, y2 + h2 - 2, 488, 86,
                 ["TANKERS HIT BY MINES"], size=33,
                 sub="Near Hormuz \u2014 US carrier joins Gulf build-up", sub_size=19)
    draw_shenzhen_panel(d, img, 522, y2, 488, h2)
    headline_bar(d, 522, y2 + h2 - 2, 488, 86,
                 ["XI, TRUMP & PUTIN TO MEET"], size=33,
                 sub="Trilateral confirmed for Thursday in Shenzhen", sub_size=19)

    # ---- also today ----
    y3 = 922
    d.rectangle([14, y3, 1010, y3 + 2], fill=RED)
    d.text((14, y3 + 8), "ALSO TODAY", font=font("sans_b", 21), fill=RED, anchor="la")
    items = [
        "Pentagon fails its audit \u2014 9th year in a row",
        "US banks hit by Zelle outage after JPMorgan glitch",
        "Measles cases in US highest since 1991",
    ]
    yy = y3 + 34
    for it in items:
        d.text((16, yy), "\u25aa", font=font("sans_b", 17), fill=RED, anchor="la")
        d.text((40, yy), it, font=font("sans", 20), fill=INK, anchor="la")
        yy += 22

    img.convert("RGB").save("entry.png", "JPEG", quality=88, optimize=True)
    print("saved entry.png", os.path.getsize("entry.png"), "bytes")


if __name__ == "__main__":
    main()
