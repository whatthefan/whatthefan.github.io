"""Ronda final: la 3 (estrella + PLEA5E debajo) y la 5 (PLEA★E), las dos
con el aro de oro metalico de la 8.

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


def defs(n):
    return (f'<defs><linearGradient id="g{n}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{ORO_CL}"/><stop offset=".45" stop-color="{ORO}"/>'
            f'<stop offset="1" stop-color="{ORO_OS}"/></linearGradient>'
            f'<radialGradient id="r{n}" cx=".5" cy=".42" r=".65"><stop offset="0" stop-color="#1A2233"/>'
            f'<stop offset="1" stop-color="{NOCHE}"/></radialGradient></defs>')


def fondo_con_aro(n):
    return (defs(n) + f'<rect width="1080" height="1080" fill="url(#r{n})"/>'
            f'<circle cx="540" cy="540" r="500" fill="none" stroke="url(#g{n})" stroke-width="12"/>')


def sello(cx, cy, esc, estrella=ORO, cinco=NOCHE):
    """(cx, cy) es el centro visual de la estrella, (512, 470) en su caja."""
    return (f'<g transform="translate({cx:.1f} {cy:.1f}) scale({esc:.4f}) translate(-512 -470)">'
            f'<path fill="{estrella}" d="{STAR}"/><path fill="{cinco}" transform="{CINCO_TR}" d="{FIVE}"/></g>')


def mini_estrellas(y, tam, paso):
    # lisas: a este tamano un 5 dentro solo es ruido
    return ''.join(sello(540 + (i - 2) * paso, y, tam / 1000, ORO, ORO) for i in range(5))


def palabra_estrella(y, tam, esp=0.03, crece=1.5):
    """PLEA★E: el sello hace de 5, y = linea base. crece = alto de la
    estrella frente a las mayusculas (mas alta = 5 mas legible)."""
    k, gap = tam / 2048, tam * esp
    plea = sum(ANCHO[c] for c in 'PLEA') * k + 3 * gap
    e = ANCHO['E'] * k
    esc = ALTO_MAYUS * tam * crece / 815            # la estrella mide 815 de alto
    ancho_estrella = 902 * esc * 0.90                # las puntas se asoman sobre la A y la E
    total = plea + gap + ancho_estrella + gap + e
    x0 = 540 - total / 2
    t = f'style="{DISPLAY};font-size:{tam}px;letter-spacing:{gap:.1f}px" fill="{BLANCO}"'
    return (f'<text x="{x0:.1f}" y="{y}" {t}>PLEA</text>'
            f'<text x="{x0 + total - e:.1f}" y="{y}" {t}>E</text>'
            + sello(x0 + plea + gap + ancho_estrella / 2, y - ALTO_MAYUS * tam / 2 - tam * 0.03, esc))


P = {
    '3-estrella-y-nombre': lambda n: fondo_con_aro(n) + sello(540, 428, .56)
        + f'<text x="540" y="852" text-anchor="middle" style="{DISPLAY};font-size:190px;letter-spacing:6px" fill="{BLANCO}">PLEA5E</text>',
    '5-plea-estrella-e': lambda n: fondo_con_aro(n) + palabra_estrella(620, 215) + mini_estrellas(745, 44, 84),
}

b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
CSS = ('<meta charset="utf-8"><style>@font-face{font-family:Anton;src:url(data:font/woff2;base64,'
       + b64('fuente/anton-latin.woff2') + ')}</style>')


def svg(cuerpo, w=1080):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="{w}" height="{w}">{cuerpo}</svg>'


base = 'marketing/instagram/avatar/final/'
for nombre, f in P.items():
    open(base + nombre + '.html', 'w').write(f'<html><head>{CSS}</head><body style="margin:0">{svg(f(0))}</body></html>')

# Las dos en un perfil de Instagram en modo oscuro, a los tamanos de verdad.
tarj = []
for i, (nombre, f) in enumerate(P.items()):
    av = lambda w, j: f'<span class="av">{svg(f(f"{i}{j}"), w)}</span>'
    tarj.append(
        f'<div class="p"><div class="t">{nombre.split("-")[0]}</div>'
        f'<div class="grande">{av(420, "a")}</div>'
        f'<div class="row">{av(86, "b")}<div><div class="n">PLEA5E® | Aumenta tus Reseñas</div><div class="s">plea5e.es</div></div></div>'
        f'<div class="bar"><div class="st"><i></i>bar_luna</div><div class="st">{av(58, "c")}plea5e.es</div>'
        f'<div class="st"><i></i>laura.m</div><div class="st"><i></i>cafeteria</div></div>'
        f'<div class="cm">{av(28, "d")}<b>plea5e.es</b> ¡Gracias por las 5 ⭐!</div></div>')
open(base + 'perfil.html', 'w').write(
    f'<html><head>{CSS}<style>body{{margin:0;background:#000;font-family:Helvetica,Arial;color:#f5f5f5;display:flex;gap:24px;padding:24px}}'
    '.p{width:460px;background:#0c1014;border-radius:18px;padding:20px}.t{color:#E9BC46;font-weight:700;font-size:22px;margin-bottom:12px}'
    '.av svg{border-radius:50%;display:block}.grande{display:flex;justify-content:center;margin-bottom:22px}'
    '.row{display:flex;gap:18px;align-items:center}.n{font-weight:700;font-size:15px}.s{font-size:13px;color:#aaa}'
    '.bar{display:flex;gap:14px;margin-top:18px}.st{display:flex;flex-direction:column;align-items:center;font-size:11px;gap:4px}'
    '.st i{width:58px;height:58px;border-radius:50%;background:linear-gradient(135deg,#556,#334)}'
    '.cm{display:flex;gap:8px;align-items:center;margin-top:16px;font-size:13px}</style></head>'
    f'<body>{"".join(tarj)}</body></html>')
