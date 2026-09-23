"""Version plana "tipo Canva" de la 3 y la 5: fondo negro liso como en la
ronda 2, sin aro, sin degradados ni brillos (eso era lo que olia a IA), y
la estrella con contorno grueso, en dos estilos:
  blanco -> contorno blanco, como una pegatina
  doble  -> una franja negra y luego una linea de oro alrededor

El 5 ahora cabe entero en la estrella: antes (escala .46) la base del 5 se
salia por la muesca entre las dos patas y se fundia con el fondo.

Desde la raiz del repo:
    python3 marketing/instagram/avatar/final/generar.py
Monta un .html por avatar, mas perfil.html (las dos puestas en Instagram).
"""
import base64
import re

ico = open('public/icono.svg').read()
STAR = re.search(r'<path fill="#E9BC46" d="([^"]+)"', ico).group(1)
FIVE = re.search(r'<path fill="#0A0E16" transform="[^"]+" d="([^"]+)"', ico).group(1)

NOCHE, ORO, ORO_CL, ORO_OS, BLANCO = '#06080E', '#E9BC46', '#F8E1A6', '#B8862A', '#FFFFFF'
DISPLAY = 'font-family:Anton,Impact,sans-serif'

# El 5 de Anton ocupa x 22..477 (centro 249.5) e y -860..12 en su trazado.
CINCO_ESC, CINCO_ARRIBA = 0.42, 316
CINCO_TR = f'translate({512 - 249.5 * CINCO_ESC:.1f} {CINCO_ARRIBA + 860 * CINCO_ESC:.1f}) scale({CINCO_ESC})'

ANCHO = {'P': 967, 'L': 814, 'E': 843, 'A': 994}   # Anton, 2048 por em
ALTO_MAYUS = 1760 / 2048


def fondo(n=None):
    return f'<rect width="1080" height="1080" fill="{NOCHE}"/>'


CONTORNO = 'blanco'   # lo cambia el bucle de abajo


def trazo(color, ancho):
    return f'<path d="{STAR}" fill="{color}" stroke="{color}" stroke-width="{ancho}" stroke-linejoin="round"/>'


def sello(cx, cy, esc, estrella=ORO, cinco=NOCHE, contorno=True):
    """(cx, cy) es el centro visual de la estrella, (512, 470) en su caja.
    Los anchos del contorno van en unidades de la caja de 1024 de la estrella."""
    borde = ''
    if contorno and CONTORNO == 'blanco':
        borde = trazo(BLANCO, 64)
    elif contorno and CONTORNO == 'doble':
        borde = trazo(ORO, 110) + trazo(NOCHE, 74)
    return (f'<g transform="translate({cx:.1f} {cy:.1f}) scale({esc:.4f}) translate(-512 -470)">'
            f'{borde}<path fill="{estrella}" d="{STAR}"/><path fill="{cinco}" transform="{CINCO_TR}" d="{FIVE}"/></g>')


def mini_estrellas(y, tam, paso):
    # lisas: a este tamano un 5 dentro solo es ruido
    return ''.join(sello(540 + (i - 2) * paso, y, tam / 1000, ORO, ORO, contorno=False) for i in range(5))


def palabra_estrella(y, tam, esp=0.03, crece=1.5):
    """PLEA★E: el sello hace de 5, y = linea base. crece = alto de la
    estrella frente a las mayusculas (mas alta = 5 mas legible)."""
    k, gap = tam / 2048, tam * esp
    plea = sum(ANCHO[c] for c in 'PLEA') * k + 3 * gap
    e = ANCHO['E'] * k
    esc = ALTO_MAYUS * tam * crece / 815            # la estrella mide 815 de alto
    ancho_estrella = 902 * esc * 1.08                # con el contorno, sitio para no pisar la A ni la E
    total = plea + gap + ancho_estrella + gap + e
    x0 = 540 - total / 2
    t = f'style="{DISPLAY};font-size:{tam}px;letter-spacing:{gap:.1f}px" fill="{BLANCO}"'
    return (f'<text x="{x0:.1f}" y="{y}" {t}>PLEA</text>'
            f'<text x="{x0 + total - e:.1f}" y="{y}" {t}>E</text>'
            + sello(x0 + plea + gap + ancho_estrella / 2, y - ALTO_MAYUS * tam / 2 - tam * 0.03, esc))


P = {
    '3-estrella-y-nombre': lambda n: fondo() + sello(540, 420, .54)
        + f'<text x="540" y="860" text-anchor="middle" style="{DISPLAY};font-size:190px;letter-spacing:6px" fill="{BLANCO}">PLEA5E</text>',
    '5-plea-estrella-e': lambda n: fondo() + palabra_estrella(620, 205) + mini_estrellas(750, 44, 84),
}

b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
CSS = ('<meta charset="utf-8"><style>@font-face{font-family:Anton;src:url(data:font/woff2;base64,'
       + b64('fuente/anton-latin.woff2') + ')}</style>')


def svg(cuerpo, w=1080):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="{w}" height="{w}">{cuerpo}</svg>'


base = 'marketing/instagram/avatar/canva/'
celdas = []
for CONTORNO in ('blanco', 'doble'):
    for nombre, f in P.items():
        cuerpo = f(0)
        open(f'{base}{nombre}-{CONTORNO}.html', 'w').write(
            f'<html><head>{CSS}</head><body style="margin:0">{svg(cuerpo)}</body></html>')
        celdas.append(f'<div class="c"><b>{nombre.split("-")[0]} · contorno {CONTORNO}</b>'
                      f'<span class="av">{svg(cuerpo, 300)}</span>'
                      f'<div class="mini"><span class="av">{svg(cuerpo, 86)}</span><span class="av">{svg(cuerpo, 58)}</span>'
                      f'<span class="av">{svg(cuerpo, 28)}</span></div></div>')
open(base + 'tablero.html', 'w').write(
    f'<html><head>{CSS}<style>body{{margin:0;background:#0c1014;color:#eee;font-family:Helvetica,Arial}}'
    '.g{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;padding:24px}'
    '.c{display:flex;flex-direction:column;align-items:center;gap:12px}.c b{color:#E9BC46;font-size:17px}'
    '.av svg{border-radius:50%;display:block}.mini{display:flex;gap:12px;align-items:center}</style></head>'
    f'<body><div class="g">{"".join(celdas)}</div></body></html>')
