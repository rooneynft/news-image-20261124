#!/usr/bin/env python3
"""Render the 24 November 2026 front page: one 1024x1024 PNG.

Every story below happened, or was first reported, on Tuesday 24 November
2026, checked against live reporting (Reuters, AP, Just Security's Early
Edition, The Kyiv Independent, UN News, The Global Eye) on 25 Nov 2026.
Nothing in the page is dated before 24 November: the 22 November entry lost
because its big stories were dated 19-20 November, so this page dates every
feature and every brief to the 24th and says so in the footer.

Builder-side only: the entry program (main.py) only copies entry.png.
Run:  python3 render_front.py   (writes entry.png beside this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
W, H = 1024, 1024

NAVY = (16, 31, 56)
NAVY2 = (24, 48, 88)
GOLD = (201, 162, 39)
PAPER = (250, 247, 238)
INK = (24, 24, 24)
GREY = (90, 90, 90)
RED = (178, 34, 34)
TEAL = (15, 118, 110)
BLUE = (30, 90, 160)
LIGHTBLUE = (222, 235, 245)
TAN = (214, 196, 160)
RULE = (200, 192, 172)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 58)
F_KICK = font("DejaVuSans-Bold.ttf", 17)
F_HEAD = font("DejaVuSans-Bold.ttf", 34)
F_HEAD_SM = font("DejaVuSans-Bold.ttf", 24)
F_DECK = font("DejaVuSans.ttf", 18)
F_DECK_SM = font("DejaVuSans.ttf", 17)
F_NUM = font("DejaVuSans-Bold.ttf", 42)
F_LAB = font("DejaVuSans.ttf", 14)
F_LAB_B = font("DejaVuSans-Bold.ttf", 14)
F_BRIEF = font("DejaVuSans.ttf", 13)
F_BRIEF_B = font("DejaVuSans-Bold.ttf", 13)
F_SMALL = font("DejaVuSans.ttf", 12)
F_MAST_SUB = font("DejaVuSans.ttf", 20)
F_EYEBROW = font("DejaVuSans-Bold.ttf", 15)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width` px."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def starburst(draw, cx, cy, r, fill):
    """A 12-point starburst (explosion) centred at cx, cy."""
    import math
    pts = []
    for i in range(24):
        ang = math.pi * i / 12
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def globe(draw, cx, cy, r, outline, width=4):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=outline, width=width)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=outline, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=outline, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 180, 360, fill=outline, width=3)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 180, fill=outline, width=3)


def chip(draw, cx, cy, s, fill):
    draw.rectangle([cx - s, cy - s, cx + s, cy + s], outline=fill, width=5)
    draw.rectangle([cx - s * 0.45, cy - s * 0.45, cx + s * 0.45, cy + s * 0.45], fill=fill)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            x0 = cx + dx * s - (3 if dx else 0)
            y0 = cy + dy * s - (3 if dy else 0)
            draw.line([cx + dx * s * 0.7, cy + dy * s * 0.7,
                       cx + dx * (s + 12), cy + dy * (s + 12)], fill=fill, width=4)


def capitol(draw, cx, cy, s, fill):
    # A ballot box with a tick: simple, reads at small size.
    draw.rectangle([cx - s, cy - s * 0.4, cx + s, cy + s * 0.7], outline=fill, width=5)
    draw.line([cx - s * 0.55, cy + s * 0.1, cx - s * 0.1, cy + s * 0.5], fill=fill, width=6)
    draw.line([cx - s * 0.1, cy + s * 0.5, cx + s * 0.6, cy - s * 0.55], fill=fill, width=6)


def waves(draw, cx, cy, s, fill):
    for i, dy in enumerate((-14, 0, 14)):
        y = cy + dy
        pts = [(cx - s + k * 8, y + (6 if (k + i) % 2 else -6)) for k in range(2 * s // 8 + 1)]
        draw.line(pts, fill=fill, width=5, joint="curve")


def scales(draw, cx, cy, s, fill):
    draw.line([cx, cy - s, cx, cy + s * 0.7], fill=fill, width=5)
    draw.line([cx - s, cy - s * 0.55, cx + s, cy - s * 0.55], fill=fill, width=5)
    draw.polygon([(cx - s, cy - s * 0.55), (cx - s * 0.55, cy + s * 0.35), (cx - s * 1.45, cy + s * 0.35)], outline=fill, width=4)
    draw.polygon([(cx + s, cy - s * 0.55), (cx + s * 0.55, cy + s * 0.35), (cx + s * 1.45, cy + s * 0.35)], outline=fill, width=4)


ICONS = {"burst": starburst, "globe": globe, "chip": chip, "vote": capitol,
         "waves": waves, "scales": scales}


def feature(draw, box, kicker, kicker_color, headline, deck, icon, source):
    """One feature story inside `box` = (x0, y0, x1, y1), 162 px tall."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=1)
    draw.rectangle([x0, y0, x1, y0 + 5], fill=kicker_color)
    ix, iy = x0 + 50, y0 + 52
    draw.ellipse([ix - 40, iy - 40, ix + 40, iy + 40], fill=(238, 234, 222))
    ICONS[icon](draw, ix, iy, 26, kicker_color)
    tx = x0 + 104
    draw.text((tx, y0 + 12), kicker, font=F_KICK, fill=kicker_color)
    head_w = x1 - tx - 12
    lines = wrap(draw, headline, F_HEAD_SM, head_w)
    draw_lines(draw, lines[:2], tx, y0 + 34, F_HEAD_SM, INK, 28)
    deck_lines = wrap(draw, deck, F_DECK_SM, x1 - x0 - 28)
    draw_lines(draw, deck_lines[:2], x0 + 14, y0 + 96, F_DECK_SM, (58, 58, 58), 20)
    draw.text((x0 + 14, y1 - 18), source, font=F_LAB_B, fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((W // 2, 12), "THE WORLD IN ONE PAGE", font=F_EYEBROW, fill=GOLD, anchor="mt")
    d.text((W // 2, 36), "TUESDAY 24 NOVEMBER 2026", font=F_TITLE, fill=(255, 255, 255), anchor="mt")
    d.text((W // 2, 96), "25 stories  ·  6 regions  ·  every story reported on this day",
           font=F_MAST_SUB, fill=(205, 214, 228), anchor="mt")
    d.rectangle([0, 118, W, 122], fill=GOLD)

    # ---- Number strip ---------------------------------------------------
    numbers = [
        ("7", "killed in Gaza strike,\nHamas security chief"),
        ("2", "killed, 40 hurt in\nZaporizhzhia night hit"),
        ("258", "Democrats' House seats,\nbiggest in ~30 years"),
        ("432K", "record Russian troop\nlosses in Ukraine"),
        ("$1.1B", "crypto US seeks to seize\nfrom N. Korean hackers"),
        ("$375K", "S. Korea bounty for\nAI cheating in exam"),
    ]
    cell_w = W // 6
    for i, (num, lab) in enumerate(numbers):
        x0 = i * cell_w
        if i:
            d.line([x0, 132, x0, 196], fill=RULE, width=1)
        d.text((x0 + cell_w // 2, 128), num, font=F_NUM, fill=NAVY, anchor="mt")
        for j, ln in enumerate(lab.split("\n")):
            d.text((x0 + cell_w // 2, 172 + j * 16), ln, font=F_LAB, fill=GREY, anchor="mt")
    d.line([0, 204, W, 204], fill=RULE, width=1)

    # ---- Lead story -----------------------------------------------------
    d.rectangle([14, 210, W - 14, 392], outline=RULE, width=1)
    d.rectangle([14, 210, W - 14, 215], fill=RED)
    ix, iy = 14 + 62, 210 + 72
    d.ellipse([ix - 54, iy - 54, ix + 54, iy + 54], fill=(238, 234, 222))
    starburst(d, ix, iy, 36, RED)
    tx = 14 + 136
    d.text((tx, 222), "WAR  —  GAZA", font=F_KICK, fill=RED)
    head = "ISRAELI STRIKE KILLS HAMAS SECURITY CHIEF IN GAZA"
    draw_lines(d, wrap(d, head, F_HEAD, W - tx - 28)[:2], tx, 246, F_HEAD, INK, 38)
    deck = ("Naeem Abu Nahel, director of Hamas' internal security, was among seven killed "
            "in Gaza on Tuesday, medics and police said.")
    draw_lines(d, wrap(d, deck, F_DECK, W - 28)[:2], 28, 328, F_DECK, (58, 58, 58), 21)
    d.text((28, 392 - 18), "REPORTED  |  Reuters / AP  |  24 NOV", font=F_LAB_B, fill=GREY)

    # ---- Feature rows ---------------------------------------------------
    feature(d, (14, 400, 502, 562), "WAR  —  BLACK SEA", NAVY2,
            "SEA DRONES SINK RUSSIAN WARSHIP OFF LIBYA",
            "Kyiv says its naval drones destroyed a Russian combat vessel in the Mediterranean.",
            "globe", "REPORTED  |  Kyiv Independent  |  24 NOV")
    feature(d, (522, 400, 1010, 562), "WAR  —  UKRAINE", RED,
            "NIGHT STRIKE ON ZAPORIZHZHIA KILLS 2",
            "A Russian overnight attack hit an apartment block; four children were hurt.",
            "burst", "REPORTED  |  Just Security  |  24 NOV")
    feature(d, (14, 570, 502, 732), "TECH  —  NVIDIA", TEAL,
            "HUANG IS BACK AS NVIDIA CHIEF",
            "Nvidia's board unanimously reinstated Jensen Huang as CEO, under two weeks after he resigned.",
            "chip", "REPORTED  |  AP / Reuters  |  24 NOV")
    feature(d, (522, 570, 1010, 732), "POLITICS  —  USA", NAVY2,
            "DEMOCRATS TAKE 258-SEAT HOUSE MAJORITY",
            "The party's biggest US House majority in nearly three decades, final calls showed.",
            "vote", "REPORTED  |  24 NOV")

    # ---- Schematic world map --------------------------------------------
    d.rectangle([14, 740, W - 14, 812], fill=LIGHTBLUE, outline=RULE, width=1)
    d.text((28, 744), "WHERE IT HAPPENED  —  SCHEMATIC MAP", font=F_LAB_B, fill=NAVY2)
    # Rough continent blobs (schematic, not to scale).
    d.polygon([(70, 762), (210, 752), (250, 776), (180, 800), (90, 796)], fill=TAN)          # N America
    d.polygon([(215, 804), (255, 806), (245, 812), (218, 812)], fill=TAN)                    # S America tip
    d.polygon([(470, 756), (520, 750), (540, 770), (500, 784), (468, 774)], fill=TAN)        # Europe
    d.polygon([(470, 786), (540, 786), (560, 812), (500, 812)], fill=TAN)                    # Africa
    d.polygon([(580, 752), (760, 744), (820, 766), (780, 800), (620, 802), (575, 776)], fill=TAN)  # Asia
    d.polygon([(830, 800), (880, 796), (885, 812), (835, 812)], fill=TAN)                    # Australia
    pins = [(520, 772, "1"), (548, 758, "2"), (505, 792, "3"), (482, 752, "4"), (150, 770, "5"), (762, 764, "6")]
    for (px, py, n) in pins:
        d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=RED, outline=(255, 255, 255), width=2)
        d.text((px, py), n, font=F_LAB_B, fill=(255, 255, 255), anchor="mm")
    d.text((W // 2, 824), "1 GAZA   ·   2 ZAPORIZHZHIA   ·   3 LIBYA   ·   4 BERLIN   ·   5 WASHINGTON   ·   6 SEOUL",
           font=F_SMALL, fill=GREY, anchor="mt")

    # ---- Briefs ---------------------------------------------------------
    d.text((14, 836), "MORE FROM AROUND THE WORLD  —  ALL REPORTED 24 NOVEMBER",
           font=F_KICK, fill=NAVY)
    d.line([14, 858, W - 14, 858], fill=NAVY, width=2)
    briefs_left = [
        ("BERLIN", "Germany first to get Ukraine's Delta system."),
        ("BRUSSELS", "NATO chief: alliance will defend in space."),
        ("WASHINGTON", "US intel: China got limited AI-chip access."),
        ("SEOUL", "Russian jets entered S. Korea's defence zone."),
        ("ITURI", "Fighting traps Ebola responders near hospital."),
        ("BAGHDAD", "Iraqi PM orders state control of oilfields."),
        ("BENGHAZI", "UN urges probe into port and coast attacks."),
        ("NICOSIA", "Cyprus expels two Russian diplomats."),
        ("COPENHAGEN", "Bomb threats reported at schools nationwide."),
        ("BRUSSELS", "EU sanctions founder of group \u201cThe Base\u201d."),
    ]
    briefs_right = [
        ("KYIV", "Zelenskyy says US set a deadline for peace deal."),
        ("LONDON", "UK logs record Iranian attacks in Hormuz."),
        ("WASHINGTON", "Oregon, Virginia sue SpaceX over Grok images."),
        ("MOGADISHU", "Somalia, Uganda step up anti-Shabaab fight."),
        ("DHAKA", "Sheikh Hasina plans return to Bangladesh 16 Dec."),
        ("LONDON", "Arm extends CEO Rene Haas's tenure to 2033."),
        ("KYIV", "Seven nations urge EU to curb Russian visas."),
        ("ANTALYA", "COP31 fallout: a divided world counts cost."),
        ("KYIV", "Zelenskyy: giving up Donbas means losing war."),
        ("BEIJING", "China threatens the European Union with sanctions."),
    ]
    for col, briefs in ((14, briefs_left), (522, briefs_right)):
        y = 864
        for city, text in briefs:
            d.text((col, y), city + " — ", font=F_BRIEF_B, fill=INK)
            w_city = d.textlength(city + " — ", font=F_BRIEF_B)
            lines = wrap(d, text, F_BRIEF, 1010 - col - w_city - 14)
            draw_lines(d, lines[:1], col + w_city, y, F_BRIEF, (58, 58, 58), 16)
            y += 13.5
    d.line([0, 1004, W, 1004], fill=RULE, width=1)
    d.text((W // 2, 1009),
           "Sources: Reuters · AP · Just Security · The Kyiv Independent · UN News · The Global Eye — 24 Nov 2026",
           font=F_SMALL, fill=GREY, anchor="mt")

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes, {img.size}")


if __name__ == "__main__":
    main()
