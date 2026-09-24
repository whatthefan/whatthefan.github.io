"""Carrusel "OYEEEE" (6 fotos de 1080x1350), al estilo de la referencia del perro
que cuchichea: fondo liso, una palabra gorda repetida por la foto (en arco,
girada, de varios tamanos y cortada por los bordes) y el personaje asomandose.
Aqui el personaje es Estrellita, y es el centro: grande, con un halo de luz
detras, un brillo que le cruza y destellos alrededor.

Todo con textura: el fondo (entre azul y verde) con grano de papel; las letras
(Titan One) en 3D, con su volumen hacia abajo a la derecha, un filo, sombra en
el suelo y un moteado fino, como impresas.

La historia, en cotilleo:
  1. OYEEEE                       (Estrellita cuchicheando, enorme)
  2. ¿SABES LO QUE DICEN DE TU BAR?
  3. NADA.
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
E = 'marketing/instagram/personaje/svg/'          # las poses de Instagram (guantes con dedos, cosas en la mano)
b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
svg = lambda f: 'data:image/svg+xml;base64,' + b64(f)
PLACA = 'data:image/png;base64,' + b64('marketing/instagram/carrusel-placa/capas/paso5-nfc.png')
W, H = 1080, 1350
# los colores de cada letra: cara, volumen (el lado) y filo
BLANCO = ('#FFFFFF', '#0B3F4A', '#0A2F38')
ORO = ('#F6CC4E', '#8A5A06', '#5E3C03')
SUAVE = ('#BFE6E4', '#0B3F4A', '#0A2F38')

CSS = f'''
@font-face{{font-family:Titan;src:url(data:font/woff2;base64,{b64('fuente/titan-one-latin.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
/* el fondo: petroleo, entre azul y verde, con luz en el centro */
body{{background:radial-gradient(ellipse 75% 65% at 50% 45%,#16898F 0%,#0F6A76 45%,#0A4A5A 100%)}}
/* grano de papel por encima de todo */
body::after{{content:"";position:absolute;inset:0;pointer-events:none;z-index:9;opacity:.55;mix-blend-mode:overlay;
  background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='320' height='320'><filter id='r'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .6 0'/></filter><rect width='320' height='320' filter='url(%23r)'/></svg>")}}
.abs{{position:absolute}}
/* Estrellita: halo detras, sombra, y un brillo que le cruza (mascara con su propia silueta) */
.foco{{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,236,160,.55) 0%,rgba(255,220,120,.18) 38%,transparent 68%)}}
.bicho{{position:absolute}}
.bicho img{{display:block;width:100%;filter:drop-shadow(0 22px 26px rgba(0,20,25,.5)) drop-shadow(0 0 22px rgba(255,214,90,.45))}}
.bicho .luz{{position:absolute;inset:0;-webkit-mask-size:100% 100%;mix-blend-mode:overlay;
  background:linear-gradient(120deg,transparent 30%,rgba(255,255,255,.75) 42%,transparent 52%,transparent 62%,rgba(255,255,255,.4) 68%,transparent 74%)}}
.chispa{{position:absolute}}
'''

n = 0


def palabra(texto, x, y, tam, giro=0, curva=0, color=BLANCO):
    """una palabra en 3D: el volumen (copias hacia abajo a la derecha), la cara con un filo y
    un moteado encima. curva > 0: arco hacia arriba; < 0: hacia abajo; 0: recta"""
    global n
    n += 1
    cara, lado, filo = color
    largo = tam * .68 * len(texto)
    if curva == 0:
        d = f'M{x - largo / 2:.0f} {y:.0f} L{x + largo / 2:.0f} {y:.0f}'
    else:
        r = largo / (2 * math.sin(min(abs(curva), 1.3) / 2))
        d = f'M{x - largo / 2:.0f} {y:.0f} A{r:.0f} {r:.0f} 0 0 {1 if curva > 0 else 0} {x + largo / 2:.0f} {y:.0f}'

    def t(fill, extra=''):
        return (f'<text font-family="Titan" font-size="{tam}" fill="{fill}" {extra}>'
                f'<textPath href="#p{n}" startOffset="50%" text-anchor="middle">{texto}</textPath></text>')
    capas = max(6, int(tam * .085))
    vol = ''.join(f'<g transform="translate({i * .55:.1f} {i * .8:.1f})">{t(lado)}</g>' for i in range(capas, 0, -1))
    filo_attr = f'stroke="{filo}" stroke-width="{tam * .035:.1f}" paint-order="stroke"'
    return (f'<g transform="rotate({giro} {x} {y})"><path id="p{n}" d="{d}" fill="none"/>'
            f'<g filter="url(#sombra)">{vol}</g>{t(cara, filo_attr)}<g filter="url(#moteado)">{t(cara)}</g></g>')


FILTROS = '''<defs>
<filter id="sombra" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="6" dy="14" stdDeviation="8" flood-color="#032028" flood-opacity=".45"/></filter>
<filter id="moteado"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="4"/>
  <feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.6 1.05"/><feComposite in2="SourceGraphic" operator="in"/>
  <feComponentTransfer><feFuncA type="linear" slope=".22"/></feComponentTransfer></filter>
</defs>'''


def lienzo(*cosas):
    return f'<svg class="abs" style="left:0;top:0" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{FILTROS}{"".join(cosas)}</svg>'


CHISPA = ('<svg viewBox="-10 -10 20 20" width="{t}" height="{t}"><path d="M0 -10Q1.2 -1.2 10 0Q1.2 1.2 0 10Q-1.2 1.2 -10 0Q-1.2 -1.2 0 -10Z" '
          'fill="#FFF4C8"/></svg>')


def bicho(pose, x, y, ancho, giro=0, chispas=((-.05, .1, 44), (1.0, .25, 30), (.9, .95, 38))):
    """Estrellita con su halo, el brillo y unos destellos alrededor (en fracciones de su ancho)"""
    src = svg(E + pose + '.svg')
    halo = f'<div class="foco" style="left:{x - ancho * .35:.0f}px;top:{y - ancho * .3:.0f}px;width:{ancho * 1.7:.0f}px;height:{ancho * 1.6:.0f}px"></div>'
    ch = ''.join(f'<div class="chispa" style="left:{x + fx * ancho:.0f}px;top:{y + fy * ancho:.0f}px">{CHISPA.format(t=t)}</div>'
                 for fx, fy, t in chispas)
    return (halo + f'<div class="bicho" style="left:{x}px;top:{y}px;width:{ancho}px;transform:rotate({giro}deg)">'
            f'<img src="{src}"><div class="luz" style="-webkit-mask-image:url({src})"></div></div>' + ch)


# una rodadora (la bola de matojos de las pelis del oeste) cruzando: aqui no pasa nada
RODADORA = ('<svg class="abs" style="left:60px;top:1000px" width="230" height="230" viewBox="-60 -60 120 120">'
            '<ellipse cx="0" cy="58" rx="46" ry="8" fill="rgba(3,32,40,.35)"/>'
            + ''.join(f'<ellipse cx="0" cy="0" rx="{48 - i * 3}" ry="{40 - i * 4}" transform="rotate({i * 37})" fill="none" '
                      f'stroke="{c}" stroke-width="{3 + i % 2}"/>' for i, c in enumerate(['#A8773A', '#8A5C26', '#C4955A'] * 3))
            + '<path d="M-70 10 L-100 10 M-66 -12 L-92 -16 M-64 30 L-88 36" stroke="#BFE6E4" stroke-width="5" stroke-linecap="round" opacity=".7"/></svg>')


def diapo(num, cuerpo):
    os.makedirs(O + 'diapositivas', exist_ok=True)
    open(f'{O}diapositivas/{num}.html', 'w').write(
        f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{cuerpo}</body></html>')


# 1 · OYEEEE; Estrellita, enorme, se asoma por la izquierda
diapo(1, bicho('susurra', -290, 330, 880, 10, ((.55, .12, 48), (.75, .55, 30), (.62, .98, 36))) + lienzo(
    palabra('OYEEEE', 300, 130, 96, -4, .8),
    palabra('OYE', 330, 330, 130, 10, .3),
    palabra('OYEEEE', 860, 300, 110, 8, .6),
    palabra('OYE', 820, 720, 250, -10, .3),
    palabra('OYEEEE', 720, 1080, 150, -6, .6),
    palabra('OYEEEE', 360, 1320, 110, 3, .7),
))

# 2 · ¿SABES LO QUE DICEN DE TU BAR?  (Estrellita con su libreta, entrando por la derecha)
diapo(2, lienzo(
    palabra('PSST', 190, 110, 76, -12, .5, SUAVE),
    palabra('PSST', 900, 120, 66, 14, .5, SUAVE),
    palabra('¿SABES', 420, 320, 130, -4, .2),
    palabra('LO QUE', 420, 500, 130, 3, .15),
    palabra('DICEN', 400, 690, 150, -3, .15),
    palabra('DE TU BAR?', 420, 880, 118, 2, .25, ORO),
) + bicho('palomitas-izq', 560, 690, 660, -6, ((.1, .12, 40), (.95, .35, 30))))

# 3 · NADA.  (Estrellita sentada, con cara de circunstancias)
diapo(3, lienzo(
    palabra('NADA.', 540, 470, 300, -4, .12),
    palabra('cri...', 170, 780, 60, -10, 0, SUAVE),
    palabra('cri...', 920, 860, 64, 8, 0, SUAVE),
    palabra('ni una reseña', 540, 1300, 62, 0, .15, SUAVE),
) + RODADORA + bicho('gota', 230, 520, 640, 0, ((.05, .2, 40), (.92, .18, 34))))

# 4 · SALEN ENCANTADOS... Y SE LES OLVIDA.  (Estrellita apoyada, resignada)
diapo(4, lienzo(
    palabra('SALEN', 540, 190, 160, -3, .15),
    palabra('ENCANTADOS...', 540, 370, 104, 2, .3),
    palabra('Y SE LES OLVIDA.', 540, 570, 90, -2, .25, ORO),
    palabra('se les olvida', 230, 790, 50, -10, .4, SUAVE),
    palabra('se les olv...', 250, 960, 40, 6, .4, ('#8FC9C6', '#0B3F4A', '#0A2F38')),
    palabra('se le...', 240, 1110, 32, -4, .4, ('#62A9A7', '#0B3F4A', '#0A2F38')),
) + bicho('apoyada-izq', 430, 600, 680, 0, ((.1, .12, 40), (.95, .45, 32))))

# 5 · TRANQUI, YO ME ENCARGO.  (la placa y Estrellita haciendo ¡tachan!)
diapo(5, lienzo(
    palabra('TRANQUI,', 540, 170, 150, -3, .2),
    palabra('YO ME ENCARGO.', 540, 330, 100, 2, .25, ORO),
    palabra('la tocan y te dejan la reseña', 540, 1300, 44, 0, 0, SUAVE),
) + f'''<div class="abs" style="left:40px;top:440px;width:580px;height:580px;transform:rotate(-8deg);
  filter:drop-shadow(0 30px 34px rgba(0,20,25,.5))">
  {''.join(f'<div style="position:absolute;inset:0;border-radius:4.2%;transform:translateY({i}px);background:rgba({205 + 2 * i},{222 + i},{220 + i},.97)"></div>' for i in range(12, 0, -1))}
  <img src="{PLACA}" style="position:absolute;inset:0;width:100%;height:100%;border-radius:4.2%"></div>'''
  + bicho('elegante', 470, 380, 700, 4, ((-.02, .2, 46), (.95, .12, 40), (.98, .8, 30))))

# 6 · COMENTA PLACA  (Estrellita sale saltando desde abajo a la izquierda)
diapo(6, lienzo(
    palabra('PLACA', 250, 130, 90, -4, .6),
    palabra('PLACA', 870, 230, 104, 8, .5),
    palabra('COMENTA', 580, 480, 150, -5, .25),
    palabra('PLACA', 620, 700, 240, 3, .2, ORO),
    palabra('PLACA', 930, 1030, 90, -18, .5),
    palabra('plea5e.es', 820, 1290, 52, -4, 0, SUAVE),
) + bicho('megafono', -120, 700, 620, -6, ((.95, .1, 44), (.2, .08, 34), (1.0, .7, 30))))
print('6 diapositivas')
