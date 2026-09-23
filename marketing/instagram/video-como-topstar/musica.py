"""Musica y efectos del reel, sintetizados aqui: sin muestras de nadie, sin
derechos que pagar.

Saca dos pistas (60 s, 44,1 kHz, estereo):
  audio.wav                musica + efectos (la que lleva el video)
  audio-solo-efectos.wav   solo los efectos, para poner encima una cancion
                           de la biblioteca de Instagram

Pop tranquilo a 96 BPM: piano electrico (FM, tipo Rhodes), bajo, bateria
por capas, pad y una melodia en la parte fuerte. Un compas dura 2,5 s y
los cortes de escena caen en compas: el golpe de PLEA5E, a los 20 s, abre
el compas 9. Los segundos de los efectos son los de render(t) en
escena.html; si se mueve una animacion, se mueve aqui su efecto.

Desde la raiz del repo:  python3 marketing/instagram/video-como-topstar/musica.py
"""
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 44100
DUR = 60
BPM = 96
NEGRA = 60 / BPM
COMPAS = 4 * NEGRA
N = int(SR * DUR)
GOLPE = 20.0          # entra PLEA5E: arranca la parte fuerte
FIN = 57.5            # ultimo acorde, que se queda sonando
rng = np.random.default_rng(7)


# ───────────────────────── utilidades ─────────────────────────
def hz(n):
    return 440 * 2 ** ((n - 69) / 12)


def tt(d):
    return np.arange(int(SR * d)) / SR


def filtro(x, tipo, f, orden=2):
    return sosfilt(butter(orden, f, tipo, fs=SR, output='sos'), x, axis=0)


def estereo(x, pan=0.0):
    """mono -> estereo con panorama de potencia constante (-1 izq, 1 der)"""
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
    fin = min(len(t), int(SR * .03))  # sin chasquido al cortar
    e[-fin:] *= np.linspace(1, 0, fin)
    return e


def ruido(d):
    return rng.standard_normal(int(SR * d))


# reverberacion: ruido que se apaga, distinto en cada canal (da anchura)
def _ir(d=2.4, caida=.85):
    t = tt(d)
    ir = np.stack([rng.standard_normal(len(t)), rng.standard_normal(len(t))], 1)
    ir *= np.exp(-t / caida)[:, None]
    ir = filtro(ir, 'lowpass', 5500)
    ir[:int(SR * .02)] = 0                       # predelay
    return ir / np.sqrt(np.sum(ir ** 2) / 2)


IR = _ir()


def reverb(p, mezcla):
    mono = p.mean(1)
    r = np.stack([fftconvolve(mono, IR[:, 0])[:N], fftconvolve(mono, IR[:, 1])[:N]], 1)
    return p + mezcla * r * .35


def eco(p, tiempo, realim=.35, n=5):
    """eco ping-pong: cada repeticion salta de lado"""
    out = p.copy()
    d = int(SR * tiempo)
    x = p.mean(1)
    for k in range(1, n + 1):
        g = realim ** k
        lado = np.array([1, 0]) if k % 2 else np.array([0, 1])
        desp = np.zeros(N)
        desp[d * k:] = x[:N - d * k]
        out += (desp * g)[:, None] * lado[None, :]
    return out


# ───────────────────────── instrumentos ─────────────────────────
def rhodes(n, d, vel=1.0):
    """piano electrico FM: el brillo del ataque se apaga y queda la campana"""
    t = tt(d)
    f = hz(n)
    idx = 1.6 * vel * np.exp(-t / .3) + .25
    x = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t))
    x += .12 * np.sin(2 * np.pi * f * 14 * t) * np.exp(-t / .02)        # el golpe del macillo
    return x * envolvente(d, .003, 1.4, .0) * vel * .16


