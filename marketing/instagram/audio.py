"""Lo comun al audio de los videos de Instagram: pistas, instrumentos
sintetizados, efectos grabados (marketing/instagram/sonidos/, todos CC0)
y el master.

Se usa asi, desde el guion de audio de cada video:

    import audio as a
    a.duracion(45)                 # antes de nada: cuanto dura la pista
    fx = a.pista()
    a.poner(fx, a.muestra('pop.mp3'), 1.2)
    a.guardar(a.master(fx), 'ruta/audio.wav')

Las rutas son desde la raiz del repo, que es desde donde se ejecuta todo.
"""
import os
import subprocess
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 44100
N = 0                                   # muestras de la pista: lo pone duracion()
SONIDOS = 'marketing/instagram/sonidos/'
FFMPEG = os.environ.get('FFMPEG', 'ffmpeg')
rng = np.random.default_rng(11)


def duracion(segundos):
    global N
    N = int(SR * segundos)


# ───────────────────────── utilidades ─────────────────────────
def hz(n):
    return 440 * 2 ** ((n - 69) / 12)


def tt(d):
    return np.arange(int(SR * d)) / SR


def filtro(x, tipo, f, orden=2):
    return sosfilt(butter(orden, f, tipo, fs=SR, output='sos'), x, axis=0)


def estereo(x, pan=0.0):
    a = (pan + 1) * np.pi / 4
    return np.stack([x * np.cos(a), x * np.sin(a)], 1) * 1.414


def pista():
    return np.zeros((N, 2))


def poner(p, x, t0, g=1.0, pan=0.0):
    if x.ndim == 1:
        x = estereo(x, pan)
    i = int(round(t0 * SR))
    if i >= N or i + len(x) <= 0:
        return
    if i < 0:
        x, i = x[-i:], 0
    x = x[:N - i]
    p[i:i + len(x)] += g * x


def envolvente(d, ataque=.005, caida=.3, sostener=0.0):
    t = tt(d)
    e = np.minimum(1, t / ataque) * (sostener + (1 - sostener) * np.exp(-t / caida))
    fin = min(len(t), int(SR * .02))
    e[-fin:] *= np.linspace(1, 0, fin)
    return e


def ruido(d):
    return rng.standard_normal(int(SR * d))


def _ir(d=2.0, caida=.6):
    t = tt(d)
    ir = np.stack([rng.standard_normal(len(t)), rng.standard_normal(len(t))], 1)
    ir *= np.exp(-t / caida)[:, None]
    ir = filtro(ir, 'lowpass', 6000)
    ir[:int(SR * .015)] = 0
    return ir / np.sqrt(np.sum(ir ** 2) / 2)


IR = _ir()


def reverb(p, mezcla):
    mono = p.mean(1)
    r = np.stack([fftconvolve(mono, IR[:, 0])[:N], fftconvolve(mono, IR[:, 1])[:N]], 1)
    return p + mezcla * r * .35


def eco(p, tiempo, realim=.3, n=4):
    out = p.copy()
    d = int(SR * tiempo)
    x = p.mean(1)
    for k in range(1, n + 1):
        lado = np.array([1, .3]) if k % 2 else np.array([.3, 1])
        desp = np.zeros(N)
        desp[d * k:] = x[:N - d * k]
        out += (desp * realim ** k)[:, None] * lado[None, :]
    return out


def compresion_al_bombo(golpes, cuanto=.5):
    """curva que baja un momento en cada golpe de bombo (sidechain)"""
    t = np.arange(N) / SR
    duck = np.ones(N)
    for tb in golpes:
        i, j = int(tb * SR), min(N, int((tb + .3) * SR))
        duck[i:j] = np.minimum(duck[i:j], 1 - cuanto * np.exp(-(t[i:j] - tb) / .08))
    return duck


# ───────────────────────── efectos grabados ─────────────────────────
_cache = {}


