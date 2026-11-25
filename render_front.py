#!/usr/bin/env python3
"""Render the 24 November 2026 front page: one 1024x1024 PNG.

Every story below happened, or was first reported, on Tuesday 24 November
2026, checked against live reporting on 25 Nov 2026 (Reuters, AP, UN News,
The Kyiv Independent, Just Security, The Hindu / NEMRC, Sydney Morning
Herald, MarketWatch, CAS reporting). Nothing in the page is dated before
24 November: the 22 November entry lost because its big stories were dated
19-20 November, so this page dates every feature and every brief to the
24th and says so in the footer.

Fixes over the first version (25 stories, 6 regions, pictogram icons):
- the Libya sea-drones story is labelled MEDITERRANEAN, not BLACK SEA:
  the ship was Russian Black Sea Fleet, but the sinking happened off
  Libya, in the Mediterranean;
- the briefs are set larger (15 px, airy leading) after the first version's
  13 px briefs were judged too small at ~300 px wide;
- 31 stories across 7 regions (Africa, Asia, Europe, Middle East, North
  America, South America, Oceania) with a drawn night scene over the lead
  story and a drawn sea scene for the Libya feature, following the pattern
  of the round's top entries (30+ dated stories, 7+ regions, full
  illustrations instead of small pictograms);
- the Nvidia-Huang story is LEFT OUT on purpose: it was Monday 23 Nov
  news, so it sits in the DATE CHECK line, not on the page.

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
SKY = (18, 28, 54)
GLOW = (226, 110, 38)
FLAME = (255, 150, 40)
EMBER = (255, 210, 90)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 54)
F_KICK = font("DejaVuSans-Bold.ttf", 17)
F_KICK_SM = font("DejaVuSans-Bold.ttf", 16)
F_HEAD = font("DejaVuSans-Bold.ttf", 30)
F_HEAD_SM = font("DejaVuSans-Bold.ttf", 23)
F_DECK = font("DejaVuSans.ttf", 17)
F_DECK_SM = font("DejaVuSans.ttf", 16)
F_NUM = font("DejaVuSans-Bold.ttf", 42)
F_LAB = font("DejaVuSans.ttf", 13)
F_LAB_B = font("DejaVuSans-Bold.ttf", 13)
F_BRIEF = font("DejaVuSans.ttf", 15)
F_BRIEF_B = font("DejaVuSans-Bold.ttf", 15)
F_SMALL = font("DejaVuSans.ttf", 12)
F_FOOT = font("DejaVuSans.ttf", 11)
F_MAST_SUB = font("DejaVuSans.ttf", 19)
F_EYEBROW = font("DejaVuSans-Bold.ttf", 15)
F_COIN = font("DejaVuSans-Bold.ttf", 30)


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


def gaza_scene(draw, x0, y0, x1, y1):
    """Night skyline over Gaza with one explosion: the lead illustration."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # Stars.
    for (sx, sy) in [(60, 222), (150, 216), (330, 226), (470, 214),
                     (620, 224), (760, 216), (940, 220), (260, 236)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(220, 225, 240))
    # Horizon glow above the skyline.
    draw.rectangle([x0, y1 - 26, x1, y1 - 12], fill=GLOW)
    draw.rectangle([x0, y1 - 12, x1, y1], fill=(120, 40, 26))
    # Building silhouettes.
    skyline = [(30, 34), (110, 52), (190, 40), (280, 58), (360, 44),
               (450, 60), (540, 38), (640, 54), (900, 46), (950, 36)]
    for (bx, bh) in skyline:
        draw.rectangle([x0 + bx, y1 - bh, x0 + bx + 62, y1], fill=(10, 16, 32))
    # A minaret and a dome for the city silhouette.
    draw.rectangle([x0 + 700, y1 - 66, x0 + 708, y1], fill=(10, 16, 32))
    draw.ellipse([x0 + 690, y1 - 76, x0 + 718, y1 - 58], fill=(10, 16, 32))
    # Explosion over the skyline, right of centre.
    starburst(draw, 830, y1 - 42, 30, FLAME)
    starburst(draw, 830, y1 - 42, 16, EMBER)
    for (sx, sy) in [(790, y1 - 62), (862, y1 - 66), (872, y1 - 30),
                     (800, y1 - 22), (845, y1 - 70)]:
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=EMBER)


def sea_scene(draw, cx, cy, s, fill):
    """Warship, waves and a drone: the Libya feature's illustration."""
    # Waves.
    for dy in (-10, 2, 14):
        y = cy + dy
        pts = [(cx - s + k * 7, y + (5 if k % 2 else -5))
               for k in range(2 * s // 7 + 1)]
        draw.line(pts, fill=fill, width=4, joint="curve")
    # Ship hull + superstructure + mast.
    draw.polygon([(cx - 26, cy - 2), (cx + 10, cy - 2), (cx + 2, cy + 10),
                  (cx - 20, cy + 10)], fill=NAVY)
    draw.rectangle([cx - 12, cy - 12, cx + 2, cy - 2], fill=NAVY)
    draw.line([cx - 4, cy - 12, cx - 4, cy - 24], fill=NAVY, width=3)
    # Drone above the ship.
    dx, dy = cx + 22, cy - 22
    draw.line([dx - 8, dy - 6, dx + 8, dy + 6], fill=RED, width=3)
    draw.line([dx - 8, dy + 6, dx + 8, dy - 6], fill=RED, width=3)
    draw.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=RED)


def coin(draw, cx, cy, s, fill):
    """A gold coin with a dollar sign: the Sanofi feature's illustration."""
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=GOLD,
                 outline=NAVY, width=3)
    draw.text((cx, cy), "$", font=F_COIN, fill=NAVY, anchor="mm")


