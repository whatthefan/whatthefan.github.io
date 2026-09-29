"""sfx_synth.py — diseña los SFX del vídeo de placas desde cero, cada uno calcado a la curva de su animación.
Sale sfx-synth.wav (22,3 s, 48 kHz, estéreo). Los que siguen siendo muestras reales van en la lista FX de la página."""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR = 48000; DUR = 22.3; N = int(SR * DUR)
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(5)

cl = lambda x, a=0, b=1: np.minimum(b, np.maximum(a, x))
p = lambda t, t0, d: cl((t - t0) / d)
def ioE(x):
    x = cl(x); y = np.where(x < .5, 2 ** (20 * x - 10) / 2, (2 - 2 ** (-20 * x + 10)) / 2)
    return np.where(x <= 0, 0, np.where(x >= 1, 1, y))
def io(x):
    x = cl(x); return np.where(x < .5, 4 * x ** 3, 1 - (-2 * x + 2) ** 3 / 2)
def iE(x):
    x = cl(x); return np.where(x <= 0, 0, 2 ** (10 * x - 10))

def put(sig, t0, pan=0.0, g=1.0):
    """pan -1..1 (equal power)"""
    i = int(t0 * SR); n = min(len(sig), N - i)
    if n <= 0: return
    a = (pan + 1) * np.pi / 4
    L[i:i + n] += sig[:n] * np.cos(a) * g; R[i:i + n] += sig[:n] * np.sin(a) * g

def tt(d): return np.arange(int(d * SR)) / SR
def env_ar(d, a, r):
    t = tt(d); return np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / r)
def noise(d): return rng.standard_normal(int(d * SR))
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def tone(freq, d):
    """freq: escalar o array del largo de d (glissando)"""
    f = np.broadcast_to(freq, tt(d).shape); return np.sin(2 * np.pi * np.cumsum(f) / SR)

def svf_sweep(x, fc, q=1.2):
    """filtro paso banda de estado variable con frecuencia que cambia muestra a muestra"""
    y = np.zeros_like(x); low = band = 0.0
    fcs = 2 * np.sin(np.pi * np.clip(fc, 20, SR / 6) / SR); damp = 1 / q
    for i in range(len(x)):
        f = fcs[i]; high = x[i] - low - damp * band; band += f * high; low += f * band; y[i] = band
    return y

def whoosh(t0, d, pos, lo=250, hi=3200, q=1.1, gain=1.0, pan_from=0, pan_to=0, pre=.12, post=.35):
    """whoosh cuya fuerza y brillo siguen la velocidad real de la animación. pos(t) va de 0 a 1."""
    T = tt(d + pre + post) - pre; v = np.gradient(pos(T), 1 / SR); v = np.maximum(v, 0); v /= v.max() + 1e-9
    # cola: la energía se apaga suave tras el movimiento
    tail = np.exp(-np.maximum(0, T - d) / .12); v = np.maximum(v, 0) * np.where(T > d, tail, 1)
    v = lp(v, 30, 1)
    fc = lo + (hi - lo) * v ** .8
    s = svf_sweep(noise(len(T) / SR), fc, q) * v ** 1.3
    s += .35 * lp(noise(len(T) / SR), 180) * v ** 2          # cuerpo grave
    s /= np.abs(s).max() + 1e-9
    i0 = int((t0 - pre) * SR); pan = np.linspace(pan_from, pan_to, len(s))
    a = (pan + 1) * np.pi / 4; n = min(len(s), N - i0)
    L[i0:i0 + n] += (s * np.cos(a) * gain)[:n]; R[i0:i0 + n] += (s * np.sin(a) * gain)[:n]

def pop(t0, f0=900, f1=260, g=.5, pan=0):
    d = .09; t = tt(d); f = f1 + (f0 - f1) * np.exp(-t / .012)
    s = tone(f, d) * env_ar(d, .002, .028) + .3 * hp(noise(d), 2000) * env_ar(d, .0005, .004)
    put(s, t0, pan, g)

