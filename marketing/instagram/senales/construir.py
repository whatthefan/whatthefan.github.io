"""Carrusel "Las senales" (5 fotos de 1080x1350 + el video de la placa girando al final).

Las fotos son las de Flow (en 9:16, fotos/): el cielo de Cordoba, la moneda, el mural, la
lona en la fachada y la placa en el marmol. Se recortan a 4:5 y una frase va de foto en
foto, en letra gruesa en 3D (cara blanca, volumen, filo, sombra y moteado):

  1. cielo    LAS SENALES / estan por todas partes.
  2. moneda   En la barra…
  3. mural    …en la pared…
  4. fachada  …en la calle.
  5. placa    ¿Mas senales? / Esta es la tuya.
  6. video    placa girando: "Llevas todo el carrusel pensandolo. Te toca."
              (../carteles/video/PLEA5E-placa-girando.mp4)

Desde la raiz del repo:  python3 marketing/instagram/senales/construir.py
y despues:               node marketing/instagram/senales/hacer-png.js
"""
import base64
import os

S = 'marketing/instagram/senales/'
b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
W, H = 1080, 1350
K = W / 1438                      # las fotos (1438x2576) a lo ancho


def texto(lineas, x, y, tam, alinea='middle', sep=1.08, vol='#0B1E2E'):
    """lineas: [(texto, escala, color)]. Letra en 3D como el titulo de las notificaciones."""
    out, yy = '', y
    for t, e, col in lineas:
        tt = tam * e
        yy += tt * (sep if out else 1)
        capas = max(6, int(tt * .14))
        txt = lambda fill, extra='': (f'<text x="{x}" y="{yy:.0f}" text-anchor="{alinea}" font-family="Mont" font-weight="900" '
                                      f'font-size="{tt:.0f}" letter-spacing="{-tt * .02:.1f}" fill="{fill}" {extra}>{t}</text>')
        out += ''.join(f'<g transform="translate({i * .45:.1f} {i * .7:.1f})">{txt(vol)}</g>' for i in range(capas, 0, -1))
        out += txt(col, f'stroke="{vol}" stroke-width="{tt * .04:.1f}" paint-order="stroke"')
        out += f'<g filter="url(#moteado)">{txt(col)}</g>'
    return f'<g filter="url(#sombra)">{out}</g>'


DEFS = '''<defs>
<filter id="sombra" x="-10%" y="-30%" width="120%" height="180%"><feDropShadow dx="4" dy="16" stdDeviation="14" flood-color="#000" flood-opacity=".5"/></filter>
<filter id="moteado"><feTurbulence type="fractalNoise" baseFrequency="1.3" numOctaves="2" seed="7"/>
  <feColorMatrix values="0 0 0 0 .55  0 0 0 0 .5  0 0 0 0 .42  0 0 0 -1.7 1.1"/><feComposite in2="SourceGraphic" operator="in"/>
  <feComponentTransfer><feFuncA type="linear" slope=".35"/></feComponentTransfer></filter></defs>'''

B, ORO = '#FFFFFF', '#F6CC4E'
DIAPOS = [
    # foto, desde que y de la foto original, textos (y el oscurecido que ayuda a leer)
    ('1-cielo', 190, texto([('LAS SEÑALES', 1.0, B), ('están por todas partes.', .52, B)], 540, 900, 120),
     'linear-gradient(180deg,transparent 55%,rgba(0,20,50,.25) 75%,transparent)'),
    ('2-moneda', 250, texto([('En la barra…', 1.0, B)], 540, 120, 118),
     'linear-gradient(180deg,rgba(0,0,0,.35),transparent 35%)'),
    ('3-mural', 500, texto([('…en la pared…', 1.0, B)], 540, 70, 118),
     'linear-gradient(180deg,rgba(0,0,0,.18),transparent 30%)'),
    ('4-fachada', 250, texto([('…en la calle.', 1.0, B)], 540, 1175, 118),
     'linear-gradient(0deg,rgba(0,0,0,.4),transparent 25%)'),
    ('5-placa', 480, texto([('¿Más señales?', .62, B), ('Esta es', 1.0, B), ('la tuya.', 1.0, ORO)], 70, 1030, 96, 'start'),
     'linear-gradient(20deg,rgba(0,0,0,.35),transparent 45%)'),
]

CSS = f'''
@font-face{{font-family:Mont;font-weight:100 900;src:url(data:font/woff2;base64,{b64('fuente/montserrat-latin.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}}
.abs{{position:absolute}}
.grano{{position:absolute;inset:0;opacity:.28;mix-blend-mode:overlay;
  background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='r'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .5 0'/></filter><rect width='300' height='300' filter='url(%23r)'/></svg>")}}
'''
os.makedirs(S + 'diapositivas', exist_ok=True)
for n, (foto, y0, txt, oscuro) in enumerate(DIAPOS, 1):
    src = 'data:image/jpeg;base64,' + b64(f'{S}fotos/{foto}.jpg')
    open(f'{S}diapositivas/{n}.html', 'w').write(f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<img class="abs" src="{src}" style="left:0;top:{-y0 * K:.0f}px;width:{W}px;filter:contrast(1.03) saturate(1.05)">
<div class="abs" style="inset:0;background:{oscuro}"></div>
<svg class="abs" style="left:0;top:0" width="{W}" height="{H}">{DEFS}{txt}</svg>
<div class="grano"></div></body></html>''')
print(len(DIAPOS), 'diapositivas')
