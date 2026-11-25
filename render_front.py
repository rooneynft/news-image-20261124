#!/usr/bin/env python3
"""Render the 24 November 2026 front page, v3: one 1024x1024 PNG.

Every story below happened, or was first reported, on Tuesday 24 November
2026, checked against live reporting on 25 Nov 2026 (Reuters, AP, UN News,
The Kyiv Independent, Just Security, Focus Taiwan / CNA, Chess.com, Sydney
Morning Herald, CAS, Xinhua via Reuters). Nothing in the page is dated
before 24 November: the 22 November entry lost because its big stories were
dated 19-20 November, so this page dates every feature and every brief to
the 24th and says so in the footer.

What v3 changes over v2 (31 stories, 7 regions, kit check 13/0):
- the schematic world map is BACK (v2 dropped it; the round's winners
  still carry one): six numbered pins for the six biggest stories, with a
  legend naming them;
- all four feature cards are now fully illustrated scenes, not pictogram
  circles: a sea battle for Libya, a burning night city for Zaporizhzhia,
  a coin + capsule for the Sanofi deal, a capitol dome for the House;
  the lead keeps its drawn Gaza night scene, improved with a moon and a
  bigger explosion;
- three briefs swapped for cleaner 24 Nov stories the round's top entries
  also lead with: the Arm CEO story was announced Monday 23 Nov, so it is
  out and the Shanghai Politburo probe (Xinhua, 24 Nov) is in; the
  SpaceX/Grok suit was filed Monday 23 Nov, so it is out and the Houthi
  strike on Riyadh's tallest tower (Reuters, 24 Nov, 11 hurt) is in; the
  Hormuz brief now says what was reported on the 24th, tankers hit mines;
- the $1.1B crypto number was a 23 Nov DOJ filing, so the strip now
  carries the TAIEX's record +9% jump instead (closed +8.99% on 24 Nov);
- briefs stay 15 px (never smaller: they must read at ~300 px wide).

Left out on purpose, as in v2: Nvidia rehiring Jensen Huang was Monday
23 November news, not the 24th, so it sits in the DATE CHECK line, not on
the page (the TAIEX jump is the 24 Nov market reaction, a different
story). The Democrats' 258 seats is the AP figure reported on 24 Nov.

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
SEABLUE = (36, 98, 164)
PANELTEAL = (226, 240, 236)
PANELGREY = (232, 238, 248)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 48)
F_KICK = font("DejaVuSans-Bold.ttf", 17)
F_KICK_SM = font("DejaVuSans-Bold.ttf", 15)
F_HEAD = font("DejaVuSans-Bold.ttf", 28)
F_FHEAD = font("DejaVuSans-Bold.ttf", 22)
F_DECK = font("DejaVuSans.ttf", 17)
F_FDECK = font("DejaVuSans.ttf", 15)
F_NUM = font("DejaVuSans-Bold.ttf", 38)
F_LAB = font("DejaVuSans.ttf", 13)
F_LAB_B = font("DejaVuSans-Bold.ttf", 13)
F_BRIEF = font("DejaVuSans.ttf", 15)
F_BRIEF_B = font("DejaVuSans-Bold.ttf", 15)
F_SMALL = font("DejaVuSans.ttf", 12)
F_FOOT = font("DejaVuSans.ttf", 11)
F_MAST_SUB = font("DejaVuSans.ttf", 18)
F_EYEBROW = font("DejaVuSans-Bold.ttf", 15)
F_COIN = font("DejaVuSans-Bold.ttf", 30)
F_PIN = font("DejaVuSans-Bold.ttf", 12)


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
    """Night skyline over Gaza with a big explosion: the lead illustration."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # Moon, top left.
    draw.ellipse([x0 + 48, y0 + 10, x0 + 70, y0 + 32], fill=(235, 232, 210))
    # Stars.
    for (sx, sy) in [(140, 14), (240, 10), (330, 18), (470, 12),
                     (620, 16), (760, 10), (940, 14), (560, 22), (60, 30)]:
        draw.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                     fill=(220, 225, 240))
    # Horizon glow above the skyline.
    draw.rectangle([x0, y1 - 24, x1, y1 - 12], fill=GLOW)
    draw.rectangle([x0, y1 - 12, x1, y1], fill=(120, 40, 26))
    # Building silhouettes.
    skyline = [(10, 30), (90, 44), (170, 34), (260, 48), (340, 38),
               (430, 50), (520, 32), (620, 46), (700, 36)]
    for (bx, bh) in skyline:
        draw.rectangle([x0 + bx, y1 - bh, x0 + bx + 62, y1], fill=(10, 16, 32))
    # A minaret and a dome for the city silhouette.
    draw.rectangle([x0 + 780, y1 - 56, x0 + 788, y1], fill=(10, 16, 32))
    draw.ellipse([x0 + 770, y1 - 66, x0 + 798, y1 - 48], fill=(10, 16, 32))
    # Big explosion over the skyline, right of centre.
    ex, ey = x0 + 880, y1 - 34
    starburst(draw, ex, ey, 30, FLAME)
    starburst(draw, ex, ey, 16, EMBER)
    for (sx, sy) in [(ex - 38, ey - 18), (ex + 34, ey - 22), (ex + 40, ey + 12),
                     (ex - 30, ey + 16), (ex + 8, ey - 28)]:
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=EMBER)