def acorde_rhodes(notas, d, vel=1.0):
    x = sum(rhodes(n, d, vel * (0.9 + .1 * i)) for i, n in enumerate(notas))
    t = tt(d)
    trem = .12 * np.sin(2 * np.pi * 4.2 * t)                               # tremolo estereo
    return np.stack([x * (1 + trem), x * (1 - trem)], 1)


def bajo(n, d):
    t = tt(d)
    f = hz(n)
    x = np.sin(2 * np.pi * f * t) + .35 * np.sin(4 * np.pi * f * t) + .1 * np.sin(6 * np.pi * f * t)
    x = np.tanh(1.3 * x) * envolvente(d, .006, .9, .5)
    return filtro(x, 'lowpass', 420) * .5


def pad(notas, d, corte):
    t = tt(d)
    l, r = np.zeros_like(t), np.zeros_like(t)
    for n in notas:
        for det, lado in ((-.1, 0), (.1, 1), (0, 2)):
            f = hz(n + det)
            onda = sum(np.sin(2 * np.pi * f * k * t + rng.uniform(0, 6)) / k for k in range(1, 8))
            if lado != 1: l += onda
            if lado != 0: r += onda
    x = np.stack([l, r], 1)
    x = filtro(x, 'lowpass', corte)
    a = np.minimum(1, t / .6) * np.minimum(1, (d - t) / .6)
    return x * a[:, None] * .018


def lead(n, d):
    t = tt(d)
    f = hz(n)
    vib = 1 + .004 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t / .25)
    fase = 2 * np.pi * np.cumsum(f * vib) / SR
    x = sum(np.sin(k * fase) / k * (.8 if k % 2 else .35) for k in range(1, 9))
    x = filtro(x, 'lowpass', 3200)
    return x * envolvente(d, .01, .35, .35) * .12


def bombo():
    t = tt(.5)
    cuerpo = np.sin(2 * np.pi * np.cumsum(48 + 110 * np.exp(-t / .035)) / SR) * np.exp(-t / .3)
    click = filtro(ruido(.5), 'highpass', 2500) * np.exp(-t / .004) * .5
    return np.tanh(1.4 * (cuerpo + click)) * .9


def caja():
    t = tt(.45)
    tono = np.sin(2 * np.pi * 190 * t) * np.exp(-t / .07) * .55
    cuerpo = filtro(ruido(.45), 'bandpass', [1400, 8000]) * np.exp(-t / .13)
    return (tono + cuerpo) * .6


def charles(d=.05, vel=1.0):
    return filtro(ruido(d), 'highpass', 8000) * np.exp(-tt(d) / (d / 4)) * .32 * vel


def shaker():
    d = .07
    t = tt(d)
    return filtro(ruido(d), 'bandpass', [4500, 11000]) * np.sin(np.pi * t / d) ** 2 * .12


def platillo(d=2.2):
    t = tt(d)
    x = filtro(ruido(d), 'highpass', 5000) * np.exp(-t / .55)
    x += filtro(ruido(d), 'bandpass', [3000, 7000]) * np.exp(-t / .2) * .5
    return x * .35


# ───────────────────────── efectos ─────────────────────────
def burbuja(f=500, g=1.0):
    """el 'pop' de algo que aparece: suave, redondo, sin chasquido"""
    t = tt(.16)
    fr = f * (1 + 1.2 * (1 - np.exp(-t / .03)))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / .045) * np.minimum(1, t / .002) * .3 * g


def campana(n, d=1.6, g=1.0):
    """campanita FM de cristal"""
    t = tt(d)
    f = hz(n)
    x = np.sin(2 * np.pi * f * t + 2.4 * np.exp(-t / .5) * np.sin(2 * np.pi * f * 3.5 * t))
    return x * envolvente(d, .002, .6) * .2 * g


