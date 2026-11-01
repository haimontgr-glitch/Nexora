"""NEXORA 2D motion-graphics animatic (1080x1920, 30 fps, 43.00 s).
Frames are drawn with Pillow, piped to ffmpeg. Timing = section 1/2 of NEXORA_PRODUCTION_PLAN.md
(segment boundaries measured; trigger times inside segments are estimates).

usage: animatic.py <repo_root> <out_video_noaudio.mp4>
       animatic.py <repo_root> --stills out_dir t1 t2 ...   (debug PNGs)
"""
import sys, os, re, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from multiprocessing import Pool

W, H, FPS, DUR = 1080, 1920, 30, 43.0
ROOT = sys.argv[1]
FONT = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
GOLD = (255, 201, 60); GOLD_T = (255, 238, 160); GOLD_B = (176, 112, 8)
GREY = (120, 126, 140)

# ---------------------------------------------------------------- helpers
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / (b - a))
def eo(x): return 1 - (1 - x) ** 3
def eb(x):
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def bump(t, t0, w=0.18):
    d = t - t0
    return 0.0 if d < 0 else math.exp(-d / w)
def sc(c, a):
    a = max(0.0, a)
    return tuple(int(min(255, v * a)) for v in c)

_fc = {}
def F(size):
    size = max(8, int(size))
    if size not in _fc: _fc[size] = ImageFont.truetype(FONT, size)
    return _fc[size]

def T(im, xy, s, size, fill, anchor="mm", stroke=0, sfill=(0, 0, 0)):
    ImageDraw.Draw(im).text(xy, s, font=F(size), fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill)

_gc = {}
def grad(w, h, top, bot):
    k = (w, h, top, bot)
    if k not in _gc:
        t = np.linspace(0, 1, h)[:, None, None]
        a = np.array(top)[None, None, :] * (1 - t) + np.array(bot)[None, None, :] * t
        _gc[k] = Image.fromarray(np.repeat(a, w, axis=1).astype(np.uint8))
        if len(_gc) > 400: _gc.pop(next(iter(_gc)))
    return _gc[k]

def gold_mask(im, box, fn, alpha=1.0, top=GOLD_T, bot=GOLD_B):
    x0, y0, x1, y1 = [int(v) for v in box]
    w, h = x1 - x0, y1 - y0
    if w <= 0 or h <= 0 or alpha <= 0: return
    m = Image.new("L", (w, h), 0)
    fn(ImageDraw.Draw(m), x0, y0)
    if alpha < 1: m = m.point([int(i * alpha) for i in range(256)])
    im.paste(grad(w, h, top, bot), (x0, y0), m)

def gold_text(im, cx, cy, s, size, alpha=1.0, top=GOLD_T, bot=GOLD_B):
    f = F(size); w = f.getlength(s)
    box = (cx - w / 2 - 12, cy - size * 0.75, cx + w / 2 + 12, cy + size * 0.75)
    gold_mask(im, box, lambda d, ox, oy: d.text((cx - ox, cy - oy), s, font=f, fill=255, anchor="mm"), alpha, top, bot)

def gold_poly(im, pts, alpha=1.0, top=GOLD_T, bot=GOLD_B):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    box = (min(xs) - 2, min(ys) - 2, max(xs) + 2, max(ys) + 2)
    gold_mask(im, box, lambda d, ox, oy: d.polygon([(x - ox, y - oy) for x, y in pts], fill=255), alpha, top, bot)

def gold_rrect(im, box, r, alpha=1.0, top=GOLD_T, bot=GOLD_B):
    gold_mask(im, box, lambda d, ox, oy: d.rounded_rectangle((box[0] - ox, box[1] - oy, box[2] - ox, box[3] - oy), r, fill=255), alpha, top, bot)

def heart_pts(cx, cy, s, n=90):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        x = 16 * math.sin(a) ** 3
        y = 13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)
        pts.append((cx + x * s / 34, cy - y * s / 34))
    return pts

def star(d, x, y, r, col):
    k = r * 0.22
    d.polygon([(x, y - r), (x + k, y - k), (x + r, y), (x + k, y + k), (x, y + r), (x - k, y + k), (x - r, y), (x - k, y - k)], fill=col)

def profile(im, cx, cy, r, ring, fill, alpha=1.0):
    d = ImageDraw.Draw(im)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=sc(fill, alpha), outline=sc(ring, alpha), width=max(3, int(r * 0.07)))
    d.ellipse((cx - 0.27 * r, cy - 0.5 * r, cx + 0.27 * r, cy + 0.04 * r), fill=sc(ring, alpha))
    d.pieslice((cx - 0.62 * r, cy + 0.12 * r, cx + 0.62 * r, cy + 1.25 * r), 180, 360, fill=sc(ring, alpha))

def phone(im, cx, cy, w, h, screen=(14, 18, 26), edge=(150, 150, 165), r=52):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), r, fill=(16, 16, 20), outline=edge, width=6)
    d.rounded_rectangle((cx - w / 2 + 16, cy - h / 2 + 16, cx + w / 2 - 16, cy + h / 2 - 16), r - 12, fill=screen)
    d.rounded_rectangle((cx - 50, cy - h / 2 + 26, cx + 50, cy - h / 2 + 44), 9, fill=(16, 16, 20))
    return (cx - w / 2 + 16, cy - h / 2 + 16, cx + w / 2 - 16, cy + h / 2 - 16)