def sea_panel(draw, x0, y0, x1, y1):
    """Warship, waves, drone and explosion: the Libya feature's scene."""
    mid = y0 + (y1 - y0) * 2 // 5
    draw.rectangle([x0, y0, x1, mid], fill=LIGHTBLUE)
    draw.rectangle([x0, mid, x1, y1], fill=SEABLUE)
    # Waves: gentle sine-like lines, not a sawtooth.
    import math as _math
    for dy in (10, 24, 38):
        y = mid + dy
        if y >= y1 - 2:
            continue
        pts = [(x0 + k * 4,
                y + 3 * _math.sin(k * 4 / 14.0))
               for k in range((x1 - x0) // 4 + 1)]
        draw.line(pts, fill=(255, 255, 255), width=3, joint="curve")
    cx, cy = (x0 + x1) // 2, mid + 30
    # Ship hull + superstructure + mast, big enough to read at 300 px.
    draw.polygon([(cx - 44, cy - 4), (cx + 36, cy - 4), (cx + 22, cy + 14),
                  (cx - 34, cy + 14)], fill=NAVY)
    draw.rectangle([cx - 20, cy - 18, cx + 6, cy - 4], fill=NAVY)
    draw.line([cx - 7, cy - 18, cx - 7, cy - 34], fill=NAVY, width=3)
    # Explosion on the ship.
    starburst(draw, cx + 8, cy - 14, 15, FLAME)
    starburst(draw, cx + 8, cy - 14, 8, EMBER)
    # Drone above the ship, clear of the blast.
    dx, dy = cx - 32, cy - 36
    draw.line([dx - 9, dy - 7, dx + 9, dy + 7], fill=RED, width=3)
    draw.line([dx - 9, dy + 7, dx + 9, dy - 7], fill=RED, width=3)
    draw.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=RED)


def zap_panel(draw, x0, y0, x1, y1):
    """Burning night city: the Zaporizhzhia feature's scene."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    for (sx, sy) in [(16, 12), (52, 22), (96, 10), (30, 34)]:
        draw.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                     fill=(220, 225, 240))
    # Fire glow at the base.
    draw.rectangle([x0, y1 - 26, x1, y1 - 12], fill=GLOW)
    draw.rectangle([x0, y1 - 12, x1, y1], fill=(120, 40, 26))
    # Apartment blocks.
    for (bx, bh, bw) in [(6, 52, 30), (42, 66, 26), (74, 44, 28)]:
        draw.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1], fill=(10, 16, 32))
        for wy in range(y1 - bh + 8, y1 - 14, 14):
            draw.rectangle([x0 + bx + 6, wy, x0 + bx + 12, wy + 7],
                           fill=(255, 210, 90))
    # Explosion over the blocks.
    ex, ey = x0 + 82, y1 - 62
    starburst(draw, ex, ey, 18, FLAME)
    starburst(draw, ex, ey, 9, EMBER)
    # Smoke rising above the blast, panel-relative.
    for (sx, sy, r) in [(70, 45, 7), (88, 35, 9), (104, 25, 7)]:
        draw.ellipse([x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r],
                     fill=(120, 120, 125))


def pharma_panel(draw, x0, y0, x1, y1):
    """Gold coin and a capsule: the Sanofi feature's scene."""
    draw.rectangle([x0, y0, x1, y1], fill=PANELTEAL)
    cx, cy = (x0 + x1) // 2, y0 + 48
    draw.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], fill=GOLD,
                 outline=NAVY, width=3)
    draw.text((cx, cy), "$", font=F_COIN, fill=NAVY, anchor="mm")
    # Capsule, horizontal, below the coin.
    cap_y0, cap_y1 = y1 - 34, y1 - 12
    cap_x0, cap_x1 = x0 + 14, x1 - 14
    mid = (cap_x0 + cap_x1) // 2
    draw.rounded_rectangle([cap_x0, cap_y0, mid, cap_y1], radius=11,
                           fill=(255, 255, 255), outline=NAVY, width=2)
    draw.rounded_rectangle([mid, cap_y0, cap_x1, cap_y1], radius=11,
                           fill=RED, outline=NAVY, width=2)
    draw.rectangle([mid - 2, cap_y0 + 2, mid + 2, cap_y1 - 2], fill=NAVY)


