"""Musica y efectos del reel.

LA MUSICA se sintetiza aqui (sin muestras de nadie). Trap-pop a 144 BPM:
808 con caida de tono, bombo seco, palmas en el tercer tiempo (medio
tiempo), charles rapidos con redobles, pad oscuro y una melodia de
campana en la menor. Un compas dura 1,667 s.

LOS EFECTOS son grabaciones reales con licencia CC0 (dominio publico,
uso comercial sin atribucion), en marketing/instagram/sonidos/: los
packs de Kenney (interfaz e impactos), los whooshes de artisticdude y
el riser de syntheffects. Procedencia y licencias, en esa carpeta.

EL VIDEO VA 1,5 VECES MAS RAPIDO que la animacion de escena.html: los
segundos de abajo se escriben en tiempo de escena (los de render(t)) y
esc() los pasa al tiempo del video. Si se mueve una animacion, se mueve
aqui su efecto con el mismo numero.

Saca dos pistas (45 s, 44,1 kHz, estereo):
  audio.wav                musica + efectos (la que lleva el video)
  audio-solo-efectos.wav   solo los efectos, para poner encima una cancion
                           de la biblioteca de Instagram

Desde la raiz del repo:  python3 marketing/instagram/video-como-topstar/musica.py
"""
import subprocess
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 44100
VEL = 1.5                       # lo mismo que VEL en grabar.js
DUR = 67.5 / VEL                # 45 s
BPM = 144
NEGRA = 60 / BPM
COMPAS = 4 * NEGRA              # 1,667 s
N = int(SR * DUR)
GOLPE = 20.0 / VEL              # entra PLEA5E: compas 8, arranca la parte fuerte
FIN = 26 * COMPAS               # 43,3 s: ultimo acorde
SONIDOS = 'marketing/instagram/sonidos/'
FFMPEG = __import__('os').environ.get('FFMPEG', 'ffmpeg')
rng = np.random.default_rng(11)


def esc(t):
    """segundo de escena.html -> segundo del video"""
    return t / VEL


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
    """campana FM, la melodia"""
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


# La m - Fa - Do - Sol, un acorde por compas
ACORDES = [(33, [57, 60, 64]), (29, [53, 57, 60]), (36, [55, 60, 64]), (31, [55, 59, 62])]
# melodia de campana, dos compases (tiempo en negras, nota, duracion en negras)
MELODIA = [
    [(0, 76, .5), (.5, 72, .5), (1, 76, .5), (1.75, 79, .75), (2.5, 76, .5), (3, 74, .5), (3.5, 72, .5)],
    [(0, 69, .75), (.75, 72, .75), (1.5, 74, .5), (2, 76, 1), (3, 72, .5), (3.5, 74, .5)],
    [(0, 79, .5), (.5, 76, .5), (1, 79, .5), (1.75, 81, .75), (2.5, 79, .5), (3, 76, .5), (3.5, 74, .5)],
    [(0, 74, .75), (.75, 76, .75), (1.5, 74, .5), (2, 71, 1.5), (3.5, 67, .5)],
]
TRAMOS_MELODIA = [(GOLPE, esc(37.5)), (esc(45), esc(60))]

teclas, bajos, pads, bateria, melodia, fx = (pista() for _ in range(6))
golpes = []

for c in range(int(FIN / COMPAS)):
    t0 = c * COMPAS
    raiz, notas = ACORDES[c % 4]
    fuerte = t0 >= GOLPE - .01
    poner(pads, pad(notas, COMPAS + .3, 600 + 1800 * min(1, c / 8) if not fuerte else 2200), t0, 1.5 if not fuerte else .6)
    # melodia: en la intro, solo la mitad y mas bajita
    if not fuerte or any(a <= t0 < z for a, z in TRAMOS_MELODIA):
        for b, n, d in MELODIA[c % 4]:
            if not fuerte and b % 1:
                continue
            poner(melodia, campana(n, d * NEGRA + .4, 1 if fuerte else .9), t0 + b * NEGRA, pan=.15)
    # charles: desde el compas 2 en la intro; redoble de fusas al final de cada 2 compases
    if c >= 2 or fuerte:
        for k in range(8):
            poner(bateria, charles(vel=.9 if k % 2 == 0 else .55), t0 + k * NEGRA / 2, 1 if fuerte else .8, pan=.3)
        if fuerte and c % 2:
            for k in range(8):                            # redoble: fusas en el ultimo tiempo
                poner(bateria, charles(.03, .4 + .08 * k), t0 + 3 * NEGRA + k * NEGRA / 8, pan=.3)
    if not fuerte:
        if c >= 4:                                        # bombo suave para ir cogiendo fuerza
            poner(bateria, bombo(), t0, .45 + .08 * (c - 4)); golpes.append(t0)
        continue
    # bateria de la parte fuerte: medio tiempo, palmas en el 3
    for b in (0, 1.5, 2.75) if c % 2 else (0, 2.5):
        poner(bateria, bombo(), t0 + b * NEGRA); golpes.append(t0 + b * NEGRA)
    poner(bateria, palmas(), t0 + 2 * NEGRA)
    # 808
    for b, d in ((0, 1.4), (1.5, .9), (2.5, 1.4)) if c % 2 == 0 else ((0, 1.4), (1.5, 1.1), (2.75, 1.2)):
        poner(bajos, ochocientos(raiz + 12, d * NEGRA), t0 + b * NEGRA)

# redoble de palmas antes del golpe y final
for k in range(8):
    poner(bateria, palmas(), GOLPE - COMPAS / 2 + k * COMPAS / 16, .15 + .1 * k)