def zas(d=.55, g=1.0, de=-.7, a=.7):
    """whoosh: tres bandas de ruido que se encienden una tras otra, de grave a
    agudo, y que cruzan de un lado al otro"""
    t = tt(d)
    base = ruido(d)
    x = np.zeros(len(t))
    for i, (b, c) in enumerate(((250, 900), (900, 2600), (2600, 7000))):
        centro = (.35 + .2 * i) * d
        x += filtro(base, 'bandpass', [b, c]) * np.exp(-((t - centro) / (.22 * d)) ** 2)
    pan = de + (a - de) * t / d
    ang = (pan + 1) * np.pi / 4
    return np.stack([x * np.cos(ang), x * np.sin(ang)], 1) * .5 * g


def subida(d):
    t = tt(d)
    base = ruido(d)
    x = sum(filtro(base, 'bandpass', [b, b * 2.5]) * np.clip((t / d) * 4 - i, 0, 1)
            for i, b in enumerate((300, 900, 2400, 5000)))
    tono = np.sin(2 * np.pi * np.cumsum(200 * 2 ** (3 * t / d)) / SR) * .15
    return (x * (t / d) ** 2 * .35 + tono * (t / d) ** 2) * np.minimum(1, (d - t) / .02)


def impacto():
    t = tt(2.5)
    sub = np.sin(2 * np.pi * np.cumsum(55 * np.exp(-t / 1.2) + 30) / SR) * np.exp(-t / .9)
    golpe = filtro(ruido(2.5), 'lowpass', 1800) * np.exp(-t / .12)
    return np.tanh(1.5 * (sub + .6 * golpe)) * .75


def clic(g=1.0):
    t = tt(.02)
    return (filtro(ruido(.02), 'highpass', 3000) * np.exp(-t / .002) + np.sin(2 * np.pi * 2200 * t) * np.exp(-t / .004) * .4) * .25 * g


def tachon():
    """el rotulador que tacha"""
    d = .32
    t = tt(d)
    x = filtro(ruido(d), 'bandpass', [1800, 6000]) * (np.sin(np.pi * t / d) ** .5) * (1 + .5 * np.sin(2 * np.pi * 38 * t))
    return x * .3


def error():
    """'no': dos notas graves y suaves, bajando"""
    x = np.concatenate([np.sin(2 * np.pi * 330 * tt(.1)) * envolvente(.1, .003, .06),
                        np.sin(2 * np.pi * 247 * tt(.18)) * envolvente(.18, .003, .09)])
    return filtro(x, 'lowpass', 1500) * .35


def acierto(g=1.0):
    """'si': arpegio de campanitas subiendo"""
    x = np.zeros(int(SR * 1.8))
    for i, n in enumerate((79, 84, 88)):
        c = campana(n, 1.4)
        j = int(SR * .07 * i)
        x[j:j + len(c)] += c
    return x * g


# ───────────────────────── armonia y ritmo ─────────────────────────
# La m7 - Fa maj7 - Do add9 - Sol6: un acorde por compas
ACORDES = [
    (45, [57, 60, 64, 67]),
    (41, [53, 57, 60, 64]),
    (48, [55, 60, 62, 64]),
    (43, [55, 59, 62, 64]),
]
# melodia de 4 compases (tiempo, nota, duracion en negras)
MELODIA = [
    [(0, 76, .5), (.5, 79, .5), (1, 81, 1.2), (2.5, 79, .5), (3, 76, 1)],
    [(0, 72, .5), (.5, 76, .5), (1, 77, 1.2), (2.5, 76, .5), (3, 72, 1)],
    [(0, 79, .5), (.5, 76, .5), (1, 74, .5), (1.5, 76, .5), (2.5, 79, 1.5)],
    [(0, 74, .5), (.5, 76, .5), (1, 74, .5), (1.5, 71, 1.2), (3, 67, .5), (3.5, 69, .5)],
]
TRAMOS_MELODIA = [(GOLPE, 35.0), (45.0, 52.5)]

teclas, bajos, pads, bateria, melodia, fx = (pista() for _ in range(6))
golpes_bombo = []

