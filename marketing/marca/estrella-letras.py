"""estrella-letras.py — logo tipográfico de PLEA5E: la palabra dibuja la estrella.

Las cinco letras P·L·E·A·E se deforman (envolvente) para ser las cinco puntas de la estrella, y el 5 se
deforma para rellenar el pentágono del centro. Fuente: Anton (SIL OFL), la misma del sello.
    python3 estrella-letras.py salida.svg [variante]      variante: oro | negro | contorno
"""
import math
import sys

from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont

FUENTE = '/home/user/whatthefan.github.io/fuente/anton-latin.woff2'
R_EXT, R_INT = 1.0, 0.47          # radios de la estrella (interior algo más grueso que el canónico 0,38)
HUECO = 0.035                     # separación entre piezas
ORDEN = ['P', 'L', 'E', 'A', 'E'] # puntas en el sentido del reloj desde arriba; el 5 va en el centro


class Muestreo(BasePen):
    """Convierte el contorno de un glifo en polígonos (curvas muestreadas)."""
    def __init__(self, glyphset, pasos=14):
        super().__init__(glyphset); self.cont = []; self.act = None; self.n = pasos
    def _moveTo(self, p): self.act = [p]; self.cont.append(self.act)
    def _lineTo(self, p): self.act.append(p)
    def _curveToOne(self, a, b, c):
        p0 = self.act[-1]
        for i in range(1, self.n + 1):
            t = i / self.n; m = 1 - t
            self.act.append((m**3*p0[0] + 3*m*m*t*a[0] + 3*m*t*t*b[0] + t**3*c[0], m**3*p0[1] + 3*m*m*t*a[1] + 3*m*t*t*b[1] + t**3*c[1]))
    def _qCurveToOne(self, a, b):
        p0 = self.act[-1]
        for i in range(1, self.n + 1):
            t = i / self.n; m = 1 - t
            self.act.append((m*m*p0[0] + 2*m*t*a[0] + t*t*b[0], m*m*p0[1] + 2*m*t*a[1] + t*t*b[1]))
    def _closePath(self): pass
    def _endPath(self): pass


def glifo(font, ch):
    gs = font.getGlyphSet(); nombre = font.getBestCmap()[ord(ch)]
    pen = Muestreo(gs); gs[nombre].draw(pen)
    xs = [x for c in pen.cont for x, _ in c]; ys = [y for c in pen.cont for _, y in c]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    # normalizado: u 0..1 izquierda→derecha, v 0..1 arriba→abajo
    return [[((x - x0) / (x1 - x0), (y1 - y) / (y1 - y0)) for x, y in c] for c in pen.cont]


def dirc(a):
    return math.cos(a), math.sin(a)


def poligono_punta(k):
    th = math.radians(-90 + 72 * k)
    tip = [R_EXT * v for v in dirc(th)]
    bl = [R_INT * v for v in dirc(th - math.radians(36))]
    br = [R_INT * v for v in dirc(th + math.radians(36))]
    return [tip, br, bl]


def poligono_centro():
    return [[R_INT * v for v in dirc(math.radians(-90 + 72 * k + 36))] for k in range(5)]


def encoge(pol, s):
    cx = sum(p[0] for p in pol) / len(pol); cy = sum(p[1] for p in pol) / len(pol)
    return [(cx + (x - cx) * s, cy + (y - cy) * s) for x, y in pol]


def cuerda(pol, y):
    """Corte horizontal del polígono (convexo) a la altura y: (xmin, xmax)."""
    xs = []
    for i in range(len(pol)):
        (x1, y1), (x2, y2) = pol[i], pol[(i + 1) % len(pol)]
        if (y1 - y) * (y2 - y) <= 0 and y1 != y2:
            xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
    return (min(xs), max(xs)) if xs else None


def envolvente(cont, pol, curva=1.0):
    """Letra DE PIE dentro del polígono: cada fila de la letra se estira al ancho del polígono a esa altura."""
    ys = [p[1] for p in pol]; y0, y1 = min(ys), max(ys)
    eps = (y1 - y0) * .002
    out = []
    for c in cont:
        pts = []
        for u, v in c:
            y = y0 + eps + (y1 - y0 - 2 * eps) * (v ** curva)
            a, b = cuerda(pol, y)
            pts.append((a + (b - a) * u, y))
        out.append(pts)
    return out


CUERPO, PUNTA = .70, .75   # la letra ocupa del 0 al 60 % del eje de la punta; el pico macizo, del 66 % al 100 %


