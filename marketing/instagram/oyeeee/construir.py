"""Carrusel "OYEEEE" (6 fotos de 1080x1350), al estilo de la referencia del perro
que cuchichea: fondo granate liso, una palabra en letra redonda y gorda (Fredoka
Bold) repetida por toda la foto, en arco, girada, de varios tamanos y cortada por
los bordes, y el personaje asomandose por un lado. Aqui el personaje es Estrellita.

La historia, en cotilleo:
  1. OYEEEE                       (Estrellita se asoma)
  2. ¿SABES LO QUE DICEN DE TU BAR?
  3. NADA.                        (cri... cri...)
  4. SALEN ENCANTADOS... Y SE LES OLVIDA.
  5. TRANQUI, YO ME ENCARGO.      (la placa)
  6. COMENTA PLACA

Desde la raiz del repo:  python3 marketing/instagram/oyeeee/construir.py
y despues:               node marketing/instagram/oyeeee/hacer-png.js
"""
import base64
import math
import os

O = 'marketing/instagram/oyeeee/'
E = 'public/marca/estrellita/'
b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
svg = lambda f: 'data:image/svg+xml;base64,' + b64(f)
PLACA = 'data:image/png;base64,' + b64('marketing/instagram/carrusel-placa/capas/paso5-nfc.png')
ROJO, BLANCO, ORO = '#6B120C', '#FFFFFF', '#E9BC46'
W, H = 1080, 1350

CSS = f'''
@font-face{{font-family:Fredoka;font-weight:700;src:url(data:font/woff2;base64,{b64('fuente/fredoka-latin-700.woff2')})}}
@font-face{{font-family:Mont;font-weight:100 900;src:url(data:font/woff2;base64,{b64('fuente/montserrat-latin.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{ROJO}}}
.abs{{position:absolute}}
.bicho{{position:absolute;filter:drop-shadow(0 18px 24px rgba(0,0,0,.35))}}
'''

n = 0


def palabra(texto, x, y, tam, giro=0, curva=0, color=BLANCO):
    """una palabra en arco: curva > 0 la dobla como una sonrisa al reves (arco hacia arriba),
    curva < 0 hacia abajo, 0 recta. (x, y) es el centro"""
    global n
    n += 1
    largo = tam * .62 * len(texto) * 1.15
    if curva == 0:
        d = f'M{x - largo / 2:.0f} {y:.0f} L{x + largo / 2:.0f} {y:.0f}'
    else:
        r = largo / (2 * math.sin(min(abs(curva), 1.3) / 2)) / 1.0
        d = f'M{x - largo / 2:.0f} {y:.0f} A{r:.0f} {r:.0f} 0 0 {1 if curva > 0 else 0} {x + largo / 2:.0f} {y:.0f}'
    return (f'<path id="p{n}" d="{d}" fill="none"/>'
            f'<text transform="rotate({giro} {x} {y})" font-family="Fredoka" font-weight="700" font-size="{tam}" fill="{color}" '
            f'letter-spacing="{tam * -.01:.1f}"><textPath href="#p{n}" startOffset="50%" text-anchor="middle">{texto}</textPath></text>')


def lienzo(*cosas):
    return f'<svg class="abs" style="left:0;top:0" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(cosas)}</svg>'


def bicho(pose, x, y, ancho, giro=0, espejo=False):
    return (f'<img class="bicho" src="{svg(E + pose + ".svg")}" style="left:{x}px;top:{y}px;width:{ancho}px;'
            f'transform:rotate({giro}deg){" scaleX(-1)" if espejo else ""}">')