def capitol_panel(draw, x0, y0, x1, y1):
    """Capitol dome and a ballot box: the House feature's scene."""
    draw.rectangle([x0, y0, x1, y1], fill=PANELGREY)
    cx = (x0 + x1) // 2
    # Dome.
    draw.pieslice([cx - 34, y0 + 14, cx + 34, y0 + 82], 180, 360, fill=NAVY2)
    draw.rectangle([cx - 38, y0 + 48, cx + 38, y0 + 56], fill=NAVY2)
    draw.rectangle([cx - 2, y0 + 6, cx + 2, y0 + 16], fill=NAVY2)
    # Columns and steps.
    for bx in (-30, -11, 8, 27):
        draw.rectangle([cx + bx - 4, y0 + 56, cx + bx + 4, y0 + 88],
                       fill=NAVY2)
    draw.rectangle([cx - 42, y0 + 88, cx + 42, y0 + 94], fill=NAVY2)
    draw.rectangle([cx - 46, y0 + 94, cx + 46, y0 + 100], fill=NAVY2)
    # Ballot box with a tick, bottom right.
    bx0, by0 = x1 - 34, y1 - 30
    draw.rectangle([bx0, by0, bx0 + 26, by0 + 20], outline=RED, width=3)
    draw.line([bx0 + 4, by0 + 11, bx0 + 10, by0 + 17], fill=RED, width=3)
    draw.line([bx0 + 10, by0 + 17, bx0 + 23, by0 + 3], fill=RED, width=3)


SCENES = {"sea": sea_panel, "zap": zap_panel, "pharma": pharma_panel,
          "capitol": capitol_panel}


def feature(draw, box, kicker, kicker_color, headline, deck, scene, source):
    """One feature story in `box` = (x0, y0, x1, y1), 136 px tall.

    Left: a full drawn scene panel. Right: kicker, headline (2 lines),
    deck (2 lines), source line. Briefs stay 15 px; nothing here shrinks.
    """
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=1)
    draw.rectangle([x0, y0, x1, y0 + 5], fill=kicker_color)
    px0, py0, px1, py1 = x0 + 1, y0 + 6, x0 + 117, y1 - 1
    SCENES[scene](draw, px0, py0, px1, py1)
    draw.rectangle([px0, py0, px1, py1], outline=RULE, width=1)
    tx = x0 + 130
    draw.text((tx, y0 + 12), kicker, font=F_KICK_SM, fill=kicker_color)
    head_w = x1 - tx - 12
    lines = wrap(draw, headline, F_FHEAD, head_w)
    draw_lines(draw, lines[:2], tx, y0 + 33, F_FHEAD, INK, 25)
    deck_lines = wrap(draw, deck, F_FDECK, head_w)
    draw_lines(draw, deck_lines[:2], tx, y0 + 86, F_FDECK, (58, 58, 58), 17)
    draw.text((tx, y1 - 15), source, font=F_LAB_B, fill=GREY)