raiz, notas = ACORDES[0]
poner(pads, pad(notas, 1.7, 1800), FIN, .9)
poner(melodia, campana(69, 1.6), FIN)
poner(bajos, ochocientos(raiz + 12, 1.6), FIN)

# compresion al ritmo del bombo
t = np.arange(N) / SR
duck = np.ones(N)
for tb in golpes:
    i, j = int(tb * SR), min(N, int((tb + .3) * SR))
    duck[i:j] = np.minimum(duck[i:j], 1 - .5 * np.exp(-(t[i:j] - tb) / .08))
bajos *= duck[:, None]
pads *= (.35 + .65 * duck)[:, None]
melodia *= (.75 + .25 * duck)[:, None]

# ───────────────────────── efectos, al segundo de cada animacion ─────────────────────────
# (tiempos de escena.html; esc() los pasa al video)
W = 'whoosh.mp3'
poner(fx, muestra('pop.mp3'), esc(.2), .7)
poner(fx, muestra('impact-bass-1.mp3'), esc(1.9), .8); poner(fx, sub_golpe(), esc(1.9), .5)
for tc in (5, 12.5, 37.5, 45, 52.5, 60):                           # cambios de escena
    poner(fx, muestra('whoosh-cinematic.mp3'), esc(tc) - .12, .9)
poner(fx, muestra(W, -3), esc(5.4), .6, pan=-.4); poner(fx, muestra(W, -2), esc(5.6), .6, pan=.4)   # suben los edificios
poner(fx, muestra('kenney-drop_002.wav'), esc(6.5), .7); poner(fx, muestra('kenney-drop_002.wav', 2), esc(6.9), .7)
for k in range(8):                                                 # pasos del cliente
    poner(fx, muestra('kenney-tick_002.wav', -5), esc(9.05) + k * .1, .35, pan=-.2 + .06 * k)
poner(fx, muestra('kenney-error_004.wav'), esc(10.1), .6)          # tu local se apaga
poner(fx, muestra('kenney-select_003.wav'), esc(13.4), .7)
poner(fx, muestra('kenney-scratch_002.wav'), esc(14.6), .8)        # el tachon
poner(fx, muestra('error.mp3'), esc(15.0), .8)
poner(fx, muestra('kenney-confirmation_002.wav'), esc(16.6), .9)   # la forma buena
poner(fx, muestra('riser.mp3'), GOLPE - 1.57, .9)
poner(fx, muestra('impact-bass-2.mp3'), GOLPE, 1); poner(fx, sub_golpe(1.8), GOLPE, .8)
poner(fx, muestra('sparkle.mp3'), esc(20.8), .8)
for m in range(3):                                                 # los tres modelos
    a = 25 + m * 4.17
    poner(fx, muestra(W), esc(a) - .08, .8, pan=.5 - .5 * m)
    for i in range(3):
        poner(fx, muestra('click-soft.mp3'), esc(a + .9 + i * .45), .6)
for i in range(3):                                                 # NFC
    poner(fx, muestra('ping.mp3', 4 * i), esc(39.0 + i * .35), .5)
for i in range(5):                                                 # las cinco estrellas
    poner(fx, muestra('kenney-glass_004.wav', [0, 2, 4, 7, 9][i]), esc(42.9 + i * .3), .7, pan=-.4 + .2 * i)
for k in range(8):
    poner(fx, muestra('key-press.mp3', rng.uniform(-1, 1)), esc(44.0) + k * .04, .35)
poner(fx, muestra('notification.mp3'), esc(44.5), .9)             # ¡publicada!
for i in range(4):
    poner(fx, muestra('pop.mp3', 2 * i), esc(45.5 + i * .9), .6)
poner(fx, muestra('chime.mp3'), esc(49.6), .6)
poner(fx, muestra('pop.mp3'), esc(53.3), .6)                       # te lo llevamos
for i in range(3):
    poner(fx, muestra('kenney-maximize_006.wav', 2 * i), esc(54.3 + i * .35), .45)
for i in range(3):
    poner(fx, muestra('click.mp3'), esc(55.9 + i * .6), .5)
poner(fx, muestra('pop.mp3', 3), esc(60.9), .7)                    # cierre
poner(fx, muestra('impact-bass-1.mp3'), esc(61.7), .6); poner(fx, muestra('kenney-confirmation_004.wav'), esc(61.7), .8)

# ───────────────────────── mezcla y master ─────────────────────────
melodia = reverb(eco(melodia, NEGRA * .75, .28), .4)
bateria = reverb(bateria, .12)
fx = reverb(fx, .22)
musica = 1.0 * bajos + .9 * pads + .95 * bateria + .9 * melodia


def master(x):
    x = filtro(x, 'highpass', 30)
    x = x - .2 * filtro(x, 'lowpass', 70) + .35 * filtro(x, 'bandpass', [1500, 7000])   # para el movil
    nivel = np.sqrt(filtro(np.mean(x ** 2, 1), 'lowpass', 6).clip(1e-9))
    umbral = np.percentile(nivel, 70)
    x = x * np.where(nivel > umbral, (umbral / nivel) ** (1 - 1 / 2.5), 1)[:, None]
    x = x / np.max(np.abs(x)) * 1.5
    x = np.tanh(x) / np.tanh(1.5)
    cola = int(SR * 1.2)
    x[-cola:] *= np.linspace(1, 0, cola)[:, None] ** 1.5
    return x * .89


def guardar(x, nombre):
    s = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open('marketing/instagram/video-como-topstar/' + nombre, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(s.tobytes())


guardar(master(musica + 1.1 * fx), 'audio.wav')
guardar(master(fx), 'audio-solo-efectos.wav')
print('audio.wav y audio-solo-efectos.wav', round(DUR, 2), 's')