def diapo(num, cuerpo):
    os.makedirs(O + 'diapositivas', exist_ok=True)
    open(f'{O}diapositivas/{num}.html', 'w').write(
        f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{cuerpo}</body></html>')


# 1 · OYEEEE, por todas partes, y Estrellita asomandose por la izquierda
diapo(1, lienzo(
    palabra('OYEEEE', 230, 150, 92, -2, .9),
    palabra('OYEEEE', 860, 250, 118, 6, .7),
    palabra('OYEEEE', 420, 470, 132, 38, .8),
    palabra('OYE', 900, 820, 300, -12, .3),
    palabra('OYEEEE', 720, 1210, 190, -8, .7),
    palabra('OYEEEE', 1000, 1420, 120, 30, .8),
    palabra('OYEEEE', 330, 1400, 110, -4, .9),
) + bicho('curiosa', -250, 520, 720, 12))

# 2 · ¿SABES LO QUE DICEN DE TU BAR? (y PSST alrededor)
diapo(2, lienzo(
    palabra('PSST', 170, 150, 84, -14, .6),
    palabra('PSST', 930, 190, 70, 16, .6),
    palabra('PSST', 980, 1270, 90, -10, .6),
    palabra('¿SABES', 540, 360, 150, -4, .25),
    palabra('LO QUE', 560, 545, 150, 3, .2),
    palabra('DICEN', 540, 725, 170, -3, .2),
    palabra('DE TU BAR?', 540, 895, 150, 2, .3),
) + bicho('curiosa-izq', 700, 960, 520, -10))

# 3 · NADA. (cri... cri...)
diapo(3, lienzo(
    palabra('NADA.', 540, 640, 330, -4, .15),
    palabra('cri...', 250, 260, 58, -10, 0, '#E7B9B3'),
    palabra('cri...', 860, 380, 50, 8, 0, '#E7B9B3'),
    palabra('cri...', 170, 960, 46, 6, 0, '#E7B9B3'),
    palabra('cri...', 900, 1010, 62, -6, 0, '#E7B9B3'),
) + bicho('asombro', 330, 800, 430))

# 4 · SALEN ENCANTADOS... Y SE LES OLVIDA.
diapo(4, lienzo(
    palabra('SALEN', 540, 230, 170, -3, .2),
    palabra('ENCANTADOS...', 540, 400, 118, 2, .35),
    palabra('Y SE LES OLVIDA.', 540, 620, 104, -2, .3, ORO),
    palabra('se les olvida', 260, 800, 56, -12, .5, '#C98F87'),
    palabra('se les olvida', 820, 880, 48, 10, .5, '#A8655D'),
    palabra('se les olvida', 300, 1000, 40, 6, .5, '#8C433B'),
    palabra('se les olvida', 800, 1080, 34, -8, .5, '#7A2A22'),
) + bicho('apoyada', 660, 900, 440, 0, True))

# 5 · TRANQUI, YO ME ENCARGO. (la placa)
diapo(5, lienzo(
    palabra('TRANQUI,', 540, 190, 160, -3, .25),
    palabra('YO ME ENCARGO.', 540, 350, 112, 2, .3),
    palabra('Tu cliente la toca y te deja la reseña.', 540, 1270, 46, 0, 0, '#F2C9C3'),
) + f'''<div class="abs" style="left:120px;top:470px;width:600px;height:600px;transform:rotate(-7deg);
  filter:drop-shadow(0 30px 34px rgba(0,0,0,.45))">
  {''.join(f'<div style="position:absolute;inset:0;border-radius:4.2%;transform:translateY({i}px);background:rgba({205 + 2 * i},{222 + i},{220 + i},.97)"></div>' for i in range(12, 0, -1))}
  <img src="{PLACA}" style="position:absolute;inset:0;width:100%;height:100%;border-radius:4.2%"></div>'''
  + bicho('tachan', 640, 780, 420, 6))

# 6 · COMENTA PLACA, como el primero
diapo(6, lienzo(
    palabra('PLACA', 230, 150, 96, -4, .8),
    palabra('PLACA', 880, 240, 120, 8, .7),
    palabra('COMENTA', 560, 560, 190, -6, .35),
    palabra('PLACA', 600, 800, 290, 4, .25, ORO),
    palabra('PLACA', 250, 1080, 110, 18, .7),
    palabra('PLACA', 1010, 1130, 130, -24, .7),
    palabra('plea5e.es', 540, 1290, 50, 0, 0, '#F2C9C3'),
) + bicho('pulgar', -170, 820, 520, 10))
print('6 diapositivas')