def repost_icon(im, cx, cy, s, col, width=None):
    d = ImageDraw.Draw(im); lw = width or max(4, int(s * 0.12))
    a = [(-0.8, 0.25), (-0.8, -0.5), (0.35, -0.5)]
    b = [(0.8, -0.25), (0.8, 0.5), (-0.35, 0.5)]
    for path, dirn in ((a, 1), (b, -1)):
        pts = [(cx + x * s, cy + y * s) for x, y in path]
        d.line(pts, fill=col, width=lw, joint="curve")
        ex, ey = pts[-1]
        d.polygon([(ex + dirn * 0.36 * s, ey), (ex - dirn * 0.02 * s, ey - 0.3 * s), (ex - dirn * 0.02 * s, ey + 0.3 * s)], fill=col)

def radial(cx, cy, r, inner, outer, power=1.7):
    y, x = np.mgrid[0:H, 0:W]
    k = np.clip(1 - np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / r, 0, 1) ** power
    a = np.array(outer)[None, None, :] + (np.array(inner) - np.array(outer))[None, None, :] * k[..., None]
    return Image.fromarray(a.astype(np.uint8))

COLD_BG = radial(540, 900, 1300, (30, 38, 54), (4, 5, 8))
GOLD_BG = radial(540, 1000, 1500, (92, 62, 12), (6, 4, 1))
_y, _x = np.mgrid[0:H, 0:W]
VIG = Image.fromarray((np.clip(1.15 - 0.55 * (np.sqrt(((_x - 540) / 540) ** 2 + ((_y - 960) / 960) ** 2) / 1.2) ** 2, 0.35, 1) * 255).astype(np.uint8)).convert("RGB")
del _x, _y

LOGO = Image.open(os.path.join(ROOT, "assets/NEXORA_logo.png")).convert("RGB")
_lc = {}; _mc = {}
def logo_s(S):
    if S not in _lc:
        _lc[S] = LOGO.resize((S, S), Image.BICUBIC)
        if len(_lc) > 60: _lc.pop(next(iter(_lc)))
    return _lc[S]
def logo_mask(S):
    if S not in _mc:
        m = Image.new("L", (S, S), 0)
        ImageDraw.Draw(m).ellipse((S * 0.0215, S * 0.0215, S * 0.9785, S * 0.9785), fill=255)
        _mc[S] = m.filter(ImageFilter.GaussianBlur(max(1, S * 0.004)))
        if len(_mc) > 60: _mc.pop(next(iter(_mc)))
    return _mc[S]

def logo_draw(im, cx, cy, size, alpha=1.0, sweep=None):
    S = int(size)
    if S < 8 or alpha <= 0: return
    lg = logo_s(S)
    x0, y0 = int(cx - S / 2), int(cy - S / 2)
    base = im.crop((x0, y0, x0 + S, y0 + S))
    new = ImageChops.screen(base, lg)                 # outer glow only (black drops out)
    new = Image.composite(lg, new, logo_mask(S))      # opaque badge disc, so the scene never shows through the logo
    if sweep is not None:
        yy, xx = np.mgrid[0:S, 0:S]
        dd = (xx + yy) / (2.0 * S)
        band = np.exp(-((dd - sweep) / 0.07) ** 2) * 0.75
        bl = Image.fromarray((band * 255).astype(np.uint8))
        bl = ImageChops.multiply(bl, logo_mask(S))
        tint = Image.merge("RGB", [bl.point([int(i * 1.0) for i in range(256)]), bl.point([int(i * 0.93) for i in range(256)]), bl.point([int(i * 0.7) for i in range(256)])])
        new = ImageChops.add(new, tint)
    if alpha < 1: new = Image.blend(base, new, alpha)
    im.paste(new, (x0, y0))

def add_layer(im, L):
    im.paste(ImageChops.add(im, L))

