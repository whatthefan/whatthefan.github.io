"""Ronda 2 de avatares: estrella con el 5 + el nombre, otros fondos y colores.

Monta tablero.html (todas juntas, con las tipografias de Google Fonts) y cada
propuesta suelta. Desde la raiz del repo:
    python3 marketing/instagram/avatar/ronda2/generar.py
"""
import base64
import re

ico = open('public/icono.svg').read()
STAR = re.search(r'<path fill="#E9BC46" d="([^"]+)"', ico).group(1)
FIVE = re.search(r'<path fill="#0A0E16" transform="[^"]+" d="([^"]+)"', ico).group(1)

NOCHE, ORO, ORO_CL, ORO_OS = '#06080E', '#E9BC46', '#F8E1A6', '#B8862A'
CREMA, NAVY, VERDE, BLANCO = '#F4EFE3', '#1B2B52', '#12251E', '#FFFFFF'
DISPLAY = "font-family:Anton,Impact,sans-serif"
SANS = "font-family:Montserrat,sans-serif;font-weight:800"


def sello(cx, cy, esc, estrella, cinco, borde=None, bw=0):
    """Estrella con el 5 entero dentro; (cx, cy) es su centro visual."""
    b = f' stroke="{borde}" stroke-width="{bw}" stroke-linejoin="round"' if borde else ''
    return (f'<g transform="translate({cx} {cy}) scale({esc}) translate(-512 -470)">'
            f'<path fill="{estrella}" d="{STAR}"{b}/>'
            f'<path fill="{cinco}" transform="translate(397.2 735.6) scale(.46)" d="{FIVE}"/></g>')


def arco(texto, color, r=400, arriba=True, tam=78, esp=14, id_='a'):
    if arriba:
        d = f'M {540-r} 540 A {r} {r} 0 0 1 {540+r} 540'
    else:
        d = f'M {540-r} 540 A {r} {r} 0 0 0 {540+r} 540'
    return (f'<path id="{id_}" d="{d}" fill="none"/>'
            f'<text style="{SANS};font-size:{tam}px;letter-spacing:{esp}px" fill="{color}">'
            f'<textPath href="#{id_}" startOffset="50%" text-anchor="middle">{texto}</textPath></text>')


def mini_estrellas(y, color, tam=34, paso=78):
    return ''.join(sello(540 + (i - 2) * paso, y, tam / 1000, color, color) for i in range(5))


# Anchos de Anton (unidades de 2048 por em) medidos con fontTools.
ANCHO = {'P': 967, 'L': 814, 'E': 843, 'A': 994}
ALTO_MAYUS = 1760 / 2048


def palabra_estrella(y, color, tam, estrella, cinco, esp=0.03):
    """PLEA5E en Anton, con el sello haciendo de 5. y = linea base."""
    k = tam / 2048
    gap = tam * esp
    plea = sum(ANCHO[c] for c in 'PLEA') * k + 3 * gap
    e = ANCHO['E'] * k
    alto_estrella = ALTO_MAYUS * tam * 1.28      # la estrella sobresale de las letras
    esc = alto_estrella / 815                    # la estrella mide 815 de alto en su caja
    ancho_estrella = 902 * esc * 0.97            # las puntas casi rozan la A y la E
    total = plea + gap + ancho_estrella + gap + e
    x0 = 540 - total / 2
    xs = x0 + plea + gap + ancho_estrella / 2
    ys = y - ALTO_MAYUS * tam / 2 - tam * 0.02
    t = f'style="{DISPLAY};font-size:{tam}px;letter-spacing:{gap:.1f}px" fill="{color}"'
    return (sello(xs, ys, esc, estrella, cinco)
            + f'<text x="{x0:.1f}" y="{y}" {t}>PLEA</text>'
            + f'<text x="{x0 + total - e:.1f}" y="{y}" {t}>E</text>')


def fondo(c):
    return f'<rect width="1080" height="1080" fill="{c}"/>'


def aro(c, r=500, w=10):
    return f'<circle cx="540" cy="540" r="{r}" fill="none" stroke="{c}" stroke-width="{w}"/>'


GRAD = ('<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{ORO_CL}"/><stop offset=".45" stop-color="{ORO}"/><stop offset="1" stop-color="{ORO_OS}"/></linearGradient>'
        '<radialGradient id="rg" cx=".5" cy=".42" r=".65"><stop offset="0" stop-color="#1A2233"/><stop offset="1" stop-color="#06080E"/></radialGradient></defs>')

BURBUJA = ('M 220 250 Q 220 170 300 170 L 780 170 Q 860 170 860 250 L 860 690 '
           'Q 860 770 780 770 L 470 770 L 330 900 L 350 770 L 300 770 Q 220 770 220 690 Z')

NFC = ''.join(f'<path d="M {760+i*55} {400-i*45} A {110+i*80} {110+i*80} 0 0 1 {760+i*55} {680+i*45}" '
              f'fill="none" stroke="{ORO}" stroke-width="30" stroke-linecap="round" opacity="{1-i*.25}"/>' for i in range(3))

