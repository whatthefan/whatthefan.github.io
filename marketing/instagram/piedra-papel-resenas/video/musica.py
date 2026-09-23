"""Sonido del video "Piedra, papel... ¡reseñas!". Los segundos son los de
render(t) en escena.html (los monta ../video.py, que tambien deja en
tiempos.json el segundo de cada tecla de la nota). Utilidades,
instrumentos y efectos grabados (CC0): ../../audio.py.

  0 - 3,6   piedra, papel, ¿tijera?: tres golpes secos
  3,6 - 7   ¡reseñas!: entra el ritmo
  7 - cta   zoom al movil: la musica se queda en un pad muy bajito y se oye
            el teclado del movil: un toque corto y suave por letra (click-soft,
            un "tic" de 20 ms, como el teclado del iPhone), la barra
            espaciadora un poco mas grave y el intro con otro click
  cta - fin la notificacion y vuelve el ritmo para el Comenta PLACA

Todos los efectos van ligeros: golpes sin subgrave, impactos y whooshes
bajitos, para que no tapen la musica ni el teclado.

Desde la raiz del repo:  python3 marketing/instagram/piedra-papel-resenas/video/musica.py
"""
import json
import sys

import numpy as np

sys.path.insert(0, 'marketing/instagram')
import audio as a  # noqa: E402

V = 'marketing/instagram/piedra-papel-resenas/video/'
T = json.load(open(V + 'tiempos.json'))
DUR, CTA = T['dur'], T['cta']
a.duracion(DUR)
K = 5 / 3                        # compas a 144 BPM
NEGRA = K / 4
REVELA = 3.6                     # "¡Reseñas!": entra la parte fuerte
ZOOM = 7.0
m = a.muestra

bajos, pads, bateria, melodia, fx, teclado = (a.pista() for _ in range(6))
golpes = []
ACORDES = [(33, [57, 60, 64]), (29, [53, 57, 60]), (36, [55, 60, 64]), (31, [55, 59, 62])]


def ritmo(desde, hasta):
    """la parte fuerte: bombo, palmas, charles, 808, campana"""
    c, t0 = 0, desde
    while t0 < hasta - .05:
        raiz, notas = ACORDES[c % 4]
        a.poner(pads, a.pad(notas, K + .3, 2200), t0, .6)
        for b in (0, 1.5, 2.75) if c % 2 else (0, 2.5):
            if t0 + b * NEGRA < hasta:
                a.poner(bateria, a.bombo(), t0 + b * NEGRA); golpes.append(t0 + b * NEGRA)
        if t0 + 2 * NEGRA < hasta:
            a.poner(bateria, a.palmas(), t0 + 2 * NEGRA)
        for k in range(8):
            if t0 + k * NEGRA / 2 < hasta:
                a.poner(bateria, a.charles(vel=.9 if k % 2 == 0 else .55), t0 + k * NEGRA / 2, pan=.3)
        for b, d in ((0, 1.4), (1.5, .9), (2.5, 1.4)):
            if t0 + b * NEGRA < hasta:
                a.poner(bajos, a.ochocientos(raiz + 12, d * NEGRA), t0 + b * NEGRA)
        for b, n in ((0, 76), (.5, 79), (1, 81), (2, 79), (2.5, 76), (3, 74)):
            if t0 + b * NEGRA < hasta:
                a.poner(melodia, a.campana(n + (0 if c % 2 == 0 else -3), .5, .8), t0 + b * NEGRA, pan=.15)
        t0 += K
        c += 1


# el "piedra... papel... tijera...": tres golpes secos, cada vez mas fuertes
for i, t in enumerate((.3, 1.3, 2.3)):
    a.poner(bateria, a.bombo(), t, .55 + .08 * i); golpes.append(t)
    a.poner(bateria, a.palmas(), t, .4 + .08 * i)
    a.poner(fx, m('whoosh.mp3', 3), t - .2, .25)
    a.poner(fx, m('kenney-drop_002.wav', -2 + 2 * i), t, .3)
    a.poner(pads, a.pad([57, 60, 64], .9, 1400), t, .6)