def a_punta(cont, k):
    """Letra en el cuerpo de la punta k (casi recta, se lee) + pico macizo aparte.
    Arriba y brazos: la letra mira hacia fuera. Piernas (k = 2, 3): mira hacia el centro, así queda casi de pie."""
    tip, br, bl = encoge(poligono_punta(k), 1 - HUECO * 2.2)
    M = ((br[0] + bl[0]) / 2, (br[1] + bl[1]) / 2)
    ax = (tip[0] - M[0], tip[1] - M[1])
    L = math.hypot(*ax); A = (ax[0] / L, ax[1] / L)
    media = math.hypot(br[0] - bl[0], br[1] - bl[1]) / 2
    fuera = k not in (2, 3)
    U = A if fuera else (-A[0], -A[1])          # «arriba» de la letra
    Rt = (-U[1], U[0])                           # su derecha
    out = []
    for c in cont:
        pts = []
        for u, v in c:
            f = (1 - v) * CUERPO if fuera else v * CUERPO
            w = media * (1 - f * .85) * 0.97
            pts.append((M[0] + ax[0] * f + Rt[0] * (u - .5) * 2 * w, M[1] + ax[1] * f + Rt[1] * (u - .5) * 2 * w))
        out.append(pts)
    # pico macizo
    fp = PUNTA; w = media * (1 - fp) * 0.94
    base_pico = [(M[0] + ax[0] * fp + s * Rt[0] * w, M[1] + ax[1] * fp + s * Rt[1] * w) for s in (-1, 1)]
    out.append([base_pico[0], tip, base_pico[1]])
    return out


def a_pentagono(cont):
    return envolvente(cont, encoge(poligono_centro(), 1 - HUECO * 2.6))


def a_punta_sello(cont, k, cuerpo=(.08, .62), estrecha=.35):
    """Sello: letra casi recta dentro de la punta (se recorta de la estrella maciza)."""
    tip, br, bl = poligono_punta(k)
    M = ((br[0] + bl[0]) / 2, (br[1] + bl[1]) / 2)
    ax = (tip[0] - M[0], tip[1] - M[1]); L = math.hypot(*ax); A = (ax[0] / L, ax[1] / L)
    media = math.hypot(br[0] - bl[0], br[1] - bl[1]) / 2
    fuera = k not in (2, 3)
    U = A if fuera else (-A[0], -A[1]); Rt = (-U[1], U[0])
    f0, f1 = cuerpo; out = []
    for c in cont:
        pts = []
        for u, v in c:
            f = f0 + ((1 - v) if fuera else v) * (f1 - f0)
            w = media * (1 - f1) * .95 * (1 + estrecha * (f1 - f) / (f1 - f0))
            pts.append((M[0] + ax[0] * f + Rt[0] * (u - .5) * 2 * w, M[1] + ax[1] * f + Rt[1] * (u - .5) * 2 * w))
        out.append(pts)
    return out


def ruta(contornos, esc, cx, cy):
    return ' '.join('M' + ' L'.join(f'{cx + x * esc:.1f} {cy + y * esc:.1f}' for x, y in c) + ' Z' for c in contornos)


def svg_sello(variante='oro'):
    font = TTFont(FUENTE)
    W = 1000; esc = 470; cx, cy = W / 2, W / 2 + 40
    estrella = [[R_EXT * v for v in dirc(math.radians(-90 + 36 * i))] if i % 2 == 0 else [R_INT * v for v in dirc(math.radians(-90 + 36 * i))] for i in range(10)]
    letras = [a_punta_sello(glifo(font, ch), k) for k, ch in enumerate(ORDEN)]
    cinco = envolvente(glifo(font, '5'), encoge(poligono_centro(), .78))
    d_est = ruta([estrella], esc, cx, cy)
    d_let = ' '.join(ruta(p, esc, cx, cy) for p in letras + [cinco])
    fondo, oro, hueco = ('#F3F1EA', '#06080E', '#F3F1EA') if variante == 'negro' else ('#06080E', 'url(#oro)', '#06080E')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="{W}" height="{W}">
<defs><linearGradient id="oro" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2CF6A"/><stop offset="1" stop-color="#D9A933"/></linearGradient></defs>
<rect width="{W}" height="{W}" fill="{fondo}"/>
<path d="{d_est}" fill="{oro}" stroke="{oro}" stroke-width="18" stroke-linejoin="round"/>
<path d="{d_let}" fill="{hueco}"/>
</svg>'''


def svg(variante='oro'):
    if variante.startswith('sello'):
        return svg_sello(variante.split('-')[1] if '-' in variante else 'oro')
    font = TTFont(FUENTE)
    piezas = [a_punta(glifo(font, ch), k) for k, ch in enumerate(ORDEN)] + [a_pentagono(glifo(font, '5'))]
    W = 1000; esc = 470; cx, cy = W / 2, W / 2 + 40
    d = ' '.join(ruta(p, esc, cx, cy) for p in piezas)
    if variante == 'negro':
        fondo, relleno, extra = '#F3F1EA', '#06080E', ''
    elif variante == 'contorno':
        fondo, relleno, extra = '#06080E', 'none', 'stroke="#E9BC46" stroke-width="5" stroke-linejoin="round"'
    else:
        fondo, relleno, extra = '#06080E', 'url(#oro)', ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="{W}" height="{W}">
<defs><linearGradient id="oro" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2CF6A"/><stop offset="1" stop-color="#D9A933"/></linearGradient></defs>
<rect width="{W}" height="{W}" fill="{fondo}"/>
<path d="{d}" fill="{relleno}" fill-rule="nonzero" {extra}/>
</svg>'''


if __name__ == '__main__':
    open(sys.argv[1], 'w').write(svg(sys.argv[2] if len(sys.argv) > 2 else 'oro'))
    print('listo', sys.argv[1])
