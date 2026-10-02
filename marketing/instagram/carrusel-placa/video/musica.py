"""Musica y efectos del video "la placa, destripada" (21,7 s = 13 compases
a 144 BPM). Los segundos son los de render(t) en escena.html, que caen en
compas. Utilidades, instrumentos y efectos grabados (CC0): ../../audio.py.

Desde la raiz del repo:  python3 marketing/instagram/carrusel-placa/video/musica.py
"""
import sys

sys.path.insert(0, 'marketing/instagram')
import audio as a  # noqa: E402

K = 5 / 3                       # un compas
DUR = 13 * K
GOLPE = 7 * K                   # 11,67 s: la placa se junta y entra la parte fuerte
FIN = 12 * K                    # 20 s: el acorde final
NEGRA = K / 4
a.duracion(DUR)
V = 'marketing/instagram/carrusel-placa/video/'

ACORDES = [(33, [57, 60, 64]), (29, [53, 57, 60]), (36, [55, 60, 64]), (31, [55, 59, 62])]
MELODIA = [
    [(0, 76, .5), (.5, 72, .5), (1, 76, .5), (1.75, 79, .75), (2.5, 76, .5), (3, 74, .5), (3.5, 72, .5)],
    [(0, 69, .75), (.75, 72, .75), (1.5, 74, .5), (2, 76, 1), (3, 72, .5), (3.5, 74, .5)],
    [(0, 79, .5), (.5, 76, .5), (1, 79, .5), (1.75, 81, .75), (2.5, 79, .5), (3, 76, .5), (3.5, 74, .5)],
    [(0, 74, .75), (.75, 76, .75), (1.5, 74, .5), (2, 71, 1.5), (3.5, 67, .5)],
]
bajos, pads, bateria, melodia, fx = (a.pista() for _ in range(5))
golpes = []
for c in range(12):
    t0 = c * K
    raiz, notas = ACORDES[c % 4]
    fuerte = t0 >= GOLPE - .01
    a.poner(pads, a.pad(notas, K + .3, 900 + 1300 * min(1, c / 7)), t0, 1.4 if not fuerte else .6)
    for b, n, d in MELODIA[c % 4]:
        if fuerte or b % 1 == 0:
            a.poner(melodia, a.campana(n, d * NEGRA + .4, 1 if fuerte else .85), t0 + b * NEGRA, pan=.15)
    for k in range(8):                                   # charles desde el principio: esto va rapido
        a.poner(bateria, a.charles(vel=.9 if k % 2 == 0 else .55), t0 + k * NEGRA / 2, 1 if fuerte else .7, pan=.3)
    if fuerte and c % 2:
        for k in range(8):
            a.poner(bateria, a.charles(.03, .4 + .08 * k), t0 + 3 * NEGRA + k * NEGRA / 8, pan=.3)
    if not fuerte:
        a.poner(bateria, a.bombo(), t0, .5); golpes.append(t0)
        if c >= 2:                                        # mientras se abre, 808 suave para que no se caiga
            a.poner(bajos, a.ochocientos(raiz + 12, 1.4 * NEGRA), t0, .45)
        continue
    for b in (0, 1.5, 2.75) if c % 2 else (0, 2.5):
        a.poner(bateria, a.bombo(), t0 + b * NEGRA); golpes.append(t0 + b * NEGRA)
    a.poner(bateria, a.palmas(), t0 + 2 * NEGRA)
    for b, d in ((0, 1.4), (1.5, .9), (2.5, 1.4)) if c % 2 == 0 else ((0, 1.4), (1.5, 1.1), (2.75, 1.2)):
        a.poner(bajos, a.ochocientos(raiz + 12, d * NEGRA), t0 + b * NEGRA)
for k in range(8):                                        # redoble antes del golpe
    a.poner(bateria, a.palmas(), GOLPE - K / 2 + k * K / 16, .15 + .1 * k)
raiz, notas = ACORDES[0]
a.poner(pads, a.pad(notas, 1.7, 1800), FIN, .9)
a.poner(melodia, a.campana(69, 1.6), FIN)
a.poner(bajos, a.ochocientos(raiz + 12, 1.6), FIN)
duck = a.compresion_al_bombo(golpes)
bajos *= duck[:, None]
pads *= (.35 + .65 * duck)[:, None]

# ── efectos, al segundo de cada animacion ──
m = a.muestra
a.poner(fx, m('whoosh.mp3', -4), .0, .7)
a.poner(fx, m('impact-bass-1.mp3'), .45, .8); a.poner(fx, a.sub_golpe(), .45, .5)       # cae la placa
a.poner(fx, m('whoosh-cinematic.mp3', -2), 1.8, .8)                                       # se inclina
a.poner(fx, m('kenney-maximize_006.wav'), 2.5, .8); a.poner(fx, m('whoosh.mp3'), 2.55, .7)  # se abre
for i in range(8):                                                                       # capa a capa
    a.poner(fx, m('kenney-select_003.wav', i), 3.33 + i * K / 2, .6)
    a.poner(fx, m('pop.mp3', i / 2), 3.36 + i * K / 2, .45)
a.poner(fx, m('riser.mp3'), GOLPE - 1.57, .9)
a.poner(fx, m('kenney-minimize_006.wav'), 10.3, .7)                                      # se juntan...
a.poner(fx, m('impact-bass-2.mp3'), GOLPE, 1); a.poner(fx, a.sub_golpe(1.8), GOLPE, .8)  # ¡golpe!
a.poner(fx, m('sparkle.mp3'), 12.4, .8)
for k in range(10):                                                                      # programando
    a.poner(fx, m('kenney-tick_002.wav', k), 13.5 + k * .1, .35)
a.poner(fx, m('kenney-confirmation_002.wav'), 14.5, .9)
for i in range(3):
    a.poner(fx, m('ping.mp3', 4 * i), 14.15 + i * .25, .45)
a.poner(fx, m('whoosh.mp3'), 15.0, .7)                                                   # entra el movil
a.poner(fx, m('ping.mp3', 7), 16.2, .6)
for i in range(5):                                                                       # cinco estrellas
    a.poner(fx, m('kenney-glass_004.wav', [0, 2, 4, 7, 9][i]), 16.67 + i * .2, .7, pan=-.4 + .2 * i)
for k in range(8):
    a.poner(fx, m('key-press.mp3', a.rng.uniform(-1, 1)), 17.6 + k * .05, .35)
a.poner(fx, m('notification.mp3'), 18.0, .9)
a.poner(fx, m('whoosh-cinematic.mp3'), 18.25, .8)                                        # cierre
a.poner(fx, m('pop.mp3', 3), 18.8, .7)
a.poner(fx, m('impact-bass-1.mp3'), 19.4, .6); a.poner(fx, m('kenney-confirmation_004.wav'), 19.4, .8)

melodia = a.reverb(a.eco(melodia, NEGRA * .75, .28), .4)
bateria = a.reverb(bateria, .12)
fx = a.reverb(fx, .22)
musica = bajos + .9 * pads + .95 * bateria + .9 * melodia
a.guardar(a.master(musica + 1.1 * fx, cola=1.0), V + 'audio.wav')
a.guardar(a.master(fx, cola=1.0), V + 'audio-solo-efectos.wav')
print('audio.wav y audio-solo-efectos.wav', round(DUR, 2), 's')
