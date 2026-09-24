"""Pega el diseno de PLEA5E sobre las fotos de verdad (las placas en blanco que
hizo el) para que parezca impreso en ellas.

  1. La perspectiva: una homografia lleva el diseno plano a las cuatro esquinas
     de la placa en la foto (medidas a mano en la foto, ver ESQUINAS).
  2. La luz: el diseno se multiplica por la luz que tiene la placa en la foto
     (su brillo suavizado), asi el sol, las sombras y el degradado siguen ahi.
  3. El acabado: un pelin de desenfoque (la foto no es perfecta) y el mismo
     grano que la foto, para que no parezca una pegatina digital.

Saca fotos/editada-NOMBRE.jpg. Desde la raiz del repo:
    node   marketing/instagram/producto-real/disenos.js     (los disenos planos)
    python3 marketing/instagram/producto-real/pegar.py
"""
import subprocess

import numpy as np
from scipy import ndimage as nd

R = 'marketing/instagram/producto-real/'
FF = '/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2'


def tam(f):
    s = subprocess.run([FF, '-i', f], capture_output=True, text=True).stderr
    import re
    w, h = re.search(r', (\d{3,5})x(\d{3,5})', s).groups()
    return int(w), int(h)


def lee(f, rgba=False):
    w, h = tam(f)
    c = 4 if rgba else 3
    b = subprocess.run([FF, '-loglevel', 'error', '-i', f, '-f', 'rawvideo', '-pix_fmt', 'rgba' if rgba else 'rgb24', '-'],
                       capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(h, w, c).astype(np.float32) / 255


def guarda(im, f, q=2):
    h, w = im.shape[:2]
    subprocess.run([FF, '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}', '-i', '-',
                    '-q:v', str(q), f], input=(np.clip(im, 0, 1) * 255).astype(np.uint8).tobytes(), check=True)


def homografia(src, dst):
    A = []
    for (x, y), (u, v) in zip(src, dst):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y, -u], [0, 0, 0, x, y, 1, -v * x, -v * y, -v]]
    _, _, V = np.linalg.svd(np.array(A))
    return V[-1].reshape(3, 3) / V[-1, -1]


def borrar(im, x0, y0, x1, y1, libre=None):
    """tapa un trozo de la foto con el fondo de alrededor (el fondo esta desenfocado,
    asi que basta con rellenarlo suave desde los bordes y ponerle el mismo grano).
    libre: otra caja que NO sirve de borde (p. ej. un dedo pegado al trozo: si no, el
    relleno cogeria el color de la piel); se calcula pero no se toca."""
    h, w = im.shape[:2]
    m = np.zeros((h, w), bool); m[y0:y1, x0:x1] = True
    # el dedo que roza el borde de arriba del trozo se respeta: en la franja de arriba,
    # lo que tiene color de piel (mas rojo que azul y mas oscuro que el suelo) no se tapa
    r_, g_, b_ = im[..., 0], im[..., 1], im[..., 2]
    piel = (r_ - b_ > .09) & (r_ - g_ > .03) & (im.mean(2) < .58)
    franja = np.zeros_like(m); franja[y0:y0 + 45, x0:x1] = True
    dedo = nd.binary_opening(piel & franja, iterations=2)
    m &= ~dedo
    suelto = m.copy()
    if libre:
        suelto[libre[1]:libre[3], libre[0]:libre[2]] = True
    k = 4
    peq = im[::k, ::k].copy(); mp = suelto[::k, ::k]
    # solo vale de muestra el suelo (claro y sin color), no la mano ni lo oscuro
    claro = (peq.mean(2) > .55) & (np.ptp(peq, axis=2) < .12)
    conocido = ((~mp) & claro).astype(np.float32)
    for c in range(3):
        canal = peq[..., c]
        # primero, la media de lo que hay alrededor (convolucion normalizada: solo cuenta
        # lo conocido), y despues se alisa para que no queden escalones
        suelo = canal[conocido > 0].mean()
        canal[mp] = suelo
        for sg in (60, 25, 10):
            peso = nd.gaussian_filter(conocido, sg)
            cerca = nd.gaussian_filter(canal * conocido, sg) / np.maximum(peso, 1e-6)
            # donde no llega ninguna muestra (muy lejos del borde), se queda el color medio del suelo
            cerca = np.where(peso > .02, cerca, suelo)
            canal[mp] = cerca[mp] if sg == 60 else .5 * canal[mp] + .5 * cerca[mp]
        for _ in range(200):
            canal[mp] = nd.uniform_filter(canal, 3)[mp]
    grande = np.stack([nd.zoom(peq[..., c], k, order=1)[:h, :w] for c in range(3)], -1)
    grande = nd.gaussian_filter(grande, (4, 4, 0))
    # la mezcla va solo hacia DENTRO del trozo: fuera no se toca nada (ni el dedo)
    borde = nd.gaussian_filter(m.astype(np.float32), 2)[..., None] * m[..., None]
    ruido = np.random.default_rng(2).normal(0, .01, (h, w))[..., None]
    return im * (1 - borde) + (grande + ruido) * borde