compases = int(FIN / COMPAS)
for c in range(compases):
    t0 = c * COMPAS
    raiz, notas = ACORDES[c % 4]
    fuerte = t0 >= GOLPE
    # pad: en la intro se va abriendo el filtro, compas a compas
    corte = 500 + 2200 * min(1, c / 8) if not fuerte else 2600
    poner(pads, pad(notas, COMPAS + .6, corte), t0, 1.0 if not fuerte else .7)
    # piano: en la intro, acordes largos; luego, el ritmo sincopado
    if not fuerte:
        poner(teclas, acorde_rhodes(notas, COMPAS, .7), t0)
        poner(teclas, acorde_rhodes(notas[1:], NEGRA * 1.5, .45), t0 + 2.5 * NEGRA)
    else:
        for b, d, v in ((0, 1.4, .95), (1.5, 1, .7), (2.5, 1.4, .85), (3.5, .5, .55)):
            poner(teclas, acorde_rhodes(notas, d * NEGRA + .15, v), t0 + b * NEGRA)
    # bateria: en la intro, solo charles desde el compas 3 y bombo suave desde el 5
    for b in range(8):
        tb = t0 + b * NEGRA / 2 + (.018 if b % 2 else 0)            # un poco de swing
        if fuerte or c >= 2:
            poner(bateria, charles(vel=(.9 if b % 2 == 0 else .55) * (1 if fuerte else .6)), tb, pan=.25)
    if fuerte:
        for s in range(16):
            poner(bateria, shaker(), t0 + s * NEGRA / 4, .8 if s % 2 else .5, pan=-.3)
        for b in (1, 3):
            poner(bateria, caja(), t0 + b * NEGRA)
        if c % 2:
            poner(bateria, charles(.22, .8), t0 + 3.5 * NEGRA, pan=.25)
    bombos = [0, 2] + ([2.75, 3.5] if (c % 2 and fuerte) else [])
    if fuerte or c >= 4:
        for b in bombos:
            tb = t0 + b * NEGRA
            poner(bateria, bombo(), tb, 1 if fuerte else .55)
            golpes_bombo.append(tb)
    # bajo
    if fuerte or c >= 4:
        for b, d, n in ((0, .9, raiz), (1.5, .5, raiz), (2.5, .9, raiz), (3.5, .45, raiz + 7)):
            poner(bajos, bajo(n, d * NEGRA), t0 + b * NEGRA, 1 if fuerte else .6)
    # melodia
    if any(a <= t0 < z for a, z in TRAMOS_MELODIA):
        for b, n, d in MELODIA[c % 4]:
            poner(melodia, lead(n, d * NEGRA + .05), t0 + b * NEGRA, pan=.1)

# redoble antes del golpe y platillos en los cambios grandes
for k in range(16):
    tk = GOLPE - COMPAS / 2 + k * (COMPAS / 2) / 16
    poner(bateria, caja(), tk, .15 + .5 * k / 16)
for tc in (GOLPE, 45.0, FIN):
    poner(bateria, platillo(), tc, .9)
# final: el acorde que se queda
raiz, notas = ACORDES[2]
poner(teclas, acorde_rhodes(notas + [72], 3.2, .9), FIN)
poner(bajos, bajo(raiz, 2.4), FIN, .9)
poner(pads, pad(notas, 2.6, 2000), FIN, .8)

# compresion al ritmo del bombo: el bajo, el pad y el piano se apartan
t = np.arange(N) / SR
duck = np.ones(N)
for tb in golpes_bombo:
    i = int(tb * SR)
    j = min(N, i + int(SR * .4))
    duck[i:j] = np.minimum(duck[i:j], 1 - .55 * np.exp(-(t[i:j] - tb) / .11))
bajos *= duck[:, None]
pads *= (0.3 + 0.7 * duck)[:, None]
teclas *= (0.7 + 0.3 * duck)[:, None]