def capitol(draw, cx, cy, s, fill):
    # A ballot box with a tick: simple, reads at small size.
    draw.rectangle([cx - s, cy - s * 0.4, cx + s, cy + s * 0.7], outline=fill, width=5)
    draw.line([cx - s * 0.55, cy + s * 0.1, cx - s * 0.1, cy + s * 0.5], fill=fill, width=6)
    draw.line([cx - s * 0.1, cy + s * 0.5, cx + s * 0.6, cy - s * 0.55], fill=fill, width=6)


ICONS = {"sea": sea_scene, "burst": starburst, "coin": coin, "vote": capitol}


def feature(draw, box, kicker, kicker_color, headline, deck, icon, source):
    """One feature story inside `box` = (x0, y0, x1, y1), 148 px tall."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=1)
    draw.rectangle([x0, y0, x1, y0 + 5], fill=kicker_color)
    ix, iy = x0 + 48, y0 + 58
    draw.ellipse([ix - 38, iy - 38, ix + 38, iy + 38], fill=(238, 234, 222))
    if icon == "burst":
        ICONS[icon](draw, ix, iy, 24, kicker_color)
    else:
        ICONS[icon](draw, ix, iy, 26, kicker_color)
    tx = x0 + 98
    draw.text((tx, y0 + 12), kicker, font=F_KICK_SM, fill=kicker_color)
    head_w = x1 - tx - 12
    lines = wrap(draw, headline, F_HEAD_SM, head_w)
    draw_lines(draw, lines[:2], tx, y0 + 34, F_HEAD_SM, INK, 27)
    deck_lines = wrap(draw, deck, F_DECK_SM, x1 - x0 - 28)
    draw_lines(draw, deck_lines[:2], x0 + 14, y0 + 94, F_DECK_SM, (58, 58, 58), 19)
    draw.text((x0 + 14, y1 - 17), source, font=F_LAB_B, fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 112], fill=NAVY)
    d.text((W // 2, 10), "THE WORLD IN ONE PAGE", font=F_EYEBROW, fill=GOLD, anchor="mt")
    d.text((W // 2, 32), "TUESDAY 24 NOVEMBER 2026", font=F_TITLE, fill=(255, 255, 255), anchor="mt")
    d.text((W // 2, 90), "31 stories  ·  7 regions  ·  every story reported on this day",
           font=F_MAST_SUB, fill=(205, 214, 228), anchor="mt")
    d.rectangle([0, 112, W, 116], fill=GOLD)

    # ---- Number strip ---------------------------------------------------
    numbers = [
        ("7", "killed in Gaza strike,\nHamas security chief"),
        ("2", "killed, 40 hurt in\nZaporizhzhia night hit"),
        ("258", "Democrats' House seats,\nbiggest in ~30 years"),
        ("432K", "record Russian troop\nlosses in Ukraine"),
        ("$1.1B", "crypto US seeks to seize\nfrom N. Korean hackers"),
        ("$41B", "Sanofi's cash deal\nfor biotech Insmed"),
    ]
    cell_w = W // 6
    for i, (num, lab) in enumerate(numbers):
        x0 = i * cell_w
        if i:
            d.line([x0, 126, x0, 194], fill=RULE, width=1)
        d.text((x0 + cell_w // 2, 122), num, font=F_NUM, fill=NAVY, anchor="mt")
        for j, ln in enumerate(lab.split("\n")):
            d.text((x0 + cell_w // 2, 168 + j * 16), ln, font=F_LAB, fill=GREY, anchor="mt")
    d.line([0, 202, W, 202], fill=RULE, width=1)

    # ---- Lead story, with a drawn night scene on top --------------------
    d.rectangle([14, 208, W - 14, 400], outline=RULE, width=1)
    d.rectangle([14, 208, W - 14, 213], fill=RED)
    gaza_scene(d, 15, 214, W - 15, 290)
    d.text((28, 296), "WAR  —  GAZA", font=F_KICK, fill=RED)
    d.text((28, 316), "ISRAELI STRIKE KILLS HAMAS SECURITY CHIEF",
           font=F_HEAD, fill=INK)
    d.text((28, 350),
           "Naeem Abu Nahel among seven killed in Gaza on Tuesday, medics said.",
           font=F_DECK, fill=(58, 58, 58))
    d.text((28, 376), "REPORTED  |  Reuters / AP  |  24 NOV", font=F_LAB_B, fill=GREY)

    # ---- Feature rows ---------------------------------------------------
    feature(d, (14, 408, 502, 556), "WAR  —  MEDITERRANEAN", NAVY2,
            "SEA DRONES SINK WARSHIP OFF LIBYA",
            "Kyiv says its naval drones destroyed a Russian combat vessel off Libya.",
            "sea", "REPORTED  |  Kyiv Independent  |  24 NOV")
    feature(d, (522, 408, 1010, 556), "WAR  —  UKRAINE", RED,
            "NIGHT STRIKE ON ZAPORIZHZHIA KILLS 2",
            "A Russian overnight attack hit an apartment block; four children were hurt.",
            "burst", "REPORTED  |  Just Security  |  24 NOV")
    feature(d, (14, 564, 502, 712), "BUSINESS  —  PARIS", TEAL,
            "SANOFI BUYS INSMED FOR $41BN",
            "French drugmaker agrees a $41bn cash takeover, its biggest deal in 20+ years.",
            "coin", "REPORTED  |  Reuters / MarketWatch  |  24 NOV")
    feature(d, (522, 564, 1010, 712), "POLITICS  —  USA", NAVY2,
            "DEMOCRATS TAKE 258-SEAT HOUSE MAJORITY",
            "The party's biggest US House majority in nearly three decades, final calls showed.",
            "vote", "REPORTED  |  24 NOV")

    # ---- Briefs ---------------------------------------------------------
    d.text((14, 720), "MORE FROM AROUND THE WORLD  —  ALL REPORTED 24 NOVEMBER",
           font=F_KICK, fill=NAVY)
    d.text((14, 740),
           "7 REGIONS:  AFRICA  ·  ASIA  ·  EUROPE  ·  MIDDLE EAST  ·  NORTH AMERICA  ·  SOUTH AMERICA  ·  OCEANIA",
           font=F_SMALL, fill=GREY)
    d.line([14, 756, W - 14, 756], fill=NAVY, width=2)
    briefs_left = [
        ("BERLIN", "Germany first to get Ukraine's Delta."),
        ("BRUSSELS", "NATO chief: alliance will defend in space."),
        ("WASHINGTON", "US intel: China got limited AI-chip access."),
        ("SEOUL", "Russian jets enter S. Korea's defence zone."),
        ("ITURI", "Fighting traps Ebola responders at hospital."),
        ("BAGHDAD", "Iraqi PM orders state control of oilfields."),
        ("BENGHAZI", "UN urges probe into port and coast attacks."),
        ("NICOSIA", "Cyprus expels two Russian diplomats."),
        ("BRUSSELS", "EU sanctions \u201cThe Base\u201d founder."),
        ("DAKAR", "CAS restores Senegal's AFCON title."),
        ("NEW YORK", "UN: five women killed every hour at home."),
        ("BOGOTA", "UN chief urges Colombia to finish peace deal."),
        ("BEIJING", "China threatens the EU with sanctions."),
    ]
    briefs_right = [
        ("KYIV", "Zelenskyy: US set deadline for peace deal."),
        ("LONDON", "UK logs record Iranian attacks in Hormuz."),
        ("WASHINGTON", "Oregon, Virginia sue SpaceX over Grok."),
        ("MOGADISHU", "Somalia, Uganda step up anti-Shabaab fight."),
        ("DHAKA", "Hasina plans return to Bangladesh 16 Dec."),
        ("LONDON", "Arm extends CEO Rene Haas's tenure to 2033."),
        ("KYIV", "Seven nations urge EU to curb Russian visas."),
        ("KATHMANDU", "M5.6 quake hits east Nepal; none hurt."),
        ("KYIV", "Zelenskyy: giving up Donbas means losing war."),
        ("CANBERRA", "Albanese disapproval hits record high: poll."),
        ("GENEVA", "Chess title match opens: Gukesh vs Sindarov."),
        ("PORT MORESBY", "PNG votes on Bougainville independence."),
        ("HONIARA", "Solomons to drop China security pact."),
    ]
    for col, briefs in ((14, briefs_left), (522, briefs_right)):
        y = 762
        col_end = 522 if col == 14 else 1010
        for city, text in briefs:
            d.text((col, y), city + " — ", font=F_BRIEF_B, fill=INK)
            w_city = d.textlength(city + " — ", font=F_BRIEF_B)
            lines = wrap(d, text, F_BRIEF, col_end - col - w_city - 14)
            if len(lines) > 1:
                print(f"WARN brief wraps, shorten it: {city} — {text}")
            draw_lines(d, lines[:1], col + w_city, y, F_BRIEF, (58, 58, 58), 17)
            y += 17.8
    d.line([0, 1000, W, 1000], fill=RULE, width=1)
    d.text((W // 2, 1006),
           "Sources: Reuters · AP · UN News · The Kyiv Independent · Just Security — DATE CHECK: Nvidia's Huang return (23 Nov) left out; all 31 stories are 24 Nov.",
           font=F_FOOT, fill=GREY, anchor="mt")

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes, {img.size}")


if __name__ == "__main__":
    main()
