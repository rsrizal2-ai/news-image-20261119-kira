#!/usr/bin/env python3
"""Render the news poster for Thursday, 19 November 2026.

Draws a newspaper-style infographic with PIL and the Noto Sans fonts:
a masthead naming the day, six story cards (each with a small drawn
icon), and an "also today" strip. Writes entry.png next to this file.
Run: python3 render_poster.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONT_DIR = Path("/usr/share/fonts/truetype/noto")

W, H = 1024, 1024
PAPER = (244, 241, 234)
INK = (18, 30, 44)
NAVY = (16, 38, 63)
NAVY_DARK = (10, 26, 44)
RED = (178, 44, 34)
CARD = (255, 255, 255)
CARD_EDGE = (210, 204, 188)
GREY = (90, 98, 108)
LIGHT = (214, 222, 232)


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


F_DATE = font("NotoSans-ExtraBold.ttf", 47)
F_KICKER = font("NotoSans-Bold.ttf", 20)
F_SUB = font("NotoSans-Regular.ttf", 21)
F_TAG = font("NotoSans-Bold.ttf", 16)
F_HEAD = font("NotoSans-ExtraBold.ttf", 28)
F_BODY = font("NotoSans-Regular.ttf", 20)
F_STRIP_HEAD = font("NotoSans-Black.ttf", 18)
F_STRIP = font("NotoSans-Regular.ttf", 20)
F_FOOT = font("NotoSans-Regular.ttf", 16)
F_BADGE_TOP = font("NotoSans-Bold.ttf", 20)
F_BADGE_NUM = font("NotoSans-Black.ttf", 52)


def text_w(draw, s, f):
    box = draw.textbbox((0, 0), s, font=f)
    return box[2] - box[0]


def draw_burst(draw, cx, cy, r1, r2, colour, spikes=10):
    import math

    pts = []
    for i in range(spikes * 2):
        r = r1 if i % 2 == 0 else r2
        ang = math.pi * i / spikes - math.pi / 2
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=colour)


def icon_summit(draw, x, y, s):
    # Skyline with three flags for the three leaders' meeting.
    base = y + s * 0.88
    heights = (0.52, 0.72, 0.42, 0.62)
    bw = (s - 16) / 4
    for i, hh in enumerate(heights):
        bx = x + 8 + i * bw
        draw.rectangle([bx, base - s * hh, bx + bw - 5, base],
                       fill=(38, 64, 92))
        draw.rectangle([bx + 4, base - s * hh + 8, bx + bw - 9,
                        base - s * hh + 14], fill=(246, 196, 64))
    for i, col in enumerate(((200, 40, 40), (40, 90, 170), (220, 220, 220))):
        fx = x + 12 + i * (s - 24) / 3
        draw.line([fx, y + 4, fx, y + 30], fill=INK, width=2)
        draw.rectangle([fx, y + 4, fx + 20, y + 18], fill=col,
                       outline=INK, width=1)


def icon_bridge(draw, x, y, s):
    # A bridge deck with a gap in the middle, over waves.
    mid = y + s * 0.45
    draw.rectangle([x + 4, mid, x + s * 0.40, mid + 10], fill=(70, 80, 92))
    draw.rectangle([x + s * 0.60, mid, x + s - 4, mid + 10], fill=(70, 80, 92))
    draw.line([x + s * 0.40, mid + 5, x + s * 0.46, y + s * 0.72],
              fill=(178, 44, 34), width=5)
    draw.line([x + s * 0.60, mid + 5, x + s * 0.54, y + s * 0.72],
              fill=(178, 44, 34), width=5)
    for wy in (0.80, 0.88):
        for k in range(4):
            wx = x + 6 + k * (s - 12) / 4
            draw.arc([wx, y + s * wy, wx + (s - 12) / 4, y + s * wy + 12],
                     start=200, end=340, fill=(31, 97, 141), width=3)


def icon_ballot(draw, x, y, s):
    # A ballot box with a large tick.
    draw.rectangle([x + s * 0.14, y + s * 0.46, x + s * 0.86, y + s * 0.90],
                   fill=(46, 111, 168))
    draw.rectangle([x + s * 0.08, y + s * 0.34, x + s * 0.92, y + s * 0.50],
                   fill=(31, 78, 122))
    draw.rectangle([x + s * 0.38, y + s * 0.39, x + s * 0.62, y + s * 0.45],
                   fill=(244, 241, 234))
    draw.line([x + s * 0.28, y + s * 0.66, x + s * 0.44, y + s * 0.79],
              fill=(255, 255, 255), width=7)
    draw.line([x + s * 0.44, y + s * 0.79, x + s * 0.74, y + s * 0.52],
              fill=(255, 255, 255), width=7)


def icon_cyclone(draw, x, y, s):
    # Spiral bands around a calm eye, over the sea.
    cx, cy = x + s / 2, y + s * 0.44
    for r, col in ((38, (20, 143, 119)), (30, (46, 170, 145)),
                   (22, (110, 200, 180)), (14, (170, 225, 210))):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
                 fill=col, width=7)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(246, 196, 64),
                 outline=INK, width=1)
    for wy in (0.80, 0.89):
        for k in range(4):
            wx = x + 6 + k * (s - 12) / 4
            draw.arc([wx, y + s * wy, wx + (s - 12) / 4, y + s * wy + 11],
                     start=200, end=340, fill=(31, 97, 141), width=3)


def icon_scales(draw, x, y, s):
    # Balance scales: a pillar, a beam, two hanging pans.
    cx = x + s / 2
    draw.rectangle([cx - 3, y + s * 0.16, cx + 3, y + s * 0.86],
                   fill=(70, 80, 92))
    draw.rectangle([x + s * 0.30, y + s * 0.84, x + s * 0.70, y + s * 0.90],
                   fill=(70, 80, 92))
    draw.line([x + s * 0.14, y + s * 0.24, x + s * 0.86, y + s * 0.24],
              fill=(70, 80, 92), width=5)
    draw.ellipse([cx - 5, y + s * 0.10, cx + 5, y + s * 0.20],
                 fill=(246, 196, 64), outline=INK, width=1)
    for px in (0.22, 0.78):
        pxc = x + s * px
        draw.line([pxc, y + s * 0.24, pxc, y + s * 0.46], fill=INK, width=2)
        draw.line([pxc - 15, y + s * 0.30, pxc, y + s * 0.46], fill=INK,
                  width=2)
        draw.line([pxc + 15, y + s * 0.30, pxc, y + s * 0.46], fill=INK,
                  width=2)
        draw.pieslice([pxc - 18, y + s * 0.44, pxc + 18, y + s * 0.80],
                      start=0, end=180, fill=(125, 60, 152))
        draw.line([pxc - 18, y + s * 0.62, pxc + 18, y + s * 0.62],
                  fill=(125, 60, 152), width=3)


def icon_controller(draw, x, y, s):
    # A game controller: body, d-pad and four buttons.
    draw.rounded_rectangle([x + s * 0.08, y + s * 0.28, x + s * 0.92,
                            y + s * 0.82], radius=18, fill=(46, 111, 168))
    draw.ellipse([x + s * 0.08, y + s * 0.62, x + s * 0.30, y + s * 0.92],
                 fill=(31, 78, 122))
    draw.ellipse([x + s * 0.70, y + s * 0.62, x + s * 0.92, y + s * 0.92],
                 fill=(31, 78, 122))
    dx, dy = x + s * 0.28, y + s * 0.52
    draw.rectangle([dx - 5, dy - 15, dx + 5, dy + 15], fill=(255, 255, 255))
    draw.rectangle([dx - 15, dy - 5, dx + 15, dy + 5], fill=(255, 255, 255))
    for bx, by, col in ((0.62, 0.42, (246, 196, 64)), (0.72, 0.52, (178, 44, 34)),
                        (0.62, 0.62, (20, 143, 119)), (0.52, 0.52, (255, 255, 255))):
        cx, cy = x + s * bx, y + s * by
        draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=col,
                     outline=(255, 255, 255), width=1)


STORIES = [
    ("APEC  •  SHENZHEN", (146, 112, 8), icon_summit,
     ["Trump, Xi, Putin", "meet in Shenzhen"],
     ["First trilateral talks at APEC;", "leaders gather in China."]),
    ("UKRAINE", (31, 97, 141), icon_bridge,
     ["Crimean Bridge", "hit a third time"],
     ["Traffic suspended after attack;", "damage being assessed."]),
    ("USA", (46, 111, 168), icon_ballot,
     ["Jeffries nominated", "for Speaker"],
     ["House Democrats back him 251-11;", "first Black Speaker if elected."]),
    ("INDIA", (20, 143, 119), icon_cyclone,
     ["Cyclone Akvan", "nears India"],
     ["Red alert on Andhra coast;", "200,000+ to evacuate."]),
    ("THE HAGUE", (125, 60, 152), icon_scales,
     ["World court rules", "on Myanmar case"],
     ["ICJ delivers genocide verdict;", "2017 Rohingya crackdown at issue."]),
    ("CULTURE", (178, 44, 34), icon_controller,
     ["GTA VI launches", "worldwide"],
     ["After a 13-year wait, Rockstar's", "Vice City game arrives."]),
]


def draw_card(draw, x, y, w, h, story):
    tag, colour, icon, head, body = story
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=CARD,
                           outline=CARD_EDGE, width=2)
    # Tag pill.
    pad = 16
    tw = text_w(draw, tag, F_TAG) + 22
    draw.rounded_rectangle([x + pad, y + pad, x + pad + tw, y + pad + 28],
                           radius=14, fill=colour)
    draw.text((x + pad + 11, y + pad + 4), tag, font=F_TAG,
              fill=(255, 255, 255))
    # Icon box, top right.
    ix, iy, isize = x + w - pad - 92, y + pad, 92
    draw.rounded_rectangle([ix, iy, ix + isize, iy + isize], radius=10,
                           fill=(238, 235, 227), outline=CARD_EDGE, width=1)
    icon(draw, ix, iy, isize)
    # Headline under the tag.
    hy = y + pad + 40
    for line in head:
        draw.text((x + pad, hy), line, font=F_HEAD, fill=INK)
        hy += 34
    # Body text.
    by = hy + 6
    for line in body:
        draw.text((x + pad, by), line, font=F_BODY, fill=(52, 62, 74))
        by += 27
    # Accent bar along the bottom of the card.
    draw.line([x + pad, y + h - 14, x + w - pad, y + h - 14], fill=colour,
              width=4)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead.
    mx, my, mw, mh = 26, 26, W - 52, 148
    draw.rounded_rectangle([mx, my, mx + mw, my + mh], radius=16, fill=NAVY)
    draw.rectangle([mx + 16, my + mh - 7, mx + mw - 16, my + mh - 1],
                   fill=RED)
    draw.text((mx + 26, my + 18), "W O R L D   N E W S   I N   O N E   I M A G E",
              font=F_KICKER, fill=(246, 196, 64))
    draw.text((mx + 24, my + 46), "Thursday, 19 November 2026",
              font=F_DATE, fill=(255, 255, 255))
    draw.text((mx + 26, my + 108),
              "The day's most consequential stories, as reported on 19 November 2026",
              font=F_SUB, fill=LIGHT)
    # Calendar badge.
    bx, by, bs = mx + mw - 122, my + 20, 96
    draw.rounded_rectangle([bx, by, bx + bs, by + bs], radius=12,
                           fill=(255, 255, 255))
    draw.rectangle([bx, by, bx + bs, by + 26], fill=RED)
    label = "NOV"
    draw.text((bx + (bs - text_w(draw, label, F_BADGE_TOP)) / 2, by + 2),
              label, font=F_BADGE_TOP, fill=(255, 255, 255))
    num = "19"
    draw.text((bx + (bs - text_w(draw, num, F_BADGE_NUM)) / 2, by + 30),
              num, font=F_BADGE_NUM, fill=NAVY)

    # Story grid: 2 columns x 3 rows.
    gx, gy = 26, 188
    gap = 14
    cw = (W - 52 - gap) // 2
    ch = 224
    for i, story in enumerate(STORIES):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        draw_card(draw, cx, cy, cw, ch, story)

    # Also-today strip.
    sy = gy + 3 * ch + 2 * gap + gap
    draw.rounded_rectangle([26, sy, W - 26, sy + 88], radius=12,
                           fill=NAVY_DARK)
    draw.text((44, sy + 8), "ALSO TODAY", font=F_STRIP_HEAD,
              fill=(246, 196, 64))
    line1 = "Van Gogh sells for a record $190.4m  •  Voyager 1 passes one light-day from Earth"
    line2 = "EU proposes €45bn Ukraine loan  •  Israeli tanks cross Gaza ceasefire line"
    draw.text((44, sy + 32), line1, font=F_STRIP, fill=(255, 255, 255))
    draw.text((44, sy + 57), line2, font=F_STRIP, fill=(255, 255, 255))

    # Footer.
    foot = "Drawn infographic — no photographs.  Sources: Reuters, NYT, AP, BBC, IMD, ICJ."
    draw.text(((W - text_w(draw, foot, F_FOOT)) / 2, H - 26), foot,
              font=F_FOOT, fill=GREY)

    out = HERE / "entry.png"
    img.save(out, format="PNG")
    print(f"wrote {out} {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