def muestra(nombre, semitonos=0.0):
    """un archivo de sonidos/ en mono, normalizado a pico 1 y, si se pide,
    subido o bajado de tono (remuestreando, como un disco mas rapido)"""
    if nombre not in _cache:
        crudo = subprocess.run([FFMPEG, '-loglevel', 'error', '-i', SONIDOS + nombre,
                                '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'],
                               capture_output=True, check=True).stdout
        x = np.frombuffer(crudo, np.int16).astype(float) / 32768
        _cache[nombre] = x / (np.max(np.abs(x)) or 1)
    x = _cache[nombre]
    if semitonos:
        r = 2 ** (semitonos / 12)
        x = np.interp(np.arange(0, len(x) - 1, r), np.arange(len(x)), x)
    return x


def sub_golpe(d=1.4):
    """el grave que se nota en el pecho debajo de un impacto grabado"""
    t = tt(d)
    return np.sin(2 * np.pi * np.cumsum(38 + 70 * np.exp(-t / .05)) / SR) * np.exp(-t / .45) * .9


# ───────────────────────── instrumentos ─────────────────────────
def ochocientos(n, d):
    """808: seno con caida de tono al empezar y saturacion"""
    t = tt(d)
    f = hz(n) * (1 + 1.2 * np.exp(-t / .018))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    x = np.tanh(2.2 * x) / np.tanh(2.2)
    return x * envolvente(d, .002, .9, .15) * .55


def bombo():
    t = tt(.35)
    cuerpo = np.sin(2 * np.pi * np.cumsum(55 + 160 * np.exp(-t / .02)) / SR) * np.exp(-t / .12)
    click = filtro(ruido(.35), 'highpass', 3000) * np.exp(-t / .003) * .6
    return np.tanh(1.8 * (cuerpo + click)) * .8


def palmas():
    t = tt(.4)
    x = np.zeros(len(t))
    for k, o in enumerate((0, .008, .017, .024)):   # varias manos, un pelin desfasadas
        i = int(o * SR)
        seg = filtro(ruido(.4 - o), 'bandpass', [1000, 5500]) * np.exp(-tt(.4 - o) / (.012 if k < 3 else .12))
        x[i:i + len(seg)] += seg
    tono = np.sin(2 * np.pi * 210 * t) * np.exp(-t / .04) * .4
    return (x + tono) * .55


def charles(d=.045, vel=1.0):
    return filtro(ruido(d), 'highpass', 7500) * np.exp(-tt(d) / (d / 5)) * .3 * vel


def campana(n, d=.9, vel=1.0):
    """campana FM, para melodias"""
    t = tt(d)
    f = hz(n)
    x = np.sin(2 * np.pi * f * t + 1.8 * np.exp(-t / .25) * np.sin(2 * np.pi * f * 2 * t))
    x += .25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t / .08)
    return x * envolvente(d, .002, .45) * .18 * vel


def pad(notas, d, corte):
    t = tt(d)
    l, r = np.zeros_like(t), np.zeros_like(t)
    for n in notas:
        for det, lado in ((-.12, 0), (.12, 1)):
            f = hz(n + det)
            onda = sum(np.sin(2 * np.pi * f * k * t + rng.uniform(0, 6)) / k for k in range(1, 7))
            (l if lado == 0 else r)[:] += onda
    x = filtro(np.stack([l, r], 1), 'lowpass', corte)
    a = np.minimum(1, t / .3) * np.minimum(1, (d - t) / .3)
    return x * a[:, None] * .02


# ───────────────────────── master ─────────────────────────
def master(x, cola=1.2):
    x = filtro(x, 'highpass', 30)
    x = x - .2 * filtro(x, 'lowpass', 70) + .35 * filtro(x, 'bandpass', [1500, 7000])   # para el movil
    nivel = np.sqrt(filtro(np.mean(x ** 2, 1), 'lowpass', 6).clip(1e-9))
    umbral = np.percentile(nivel, 70)
    x = x * np.where(nivel > umbral, (umbral / nivel) ** (1 - 1 / 2.5), 1)[:, None]
    x = x / np.max(np.abs(x)) * 1.5
    x = np.tanh(x) / np.tanh(1.5)
    c = int(SR * cola)
    x[-c:] *= np.linspace(1, 0, c)[:, None] ** 1.5
    return x * .89                                                   # -1 dBFS


def guardar(x, ruta):
    s = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(ruta, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(s.tobytes())