def rays(im, cx, cy, t, n, length, col, a=1.0, spread=0.05, rot=0.25):
    if a <= 0: return
    L = Image.new("RGB", (W // 4, H // 4)); d = ImageDraw.Draw(L)
    for i in range(n):
        ang = rot * t + i * 2 * math.pi / n
        d.polygon([(cx / 4, cy / 4), ((cx + math.cos(ang - spread) * length) / 4, (cy + math.sin(ang - spread) * length) / 4),
                   ((cx + math.cos(ang + spread) * length) / 4, (cy + math.sin(ang + spread) * length) / 4)], fill=sc(col, a))
    add_layer(im, L.filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR))

_br = {}
def burst(im, t, t0, ox, oy, n, speed, seed, col=GOLD, life=1.3, grav=0.0, r=7):
    dt = t - t0
    if dt < 0 or dt > life: return
    if (seed, n) not in _br:
        rs = np.random.RandomState(seed); _br[(seed, n)] = (rs.rand(n) * 6.283, 0.35 + rs.rand(n), rs.rand(n))
    ang, spd, rr = _br[(seed, n)]
    d = ImageDraw.Draw(im); f = 1 - dt / life
    for i in range(n):
        x = ox + math.cos(ang[i]) * speed * spd[i] * dt
        y = oy + math.sin(ang[i]) * speed * spd[i] * dt + grav * dt * dt
        rad = r * (0.5 + rr[i]) * (0.4 + 0.6 * f)
        if rr[i] > 0.6: star(d, x, y, rad * 1.8, sc(col, f + 0.2))
        else: d.ellipse((x - rad, y - rad, x + rad, y + rad), fill=sc(col, f + 0.2))

_rs = np.random.RandomState(7)
PX, PY, PS, PR, PH = _rs.rand(260) * W, _rs.rand(260) * H, _rs.rand(260) * 0.6 + 0.4, _rs.rand(260) * 3 + 1.5, _rs.rand(260) * 6.28
def dust(im, t, n, col, a=1.0):
    d = ImageDraw.Draw(im)
    for i in range(n):
        x = (PX[i] + 30 * math.sin(t * 0.5 + PH[i])) % W; y = (PY[i] - t * 60 * PS[i]) % H
        tw = 0.5 + 0.5 * math.sin(t * 3 + PH[i] * 3); r = PR[i] * (0.6 + 0.6 * tw)
        d.ellipse((x - r, y - r, x + r, y + r), fill=sc(col, a * (0.35 + 0.65 * tw)))

TOWERS = [(60, 70, 380), (150, 60, 520), (235, 90, 300), (335, 50, 430), (745, 50, 450), (830, 90, 310), (925, 60, 540), (1015, 70, 390)]
def world(im, t, k=1.0):
    d = ImageDraw.Draw(im); hy = 1000
    for x, w, h in TOWERS:
        d.rectangle((x - w / 2, hy - h, x + w / 2, hy), fill=(10, 8, 3), outline=sc((190, 140, 30), k), width=3)
        for j in range(1, int(h / 60)):
            d.line((x - w / 2 + 8, hy - j * 60, x + w / 2 - 8, hy - j * 60), fill=sc((120, 85, 15), k * 0.7), width=2)
    d.rectangle((0, hy, W, H), fill=(5, 4, 2))
    for i in range(-14, 15): d.line((540, hy, 540 + i * 260, H), fill=sc((190, 140, 30), k * 0.55), width=2)
    for j in range(14):
        z = (j + (t * 0.6) % 1) / 14
        d.line((0, hy + (H - hy) * z ** 2.2, W, hy + (H - hy) * z ** 2.2), fill=sc((190, 140, 30), k * (0.15 + 0.5 * z)), width=2)
    d.line((0, hy, W, hy), fill=sc(GOLD, k), width=3)
    for r in (330, 430, 540):
        rr = r * (1 + 0.03 * math.sin(t * 2 + r))
        d.ellipse((540 - rr, 620 - rr * 0.28, 540 + rr, 620 + rr * 0.28), outline=sc((200, 150, 35), k * 0.55), width=2)

def gold_base(t, k=1.0, rays_a=0.5):
    im = GOLD_BG.copy()
    rays(im, 540, -80, t, 9, 2300, (60, 42, 10), a=rays_a * k, spread=0.06, rot=0.0)
    world(im, t, k)
    dust(im, t, 110, GOLD, k)
    return im

def counter(im, cx, cy, label, val, t, t0, col, size, lab_col=(150, 156, 170)):
    T(im, (cx, cy - size * 0.9), label, size * 0.36, lab_col)
    if t < t0: T(im, (cx, cy), "–", size, (70, 76, 90)); return
    pop = bump(t, t0, 0.15)
    T(im, (cx, cy), val, size * (1 + 0.35 * pop), col)

# ---------------------------------------------------------------- scenes
def s01(im, t):
    k = eo(prog(t, 0, 0.6))
    box = phone(im, 540, 960 + (1 - k) * 140, 580, 1100, (12, 15, 22), (120, 126, 140))
    d = ImageDraw.Draw(im); y0 = box[1]
    profile(im, 540, y0 + 190, 92, (110, 116, 130), (45, 50, 62))
    d.rounded_rectangle((410, y0 + 320, 670, y0 + 344), 12, fill=(58, 64, 78))
    d.rounded_rectangle((450, y0 + 360, 630, y0 + 376), 8, fill=(40, 45, 56))
    counter(im, 540, y0 + 560, "Followers", "128", t, 2.63, (175, 180, 195), 120)
    if t >= 2.63:
        a = prog(t, 2.63, 2.9); d.polygon([(540 - 22, y0 + 650), (540 + 22, y0 + 650), (540, y0 + 680)], fill=sc((190, 75, 75), a))
    for i in range(6):
        x = 540 + (i - 2.5) * 78
        on = (i < 2 and t > 2.63 + i * 0.1) or (i == 0)
        profile(im, x, y0 + 800, 30, (60, 66, 80) if on else (34, 38, 48), (24, 28, 36), 1.0)
    dust(im, t, 35, (120, 130, 150), 0.6)

def s02(im, t):
    d = ImageDraw.Draw(im)
    for i, (x, y, s) in enumerate([(300, 860, 230), (560, 1000, 300), (810, 850, 230)]):
        a = eb(prog(t, 3.2 + i * 0.07, 3.5 + i * 0.07))
        if a <= 0: continue
        pts = heart_pts(x, y, s * a)
        d.polygon(pts, fill=(78, 84, 98), outline=(140, 146, 160))
        d.line([(x, y - 0.25 * s * a), (x + 0.05 * s * a, y - 0.08 * s * a), (x - 0.06 * s * a, y + 0.04 * s * a), (x + 0.04 * s * a, y + 0.2 * s * a)], fill=(8, 10, 14), width=6)
    counter(im, 540, 1330, "Likes", "12", t, 3.54, (175, 180, 195), 130)
    dust(im, t, 30, (120, 130, 150), 0.6)

def s03(im, t):
    d = ImageDraw.Draw(im)
    a = eo(prog(t, 3.95, 4.3))
    d.rounded_rectangle((110, 560 + (1 - a) * 60, 970, 1040 + (1 - a) * 60), 28, fill=(16, 20, 28), outline=(95, 102, 118), width=4)
    cy = 800 + (1 - a) * 60
    d.polygon([(500, cy - 70), (500, cy + 70), (620, cy)], fill=(100, 106, 122))
    d.rounded_rectangle((150, 1000 + (1 - a) * 60, 930, 1010 + (1 - a) * 60), 5, fill=(50, 55, 68))
    d.rounded_rectangle((150, 1000 + (1 - a) * 60, 190, 1010 + (1 - a) * 60), 5, fill=(110, 116, 132))
    counter(im, 540, 1250, "Views", "41", t, 4.08, (175, 180, 195), 140)
    d.line((140, 1640, 940, 1640), fill=(60, 66, 80), width=3); d.line((140, 1380, 140, 1640), fill=(60, 66, 80), width=3)
    drop = eo(prog(t, 4.5, 5.6)); pts = []
    for i in range(12):
        pts.append((140 + i * 72, 1480 + 12 * math.sin(i * 1.7) * (1 - drop) + drop * 160 * (i / 11) ** 1.2))
    d.line(pts, fill=sc((190, 80, 80), a), width=7, joint="curve")
    dust(im, t, 30, (120, 130, 150), 0.6)

def s04(im, t):
    d = ImageDraw.Draw(im); u = t - 6.5
    dx = 7 * math.sin(u * 2.4) * prog(t, 8.0, 8.6)
    dy = 8 * math.sin(u * 1.1)
    d.ellipse((120, 1320, 960, 2000), fill=(34, 40, 52))
    d.rectangle((480, 1090, 600, 1340), fill=(80, 86, 100))
    hx = 540 + dx
    d.ellipse((hx - 175, 700 + dy, hx + 175, 1120 + dy), fill=(104, 110, 124))
    d.chord((hx - 180, 690 + dy, hx + 180, 1020 + dy), 180, 360, fill=(20, 24, 34))
    for sx in (-1, 1):
        ex = hx + sx * 68
        d.ellipse((ex - 30, 920 + dy, ex + 30, 962 + dy), fill=(176, 180, 190))
        d.ellipse((ex - 11 + sx * 2, 932 + dy + 6, ex + 11 + sx * 2, 954 + dy + 6), fill=(24, 28, 40))
        d.line((hx + sx * 112, 892 + dy, hx + sx * 36, 858 + dy), fill=(16, 18, 26), width=13)
    d.arc((hx - 52, 1010 + dy, hx + 52, 1064 + dy), 205, 335, fill=(60, 50, 60), width=9)
    pw = 6 * math.sin(u * 3)
    d.ellipse((330, 1370, 410, 1540), fill=(84, 90, 104)); d.ellipse((670, 1370, 750, 1540), fill=(84, 90, 104))
    phone(im, 540, 1500 + pw, 300, 480, (70, 98, 150), (150, 154, 168))
    if t > 8.83:
        f = prog(t, 8.83, 9.7); sx, sy = hx + 210, 850 + dy + f * 150
        d.ellipse((sx - 14, sy - 6, sx + 14, sy + 24), fill=sc((160, 205, 255), 1 - f * 0.6)); d.polygon([(sx - 12, sy), (sx + 12, sy), (sx, sy - 30)], fill=sc((160, 205, 255), 1 - f * 0.6))
    dust(im, t, 25, (120, 130, 150), 0.5)

def s05_dark(im, t):
    if t > 11.5:
        f = prog(t, 11.5, 11.92); h = H * eo(f)
        ImageDraw.Draw(im).line((540, 960 - h / 2, 540, 960 + h / 2), fill=sc(GOLD_T, 0.3 + 0.7 * f), width=6)

def s06(im, t):
    pass  # logo drawn in render (needs world dimming first)

def s07(im, t):
    d = ImageDraw.Draw(im)
    open_ = prog(t, 16.8, 17.3)
    oy = -700 * (1 - eb(prog(t, 15.9, 16.4)))
    if t >= 16.8:
        rays(im, 540, 1010, t, 14, 1700, (110, 80, 20), a=min(1, (t - 16.8) / 0.25) * (0.5 + 0.5 * bump(t, 16.8, 0.8)), spread=0.05, rot=0.6)
    gold_rrect(im, (360, 1090 + oy, 720, 1390 + oy), 14, top=(232, 178, 50), bot=(110, 70, 6))
    d.rounded_rectangle((498, 1090 + oy, 582, 1390 + oy), 4, fill=(14, 10, 4), outline=sc(GOLD, 0.9), width=3)
    d.line((372, 1160 + oy, 708, 1160 + oy), fill=sc((255, 225, 120), 0.35), width=3)
    lift = eo(open_) * 330; ang = math.radians(-24 * eo(open_)); lcx, lcy = 540 + 120 * eo(open_), 1040 + oy - lift
    def X(x, y): return (lcx + x * math.cos(ang) - y * math.sin(ang), lcy + x * math.sin(ang) + y * math.cos(ang))
    gold_poly(im, [X(-230, -55), X(230, -55), X(230, 55), X(-230, 55)], top=(250, 214, 92), bot=(176, 112, 10))
    d.polygon([X(-42, -55), X(42, -55), X(42, 55), X(-42, 55)], fill=(14, 10, 4), outline=sc(GOLD, 0.9))
    for sx in (-1, 1):
        bx, by_ = X(sx * 62, -88); d.ellipse((bx - 62, by_ - 40, bx + 62, by_ + 40), outline=GOLD, width=13, fill=(14, 10, 4))
    bx, by_ = X(0, -70); d.ellipse((bx - 24, by_ - 24, bx + 24, by_ + 24), fill=GOLD)
    burst(im, t, 16.8, 540, 1010, 70, 1100, 3, life=1.6, grav=700, r=8)
    a = eb(prog(t, 16.19, 16.6))
    if a > 0:
        gold_text(im, 540, 400, "FREE PROMOTION", 96 * a, clamp(a))
        gold_text(im, 540, 530, "CAMPAIGN", 134 * a, clamp(a))

def _target50():
    f = F(620); m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).text((540, 860), "50", font=f, fill=255, anchor="mm")
    ys, xs = np.nonzero(np.array(m)[::7, ::7] > 128); pts = np.stack([xs * 7, ys * 7], 1).astype(float)
    sel = [int(np.argmin(pts[:, 0] + pts[:, 1] * 0.01))]; dmin = np.linalg.norm(pts - pts[sel[0]], axis=1)
    while len(sel) < 50:
        j = int(np.argmax(dmin)); sel.append(j); dmin = np.minimum(dmin, np.linalg.norm(pts - pts[j], axis=1))
    return pts[sel]
