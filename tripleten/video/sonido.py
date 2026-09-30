"""Banda sonora del vídeo de demo.

    python3 sonido.py efectos.json salida.wav

Lee los efectos que apunta director.js durante la grabación (cada toque,
tecla, mensaje de Nova, confeti...) y sintetiza cada uno en su instante exacto,
más una base musical suave debajo. Todo se genera aquí con numpy: no hay
samples de terceros ni licencias de por medio.
"""
import json
import sys
import wave

import numpy as np

SR = 48000
rng = np.random.default_rng(7)


def t_axis(dur):
    return np.arange(int(dur * SR)) / SR


def env(n, attack=0.004, decay=0.1, curve=1.0):
    """Ataque lineal y caída exponencial."""
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-t / decay) ** curve


def tone(freq, dur, decay=0.2, attack=0.003, partials=((1, 1.0),), vib=0.0):
    t = t_axis(dur)
    out = np.zeros_like(t)
    for mult, amp in partials:
        f = freq * mult
        phase = 2 * np.pi * f * t + (vib * np.sin(2 * np.pi * 5 * t) if vib else 0)
        out += amp * np.sin(phase) * np.exp(-t / (decay / mult ** 0.5))
    return out * np.clip(t / attack, 0, 1)


def sweep(f0, f1, dur, decay=None):
    t = t_axis(dur)
    f = f0 * (f1 / f0) ** (t / dur)
    ph = 2 * np.pi * np.cumsum(f) / SR
    e = np.sin(np.pi * np.clip(t / dur, 0, 1)) if decay is None else np.exp(-t / decay)
    return np.sin(ph) * e


def lowpass(x, cutoff):
    """Filtro de un polo (suficiente para suavizar ruido)."""
    a = np.exp(-2 * np.pi * np.asarray(cutoff) / SR)
    if np.ndim(a) == 0:
        a = np.full(len(x), a)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc
        y[i] = acc
    return y