def campana(t0, f, g=.35, dec=1.1, pan=0):
    d = dec * 3; t = tt(d)
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t / dec) + .45 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t / (dec * .45))
         + .22 * np.sin(2 * np.pi * f * 3.01 * t) * np.exp(-t / (dec * .25)) + .12 * np.sin(2 * np.pi * f * 5.43 * t) * np.exp(-t / (dec * .12)))
    s *= np.minimum(1, t / .002); put(s, t0, pan, g)

def brillo(t0, d=.8, dens=60, g=.12, lo=3500, hi=9000, pan=0):
    """polvo de estrellas: granos agudos cada vez más espaciados"""
    n = int(dens * d)
    for k in range(n):
        tk = t0 + d * (rng.random() ** 1.8); f = rng.uniform(lo, hi); dd = .06
        s = np.sin(2 * np.pi * f * tt(dd)) * env_ar(dd, .001, .012) * (1 - (tk - t0) / d) ** 1.5
        put(s, tk, np.clip(pan + rng.uniform(-.7, .7), -1, 1), g)

def golpe(t0, f=62, g=.9, click=.4):
    d = .35; t = tt(d); fr = f * (1 + 1.6 * np.exp(-t / .02))
    s = tone(fr, d) * env_ar(d, .001, .09) + click * lp(noise(d), 2500) * env_ar(d, .0005, .01)
    put(s, t0, 0, g)

def madera(t0, f, g=.45, pan=0):
    d = .18; t = tt(d)
    s = tone(f, d) * env_ar(d, .0007, .035) + .5 * tone(f * 2.7, d) * env_ar(d, .0005, .012) + .5 * bp(noise(d), 1500, 4000) * env_ar(d, .0003, .004)
    put(s, t0, pan, g)

def tic(t0, f=2600, g=.12, pan=0):
    d = .03; s = bp(noise(d), f * .7, f * 1.3) * env_ar(d, .0003, .004) + .4 * tone(f * .5, d) * env_ar(d, .0005, .006)
    put(s, t0, pan, g)

def lapiz(t0, d, g=.07, pan=0):
    """trazo de lápiz: ruido raspado con temblor, fuerza según la velocidad del trazo (io)"""
    T = tt(d + .05); v = np.gradient(io(T / d), 1 / SR); v = np.maximum(v, 0) / (np.max(v) + 1e-9)
    jit = lp(rng.standard_normal(len(T)), 35) ; jit = .6 + .4 * jit / (np.abs(jit).max() + 1e-9)
    s = bp(noise(len(T) / SR), 1800, 6500) * v * jit
    put(s / (np.abs(s).max() + 1e-9), t0, pan, g)

# ---------------- la partitura ----------------
# 2,5–3,55 · la estrella piensa: un zumbido dorado que respira con los rayos
d = 1.25; t = tt(d); k = np.minimum(1, t / .35) * np.where(t > 1.0, np.exp(-(t - 1.0) / .08), 1)
trem = .65 + .35 * np.sin((2.5 + t) * 7)
pad = sum(a * np.sin(2 * np.pi * f * t + ph) for a, f, ph in [(.5, 659.3, 0), (.35, 987.8, 1), (.25, 1318.5, 2), (.12, 1975.5, .5)])
put(pad * k * trem, 2.5, 0, .16); brillo(2.5, .9, 30, .08)

# 3,5–3,85 la estrella se encoge y 3,6–4,15 las líneas de la rejilla salen disparadas (4 cremalleras)
for i, pn in enumerate([-.6, .6, -.25, .25]):
    t0 = 3.6 + i * .06; dd = .55; T = tt(dd + .25); pos = ioE(T / dd); v = np.maximum(np.gradient(pos, 1 / SR), 0); v /= v.max()
    fc = 900 + 5200 * pos; s = svf_sweep(noise(len(T) / SR), fc, 5) * v ** 1.2
    put(s / np.abs(s).max(), t0, pn, .4)
