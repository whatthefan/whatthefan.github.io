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
ROJO, BLANCO, ORO = '#1B3E9C', '#FFFFFF', '#F2C94C'          # fondo azul intenso (ROJO se queda de nombre)
W, H = 1080, 1350

CSS = f'''
@font-face{{font-family:Fredoka;font-weight:700;src:url(data:font/woff2;base64,{b64('fuente/fredoka-latin-700.woff2')})}}
@font-face{{font-family:Mont;font-weight:100 900;src:url(data:font/woff2;base64,{b64('fuente/montserrat-latin.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{ROJO}}}
/* textura de papel: grano fino y un poco de luz en el centro, como una foto impresa */
body::after{{content:"";position:absolute;inset:0;pointer-events:none;z-index:9;opacity:.5;
  background:radial-gradient(ellipse 70% 60% at 50% 45%,rgba(255,255,255,.10),rgba(0,0,0,.28)),
  url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='r'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .55 0'/></filter><rect width='300' height='300' filter='url(%23r)'/></svg>");mix-blend-mode:overlay}}
svg text{{paint-order:stroke;stroke:rgba(0,0,0,.14);stroke-width:3px}}
.bocadillo{{position:absolute;background:#fff;color:#16255E;font-family:Fredoka;font-weight:700;border-radius:40px;padding:14px 30px;
  box-shadow:0 10px 0 rgba(0,0,0,.18);white-space:nowrap}}
.bocadillo::after{{content:"";position:absolute;bottom:-22px;border:14px solid transparent;border-top:18px solid #fff}}
.bocadillo.izq::after{{left:34px}} .bocadillo.der::after{{right:34px}}
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


def bocadillo(texto, x, y, tam, giro=0, cola='izq'):
    return f'<div class="bocadillo {cola}" style="left:{x}px;top:{y}px;font-size:{tam}px;transform:rotate({giro}deg)">{texto}</div>'


def diapo(num, cuerpo):
    os.makedirs(O + 'diapositivas', exist_ok=True)
    open(f'{O}diapositivas/{num}.html', 'w').write(
        f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{cuerpo}</body></html>')


# 1 · OYEEEE por todas partes; Estrellita, enorme, se asoma por la izquierda
diapo(1, lienzo(
    palabra('OYEEEE', 260, 110, 96, -3, .9),
    palabra('OYEEEE', 870, 200, 124, 7, .7),
    palabra('OYEEEE', 520, 420, 140, 34, .8),
    palabra('OYE', 870, 760, 320, -12, .3),
    palabra('OYEEEE', 700, 1130, 200, -8, .7),
    palabra('OYEEEE', 1010, 1380, 130, 28, .8),
    palabra('OYEEEE', 300, 1390, 120, -4, .9),
) + bicho('curiosa', -330, 430, 900, 14) + bocadillo('psst...', 40, 250, 58, -8, 'izq'))

# 2 · ¿SABES LO QUE DICEN DE TU BAR? · Estrellita apuntando en su libreta, entrando por la derecha
diapo(2, lienzo(
    palabra('PSST', 170, 120, 90, -14, .6),
    palabra('PSST', 900, 110, 80, 16, .6),
    palabra('PSST', 70, 1270, 110, 20, .6),
    palabra('PSST', 560, 1330, 80, -6, .6),
    palabra('¿SABES', 430, 330, 150, -4, .25),
    palabra('LO QUE', 430, 515, 150, 3, .2),
    palabra('DICEN', 420, 700, 180, -3, .2),
    palabra('DE TU BAR?', 460, 880, 150, 2, .3, ORO),
) + bicho('apunta-izq', 560, 780, 700, -8) + bocadillo('lo apunto todo', 330, 1010, 44, -4, 'der'))

# 3 · NADA. · Estrellita sentada, con la cara de circunstancias
diapo(3, lienzo(
    palabra('NADA.', 540, 500, 340, -4, .15),
    palabra('NADA', 180, 140, 80, -12, .5, '#8FA3DA'),
    palabra('NADA', 900, 230, 70, 10, .5, '#8FA3DA'),
    palabra('nada de nada', 870, 820, 54, -8, .4, '#8FA3DA'),
    palabra('cri...', 150, 760, 62, -10, 0, '#C7D2F2'),
    palabra('cri...', 170, 1000, 50, 6, 0, '#C7D2F2'),
    palabra('cri...', 960, 1000, 66, -6, 0, '#C7D2F2'),
    palabra('ni una reseña', 540, 1320, 60, 0, .2, '#8FA3DA'),
) + bicho('sentada', 200, 620, 680) + bocadillo('...', 700, 560, 70, 4, 'izq'))

# 4 · SALEN ENCANTADOS... Y SE LES OLVIDA. · Estrellita apoyada en las letras, resignada
diapo(4, lienzo(
    palabra('SALEN', 540, 190, 180, -3, .2),
    palabra('ENCANTADOS...', 540, 370, 122, 2, .35),
    palabra('Y SE LES OLVIDA.', 540, 590, 106, -2, .3, ORO),
    palabra('se les olvida', 230, 760, 62, -12, .5, '#C7D2F2'),
    palabra('se les olvida', 860, 820, 54, 10, .5, '#9FB0E0'),
    palabra('se les olvida', 220, 950, 46, 6, .5, '#7A8FCC'),
    palabra('se les olvida', 870, 1010, 40, -8, .5, '#5C74BD'),
    palabra('se les olvi...', 200, 1130, 34, 4, .5, '#4863B0'),
    palabra('se le...', 900, 1200, 28, -6, .5, '#3A56A6'),
) + bicho('apoyada-izq', 420, 690, 700, 0) + bocadillo('otra vez...', 180, 1180, 46, -4, 'der'))

# 5 · TRANQUI, YO ME ENCARGO. · la placa y Estrellita haciendo ¡tachan! desde la derecha
diapo(5, lienzo(
    palabra('TRANQUI,', 540, 170, 170, -3, .25),
    palabra('YO ME ENCARGO.', 540, 330, 116, 2, .3, ORO),
    palabra('Tu cliente la toca y te deja la reseña.', 540, 1300, 44, 0, 0, '#C7D2F2'),
) + f'''<div class="abs" style="left:40px;top:430px;width:600px;height:600px;transform:rotate(-8deg);
  filter:drop-shadow(0 30px 34px rgba(0,0,0,.45))">
  {''.join(f'<div style="position:absolute;inset:0;border-radius:4.2%;transform:translateY({i}px);background:rgba({205 + 2 * i},{222 + i},{220 + i},.97)"></div>' for i in range(12, 0, -1))}
  <img src="{PLACA}" style="position:absolute;inset:0;width:100%;height:100%;border-radius:4.2%"></div>'''
  + bicho('tachan', 560, 600, 640, 8) + bocadillo('¡TACHÁN!', 690, 500, 60, 6, 'izq'))

# 6 · COMENTA PLACA · Estrellita salta desde abajo a la izquierda
diapo(6, lienzo(
    palabra('PLACA', 230, 120, 100, -4, .8),
    palabra('PLACA', 880, 210, 124, 8, .7),
    palabra('PLACA', 90, 420, 80, -28, .7),
    palabra('COMENTA', 600, 480, 180, -6, .35),
    palabra('PLACA', 640, 720, 290, 4, .25, ORO),
    palabra('PLACA', 960, 1000, 110, -22, .7),
    palabra('plea5e.es', 820, 1290, 56, -4, 0, '#C7D2F2'),
) + bicho('salta', -120, 760, 640, -12) + bocadillo('¡corre!', 390, 800, 52, -8, 'izq'))
print('6 diapositivas')
