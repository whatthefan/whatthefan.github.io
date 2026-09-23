"""Musica y efectos del video, sintetizados aqui: sin muestras de nadie, sin
derechos que pagar. Saca audio.wav (60 s, 44,1 kHz, estereo).

96 BPM: un compas dura 2,5 s, y los cortes de escena caen en compas
(el golpe de PLEA5E, a los 20 s, es el comienzo del compas 9).
Desde la raiz del repo:  python3 marketing/instagram/video-como-topstar/musica.py
"""
import wave

import numpy as np
from scipy.signal import butter, sosfilt

SR = 44100
DUR = 60
BPM = 96
NEGRA = 60 / BPM
COMPAS = 4 * NEGRA
N = int(SR * DUR)
rng = np.random.default_rng(5)


def hz(nota):  # 60 = do central
    return 440 * 2 ** ((nota - 69) / 12)


def t_(d):
    return np.arange(int(SR * d)) / SR


def env(d, a=.005, r=.2):
    t = t_(d)
    return np.minimum(1, t / a) * np.exp(-t / r)


def poner(pista, x, t0, g=1.0):
    i = int(t0 * SR)
    if i >= len(pista):
        return
    x = x[:len(pista) - i]
    pista[i:i + len(x)] += g * x


def filtro(x, tipo, f, orden=2):
    return sosfilt(butter(orden, f, tipo, fs=SR, output='sos'), x)


# ---------- instrumentos ----------
def kick():
    t = t_(.45)
    f = 45 + 110 * np.exp(-t / .045)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .16)


def palmas():
    x = rng.standard_normal(int(SR * .25))
    x = filtro(x, 'bandpass', [900, 3200])
    t = t_(.25)
    return x * (np.exp(-t / .06) + .5 * np.exp(-np.maximum(0, t - .012) / .05) * (t > .012)) * .6


def charles(abierto=False):
    d = .22 if abierto else .06
    x = filtro(rng.standard_normal(int(SR * d)), 'highpass', 7000)
    return x * np.exp(-t_(d) / (d / 3)) * .35


def bajo(nota, d):
    t = t_(d)
    f = hz(nota)
    x = np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t)
    return np.tanh(1.5 * x) * np.minimum(1, t / .01) * np.exp(-t / .5) * .55


def pluck(nota, d=.5):
    t = t_(d)
    f = hz(nota)
    x = np.sin(2 * np.pi * f * t) + .45 * np.sin(4 * np.pi * f * t) + .15 * np.sin(6 * np.pi * f * t)
    return x * env(d, .003, .16) * .22


def pad(notas, d):
    t = t_(d)
    x = np.zeros_like(t)
    for n in notas:
        for det in (-.08, .08):
            f = hz(n + det)
            for k in range(1, 7):  # sierra suave
                x += np.sin(2 * np.pi * f * k * t + k) / k
    x = filtro(x, 'lowpass', 1800)
    a = np.minimum(1, t / .35) * np.minimum(1, (d - t) / .4)
    return x * a * .035


# ---------- efectos ----------
def pop(f=900):
    t = t_(.12)
    return np.sin(2 * np.pi * (f + 900 * np.exp(-t / .02)) * t) * np.exp(-t / .03) * .5


def ding(nota):
    t = t_(1.2)
    f = hz(nota)
    x = np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / .2) + .25 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t / .08)
    return x * env(1.2, .002, .35) * .32


def whoosh(d=.5):
    x = rng.standard_normal(int(SR * d))
    t = t_(d)
    # barrido de un paso-banda de grave a agudo
    trozos = np.array_split(x, 10)
    y = np.concatenate([filtro(c, 'bandpass', [300 + 500 * i, 900 + 900 * i]) for i, c in enumerate(trozos)])
    return y * np.sin(np.pi * t / d) ** 2 * .45


def subida(d):
    x = rng.standard_normal(int(SR * d))
    t = t_(d)
    trozos = np.array_split(x, 24)
    y = np.concatenate([filtro(c, 'bandpass', [200 + 250 * i, 600 + 500 * i]) for i, c in enumerate(trozos)])
    return y * (t / d) ** 2 * .5


def golpe():
    t = t_(1.6)
    x = np.sin(2 * np.pi * np.cumsum(38 + 90 * np.exp(-t / .06)) / SR) * np.exp(-t / .5)
    x += filtro(rng.standard_normal(len(t)), 'lowpass', 2500) * np.exp(-t / .25) * .4
    return x * .9


def tecla():
    return filtro(rng.standard_normal(int(SR * .03)), 'bandpass', [2000, 5000]) * np.exp(-t_(.03) / .006) * .25


def thud():
    t = t_(.3)
    return np.sin(2 * np.pi * np.cumsum(70 + 80 * np.exp(-t / .03)) / SR) * np.exp(-t / .09) * .8


