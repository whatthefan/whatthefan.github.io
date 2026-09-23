"""Video "Piedra, papel... ¡reseñas!" (1080x1920): el juego de toda la
vida, pero la tijera se tacha y la jugada que gana es la mano con el movil
tocando la placa. Despues, zoom al movil: en una nota se escribe, tecla a
tecla, el mensaje ("No tengas miedo... Sin riesgo, no hay reseñas.") y
cierra con Comenta PLACA.

Monta video/escena.html y video/tiempos.json (el segundo de cada tecla,
que usa musica.py para poner su sonido). Lo graban video/grabar.js
(imagen) y video/musica.py (sonido).

Desde la raiz del repo:
    python3 marketing/instagram/piedra-papel-resenas/video.py
    python3 marketing/instagram/piedra-papel-resenas/video/musica.py
    FFMPEG=ffmpeg node marketing/instagram/piedra-papel-resenas/video/grabar.js
"""
import json
import os
import random

P = 'marketing/instagram/piedra-papel-resenas/'
# lo mismo que usan las fotos del carrusel: manos, estrella, placa, letras
exec(open(P + 'construir.py').read().split("CSS = f'''")[0])   # mano(), ESTRELLA, PLACA, SELLO, b64, svg_uri
tijera = svg_uri(open(P + 'manos/tijera.svg').read())

# ───────────────────────── la nota que se escribe en el movil ─────────────────────────
TEXTO = [('No tengas miedo.', ''),
         ('Los que llegan arriba no se echaron para atrás.', ''),
         ('Sin riesgo, no hay reseñas.', 'oro')]
ESCRIBE = 8.45                   # primera tecla
rnd = random.Random(5)
teclas, t = [], ESCRIBE          # (segundo, letra)
for n, (frase, _) in enumerate(TEXTO):
    for c in frase:
        teclas.append((round(t, 3), c))
        t += .09 + rnd.uniform(0, .04) if c == ' ' else .055 + rnd.uniform(0, .035)
        if c == ',':
            t += .22
        if c == '.':
            t += .42
    if n < len(TEXTO) - 1:
        teclas.append((round(t, 3), '\n'))
        t += .3
FIN_NOTA = teclas[-1][0]
CTA = round(FIN_NOTA + .9, 2)    # baja el teclado y entra la notificacion
DUR = round(CTA + 3.4, 2)

# cada letra, en su span: la nota ya esta maquetada y solo se va "encendiendo"
NOTA, k = '', 0
for frase, clase in TEXTO:
    NOTA += f'<p class="{clase}">'
    for c in frase:
        NOTA += f'<span id="c{k}">{c}</span>'
        k += 1
    NOTA += '</p>'
    k += 1                                                  # el salto de linea
FILAS = ['QWERTYUIOP', 'ASDFGHJKLÑ', 'ZXCVBNM']
TECLADO = ''.join('<div class="fila">' + ''.join(f'<i id="k{c}">{c}</i>' for c in f) + '</div>' for f in FILAS)
TECLADO += ('<div class="fila"><i class="gris" style="flex:1.3">123</i><i id="k,">,</i><i id="k " class="esp">espacio</i>'
            '<i id="k.">.</i><i id="k\n" class="gris" style="flex:1.6">intro</i></div>')

ESTRELLAS = ''.join(f'<img class="est" id="e{i}" src="{ESTRELLA}" style="left:{x}px;top:{y}px;width:{w}px">'
                    for i, (x, y, w) in enumerate(((95, 610, 130), (275, 560, 150), (465, 540, 160), (655, 560, 150), (845, 610, 130))))
CANTO = ''.join(f'<div style="position:absolute;inset:0;border-radius:4.2%;transform:translateY({i}px);'
                f'background:rgba({200 + 3 * i},{215 + 2 * i},{212 + 2 * i},.95);border:1px solid rgba(255,255,255,.3)"></div>'
                for i in range(12, 0, -1))
FONDO = ''.join(f'<div class="rio" id="r{i}" style="top:{y}px">{"PIEDRA · PAPEL · RESEÑAS · " * 4}</div>'
                for i, y in enumerate((30, 640, 1130, 1760)))
HUECO = ''.join(f'<div class="hueco" id="s{i}" style="left:{150 + 290 * i}px"><div class="aro"></div>'
                f'<img src="{src}"><b>{txt}</b></div>'
                for i, (src, txt) in enumerate(((mano('piedra')[0], 'PIEDRA'), (mano('papel')[0], 'PAPEL'), (tijera, 'TIJERA'))))
RAYAS = ''.join(f'<line x1="{540 + 330 * c}" y1="{1010 + 330 * s}" x2="{540 + 420 * c}" y2="{1010 + 420 * s}"/>'
                for c, s in ((__import__('math').cos(a), __import__('math').sin(a))
                             for a in (i * 3.14159 / 5 + .3 for i in range(10))))

html = open(P + 'video/plantilla.html').read()
for k_, v in {'MONT': b64('fuente/montserrat-latin.woff2'), 'PIEDRA': mano('piedra')[0], 'PAPEL': mano('papel')[0],
              'TIJERA': tijera, 'MOVIL': mano('resenas')[0], 'PLACA': PLACA, 'CANTO': CANTO, 'ESTRELLAS': ESTRELLAS,
              'FONDO': FONDO, 'HUECOS': HUECO, 'RAYAS': RAYAS, 'NOTA': NOTA, 'TECLADO': TECLADO, 'SELLO': SELLO.replace('#B98B2E', '#E9BC46').replace('#E2D3BE', '#06080E'),
              'ESTRELLA': ESTRELLA, 'TECLAS': json.dumps(teclas, ensure_ascii=False),
              'CTA': str(CTA), 'DUR': str(DUR)}.items():
    html = html.replace('%' + k_ + '%', v)
open(P + 'video/escena.html', 'w').write(html)
json.dump({'teclas': teclas, 'escribe': ESCRIBE, 'fin_nota': FIN_NOTA, 'cta': CTA, 'dur': DUR},
          open(P + 'video/tiempos.json', 'w'), ensure_ascii=False, indent=0)
print('video/escena.html', DUR, 's ·', len(teclas), 'teclas, nota', ESCRIBE, '->', FIN_NOTA)