def noise_swoosh(dur, f0, f1, amp=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    cut = f0 * (f1 / f0) ** (t / dur)
    x = rng.standard_normal(n)
    y = lowpass(x, cut) - lowpass(x, cut * 0.35)
    shape = np.sin(np.pi * t / dur) ** 1.6
    return y * shape * amp / (np.abs(y).max() + 1e-9)


def mixs(*parts):
    """Suma señales de distinta longitud."""
    out = np.zeros(max(len(p) for p in parts))
    for p in parts:
        out[: len(p)] += p
    return out


BELL = ((1, 1.0), (2.0, 0.35), (3.01, 0.12), (4.2, 0.06))
PLUCK = ((1, 1.0), (2, 0.4), (3, 0.15))


def note(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


# ---------- Efectos ----------
def s_tap(x=0.5):
    click = rng.standard_normal(int(0.006 * SR)) * env(int(0.006 * SR), 0.0005, 0.0015)
    body = tone(1250 + 300 * x, 0.06, decay=0.012, partials=((1, 1.0), (1.5, 0.3)))
    out = np.zeros(int(0.07 * SR))
    out[: len(click)] += click * 0.35
    out[: len(body)] += body * 0.8
    return out * 0.42


def s_tapsoft(x=0.5):
    return s_tap(x) * 0.6


def s_key():
    f = rng.uniform(2100, 2700)
    c = tone(f, 0.035, decay=0.006, partials=((1, 1.0), (1.7, 0.4)))
    n = rng.standard_normal(len(c)) * env(len(c), 0.0003, 0.002) * 0.3
    return (c + n) * 0.16 * rng.uniform(0.8, 1.1)


def s_pop():
    return mixs(sweep(520, 1150, 0.09, decay=0.035) * 0.34, tone(1150, 0.12, decay=0.03) * 0.08)


def s_msg():
    a = tone(note(84), 0.5, decay=0.14, partials=BELL)
    b = tone(note(91), 0.5, decay=0.18, partials=BELL)
    out = np.zeros(int(0.62 * SR))
    out[: len(a)] += a
    o = int(0.075 * SR)
    out[o : o + len(b)] += b * 0.8
    return out * 0.16


def s_send():
    return mixs(noise_swoosh(0.2, 700, 5000) * 0.16, sweep(600, 1400, 0.12, decay=0.05) * 0.1)


def s_open():
    return mixs(noise_swoosh(0.28, 400, 3800) * 0.18, tone(note(76), 0.3, decay=0.09, partials=PLUCK) * 0.08)


def s_close():
    return noise_swoosh(0.24, 3200, 380) * 0.15


def s_whoosh():
    return noise_swoosh(0.34, 500, 4200) * 0.12


def s_swoosh():
    return noise_swoosh(0.7, 250, 3000) * 0.22


def s_switch():
    out = np.zeros(int(0.3 * SR))
    for i, f in enumerate((note(79), note(86))):
        c = tone(f, 0.15, decay=0.05, partials=PLUCK)
        o = int(i * 0.07 * SR)
        out[o : o + len(c)] += c
    return out * 0.16


def arp(midis, gap, decay=0.35, partials=BELL, tail=0.8):
    out = np.zeros(int((gap * len(midis) + tail) * SR))
    for i, m in enumerate(midis):
        c = tone(note(m), tail, decay=decay, partials=partials)
        o = int(i * gap * SR)
        out[o : o + len(c)] += c * (0.9 ** i)
    return out


def s_match():
    return arp([72, 76, 79, 84], 0.085) * 0.14


def s_step():
    return arp([79, 84], 0.09, decay=0.25) * 0.14


def s_tick():
    return tone(note(84), 0.35, decay=0.08, partials=((1, 1.0), (4, 0.25), (9.2, 0.05))) * 0.13


def s_ding():
    return tone(note(88), 0.9, decay=0.3, partials=BELL) * 0.12


def s_li():
    return tone(note(81), 0.4, decay=0.1, partials=PLUCK) * 0.12


def s_reveal():
    dur = 1.6
    t = t_axis(dur)
    rise = noise_swoosh(0.55, 200, 6000) * 0.16
    chord = sum(tone(note(m), dur, decay=0.7, attack=0.01, partials=BELL) for m in (60, 67, 72, 76, 79))
    out = np.zeros(int((0.45 + dur) * SR))
    out[: len(rise)] += rise
    o = int(0.42 * SR)
    out[o : o + len(chord)] += chord * 0.085
    sub = np.sin(2 * np.pi * 55 * t) * np.exp(-t / 0.25)
    out[o : o + len(sub)] += sub * 0.25
    return out


def s_success():
    out = np.zeros(int(2.2 * SR))
    for i in range(14):
        m = int(rng.choice([84, 86, 88, 91, 93, 96, 98]))
        c = tone(note(m), 0.6, decay=0.12, partials=BELL)
        o = int((0.03 + i * 0.07 + rng.uniform(0, 0.03)) * SR)
        pan_amp = rng.uniform(0.5, 1.0)
        out[o : o + len(c)] += c * pan_amp * (1 - i / 18)
    return out * 0.075


def s_scrub(d=2.2):
    n = int(d * SR)
    out = np.zeros(n + int(0.3 * SR))
    steps = 22
    for i in range(steps):
        m = 67 + round(i * 17 / steps)
        c = tone(note(m), 0.18, decay=0.035, partials=PLUCK)
        o = int(i * d / steps * SR)
        out[o : o + len(c)] += c * (0.6 + 0.4 * i / steps)
    return out * 0.07


def s_intro():
    dur = 3.4
    t = t_axis(dur)
    pad = sum(np.sin(2 * np.pi * note(m) * t + 0.3 * np.sin(2 * np.pi * 0.2 * t)) for m in (48, 55, 60, 64, 67))
    pad *= np.clip(t / 1.2, 0, 1) * np.exp(-np.maximum(t - 2.2, 0) / 0.5)
    out = pad * 0.035
    logo = arp([72, 79, 84, 88], 0.11, decay=0.5, tail=1.6) * 0.13
    o = int(0.5 * SR)
    out[o : o + len(logo)] += logo[: len(out) - o]
    return out


def s_outro():
    dur = 4.5
    t = t_axis(dur)
    chord = sum(tone(note(m), dur, decay=1.4, attack=0.02, partials=BELL) for m in (53, 60, 65, 69, 72, 77))
    sub = np.sin(2 * np.pi * note(41) * t) * np.exp(-t / 0.8)
    out = chord * 0.06 + sub * 0.18
    sparkle = arp([84, 89, 93, 96, 101], 0.09, decay=0.3, tail=1.0) * 0.08
    o = int(0.25 * SR)
    out[o : o + len(sparkle)] += sparkle
    return out


SFX = {
    "tap": s_tap, "tapsoft": s_tapsoft, "key": s_key, "pop": s_pop, "msg": s_msg,
    "send": s_send, "open": s_open, "close": s_close, "whoosh": s_whoosh, "swoosh": s_swoosh,
    "switch": s_switch, "match": s_match, "step": s_step, "tick": s_tick, "ding": s_ding,
    "li": s_li, "reveal": s_reveal, "success": s_success, "scrub": s_scrub,
    "intro": s_intro, "outro": s_outro,
}
# Separación mínima entre dos efectos iguales (evita metralletas).
MIN_GAP = {"pop": 0.25, "tick": 0.12, "ding": 0.3, "success": 1.0, "whoosh": 0.2, "step": 0.4}


# ---------- Base musical ----------
def music(total):
    """Pads cálidos + arpegio suave a 96 BPM: Am9 · Fmaj7 · C · G6."""
    bpm = 96
    beat = 60 / bpm
    bar = beat * 4
    prog = [(57, [60, 64, 67, 71]), (53, [57, 60, 64, 69]), (48, [55, 60, 64, 67]), (55, [59, 62, 64, 67])]
    n = int(total * SR)
    L = np.zeros(n)
    R = np.zeros(n)
    t_bar = t_axis(bar + 1.5)
    k = 0
    start = 0.0
    while start < total:
        root, chord = prog[k % 4]
        o = int(start * SR)
        seg = np.zeros(len(t_bar))
        for j, m in enumerate(chord):
            f = note(m)
            det = 1 + 0.0025 * (j - 1.5)
            v = np.sin(2 * np.pi * f * det * t_bar) + 0.3 * np.sin(2 * np.pi * 2 * f * t_bar)
            seg += v
        shape = np.clip(t_bar / 0.6, 0, 1) * np.clip((bar + 1.2 - t_bar) / 1.2, 0, 1)
        seg *= shape * 0.012
        bass = np.sin(2 * np.pi * note(root - 12) * t_bar) * np.clip(t_bar / 0.05, 0, 1) * np.exp(-t_bar / 1.6) * 0.05
        m = min(len(seg), n - o)
        L[o : o + m] += seg[:m] * 1.0 + bass[:m]
        R[o : o + m] += seg[:m] * 0.85 + bass[:m]
        # arpegio en corcheas, alternando canales
        for s8 in range(8):
            mm = chord[[0, 2, 1, 3, 2, 0, 3, 1][s8]] + 12
            c = tone(note(mm), 0.5, decay=0.16, partials=PLUCK) * 0.022
            oo = o + int(s8 * beat / 2 * SR)
            if oo >= n:
                break
            mm_ = min(len(c), n - oo)
            (L if s8 % 2 == 0 else R)[oo : oo + mm_] += c[:mm_]
            (R if s8 % 2 == 0 else L)[oo : oo + mm_] += c[:mm_] * 0.45
        # hi-hat suave en las partes débiles
        for s8 in range(1, 8, 2):
            h = rng.standard_normal(int(0.03 * SR))
            h = (h - lowpass(h, 6000)) * env(len(h), 0.001, 0.008) * 0.012
            oo = o + int(s8 * beat / 2 * SR)
            if oo + len(h) < n:
                L[oo : oo + len(h)] += h * 0.8
                R[oo : oo + len(h)] += h
        start += bar
        k += 1
    fade_in = np.clip(t_axis(total)[:n] / 2.5, 0, 1)
    fade_out = np.clip((total - t_axis(total)[:n]) / 3.0, 0, 1)
    g = fade_in * fade_out
    return L * g, R * g


def reverb(x, secs=1.1, mix=0.18):
    n = int(secs * SR)
    t = np.arange(n) / SR
    ir = rng.standard_normal(n) * np.exp(-t / (secs / 5))
    ir = lowpass(ir, 5500)
    ir[: int(0.012 * SR)] = 0
    ir /= np.sqrt(np.sum(ir ** 2))
    size = 1
    while size < len(x) + n:
        size *= 2
    wet = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return x + wet * mix


def limiter(st, ceil):
    """Limitador con 10 ms de anticipación y 150 ms de recuperación."""
    blk = 240
    n = len(st)
    nb = (n + blk - 1) // blk
    pad = np.zeros((nb * blk, 2))
    pad[:n] = st
    peak = np.abs(pad).reshape(nb, blk, 2).max(axis=(1, 2)) + 1e-9
    g = np.minimum(1.0, ceil / peak)
    g = np.minimum.reduce([np.roll(g, -k) for k in range(3)] + [g])
    rel = np.exp(-blk / (0.15 * SR))
    out = np.empty_like(g)
    cur = 1.0
    for i in range(nb):
        cur = g[i] if g[i] < cur else g[i] + (cur - g[i]) * rel
        out[i] = cur
    gs = np.interp(np.arange(nb * blk), np.arange(nb) * blk + blk / 2, out)[:n]
    return np.clip(st * gs[:, None], -ceil, ceil)


def main():
    src, dst = sys.argv[1], sys.argv[2]
    data = json.load(open(src, encoding="utf-8"))
    total = float(data["duration"])
    offset = float(data.get("offset", 0))
    n = int(total * SR)
    fxL = np.zeros(n + SR * 5)
    fxR = np.zeros(n + SR * 5)
    duck = np.ones(n + SR * 5)
    last = {}
    for e in data["events"]:
        name = e["n"]
        if name not in SFX:
            continue
        t = float(e["t"]) - offset
        if t < 0 or t > total:
            continue
        if name in MIN_GAP and t - last.get(name, -9) < MIN_GAP[name]:
            continue
        last[name] = t
        if name in ("tap", "tapsoft"):
            snd = SFX[name](e.get("x", 0.5))
        elif name == "scrub":
            snd = SFX[name](e.get("d", 2.2))
        else:
            snd = SFX[name]()
        pan = float(e.get("x", 0.5)) - 0.5 if name in ("tap", "tapsoft") else rng.uniform(-0.12, 0.12)
        pan = max(-0.6, min(0.6, pan))
        o = int(t * SR)
        m = min(len(snd), len(fxL) - o)
        fxL[o : o + m] += snd[:m] * np.sqrt(0.5 - pan / 2) * 1.41
        fxR[o : o + m] += snd[:m] * np.sqrt(0.5 + pan / 2) * 1.41
        if name in ("reveal", "success", "outro", "match"):
            d = int(1.2 * SR)
            dd = min(d, len(duck) - o)
            duck[o : o + dd] = np.minimum(duck[o : o + dd], 0.55 + 0.45 * np.linspace(0, 1, dd) ** 2)
    fxL, fxR = reverb(fxL[:n]), reverb(fxR[:n])
    mL, mR = music(total)
    L = fxL + mL[:n] * duck[:n]
    R = fxR + mR[:n] * duck[:n]
    st = np.stack([L, R], axis=1)
    st -= st.mean(axis=0)
    st *= 0.075 / (np.sqrt(np.mean(st ** 2)) + 1e-9)  # nivel medio ~ -22 dBFS
    st = limiter(st, 0.89)  # picos a ~ -1 dBFS sin distorsionar
    pcm = (st * 32767).astype("<i2")
    with wave.open(dst, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("sonido:", dst, "%.1f s" % total, len(data["events"]), "eventos")


if __name__ == "__main__":
    main()