P = [
    ('01-sello-aro-noche', 'Sello con el nombre en el aro · noche',
     fondo(NOCHE) + aro(ORO, 505, 8) + sello(540, 555, .58, ORO, NOCHE)
     + arco('PLEA5E', ORO, 400, True, 96, 30, 'a1') + arco('★ AUMENTA TUS RESEÑAS ★', ORO, 432, False, 44, 6, 'b1')),
    ('02-sello-aro-azul', 'Sello con aro · azul (guiño al logo antiguo)',
     fondo(NAVY) + aro(ORO, 505, 8) + sello(540, 555, .58, ORO, NAVY)
     + arco('PLEA5E', BLANCO, 400, True, 96, 30, 'a2') + arco('★ ★ ★ ★ ★', ORO, 432, False, 44, 18, 'b2')),
    ('03-apilado-noche', 'Estrella encima, nombre debajo · noche',
     fondo(NOCHE) + sello(540, 420, .62, ORO, NOCHE)
     + f'<text x="540" y="850" text-anchor="middle" style="{DISPLAY};font-size:200px;letter-spacing:6px" fill="{BLANCO}">PLEA5E</text>'),
    ('04-apilado-crema', 'Estrella encima, nombre debajo · crema',
     fondo(CREMA) + sello(540, 420, .62, ORO, NOCHE, NOCHE, 22)
     + f'<text x="540" y="850" text-anchor="middle" style="{DISPLAY};font-size:200px;letter-spacing:6px" fill="{NOCHE}">PLEA5E</text>'),
    ('05-nombre-grande-noche', 'Solo el nombre, grande, el 5 en su estrella · noche',
     fondo(NOCHE) + palabra_estrella(640, BLANCO, 250, ORO, NOCHE) + mini_estrellas(770, ORO, 46, 90)),
    ('06-nombre-grande-oro', 'Solo el nombre, grande · oro',
     fondo(ORO) + palabra_estrella(640, NOCHE, 250, NOCHE, ORO) + mini_estrellas(770, NOCHE, 46, 90)),
    ('07-azul-cinco-estrellas', 'Sello · azul y oro con las cinco estrellitas',
     fondo(NAVY) + sello(540, 480, .66, ORO, NAVY) + mini_estrellas(860, ORO, 50, 92)),
    ('08-oro-metalico', 'Sello oro metálico · premium',
     GRAD + '<rect width="1080" height="1080" fill="url(#rg)"/>' + aro('url(#g)', 500, 12)
     + sello(540, 560, .78, 'url(#g)', NOCHE)),
    ('09-burbuja-resena', 'La estrella dentro de un bocadillo = una reseña',
     fondo(NOCHE) + f'<path d="{BURBUJA}" fill="{ORO}"/>' + sello(540, 480, .47, NOCHE, ORO)),
    ('10-nfc', 'Estrella + ondas de "acerca el móvil"',
     fondo(NOCHE) + sello(430, 560, .62, ORO, NOCHE) + NFC),
    ('11-verde-oro', 'Sello · verde botella y oro',
     fondo(VERDE) + aro(ORO, 505, 8) + sello(540, 560, .80, ORO, VERDE)),
    ('12-blanco-contorno', 'Blanco, estrella con contorno y nombre abajo',
     fondo(BLANCO) + sello(540, 480, .64, ORO, NOCHE, NOCHE, 26)
     + arco('PLEA5E', NOCHE, 420, False, 90, 30, 'b12')),
]

# Las letras van dentro en base64 (ver fuente/LEEME.txt): sin red, sin sorpresas.
_b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
CSS = ('<style>@font-face{font-family:Anton;src:url(data:font/woff2;base64,' + _b64('fuente/anton-latin.woff2') + ')}'
       '@font-face{font-family:Montserrat;font-weight:100 900;src:url(data:font/woff2;base64,' + _b64('fuente/montserrat-latin.woff2') + ')}'
       'body{margin:0;background:#0c1014;color:#eee;font-family:Montserrat,sans-serif}'
       '.g{display:grid;grid-template-columns:repeat(4,1fr);gap:26px;padding:26px}'
       '.c{display:flex;flex-direction:column;gap:10px;align-items:center;text-align:center;font-size:13px}'
       '.c b{color:#E9BC46;font-size:22px}.big svg{width:240px;height:240px;border-radius:50%;display:block}'
       '.mini{display:flex;gap:10px;align-items:center}.mini svg{border-radius:50%;display:block}</style>')


def svg(cuerpo, w=1080):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="{w}" height="{w}">{cuerpo}</svg>'


def uniq(cuerpo, n):
    # ids distintos en cada copia del tablero
    return re.sub(r'(id="|href="#|url\(#)(\w+)', lambda m: f'{m.group(1)}{m.group(2)}_{n}', cuerpo)


base = 'marketing/instagram/avatar/ronda2/'
celdas = []
for i, (nombre, titulo, cuerpo) in enumerate(P, 1):
    celdas.append(f'<div class="c"><b>{i}</b><div class="big">{svg(uniq(cuerpo, f"{i}a"), 240)}</div>'
                  f'<div class="mini">{svg(uniq(cuerpo, f"{i}b"), 77)}{svg(uniq(cuerpo, f"{i}c"), 32)}</div>{titulo}</div>')
    open(base + nombre + '.html', 'w').write(f'<html><head>{CSS}</head><body style="margin:0">{svg(cuerpo)}</body></html>')
open(base + 'tablero.html', 'w').write(f'<html><head><meta charset="utf-8">{CSS}</head><body><div class="g">{"".join(celdas)}</div></body></html>')
print(len(P))