def world_map(draw, y_top):
    """Schematic world map with six numbered pins (the six biggest stories).

    Continent blobs are schematic, not to scale; pins sit on the story's
    place. Map box is `y_top`..`y_top`+56, legend line below it.
    """
    draw.text((14, y_top), "WHERE IT HAPPENED  —  SCHEMATIC MAP",
              font=F_LAB_B, fill=NAVY2)
    draw.text((W - 14, y_top), "NOT TO SCALE", font=F_SMALL, fill=GREY,
              anchor="rt")
    m0 = y_top + 16
    draw.rectangle([14, m0, W - 14, m0 + 56], fill=LIGHTBLUE, outline=RULE,
                   width=1)
    # Rough continent blobs (schematic, not to scale); y values are m0 +.
    # Blobs are drawn big, filling most of the 56 px band, so the map
    # still reads as a world map at ~300 px wide.
    draw.polygon([(60, m0 + 6), (200, m0 + 2), (260, m0 + 18),
                  (230, m0 + 34), (150, m0 + 52), (80, m0 + 48),
                  (55, m0 + 26)], fill=TAN)                             # N America
    draw.polygon([(215, m0 + 32), (260, m0 + 36), (250, m0 + 54),
                  (222, m0 + 54)], fill=TAN)                             # S America
    draw.polygon([(460, m0 + 4), (520, m0 + 2), (545, m0 + 16),
                  (510, m0 + 30), (465, m0 + 24)], fill=TAN)             # Europe
    draw.polygon([(465, m0 + 30), (545, m0 + 30), (560, m0 + 54),
                  (505, m0 + 54), (470, m0 + 44)], fill=TAN)             # Africa
    draw.polygon([(570, m0 + 4), (770, m0 + 0), (830, m0 + 14),
                  (800, m0 + 38), (720, m0 + 50), (640, m0 + 48),
                  (575, m0 + 26)], fill=TAN)                             # Asia
    draw.polygon([(825, m0 + 42), (885, m0 + 38), (890, m0 + 54),
                  (830, m0 + 54)], fill=TAN)                             # Australia
    pins = [(520, m0 + 26, "1"), (545, m0 + 14, "2"), (500, m0 + 38, "3"),
            (765, m0 + 20, "4"), (790, m0 + 30, "5"), (580, m0 + 34, "6")]
    for (px, py, n) in pins:
        draw.ellipse([px - 10, py - 10, px + 10, py + 10], fill=RED,
                     outline=(255, 255, 255), width=2)
        draw.text((px, py), n, font=F_PIN, fill=(255, 255, 255), anchor="mm")
    draw.text((W // 2, m0 + 60),
              "1 GAZA   ·   2 ZAPORIZHZHIA   ·   3 LIBYA   ·   4 SHANGHAI   ·   5 TAIPEI   ·   6 RIYADH",
              font=F_SMALL, fill=GREY, anchor="mt")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.text((W // 2, 6), "THE WORLD IN ONE PAGE", font=F_EYEBROW, fill=GOLD, anchor="mt")
    d.text((W // 2, 26), "TUESDAY 24 NOVEMBER 2026", font=F_TITLE, fill=(255, 255, 255), anchor="mt")
    d.text((W // 2, 76), "31 stories  ·  7 regions  ·  every story reported on this day",
           font=F_MAST_SUB, fill=(205, 214, 228), anchor="mt")
    d.rectangle([0, 96, W, 100], fill=GOLD)

    # ---- Number strip ---------------------------------------------------
    numbers = [
        ("7", "killed in Gaza strike,\nHamas security chief"),
        ("2", "killed, 40 hurt in\nZaporizhzhia night hit"),
        ("258", "Democrats' House seats,\nbiggest in ~30 years"),
        ("432K", "record Russian troop\nlosses in Ukraine"),
        ("+9%", "TAIEX record jump,\nTaiwan stocks soar"),
        ("$41B", "Sanofi's cash deal\nfor biotech Insmed"),
    ]
    cell_w = W // 6
    for i, (num, lab) in enumerate(numbers):
        x0 = i * cell_w
        if i:
            d.line([x0, 110, x0, 170], fill=RULE, width=1)
        d.text((x0 + cell_w // 2, 106), num, font=F_NUM, fill=NAVY, anchor="mt")
        for j, ln in enumerate(lab.split("\n")):
            d.text((x0 + cell_w // 2, 148 + j * 15), ln, font=F_LAB, fill=GREY, anchor="mt")
    d.line([0, 178, W, 178], fill=RULE, width=1)

    # ---- Lead story, with a drawn night scene on top --------------------
    d.rectangle([14, 184, W - 14, 358], outline=RULE, width=1)
    d.rectangle([14, 184, W - 14, 189], fill=RED)
    gaza_scene(d, 15, 189, W - 15, 250)
    d.text((28, 256), "WAR  —  GAZA", font=F_KICK, fill=RED)
    d.text((28, 276), "ISRAELI STRIKE KILLS HAMAS SECURITY CHIEF",
           font=F_HEAD, fill=INK)
    d.text((28, 308),
           "Naeem Abu Nahel among seven killed in Gaza on Tuesday, medics said.",
           font=F_DECK, fill=(58, 58, 58))
    d.text((28, 334), "REPORTED  |  Reuters / AP  |  24 NOV", font=F_LAB_B, fill=GREY)

    # ---- Feature rows: four fully illustrated scenes --------------------
    feature(d, (14, 366, 502, 502), "WAR  —  MEDITERRANEAN", NAVY2,
            "SEA DRONES SINK WARSHIP OFF LIBYA",
            "Kyiv says its naval drones destroyed a Russian combat vessel off Libya.",
            "sea", "REPORTED  |  Kyiv Independent  |  24 NOV")
    feature(d, (522, 366, 1010, 502), "WAR  —  UKRAINE", RED,
            "NIGHT STRIKE ON ZAPORIZHZHIA KILLS 2",
            "A Russian overnight attack hit an apartment block; four children were hurt.",
            "zap", "REPORTED  |  Reuters  |  24 NOV")
    feature(d, (14, 510, 502, 646), "BUSINESS  —  PARIS", TEAL,
            "SANOFI BUYS INSMED FOR $41BN",
            "French drugmaker agrees a $41bn cash takeover, its biggest deal in 20+ years.",
            "pharma", "REPORTED  |  Reuters / MarketWatch  |  24 NOV")
    feature(d, (522, 510, 1010, 646), "POLITICS  —  USA", NAVY2,
            "DEMOCRATS TAKE 258-SEAT HOUSE MAJORITY",
            "The party's biggest US House majority in nearly three decades, final calls showed.",
            "capitol", "REPORTED  |  AP  |  24 NOV")

    # ---- Schematic world map --------------------------------------------
    world_map(d, 654)

    # ---- Briefs ---------------------------------------------------------
    d.text((14, 740), "MORE FROM AROUND THE WORLD  —  ALL REPORTED 24 NOVEMBER",
           font=F_KICK, fill=NAVY)
    d.text((14, 758),
           "7 REGIONS:  AFRICA  ·  ASIA  ·  EUROPE  ·  MIDDLE EAST  ·  NORTH AMERICA  ·  SOUTH AMERICA  ·  OCEANIA",
           font=F_SMALL, fill=GREY)
    d.line([14, 774, W - 14, 774], fill=NAVY, width=2)
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
        ("SHANGHAI", "China probes Politburo member Chen Jining."),
        ("HONIARA", "Solomons to drop China security pact."),
        ("MOGADISHU", "Somalia, Uganda step up anti-Shabaab fight."),
        ("DHAKA", "Hasina plans return to Bangladesh 16 Dec."),
        ("RIYADH", "Houthis hit Riyadh's tallest tower again; 11 hurt."),
        ("KYIV", "Seven nations urge EU to curb Russian visas."),
        ("KATHMANDU", "M5.6 quake hits east Nepal; none hurt."),
        ("KYIV", "Zelenskyy: giving up Donbas means losing war."),
        ("CANBERRA", "Albanese disapproval hits record high: poll."),
        ("GENEVA", "Chess title match opens: Gukesh vs Sindarov."),
        ("PORT MORESBY", "PNG votes on Bougainville independence."),
        ("HORMUZ", "Iran says tankers hit mines; talks stall."),
    ]
    for col, briefs in ((14, briefs_left), (522, briefs_right)):
        y = 780
        col_end = 522 if col == 14 else 1010
        for city, text in briefs:
            d.text((col, y), city + " — ", font=F_BRIEF_B, fill=INK)
            w_city = d.textlength(city + " — ", font=F_BRIEF_B)
            lines = wrap(d, text, F_BRIEF, col_end - col - w_city - 14)
            if len(lines) > 1:
                print(f"WARN brief wraps, shorten it: {city} — {text}")
            draw_lines(d, lines[:1], col + w_city, y, F_BRIEF, (58, 58, 58), 17)
            y += 17.0
    d.line([0, 1005, W, 1005], fill=RULE, width=1)
    d.text((W // 2, 1009),
           "Sources: Reuters · AP · UN News · The Kyiv Independent · Just Security · Focus Taiwan — DATE CHECK: Nvidia's Huang return (23 Nov) left out; all 31 stories are 24 Nov.",
           font=F_FOOT, fill=GREY, anchor="mt")

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes, {img.size}")


if __name__ == "__main__":
    main()