# 4,0–5,1 · los 9 bocetos se dibujan a lápiz
for j in range(9): lapiz(4.0 + j * .07, .55, .14, [-.5, 0, .5][j % 3])
# 5,1–5,95 · zambullida en la viñeta: whoosh que sigue la velocidad de la cámara
whoosh(5.1, .85, lambda T: ioE(T / .85), 180, 2600, 1.0, 1.5, -.2, .2)
# 5,9–6,35 cae la bola · 6,35 bota (cuerpo) + muelle de goma que sube con el rebote
whoosh(5.9, .45, lambda T: cl(T / .45) ** 2, 400, 2200, 1.8, .18)
golpe(6.35, 70, .65, .25)
d = .55; t = tt(d); f = 190 + 120 * np.sin(np.minimum(1, t / .4) * np.pi) ; vib = 1 + .05 * np.sin(2 * np.pi * 16 * t) * np.exp(-t / .2)
put(tone(f * vib, d) * env_ar(d, .004, .14), 6.37, 0, .22)
# 6,95 · la bola se parte en 5 estrellas: 5 pops que se abren a los lados
for i in range(5): pop(6.95 + i * .03, 700 + i * 140, 240 + i * 40, .32, (i - 2) * .35)
# 7,2–7,84 · se llenan una a una: escala pentatónica ascendente · 7,95 brillo final
for i, f in enumerate([880, 987.8, 1108.7, 1318.5, 1480]): campana(7.2 + i * .16, f, .16, .7, (i - 2) * .35)
campana(7.95, 1760, .13, 1.2); campana(7.97, 2217.5, .08, 1.0); brillo(7.95, 1.0, 70, .07)
# 8,25–8,65 · las estrellas se juntan en una raya (whoosh corto que se cierra al centro)
whoosh(8.25, .4, lambda T: ioE(T / .4), 600, 4200, 2.2, .45, 0, 0, .05, .2)
# 8,8–9,3 · cada letra de «placas» baraja 6 fuentes: un tic por cambio, y un toque seco al quedarse
for i in range(6):
    t0 = 8.8 + i * .07
    for kk in range(6): tic(t0 + kk * .07, 2000 + 300 * i + 150 * kk, .1, (i - 2.5) * .25)
    madera(t0 + .42, 520 + 40 * i, .12, (i - 2.5) * .25)
