"""Synthesises a music + SFX bed (numpy only) for the animatic, ducked under the voiceover.
The voiceover itself is NOT processed here: it is mixed in by ffmpeg at unity gain.
usage: make_audio.py <voice.mp3> <out_bed.wav>"""
import sys, subprocess, wave
import numpy as np

SR = 44100; DUR = 43.0; N = int(SR * DUR)
rs = np.random.RandomState(3)
bed = np.zeros(N); sfx = np.zeros(N)

def put(buf, t, x, g=1.0):
    i = int(t * SR)
    if i >= N or i + len(x) <= 0: return
    a = max(0, -i); b = min(len(x), N - i)
    buf[i + a:i + b] += g * x[a:b]

def tt(d): return np.arange(int(d * SR)) / SR
def env(d, a=0.005, r=None):
    t = tt(d); r = r or d * 0.8
    return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / (r / 4))
def sine(f, d, g=1.0, a=0.005, r=None): return g * np.sin(2 * np.pi * f * tt(d)) * env(d, a, r)
def lp_sweep(x, f0, f1):
    n = len(x); fc = np.linspace(f0, f1, n); al = 1 - np.exp(-2 * np.pi * fc / SR); y = np.empty(n); s = 0.0
    for i in range(n):
        s += al[i] * (x[i] - s); y[i] = s
    return y
def noise(d): return rs.randn(int(d * SR))
def whoosh(d, f0, f1, g=1.0):
    y = lp_sweep(noise(d), f0, f1); y /= np.abs(y).max() + 1e-9
    t = tt(d); e = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5
    return g * y * e
def riser(d, g=1.0):
    y = lp_sweep(noise(d), 300, 7000); y /= np.abs(y).max() + 1e-9
    t = tt(d); return g * y * (t / d) ** 2 + g * 0.25 * np.sin(2 * np.pi * np.cumsum(200 + 1400 * (t / d) ** 2) / SR) * (t / d)
def impact(g=1.0):
    t = tt(1.6); f = 48 + 90 * np.exp(-t * 14)
    return g * (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.8) + 0.35 * lp_sweep(noise(1.6), 3000, 200) * np.exp(-t * 6))
def ding(f=1760, d=1.2, g=1.0): return g * (sine(f, d, 1, 0.002, d) + 0.4 * sine(f * 1.5, d, 1, 0.002, d * 0.7) + 0.25 * sine(f * 2.01, d, 1, 0.002, d * 0.5))
def tick(f, g=1.0): return g * sine(f, 0.12, 1, 0.001, 0.1)
def click(g=1.0): return g * (lp_sweep(noise(0.05), 8000, 1500) * np.exp(-tt(0.05) * 90) * 3 + sine(1800, 0.05, 0.4, 0.001, 0.04))
def thump(f=55, g=1.0): t = tt(0.35); return g * np.sin(2 * np.pi * np.cumsum(f + 60 * np.exp(-t * 30)) / SR) * np.exp(-t * 11)
def shimmer(d, g=1.0, f=2600):
    t = tt(d); x = np.zeros_like(t)
    for k in range(6): x += np.sin(2 * np.pi * f * (1 + 0.31 * k) * t + k) * (0.5 + 0.5 * np.sin(2 * np.pi * (3 + k) * t))
    return g * x / 6 * np.minimum(t / 0.2, 1) * np.exp(-t / (d / 3))
def buzz(d=0.3, g=1.0): t = tt(d); return g * np.sign(np.sin(2 * np.pi * 70 * t)) * 0.4 * np.minimum(t / 0.01, 1) * (1 - t / d)
def chime2(g=1.0): return np.concatenate([ding(1318, 0.5, g), ding(1760, 0.9, g)]) if False else None