# la tijera, tachada y al suelo
a.poner(fx, m('kenney-scratch_002.wav'), 2.85, .45)
a.poner(fx, m('kenney-error_004.wav'), 3.0, .5)
a.poner(fx, m('whoosh-short.mp3', -4), 3.2, .3)
# ¡reseñas!: golpe y arranca el ritmo
a.poner(fx, m('riser.mp3'), REVELA - 1.1, .3)
a.poner(fx, m('impact-bass-2.mp3'), REVELA, .45)
a.poner(fx, m('kenney-confirmation_002.wav'), REVELA + .05, .4)   # el marcador: gana la estrella
ritmo(REVELA, ZOOM)
a.poner(fx, m('whoosh-cinematic.mp3'), 3.62, .4)                   # entra la placa
a.poner(fx, m('whoosh.mp3', -2), 3.75, .3)                          # entra el movil
for i in range(3):
    a.poner(fx, m('ping.mp3', 4 * i), 4.3 + i * .2, .3)             # NFC
for i in range(5):
    a.poner(fx, m('kenney-glass_004.wav', [0, 2, 4, 7, 9][i]), 4.5 + i * .16, .5, pan=-.5 + .25 * i)
a.poner(fx, m('sparkle.mp3'), 5.4, .4)
a.poner(fx, m('pop.mp3', 2), 5.6, .35)

# zoom al movil: whoosh largo y la musica se queda en un pad bajito
a.poner(fx, m('whoosh-cinematic.mp3', -3), ZOOM - .1, .45)
t0, c = ZOOM + .85, 0
while t0 < CTA:
    raiz, notas = ACORDES[c % 4]
    a.poner(pads, a.pad(notas, 2 * K + .4, 800), t0, .45)
    t0 += 2 * K
    c += 1
# el teclado del movil: un "tic" corto y suave por letra, casi igual cada vez
for i, (t, ch) in enumerate(T['teclas']):
    if ch == '\n':
        a.poner(teclado, m('click.mp3', -3), t, .6)
    elif ch == ' ':
        a.poner(teclado, m('click-soft.mp3', -3), t, .6)
    else:
        a.poner(teclado, m('click-soft.mp3', 1 + a.rng.uniform(-.2, .2)), t, .55 + .1 * a.rng.random(),
                pan=-.08 + .16 * a.rng.random())

# el final: notificacion y vuelve el ritmo
a.poner(fx, m('whoosh-short.mp3'), CTA, .25)                        # baja el teclado
a.poner(fx, m('notification.mp3'), CTA + .25, .6)
a.poner(fx, m('pop.mp3', 3), CTA + .55, .35)
ritmo(CTA + .55, DUR - .9)
raiz, notas = ACORDES[0]
a.poner(pads, a.pad(notas, 1.4, 1800), DUR - .9, .8); a.poner(melodia, a.campana(69, 1.4), DUR - .9)

duck = a.compresion_al_bombo(golpes)
bajos *= duck[:, None]
pads *= (.35 + .65 * duck)[:, None]
melodia = a.reverb(a.eco(melodia, NEGRA * .75, .28), .4)
bateria = a.reverb(bateria, .12)
fx = a.reverb(fx, .22)
# el teclado, como el del iPhone: suave y apagado. Sin los agudos (que es lo que lo hace
# sonar duro), sin recortar el pico y bajito: se oye porque la musica esta casi en silencio
teclado = a.filtro(a.filtro(teclado, 'lowpass', 4500), 'highpass', 400)
teclado = teclado / np.max(np.abs(teclado)) * .13
a.guardar(a.master(.9 * bajos + .85 * pads + .8 * bateria + .8 * melodia + .8 * fx + teclado, cola=.8), V + 'audio.wav')
a.guardar(a.master(fx + teclado, cola=.8), V + 'audio-solo-efectos.wav')
print('audio.wav', DUR, 's')