# 9,85–10,4 · la palabra vuela al buscador (arriba a la izquierda) y la barra se estira
whoosh(9.85, .55, lambda T: ioE(T / .55), 300, 3000, 1.3, 1.2, .3, -.4)
# 11,15 · Enter · 11,2 / 11,3 / 11,38 · suben los tres resultados
madera(11.12, 180, .25)
for i, t0 in enumerate([11.2, 11.3, 11.38]): whoosh(t0, .6, lambda T: 1 - (1 - cl(T / .6)) ** 5, 500 + 200 * i, 2400, 1.6, .4 - .08 * i, 0, 0, .02, .15)
# 12,05–12,6 · el resultado se abre hasta ser la web: whoosh + subida grave
whoosh(12.05, .55, lambda T: ioE(T / .55), 150, 2000, .9, .8)
d = .7; t = tt(d); put(tone(60 + 70 * cl(t / .55), d) * np.minimum(1, t / .3) * np.exp(-np.maximum(0, t - .5) / .1), 12.05, 0, .2)
# 12,6 · aparece la estrella en la portada
campana(12.62, 1318.5, .15, .9); brillo(12.6, .6, 40, .06)
# 12,85–16,2 · LA CAÍDA: silbato de caída que baja con la estrella + viento según la velocidad del scroll
d = 3.4; t = tt(d); kc = io(t / 3.35)
f = 2100 * (1 - kc) + 330 * kc; vib = 1 + .012 * np.sin(2 * np.pi * 5.5 * t)
amp = np.minimum(1, t / .25) * (.55 + .45 * kc) * np.where(t > 3.33, np.exp(-(t - 3.33) / .02), 1)
put(tone(f * vib, d) * amp + .25 * tone(f * 2 * vib, d) * amp * .3, 12.85, 0, .17)
v = np.maximum(np.gradient(kc, 1 / SR), 0); v /= v.max(); wind = svf_sweep(noise(d), 250 + 2400 * v, .8) * v ** 1.4
put(wind / np.abs(wind).max() * np.where(t > 3.33, np.exp(-(t - 3.33) / .05), 1), 12.85, 0, .5)
# pasa por las secciones de la web: 6 «fush» cortos cuando la estrella cruza cada bloque
for tk in [13.55, 14.05, 14.4, 14.72, 15.05, 15.45]: whoosh(tk, .18, lambda T: cl(T / .18), 1500, 5000, 2.5, .08, rng.uniform(-.6, .6), rng.uniform(-.6, .6), .02, .06)
# 16,22 · aterriza en el pie: golpe + polvo de estrellas
golpe(16.22, 55, .75, .5); brillo(16.22, .7, 60, .09); campana(16.23, 659.3, .12, .8)
# 16,35–16,85 · sube (silbido ascendente) · 16,98–17,3 · cae al hueco (descendente, acelera)
d = .55; t = tt(d); k = ioE(t / .5); put(tone(420 + 1400 * k, d) * np.sin(np.pi * cl(t / .55)) ** .7, 16.35, .2, .1)
whoosh(16.35, .5, lambda T: ioE(T / .5), 400, 3000, 1.4, .2, 0, .4, .05, .1)
d = .33; t = tt(d); k = (t / .32) ** 2; put(tone(1900 - 1300 * k, d) * np.minimum(1, t / .05), 16.98, .4, .11)
whoosh(16.98, .32, lambda T: cl(T / .32) ** 2, 600, 3800, 1.6, .28, .4, .4, .02, .02)
# 16,88–17,2 · aterrizan las letras P L E A E (bloques de madera, graves)
for i, (tk, f) in enumerate(zip([16.88, 16.96, 17.04, 17.12, 17.2], [196, 220, 247, 262, 294])): madera(tk, f, .42, [-.7, -.45, -.2, 0, .7][i]); golpe(tk, 90, .18, 0)
# 17,3 · (woah-drop real) + los rayos: cola de brillo
brillo(17.32, 1.4, 80, .06)
# 17,75 · «Pide tu placa.» se enfoca: soplo suave
whoosh(17.75, .7, lambda T: 1 - 2 ** (-10 * cl(T / .7)), 800, 4500, .8, .08)
# 18,0 · el botón entra con muelle: «bloop» que sigue al muelle
d = .7; t = tt(d); w = 2 * np.pi * 2.4; z = .45; m = 1 - np.exp(-z * w * t) * np.cos(w * np.sqrt(1 - z * z) * t)
put(tone(260 + 260 * m, d) * env_ar(d, .005, .18), 18.0, 0, .5)
# 18,6 · (clic real) + onda que se expande
d = .8; t = tt(d); put(tone(95 - 25 * cl(t / .6), d) * env_ar(d, .003, .22), 18.6, 0, .45); brillo(18.62, .5, 25, .05)
# 19,3–20,25 · la cámara se aleja al chat
whoosh(19.3, .95, lambda T: ioE(T / .95), 140, 1600, .9, 1.4, .1, -.1)

# ---------------- mezcla ----------------
ir_t = np.arange(int(1.3 * SR)) / SR
irL = rng.standard_normal(len(ir_t)) * np.exp(-ir_t / .32); irR = rng.standard_normal(len(ir_t)) * np.exp(-ir_t / .32)
irL[:int(.012 * SR)] = 0; irR[:int(.017 * SR)] = 0; irL /= np.sqrt((irL ** 2).sum()); irR /= np.sqrt((irR ** 2).sum())
wetL = fftconvolve(L, irL)[:N]; wetR = fftconvolve(R, irR)[:N]
L2 = L + .22 * wetL; R2 = R + .22 * wetR
L2 = hp(L2, 30); R2 = hp(R2, 30)
pk = max(np.abs(L2).max(), np.abs(R2).max()); g = 10 ** (-5 / 20) / pk
st = np.stack([L2, R2], 1) * g
wavfile.write('sfx-synth.wav', SR, (np.tanh(st * 1.1) / np.tanh(1.1) * 32767 * .95).astype(np.int16))
print('ok', DUR)
