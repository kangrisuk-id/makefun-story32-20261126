"""Build-time image generator for the README (NOT imported by main.py).

Generates, with Pillow only:
  assets/hero.png            1200x630  hero cover
  assets/gallery-phone.png   800x500   phone network-list mockup
  assets/gallery-story.png   800x500   three-beat storyboard of the joke
  assets/gallery-bracket.png 800x500   knockout bracket
  assets/gallery-score.png   800x500   scorecard

Run:  python3 tools/make_images.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
os.makedirs(ASSETS, exist_ok=True)

BG = (18, 18, 22)          # charcoal
PANEL = (32, 32, 40)
GOLD = (212, 175, 55)
CREAM = (245, 240, 225)
MUTED = (160, 155, 140)
GREEN = (90, 200, 130)
RED = (220, 90, 90)
BLUE = (90, 160, 230)

ENTRY = "The WiFi died with the marriage"


def font(size, bold=True):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for path in (f"/usr/share/fonts/truetype/dejavu/{name}",
                 f"/usr/share/fonts/{name}"):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def text_wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 4


def rounded_panel(draw, box, fill, outline=None, radius=18, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill,
                           outline=outline, width=width)


def wifi_arcs(draw, cx, cy, scale, color):
    """Draw a small Wi-Fi symbol (three arcs + dot)."""
    for r, w in ((26, 5), (18, 5), (10, 5)):
        draw.arc([cx - r * scale, cy - r * scale, cx + r * scale, cy + r * scale],
                 start=225, end=315, fill=color, width=w)
    draw.ellipse([cx - 4 * scale, cy - 4 * scale, cx + 4 * scale, cy + 4 * scale],
                 fill=color)


def phone(draw, x, y, w, h, networks, highlight=0):
    """Draw a phone mockup; networks = list of (name, locked)."""
    rounded_panel(draw, [x, y, x + w, y + h], (12, 12, 16), GOLD, 26, 3)
    draw.rounded_rectangle([x + w // 2 - 45, y + 10, x + w // 2 + 45, y + 22],
                           radius=6, fill=(50, 50, 58))
    f_title = font(26)
    f_item = font(24)
    f_small = font(18, bold=False)
    centered(draw, x + w // 2, y + 34, "Wi-Fi", f_title, CREAM)
    draw.line([x + 24, y + 74, x + w - 24, y + 74], fill=(60, 60, 70), width=2)
    yy = y + 92
    for i, (name, locked) in enumerate(networks):
        if i == highlight:
            draw.rounded_rectangle([x + 14, yy - 8, x + w - 14, yy + 42],
                                   radius=12, fill=(58, 48, 18),
                                   outline=GOLD, width=2)
        wifi_arcs(draw, x + w - 52, yy + 16, 0.8,
                  GOLD if i == highlight else (150, 150, 160))
        # Shrink the item font until the name fits beside the Wi-Fi icon.
        size = 24
        while size > 14 and draw.textlength(name, font=font(size)) > w - 150:
            size -= 1
        draw.text((x + 28, yy + (24 - size) // 2), name, font=font(size),
                  fill=GOLD if i == highlight else CREAM)
        yy += 56
    centered(draw, x + w // 2, y + h - 44, "31 characters · 1 story",
             f_small, MUTED)


# ---------------------------------------------------------------- hero 1200x630
img = Image.new("RGB", (1200, 630), BG)
d = ImageDraw.Draw(img)
d.rectangle([0, 0, 1199, 6], fill=GOLD)
d.rectangle([0, 624, 1199, 629], fill=GOLD)
centered(d, 600, 36, "TELL A WHOLE STORY IN 32 CHARACTERS", font(30), GOLD)
centered(d, 600, 84, "one Wi-Fi name · one divorce · zero survivors",
         font(24, bold=False), MUTED)
# Left: the entry, big, wrapped.
lines = text_wrap(d, ENTRY, font(64), 620)
yy = 190
for ln in lines:
    yy = centered(d, 330, yy, ln, font(64), CREAM)
d.rectangle([40, yy + 14, 620, yy + 18], fill=GOLD)
centered(d, 330, yy + 34, "31 characters", font(28), GOLD)
centered(d, 330, yy + 74, "Joke 9/10 · Story 7/7 · Fresh 4/5 · Tight 3/3",
         font(22, bold=False), MUTED)
centered(d, 330, yy + 108, "Tournament winner: 23/25", font(22, bold=False), MUTED)
# Right: phone mockup.
phone(d, 700, 130, 440, 460, [
    ("The WiFi died with the marriage", True),
    ("FBI Surveillance Van", True),
    ("Pretty Fly for a Wi-Fi", True),
    ("Tell My WiFi Love Her", True),
    ("CoffeeShop_Guest", False),
], highlight=0)
img.save(os.path.join(ASSETS, "hero.png"))

# ------------------------------------------------------- gallery 1: phone list
img = Image.new("RGB", (800, 500), BG)
d = ImageDraw.Draw(img)
centered(d, 400, 22, "As strangers see it — in the network list",
         font(28), GOLD)
phone(d, 190, 70, 420, 400, [
    ("The WiFi died with the marriage", True),
    ("FBI Surveillance Van", True),
    ("Pretty Fly for a Wi-Fi", True),
    ("Tell My WiFi Love Her", True),
    ("xfinitywifi", False),
], highlight=0)
img.save(os.path.join(ASSETS, "gallery-phone.png"))

# ------------------------------------------------------- gallery 2: storyboard
img = Image.new("RGB", (800, 500), BG)
d = ImageDraw.Draw(img)
centered(d, 400, 22, "The whole story, in three beats", font(28), GOLD)
panels = [
    ("1 · THE WEDDING", "Two people, one router,\none happy network.", GOLD),
    ("2 · THE SPLIT", "The marriage ends.\nSomebody has to go.", RED),
    ("3 · THE CASUALTY", "Not the couch. Not the dog.\nThe Wi-Fi.", CREAM),
]
x = 30
for title, body, col in panels:
    rounded_panel(d, [x, 80, x + 230, 400], PANEL, col, 16, 3)
    centered(d, x + 115, 100, title, font(22), col)
    body_lines = []
    for raw in body.split("\n"):
        body_lines.extend(text_wrap(d, raw, font(20, bold=False), 200))
    for i, ln in enumerate(body_lines):
        centered(d, x + 115, 160 + i * 32, ln, font(20, bold=False), CREAM)
    if title.startswith("3"):
        wifi_arcs(d, x + 115, 300, 1.6, RED)
        centered(d, x + 115, 340, "signal lost", font(20, bold=False), RED)
    elif title.startswith("1"):
        wifi_arcs(d, x + 115, 300, 1.6, GREEN)
        centered(d, x + 115, 340, "connected", font(20, bold=False), GREEN)
    else:
        d.line([x + 55, 300, x + 175, 300], fill=RED, width=6)
        centered(d, x + 115, 340, "disconnected", font(20, bold=False), RED)
    x += 250
centered(d, 400, 430, "Six words. Beginning, middle, end.",
         font(22, bold=False), MUTED)
img.save(os.path.join(ASSETS, "gallery-story.png"))

# ------------------------------------------------------- gallery 3: bracket
img = Image.new("RGB", (800, 500), BG)
d = ImageDraw.Draw(img)
centered(d, 400, 22, "Knockout bracket — top 8 of 48 candidates",
         font(28), GOLD)


def bracket_box(x, y, w, text, winner):
    rounded_panel(d, [x, y, x + w, y + 40], PANEL,
                  GOLD if winner else (70, 70, 80), 10, 2)
    size = 17
    while size > 12 and d.textlength(text, font=font(size)) > w - 20:
        size -= 1
    f = font(size)
    if d.textlength(text, font=f) > w - 20:
        # truncate at a word boundary, then ellipsis
        words = text.split()
        short = ""
        for wd in words:
            trial = (short + " " + wd).strip()
            if d.textlength(trial + "…", font=f) <= w - 20:
                short = trial
            else:
                break
        text = (short + "…") if short else text[:8] + "…"
    d.text((x + 10, y + 9), text, font=f,
           fill=GOLD if winner else CREAM)


qf = [
    ("The WiFi died with the marriage", "Signal's strong, marriage isn't"),
    ("He took the couch, I kept WiFi", "Ask Dave, he's still paying"),
    ("The router knows what you did", "Your ex changed the password"),
    ("Password: the day you left me", "She took the dog, not the router"),
]
y = 76
for a, b in qf:
    bracket_box(30, y, 300, a, True)
    bracket_box(30, y + 48, 300, b, False)
    y += 92
sf = [
    ("The WiFi died with the marriage", "Password: the day you left me"),
    ("He took the couch, I kept WiFi", "The router knows what you did"),
]
y = 100
for a, b in sf:
    bracket_box(360, y, 200, a, True)
    bracket_box(360, y + 48, 200, b, False)
    d.line([330, y + 20, 360, y + 20], fill=(90, 90, 100), width=2)
    d.line([330, y + 68, 360, y + 68], fill=(90, 90, 100), width=2)
    y += 148
bracket_box(590, 190, 180, "The WiFi died", True)
d.text((590, 238), "with the marriage", font=font(17), fill=GOLD)
d.line([560, 120, 590, 210], fill=(90, 90, 100), width=2)
d.line([560, 268, 590, 210], fill=(90, 90, 100), width=2)
centered(d, 680, 292, "WINNER", font(26), GOLD)
centered(d, 680, 328, "23/25", font(24), CREAM)
centered(d, 400, 452, "Quarter-finals → semi-finals → final. First differing judge criterion decides.",
         font(20, bold=False), MUTED)
img.save(os.path.join(ASSETS, "gallery-bracket.png"))

# ------------------------------------------------------- gallery 4: scorecard
img = Image.new("RGB", (800, 500), BG)
d = ImageDraw.Draw(img)
centered(d, 400, 22, "Scorecard — judged against the brief, in order",
         font(28), GOLD)
rows = [
    ("1 · Joke — lands on first read", 9, 10, GOLD),
    ("2 · Story — situation + character + event", 7, 7, GREEN),
    ("3 · Freshness — no stock Wi-Fi joke", 4, 5, BLUE),
    ("4 · Tight — every character earns its place", 3, 3, CREAM),
]
y = 90
for label, got, total, col in rows:
    d.text((50, y), label, font=font(22), fill=CREAM)
    bar_x, bar_w = 50, 620
    d.rounded_rectangle([bar_x, y + 36, bar_x + bar_w, y + 62],
                        radius=10, fill=(45, 45, 55))
    d.rounded_rectangle([bar_x, y + 36, bar_x + bar_w * got // total, y + 62],
                        radius=10, fill=col)
    d.text((bar_x + bar_w + 16, y + 34), f"{got}/{total}", font=font(24),
           fill=col)
    y += 92
centered(d, 400, 440, "TOTAL  23 / 25", font(30), GOLD)
img.save(os.path.join(ASSETS, "gallery-score.png"))

print("wrote:", sorted(os.listdir(ASSETS)))
for name in sorted(os.listdir(ASSETS)):
    im = Image.open(os.path.join(ASSETS, name))
    print(name, im.size, im.mode)