TARGET = _target50()
assert len(TARGET) == 50

def s08(im, t):
    d = ImageDraw.Draw(im)
    s = eo(prog(t, 18.85, 19.95)); tt = t - 18.85
    for r in (200, 300, 400):
        a = 0.4 * (1 - s) * prog(t, 18.3, 18.85)
        if a > 0: d.ellipse((540 - r, 880 - r, 540 + r, 880 + r), outline=sc(GOLD, a), width=2)
    if t >= 18.85:
        for j in (2, 1, 0):
            tj = tt - j * 0.035; sj = eo(prog(tj + 18.85, 18.85, 19.95))
            for i in range(50):
                ang = i * 2.4 + 3.0 * tj * (1 - sj * 0.7); rad = (150 + (i % 10) * 48) * (1 - sj)
                ox, oy = 540 + math.cos(ang) * rad, 880 + math.sin(ang) * rad * 0.8
                x = ox * (1 - sj) + TARGET[i][0] * sj; y = oy * (1 - sj) + TARGET[i][1] * sj
                r = 12 - j * 3; d.ellipse((x - r, y - r, x + r, y + r), fill=sc(GOLD_T if j == 0 else GOLD, 1 - j * 0.35))
    gold_text(im, 540, 860, "50", 620, prog(t, 19.9, 20.25) * 0.85)
    burst(im, t, 19.95, 540, 880, 40, 700, 5, life=0.9)