# ---------- composicion ----------
musica = np.zeros(N)
bateria = np.zeros(N)
fx = np.zeros(N)

# Do - Sol - La m - Fa, un acorde por compas
ACORDES = [(48, [60, 64, 67, 72]), (43, [59, 62, 67, 71]), (45, [60, 64, 69, 72]), (41, [60, 65, 69, 72])]
GOLPE = 20              # entra PLEA5E
FIN_RITMO = 57.5
compases = int(DUR / COMPAS) + 1

for c in range(compases):
    t0 = c * COMPAS
    raiz, notas = ACORDES[c % 4]
    intro = t0 < GOLPE
    poner(musica, pad(notas, COMPAS + .3), t0, .7 if intro else 1)
    # arpegio en semicorcheas (en la intro, corcheas y mas bajito)
    paso = NEGRA / (2 if intro else 4)
    orden = [0, 1, 2, 3, 2, 1, 2, 3]
    for k in range(int(COMPAS / paso)):
        tt = t0 + k * paso
        if tt >= FIN_RITMO:
            break
        poner(musica, pluck(notas[orden[k % 8]] + 12), tt, .55 if intro else .8)
    if intro:
        # latido suave de bombo en la intro, que va cogiendo fuerza
        if c >= 2:
            for b in range(4):
                poner(bateria, kick(), t0 + b * NEGRA, .35 + .1 * (c - 2))
        continue
    if t0 >= FIN_RITMO:
        continue
    for b in range(4):
        tb = t0 + b * NEGRA
        poner(bateria, kick(), tb, .9)
        if b in (1, 3):
            poner(bateria, palmas(), tb, .7)
        poner(bateria, charles(), tb + NEGRA / 2, .9)
        poner(bateria, charles(), tb, .5)
        # bajo en corcheas con salto de octava
        poner(musica, bajo(raiz, NEGRA / 2), tb, 1)
        poner(musica, bajo(raiz + 12, NEGRA / 2), tb + NEGRA / 2, .7)

# acorde final que se queda sonando
poner(musica, pad([48, 55, 60, 64, 67, 72], 3.5), FIN_RITMO, 1.4)
poner(musica, ding(84), FIN_RITMO, .8)

# efectos, al segundo de cada animacion (ver render(t) en escena.html)
poner(fx, pop(600), .2); poner(fx, golpe(), 1.9, .45)          # gancho
for t in (6.5, 6.9):
    poner(fx, pop(700), t)                                      # notas de los locales
poner(fx, whoosh(.9), 9.0, .6)                                  # el cliente cruza
poner(fx, pop(700), 13.4)
poner(fx, whoosh(.35), 14.6, .8); poner(fx, pop(300), 15.0)    # tachon y X
poner(fx, ding(84), 16.6, .8); poner(fx, ding(91), 16.72, .6)  # la forma buena
poner(fx, subida(2.0), 18.0)
poner(fx, golpe(), GOLPE)
poner(fx, ding(96), 20.8, .5)
for m in range(3):                                              # los tres modelos
    a = 25 + m * 4.17
    poner(fx, whoosh(.6), a - .2, .8)
    for i in range(3):
        poner(fx, pop(900 + 100 * i), a + .9 + i * .45, .55)
for t in (5, 12.5, 37.5, 45, 52.5):
    poner(fx, whoosh(.5), t - .3, .9)
for i in range(3):
    poner(fx, ding(96), 39.0 + i * .35, .35)                    # NFC
for i in range(5):
    poner(fx, ding(76 + [0, 4, 7, 12, 16][i]), 42.9 + i * .3, .9)
for k in range(10):
    poner(fx, tecla(), 44.0 + k * .05)
poner(fx, ding(91), 44.5, .8); poner(fx, ding(96), 44.62, .6)
for i in range(4):
    poner(fx, pop(800 + 80 * i), 45.5 + i * .9, .6)
poner(fx, ding(88), 49.6, .7)
poner(fx, pop(700), 53.4); poner(fx, golpe(), 54.2, .4); poner(fx, ding(91), 54.2, .7)

# mezcla: la musica un poco agachada donde hay efectos grandes
mezcla = .8 * musica + .75 * bateria + fx
mezcla = filtro(mezcla, 'highpass', 30)
mezcla[-int(SR * 1.2):] *= np.linspace(1, 0, int(SR * 1.2))
mezcla = np.tanh(1.2 * mezcla / np.max(np.abs(mezcla)) * 1.6) / np.tanh(1.2 * 1.6)
mezcla *= .89  # -1 dBFS

# estereo: un poco de anchura retrasando un canal unos milisegundos
izq = mezcla
der = np.concatenate([np.zeros(int(SR * .012)), mezcla[:-int(SR * .012)]]) * .5 + mezcla * .5
st = (np.stack([izq, der], 1) * 32767).astype(np.int16)
with wave.open('marketing/instagram/video-como-topstar/audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
print('audio.wav', DUR, 's')