# ---------------- SFX (times: measured segment boundaries / estimated triggers from NEXORA_PRODUCTION_PLAN.md)
S = lambda t, x, g=0.5: put(sfx, t, x, g)
S(2.63, tick(260)); S(3.54, tick(420)); S(4.08, tick(200))
S(4.53, sine(330, 0.9, 1, 0.01, 0.9) * np.linspace(1, 0.2, int(0.9 * SR)) * 0.5, 0.4)
S(8.83, thump(50), 0.7); S(9.20, thump(46), 0.55)
S(11.40, riser(0.52), 0.55)
S(11.92, impact(), 0.95); S(11.92, whoosh(1.2, 400, 6000), 0.7); S(12.2, shimmer(2.0), 0.35)
S(14.15, impact(), 0.8); S(14.15, shimmer(2.2, 1, 3200), 0.45); S(14.4, whoosh(0.9, 1000, 8000), 0.4)
S(16.70, click(), 0.6); S(16.80, whoosh(0.8, 500, 7000), 0.6); S(16.85, ding(1568, 1.2), 0.45); S(16.9, shimmer(1.5), 0.35)
S(18.85, whoosh(1.1, 300, 5000), 0.55); S(19.95, ding(2093, 1.3), 0.5)
S(20.40, tick(900), 0.6); S(21.56, whoosh(1.0, 300, 4500), 0.6)
for i, f in enumerate((523, 659, 784, 1047)): S(22.97 + 0.48 * i, ding(f, 0.7), 0.35)
S(25.60, thump(60), 0.8); S(25.90, thump(66), 0.9); S(26.20, shimmer(1.2), 0.4)
for i in range(10): S(27.40 + 0.15 * i, tick(500 * 2 ** (i / 12 * 1.2), 1.0) * 1.0, 0.55)
S(28.15, ding(1976, 0.8), 0.4)
for i in range(4): S(29.75 + 0.5 * i, whoosh(0.5, 600 + 300 * i, 6000), 0.5)
S(33.35, click(), 0.9); S(33.38, ding(1568, 0.9), 0.5)
S(35.50, ding(1760, 0.9), 0.45)
S(36.40, buzz(0.3), 0.5); S(36.45, ding(1318, 0.5), 0.5); S(36.70, ding(1760, 0.9), 0.5)
S(38.95, impact(), 1.0); S(38.95, whoosh(1.2, 500, 9000), 0.6); S(39.0, shimmer(4.0, 1, 3000), 0.5)
for b in (3.2, 3.95, 13.6, 15.9, 18.2, 20.3, 22.9, 25.0, 27.1, 29.1, 32.0, 34.7): S(b - 0.05, whoosh(0.3, 800, 5000), 0.18)

# ---------------- music
def note(f): return 440 * 2 ** ((f - 69) / 12)
def pad(freqs, t0, d, g):
    t = tt(d); x = np.zeros_like(t)
    for f in freqs:
        for dt in (-0.4, 0.4): x += np.sin(2 * np.pi * (f + dt) * t) + 0.3 * np.sin(2 * np.pi * 2 * (f + dt) * t)
    x *= np.minimum(t / 0.6, 1) * np.minimum((d - t) / 0.5, 1)
    put(bed, t0, x / (len(freqs) * 2.5) * g)
# tense cold bed 0 - 11.4
pad([55, 82.4], 0, 11.4, 0.55); pad([110, 130.8], 0, 11.4, 0.18)
for k in range(int(11.4 / 1.2)): put(bed, k * 1.2, thump(45, 0.25))
# gold bed 11.92 - 43
BAR = 2.4
chords = [[57, 60, 64], [53, 57, 60], [60, 64, 67], [55, 59, 62]]; bass = [33, 29, 36, 31]
t0 = 11.92; k = 0
while t0 < 38.95:
    ch = chords[k % 4]; d = min(BAR, 38.95 - t0)
    pad([note(n) for n in ch], t0, d + 0.2, 0.9); pad([note(bass[k % 4] + 12)], t0, d + 0.2, 0.7)
    for b in range(4):
        tb = t0 + b * BAR / 4
        if tb < 38.95: put(bed, tb, thump(52, 0.9))
    for e in range(8):
        te = t0 + e * BAR / 8
        if te < 38.95:
            put(bed, te, sine(note(ch[e % 3] + 12), 0.35, 0.28, 0.003, 0.3))
            if e % 2: put(bed, te, lp_sweep(noise(0.05), 9000, 6000) * np.exp(-tt(0.05) * 70) * 0.25)
    t0 += BAR; k += 1
pad([note(n) for n in (57, 60, 64, 69)], 38.95, 4.05, 1.1); pad([note(33), note(45)], 38.95, 4.05, 0.9)
bed *= np.minimum(1, np.clip((DUR - np.arange(N) / SR) / 0.9, 0, 1))  # fade out

# ---------------- ducking from the voiceover
v = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", sys.argv[1], "-f", "s16le", "-ac", "1", "-ar", "8000", "-"], capture_output=True).stdout, np.int16) / 32768.0
hop = 160; e = np.array([np.sqrt(np.mean(v[i:i + hop] ** 2)) for i in range(0, len(v), hop)])
e = np.convolve(e, np.ones(8) / 8, "same"); duck = 1 - 0.6 * np.clip(e / 0.04, 0, 1)
duck = np.interp(np.arange(N) / SR, np.arange(len(duck)) * hop / 8000, duck)
duck = np.convolve(duck, np.ones(2205) / 2205, "same")
bed *= duck; sfx *= (1 - 0.25 * (1 - duck / duck.max()))   # SFX duck slightly

bed *= 0.20 / (np.abs(bed).max() + 1e-9) * 1.0; sfx *= 0.40 / (np.abs(sfx).max() + 1e-9)
mix = np.clip(bed + sfx, -0.95, 0.95)
with wave.open(sys.argv[2], "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print("bed written", len(mix) / SR, "s")