def s09(im, t):
    fly = eo(prog(t, 20.3, 20.75)); rise = eo(prog(t, 21.56, 22.5))
    cy = 1400 - 300 * fly - 440 * rise
    if rise > 0:
        L = Image.new("RGB", (W // 4, H // 4)); ImageDraw.Draw(L).polygon([(540 / 4 - 30, 0), (540 / 4 + 30, 0), (540 / 4 + 190 * rise, cy / 4 + 100), (540 / 4 - 190 * rise, cy / 4 + 100)], fill=sc((120, 90, 25), rise))
        add_layer(im, L.filter(ImageFilter.GaussianBlur(4)).resize((W, H), Image.BILINEAR))
    box = phone(im, 540, cy, 400, 780, (22, 18, 10), (210, 170, 70))
    d = ImageDraw.Draw(im); cx = 540
    if t < 20.7: d.polygon([(cx - 36, cy - 50), (cx - 36, cy + 50), (cx + 50, cy)], fill=GOLD)
    else:
        u = t - 20.7
        d.rounded_rectangle((box[0] + 30, box[1] + 90, box[2] - 30, box[1] + 390), 20, fill=(48, 34, 8), outline=sc(GOLD, 0.8), width=3)
        for i in range(9):
            h = 40 + 110 * (0.5 + 0.5 * math.sin(u * 7 + i * 1.3))
            d.rounded_rectangle((box[0] + 52 + i * 33, box[1] + 390 - 24 - h, box[0] + 52 + i * 33 + 22, box[1] + 390 - 24), 6, fill=sc(GOLD_T, 0.9))
        d.polygon([(cx - 30, box[1] + 195), (cx - 30, box[1] + 285), (cx + 45, box[1] + 240)], fill=sc((255, 255, 255), 0.18))
        d.rounded_rectangle((box[0] + 30, box[1] + 440, box[0] + 30 + 300 * clamp(u / 2.2), box[1] + 452), 6, fill=GOLD)
        d.rounded_rectangle((box[0] + 30, box[1] + 480, box[2] - 120, box[1] + 496), 8, fill=(60, 44, 12))
        d.rounded_rectangle((box[0] + 30, box[1] + 516, box[2] - 190, box[1] + 532), 8, fill=(44, 32, 10))
    burst(im, t, 21.56, 540, cy, 30, 500, 9, life=1.0)

def s10(im, t):
    d = ImageDraw.Draw(im); lit_t = [22.97, 23.45, 23.95, 24.45]
    for i in range(4):
        x = 180 + i * 240; on = prog(t, lit_t[i], lit_t[i] + 0.25)
        fl = bump(t, 24.75, 0.15) if i == 0 and t > 24.75 else 0
        if on > 0:
            L = Image.new("RGB", (W // 4, H // 4)); ImageDraw.Draw(L).rectangle((x / 4 - 5, 20, x / 4 + 5, 1130 / 4), fill=sc((120, 88, 20), on * (1 + fl)))
            add_layer(im, L.filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR))
        top = 1150 - 20 * on
        d.rectangle((x - 80, top, x + 80, 1330), fill=sc((90, 62, 12), 0.35 + 0.65 * on), outline=sc(GOLD, 0.3 + 0.7 * on), width=3)
        d.ellipse((x - 80, top - 26, x + 80, top + 26), fill=sc(GOLD_T, 0.3 + 0.7 * on), outline=sc(GOLD, 1), width=3)
        gold_text(im, x, top - 120 - 30 * on, str(i + 1), 120, 0.2 + 0.8 * on)

def s11(im, t):
    pulse = bump(t, 25.6, 0.14) * 0.7 + bump(t, 25.9, 0.18)
    s = 520 * (0.4 + 0.6 * eb(prog(t, 25.0, 25.5))) * (1 + 0.14 * pulse)
    rays(im, 540, 900, t, 12, 1300, (90, 64, 14), a=0.3 + 0.5 * pulse, spread=0.04, rot=0.3)
    gold_poly(im, heart_pts(540, 900, s), top=(255, 232, 140), bot=(190, 110, 10))
    ImageDraw.Draw(im).ellipse((540 - s * 0.27, 900 - s * 0.25, 540 - s * 0.13, 900 - s * 0.16), fill=sc((255, 240, 190), 0.4))
    for k in range(2):
        r = 420 * prog(t, 25.9 + k * 0.1, 26.7)
        if r > 0: ImageDraw.Draw(im).ellipse((540 - r, 900 - r, 540 + r, 900 + r), outline=sc(GOLD, 1 - prog(t, 25.9, 26.7)), width=5)
    burst(im, t, 26.2, 540, 900, 36, 800, 11, life=0.9)

def s12(im, t):
    n = 0
    for i in range(10):
        ti = 27.40 + 0.15 * i
        a = eb(prog(t, ti, ti + 0.2))
        if a <= 0.02 or t < ti: continue
        n += 1
        x = 140 + (i % 5) * 200; y = 780 + (i // 5) * 240
        profile(im, x, y, 80 * a, GOLD, (34, 24, 6))
        burst(im, t, ti, x, y, 8, 220, 20 + i, life=0.4, r=5)
    gold_text(im, 540, 520, str(n) if n else "", 190, 1.0)
    a = eb(prog(t, 28.15, 28.5))
    if a > 0:
        ImageDraw.Draw(im).ellipse((540 - 70 * a, 1190 - 70 * a, 540 + 70 * a, 1190 + 70 * a), fill=(34, 24, 6), outline=GOLD, width=6)
        gold_text(im, 540, 1188, "@", 100 * a)

def s13(im, t):
    u = max(0, t - 29.2); cx, cy = 540, 960
    def draw_sym(delay, front):
        uu = max(0, u - delay); th = 4.0 * uu + 1.6 * uu * uu
        for k in range(3):
            ph = th + k * 2 * math.pi / 3; dep = math.sin(ph)
            if (dep >= 0) != front: continue
            x = cx + 380 * math.cos(ph); y = cy + 120 * dep; s = 0.7 + 0.3 * (dep + 1) / 2
            repost_icon(im, x, y, 120 * s, sc(GOLD_T if delay == 0 else GOLD, (0.4 + 0.6 * (dep + 1) / 2) * (1 - delay * 7)))
    for j in (2, 1):
        draw_sym(j * 0.04, False)
    draw_sym(0, False)
    box = phone(im, cx, cy, 340, 680, (22, 18, 10), (210, 170, 70))
    repost_icon(im, cx, cy, 90 * (1 + 0.1 * bump(t, 30.47, 0.2)), sc(GOLD, 0.8))
    for j in (2, 1):
        draw_sym(j * 0.04, True)
    draw_sym(0, True)

def s14(im, t):
    d = ImageDraw.Draw(im); k = eo(prog(t, 32.0, 32.6)); oy = (1 - k) * 160
    d.rounded_rectangle((90, 380 + oy, 990, 1340 + oy), 44, fill=(14, 11, 6), outline=sc(GOLD, 0.8), width=4)
    S = 250; av = logo_s(S); m = logo_mask(S)
    im.paste(av, (540 - S // 2, int(560 + oy) - S // 2), m)
    gold_text(im, 540, 790 + oy, "NEXORA", 84); T(im, (540, 860 + oy), "Official Page", 40, (200, 204, 214))
    for i, lab in enumerate(["Posts", "Followers", "Following"]):
        x = 240 + i * 300; d.rounded_rectangle((x - 70, 920 + oy, x + 70, 944 + oy), 12, fill=(52, 40, 12))
    press = prog(t, 33.3, 33.45) * (1 - prog(t, 33.45, 33.7))
    done = t >= 33.35; sz = 1 + 0.03 * math.sin(t * 6) * (0 if done else 1) - 0.08 * press
    bw, bh = 280 * sz, 70 * sz; by = 1090 + oy
    if not done:
        gold_rrect(im, (540 - bw, by - bh, 540 + bw, by + bh), 70, top=(255, 238, 160), bot=(200, 134, 14))
        T(im, (540, by), "Follow", 70 * sz, (30, 20, 4))
    else:
        d.rounded_rectangle((540 - bw, by - bh, 540 + bw, by + bh), 70, fill=(30, 22, 6), outline=GOLD, width=6)
        T(im, (480, by), "Following", 62, GOLD_T)
        ck = eo(prog(t, 33.4, 33.65)); d.line([(630, by), (650, by + 22 * ck), (690, by - 26 * ck)], fill=GOLD_T, width=10, joint="curve")
        r = 420 * prog(t, 33.35, 33.95)
        d.ellipse((540 - r, by - r * 0.6, 540 + r, by + r * 0.6), outline=sc(GOLD, 1 - prog(t, 33.35, 33.95)), width=5)
    burst(im, t, 33.35, 540, by, 40, 700, 14, life=0.9)
    if t < 33.35:
        r = 40 + 20 * ((t * 1.6) % 1); d.ellipse((760 - r, by + 70 - r, 760 + r, by + 70 + r), outline=sc(GOLD_T, 0.6))

def s15(im, t):
    d = ImageDraw.Draw(im)
    a = eb(prog(t, 35.4, 35.8)); cx, cy = 540, 520
    if a > 0:
        rays(im, cx, cy, t, 12, 700, (90, 64, 14), a=0.5, spread=0.04, rot=0.5)
        r = 190 * a
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(34, 24, 6), outline=GOLD, width=10)
        if r > 30: d.ellipse((cx - r + 22, cy - r + 22, cx + r - 22, cy + r - 22), outline=sc(GOLD, 0.5), width=3)
        gold_text(im, cx, cy + 6, "50", 170 * a)
        burst(im, t, 35.5, cx, cy, 24, 500, 15, life=0.8)
    k = eo(prog(t, 35.9, 36.4)); shake = 5 * math.sin(t * 60) * bump(t, 36.4, 0.15) if t > 36.4 else 0
    pcy = 1230 + (1 - k) * 600
    phone(im, 540 + shake, pcy, 440, 760, (20, 16, 8), (210, 170, 70))
    b = eo(prog(t, 36.4, 36.7))
    if b > 0:
        by = pcy - 250 - (1 - b) * 200
        d.rounded_rectangle((350, by - 62, 730, by + 62), 28, fill=(30, 22, 8), outline=GOLD, width=4)
        S = 90; m = logo_mask(S); im.paste(logo_s(S), (372, int(by) - S // 2), m)
        T(im, (480, by - 22), "NEXORA", 34, GOLD_T, anchor="lm"); T(im, (480, by + 20), "New message", 28, (210, 214, 224), anchor="lm")
        ab = eb(prog(t, 36.75, 37.1))
        if ab > 0:
            r = 74 * ab; d.ellipse((540 - r, pcy + 60 - r, 540 + r, pcy + 60 + r), fill=GOLD)
            d.polygon([(500, pcy + 110), (470, pcy + 150), (545, pcy + 128)], fill=GOLD)
            for j in range(3): d.ellipse((540 - 38 + j * 38 - 8, pcy + 60 - 8, 540 - 38 + j * 38 + 8, pcy + 60 + 8), fill=(40, 28, 6))
        burst(im, t, 36.4, 540, by, 20, 400, 16, life=0.7)

def s16(im, t):
    t0 = 38.95; a = prog(t, t0, t0 + 0.2)
    rays(im, 540, 840, t, 18, 1500, (100, 72, 16), a=0.7 * prog(t, t0, t0 + 0.6), spread=0.035, rot=0.18)
    d = ImageDraw.Draw(im)
    for j in range(3):
        f = prog(t, t0 + j * 0.18, t0 + 1.0 + j * 0.18)
        if 0 < f < 1: d.ellipse((540 - 1300 * eo(f), 840 - 1300 * eo(f), 540 + 1300 * eo(f), 840 + 1300 * eo(f)), outline=sc(GOLD, 1 - f), width=9)
    burst(im, t, t0, 540, 840, 80, 1300, 21, life=1.6, r=8)
    s = 0.25 + 0.80 * eb(prog(t, t0, t0 + 0.65)) + 0.0
    sw = prog(t, 39.7, 40.6)
    logo_draw(im, 540, 840, 860 * min(s, 1.04) * (1 + 0.01 * (t - t0)), a, sweep=(sw * 1.4 - 0.2) if 0 < sw < 1 else None)

SCENES = [(0, 3.2, s01), (3.2, 3.95, s02), (3.95, 6.5, s03), (6.5, 10.3, s04), (10.3, 13.6, None), (13.6, 15.9, s06),
          (15.9, 18.2, s07), (18.2, 20.3, s08), (20.3, 22.9, s09), (22.9, 25.0, s10), (25.0, 27.1, s11), (27.1, 29.1, s12),
          (29.1, 32.0, s13), (32.0, 34.7, s14), (34.7, 38.7, s15), (38.7, 43.01, s16)]
FLASH = [3.2, 3.95, 13.6, 15.9, 18.2, 20.3, 22.9, 25.0, 27.1, 29.1, 32.0, 34.7, 38.7]
PUNCH = [2.63, 3.54, 4.08, 14.15, 16.19, 25.82, 33.35, 36.48, 38.95]

# ---------------------------------------------------------------- subtitles
def tosec(s):
    h, m, r = s.split(":"); sec, ms = r.split(","); return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000
def parse_srt(path):
    cues = []
    for b in open(path, encoding="utf8").read().strip().split("\n\n"):
        l = b.split("\n"); a, bb = l[1].split(" --> "); txt = " ".join(l[2:]); toks = []; space = False
        for m in re.finditer(r'<font color="#[0-9A-Fa-f]+"><b>(.*?)</b></font>|([^<]+)', txt):
            gold = m.group(1) is not None; s = m.group(1) if gold else m.group(2)
            for p in re.finditer(r"\s+|\S+", s):
                if p.group().isspace(): space = True
                else: toks.append((p.group(), gold, space)); space = False
        cues.append((tosec(a), tosec(bb), toks))
    return cues
CUES = parse_srt(os.path.join(ROOT, "subtitles/nexora_ne_gold_tags.srt"))
_sc = {}
def cue_img(i):
    if i in _sc: return _sc[i]
    toks = CUES[i][2]
    for fs in (56, 50, 45, 41):
        f = F(fs); sp = f.getlength(" "); lines = [[]]; wcur = 0
        for tk, g, s_ in toks:
            w = f.getlength(tk) + (sp if s_ and lines[-1] else 0)
            if wcur + w > 1010 and lines[-1]: lines.append([]); wcur = 0; w = f.getlength(tk)
            lines[-1].append((tk, g, s_ and len(lines[-1]) > 0, w)); wcur += w
        if len(lines) == 1: break
    lh = 82; hh = lh * len(lines) + 40; img = Image.new("RGBA", (W, hh), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    lw = [sum(x[3] for x in ln) for ln in lines]; mw = max(lw)
    d.rounded_rectangle((540 - mw / 2 - 36, 4, 540 + mw / 2 + 36, hh - 4), 30, fill=(0, 0, 0, 135))
    for li, ln in enumerate(lines):
        x = 540 - lw[li] / 2; y = 20 + li * lh + lh / 2
        for tk, g, s, w in ln:
            if s: x += sp
            d.text((x, y), tk, font=f, fill=(255, 201, 60, 255) if g else (255, 255, 255, 255), anchor="lm", stroke_width=3, stroke_fill=(0, 0, 0, 255))
            x += f.getlength(tk)
    _sc[i] = img; return img

def draw_sub(im, t):
    for i, (a, b, toks) in enumerate(CUES):
        if a <= t < b:
            img = cue_img(i); f = prog(t, a, a + 0.12)
            if f < 1: img = img.copy(); img.putalpha(img.getchannel("A").point([int(v * f) for v in range(256)]))
            im.paste(img, (0, int(1420 - img.height / 2 + (1 - f) * 14)), img); return

# ---------------------------------------------------------------- frame
LUT_B = [min(255, max(0, int((v - 150) * 1.7))) for v in range(256)] * 3
def bloom(im):
    s = im.resize((W // 4, H // 4), Image.BILINEAR).point(LUT_B)
    b = ImageChops.add(s.filter(ImageFilter.GaussianBlur(6)), s.filter(ImageFilter.GaussianBlur(18)).point([int(v * 0.8) for v in range(256)] * 3))
    return ImageChops.add(im, b.resize((W, H), Image.BILINEAR))

def render_img(t):
    sid = next(i for i, s in enumerate(SCENES) if s[0] <= t < s[1])
    a, b, fn = SCENES[sid]
    if sid <= 3:
        im = COLD_BG.copy(); fn(im, t)
    elif sid == 4:
        if t < 11.92:
            im = Image.new("RGB", (W, H), (3, 3, 5)); s05_dark(im, t); dust(im, t, 18, (110, 120, 140), 0.35)
        else:
            g = gold_base(t, 1.0)
            f = prog(t, 11.92, 12.75); r = 1900 * eo(f) + 1
            if f < 1:
                m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).ellipse((540 - r, 960 - r, 540 + r, 960 + r), fill=255)
                im = Image.composite(g, Image.new("RGB", (W, H), (3, 3, 5)), m.filter(ImageFilter.GaussianBlur(4)))
                dd = ImageDraw.Draw(im)
                for w_, c_ in ((16, GOLD_T), (40, (140, 100, 20))): dd.ellipse((540 - r, 960 - r, 540 + r, 960 + r), outline=sc(c_, 1 - f * 0.7), width=w_)
            else: im = g
    elif sid == 5:
        im = gold_base(t, 0.45 if t < 14.15 else 0.35)
        d = ImageDraw.Draw(im)
        if t < 14.15:
            r = 400 + 30 * math.sin(t * 6); d.ellipse((540 - r, 900 - r, 540 + r, 900 + r), outline=sc(GOLD, 0.5), width=4)
        rays(im, 540, 900, t, 16, 1500, (90, 64, 14), a=0.6 * prog(t, 14.15, 14.7), spread=0.03, rot=0.15)
        k = prog(t, 14.15, 14.7)
        if k > 0:
            sw = prog(t, 14.45, 15.2)
            logo_draw(im, 540, 840, 860 * (0.5 + 0.5 * eb(k)) * (1 + 0.012 * (t - 14.15)), clamp(k * 3), sweep=(sw * 1.4 - 0.2) if 0 < sw < 1 else None)
            burst(im, t, 14.15, 540, 840, 50, 1100, 31, life=1.4)
    elif sid == 15:
        im = gold_base(t, 0.35); fn(im, t)
    else:
        im = gold_base(t, 0.6 if sid in (6, 7) else 0.5); fn(im, t)
    # camera: slow push + punch on triggers
    z = 1 + 0.055 * prog(t, a, min(b, 43.0)) + sum(0.05 * bump(t, p, 0.1) for p in PUNCH)
    if z > 1.0005:
        bw, bh = W / z, H / z; im = im.resize((W, H), Image.BILINEAR, box=(540 - bw / 2, 960 - bh / 2, 540 + bw / 2, 960 + bh / 2))
    dim = 1.0
    if 6.05 <= t < 6.5: dim = 1 - prog(t, 6.05, 6.5)
    elif 6.5 <= t < 6.9: dim = prog(t, 6.5, 6.9)
    elif 9.7 <= t < 10.3: dim = 1 - prog(t, 9.7, 10.3)
    elif t >= 42.55: dim = 1 - prog(t, 42.55, 43.0)
    im = bloom(im)
    im = ImageChops.multiply(im, VIG)
    for fb in FLASH:
        if fb <= t < fb + 0.3:
            fa = 0.55 * math.exp(-(t - fb) / 0.06); im = Image.blend(im, Image.new("RGB", (W, H), (255, 236, 170)), min(0.7, fa))
    if dim < 1: im = ImageChops.multiply(im, Image.new("RGB", (W, H), (int(255 * dim),) * 3))
    draw_sub(im, t)
    return im

def render(i): return render_img(i / FPS).tobytes()

if __name__ == "__main__":
    if sys.argv[2] == "--stills":
        os.makedirs(sys.argv[3], exist_ok=True)
        for ts in sys.argv[4:]: render_img(float(ts)).save(f"{sys.argv[3]}/t{float(ts):05.2f}.png")
        sys.exit()
    n = int(DUR * FPS)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", sys.argv[2]], stdin=subprocess.PIPE)
    with Pool(4) as p:
        for k, fr in enumerate(p.imap(render, range(n), chunksize=3)):
            ff.stdin.write(fr)
            if k % 100 == 0: print(f"frame {k}/{n}", flush=True)
    ff.stdin.close(); ff.wait(); print("done", ff.returncode)