def pegar(foto, diseno, esquinas, luz='placa', margen=0, salida=None, tapar=None, revelar_foto=False):
    im = lee(R + 'fotos/' + foto)
    if tapar:
        im = borrar(im, *tapar[:4], libre=tapar[4] if len(tapar) > 4 else None)
    d = lee(R + 'disenos/' + diseno, rgba=True)
    dh, dw = d.shape[:2]
    Hm = homografia([(0, 0), (dw, 0), (dw, dh), (0, dh)], esquinas)
    Hi = np.linalg.inv(Hm)
    xs, ys = [p[0] for p in esquinas], [p[1] for p in esquinas]
    x0, x1, y0, y1 = int(min(xs)) - 2, int(max(xs)) + 3, int(min(ys)) - 2, int(max(ys)) + 3
    gy, gx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    pts = Hi @ np.stack([gx.ravel() + .5, gy.ravel() + .5, np.ones(gx.size)])
    u, v = (pts[0] / pts[2]).reshape(gx.shape) - .5, (pts[1] / pts[2]).reshape(gx.shape) - .5
    # supermuestreo sencillo: el diseno es mas grande que la placa en la foto, asi que
    # primero se suaviza el diseno a la escala de destino (evita dientes y moire en el QR)
    esc = dw / max(1, (max(xs) - min(xs)))
    ds = np.stack([nd.gaussian_filter(d[..., c], esc * .45) for c in range(4)], -1)
    capa = np.stack([nd.map_coordinates(ds[..., c], [v, u], order=1, mode='constant', cval=0) for c in range(4)], -1)
    # el borde de la pieza: se recorta unos px hacia dentro para que se vea el canto de la foto
    dentro = (u >= margen) & (v >= margen) & (u <= dw - 1 - margen) & (v <= dh - 1 - margen)
    a = capa[..., 3] * dentro
    a = nd.gaussian_filter(a, .7)
    trozo = im[y0:y1, x0:x1]
    lum = trozo.mean(2)
    if luz == 'placa':           # la placa esta en blanco: su brillo ES la luz
        L = nd.gaussian_filter(lum, 6)
    else:                        # la placa ya tenia algo impreso: la luz sale de lo mas claro de cada zona
        L = nd.gaussian_filter(nd.maximum_filter(lum * dentro + (1 - dentro) * lum.max(), 90), 60)
    blanco = np.percentile(L[a > .5], 97)
    L = (L / blanco)[..., None]
    color = capa[..., :3] * L * 1.02
    # el tinte de la luz de la foto (el blanco de la placa no es blanco puro)
    tinte = np.array([np.percentile(trozo[..., c][a > .5], 95) for c in range(3)])
    tinte = tinte / tinte.max()
    color = color * (.35 + .65 * tinte)
    color = nd.gaussian_filter(color, (.35, .35, 0))
    ruido = np.random.default_rng(1).normal(0, .012, color.shape[:2])[..., None]
    color = color + ruido
    im[y0:y1, x0:x1] = trozo * (1 - a[..., None]) + color * a[..., None]
    if revelar_foto:
        im = revelar(im)
    guarda(im, R + 'fotos/' + (salida or 'editada-' + foto))
    return im


def revelar(im):
    """el 'revelado' de la foto a contraluz: le quita la neblina (niveles), le da
    claridad (contraste local), la enfoca un poco y le sube el color. Es lo que hace que
    la del expositor, con sol directo, se vea tan nitida: aqui se le da lo mismo"""
    lo, hi = np.percentile(im, .3, axis=(0, 1)) * .6, np.percentile(im, 99.9, axis=(0, 1))
    im = np.clip((im - lo) / (hi - lo), 0, 1)
    L = im.mean(2, keepdims=True)
    im = im + .18 * (L - nd.gaussian_filter(L, (40, 40, 0)))           # claridad
    im = im + .45 * (im - nd.gaussian_filter(im, (1.2, 1.2, 0)))         # enfoque
    L = im.mean(2, keepdims=True)
    im = L + 1.1 * (im - L)                                            # color
    im = im * np.array([1.02, 1.0, .97])                                # un punto calido
    im = np.clip(im, 0, 1)                                      # sombras un poco mas hondas
    return im


if __name__ == '__main__':
    # la placa de mesa (9x9) en la mano
    pegar('placa-en-mano.jpg', 'placa.png', [(337, 870), (1341, 892), (1351, 1891), (352, 1937)], 'placa', margen=6,
          tapar=(1116, 2000, 1932, 2576, (900, 1850, 1440, 2000)), revelar_foto=True)                     # la tarjeta de otra marca que asoma abajo
    # el expositor de pie en la cornisa (la cara de delante, antes de la doblez)
    pegar('expositor-cornisa.jpg', 'stand.png', [(836, 173), (1437, 242), (1610, 1213), (941, 1332)], 'impresa', margen=4)
    print('fotos editadas')
