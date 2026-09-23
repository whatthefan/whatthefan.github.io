"""Sonido de la placa girando (8,5 s): cae (golpe), se da la vuelta (whoosh) y
aparece Estrellita guinando ("bong"), vuelve, Estrellita salta (whoosh) y cae
(pasito), y el boton (confirmacion). Ritmo suave debajo. Efectos ligeros.
Desde la raiz del repo:  python3 marketing/instagram/carteles/video/musica.py
"""
import sys

sys.path.insert(0, 'marketing/instagram')
import audio as a  # noqa: E402

V = 'marketing/instagram/carteles/video/'
DUR = 8.5
a.duracion(DUR)
K = 5 / 3
NEGRA = K / 4
m = a.muestra
bajos, pads, bateria, melodia, fx = (a.pista() for _ in range(5))
golpes = []
ACORDES = [(33, [57, 60, 64]), (29, [53, 57, 60]), (36, [55, 60, 64]), (31, [55, 59, 62])]
t0, c = .9, 0
while t0 < DUR - 1:
    raiz, notas = ACORDES[c % 4]
    a.poner(pads, a.pad(notas, K + .3, 1800), t0, .5)
    for b in (0, 2.5):
        a.poner(bateria, a.bombo(), t0 + b * NEGRA, .6); golpes.append(t0 + b * NEGRA)
    a.poner(bateria, a.palmas(), t0 + 2 * NEGRA, .45)
    for k in range(8):
        a.poner(bateria, a.charles(vel=.8 if k % 2 == 0 else .45), t0 + k * NEGRA / 2, .7, pan=.3)
    for b, d in ((0, 1.4), (2.5, 1.2)):
        a.poner(bajos, a.ochocientos(raiz + 12, d * NEGRA), t0 + b * NEGRA, .8)
    t0 += K
    c += 1
a.poner(pads, a.pad(ACORDES[0][1], 1.2, 1600), DUR - 1, .6); a.poner(melodia, a.campana(69, 1.2, .7), DUR - 1)
a.poner(fx, m('whoosh.mp3', -2), .1, .3)                      # cae
a.poner(fx, m('impact-bass-1.mp3'), 1.0, .3)
for i in range(3):
    a.poner(fx, m('pop.mp3', 2 * i), 1.1 + i * .24, .25)        # TOCA · 5★ · LISTO
a.poner(fx, m('whoosh-short.mp3'), 2.55, .35)                  # se da la vuelta
a.poner(fx, m('kenney-bong_001.wav', 3), 3.0, .35)             # Estrellita, pillada
a.poner(fx, m('whoosh-short.mp3', 2), 4.55, .3)                # vuelve
a.poner(fx, m('whoosh.mp3', 4), 4.75, .3)                      # salta
a.poner(fx, m('kenney-drop_002.wav', 3), 5.45, .35)            # cae de pie
a.poner(fx, m('kenney-confirmation_002.wav'), 5.65, .4)        # el boton
duck = a.compresion_al_bombo(golpes)
bajos *= duck[:, None]
pads *= (.4 + .6 * duck)[:, None]
melodia = a.reverb(melodia, .4)
fx = a.reverb(fx, .2)
a.guardar(a.master(.9 * bajos + .85 * pads + .8 * bateria + .8 * melodia + .8 * fx, cola=.8), V + 'audio.wav')
print('audio.wav', DUR, 's')