# ───────────────────────── efectos, al segundo de cada animacion ─────────────────────────
poner(fx, burbuja(420), .2)
poner(fx, impacto(), 1.9, .45)                                   # "esto te está costando clientes"
for tc in (5, 12.5, 37.5, 45, 52.5):
    poner(fx, zas(), tc - .35)
poner(fx, zas(.8, .8, -.9, .9), 5.3)                             # suben los edificios
poner(fx, burbuja(520), 6.2, .6); poner(fx, burbuja(560), 6.4, .6)
poner(fx, burbuja(640), 6.5); poner(fx, burbuja(700), 6.9)
for k in range(10):                                              # pasos del cliente
    poner(fx, clic(.5), 9.05 + k * .15, pan=-.2 + .05 * k)
poner(fx, error(), 10.1, .8)                                     # tu local se apaga
poner(fx, burbuja(480), 13.4)
poner(fx, tachon(), 14.6); poner(fx, error(), 15.0)
poner(fx, acierto(.9), 16.6)
poner(fx, subida(2.4), 17.6, .8)
poner(fx, impacto(), GOLPE)
poner(fx, campana(91, 2.0, .7), 20.4, pan=-.3); poner(fx, campana(96, 2.0, .5), 20.8, pan=.3)
for m in range(3):                                               # los tres modelos
    a = 25 + m * 4.17
    poner(fx, zas(.6, .8, .8, -.2), a - .15)
    for i in range(3):
        poner(fx, clic(.8), a + .9 + i * .45)
for i in range(3):                                               # NFC
    poner(fx, campana(98, .8, .35), 39.0 + i * .35)
for i in range(5):                                               # las cinco estrellas
    poner(fx, campana([76, 79, 84, 88, 91][i], 1.4, .9), 42.9 + i * .3, pan=-.4 + .2 * i)
for k in range(12):
    poner(fx, clic(.35), 44.0 + k * .042)
poner(fx, acierto(), 44.5)
for i in range(4):
    poner(fx, burbuja(520 + 60 * i), 45.5 + i * .9)
poner(fx, campana(88, 1.4, .7), 49.6)
poner(fx, burbuja(480), 53.4); poner(fx, impacto(), 54.2, .35); poner(fx, acierto(), 54.2)

# ───────────────────────── mezcla y master ─────────────────────────
teclas = reverb(teclas, .5)
melodia = reverb(eco(melodia, NEGRA * .75, .32), .45)
bateria = reverb(bateria, .18)
fx = reverb(fx, .4)

musica = 1.1 * teclas + .7 * bajos + .9 * pads + .8 * bateria + .95 * melodia


def master(x):
    x = filtro(x, 'highpass', 28)
    # se va a oir en un movil: menos grave de relleno y mas presencia
    x = x - .3 * filtro(x, 'lowpass', 90) + .45 * filtro(x, 'bandpass', [1200, 6000])
    # compresor lento sobre el nivel medio (pega la mezcla sin bombear)
    nivel = np.sqrt(filtro(np.mean(x ** 2, 1), 'lowpass', 6).clip(1e-9))
    umbral = np.percentile(nivel, 70)
    gan = np.where(nivel > umbral, (umbral / nivel) ** (1 - 1 / 2.5), 1)
    x = x * gan[:, None]
    x = x / np.max(np.abs(x)) * 1.5
    x = np.tanh(x) / np.tanh(1.5)                                  # limitador suave
    cola = int(SR * 1.5)
    x[-cola:] *= np.linspace(1, 0, cola)[:, None] ** 1.5
    return x * .89                                                 # -1 dBFS


def guardar(x, nombre):
    s = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open('marketing/instagram/video-como-topstar/' + nombre, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(s.tobytes())


guardar(master(musica + .9 * fx), 'audio.wav')
guardar(master(fx), 'audio-solo-efectos.wav')
print('audio.wav y audio-solo-efectos.wav', DUR, 's')
