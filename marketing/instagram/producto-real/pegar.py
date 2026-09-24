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


def borrar(im, x0, y0, x1, y1):
    """tapa un trozo de la foto con el fondo de alrededor (el fondo esta desenfocado,
    asi que basta con rellenarlo suave desde los bordes y ponerle el mismo grano)"""
    h, w = im.shape[:2]
    m = np.zeros((h, w), bool); m[y0:y1, x0:x1] = True
    k = 8                                                     # se rellena a 1/8 y se sube
    peq = im[::k, ::k].copy(); mp = m[::k, ::k]
    for c in range(3):
        canal = peq[..., c]
        canal[mp] = canal[~mp].mean()
        for _ in range(400):
            canal[mp] = nd.uniform_filter(canal, 5)[mp]
    grande = np.stack([nd.zoom(peq[..., c], k, order=1)[:h, :w] for c in range(3)], -1)
    grande = nd.gaussian_filter(grande, (6, 6, 0))
    borde = nd.gaussian_filter(nd.binary_dilation(m, iterations=6).astype(np.float32), 8)[..., None]
    ruido = np.random.default_rng(2).normal(0, .012, (h, w))[..., None]
    return im * (1 - borde) + (grande + ruido) * borde


def pegar(foto, diseno, esquinas, luz='placa', margen=0, salida=None, tapar=None):
    im = lee(R + 'fotos/' + foto)
    if tapar:
        im = borrar(im, *tapar)
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
    color = nd.gaussian_filter(color, (.6, .6, 0))
    ruido = np.random.default_rng(1).normal(0, .012, color.shape[:2])[..., None]
    color = color + ruido
    im[y0:y1, x0:x1] = trozo * (1 - a[..., None]) + color * a[..., None]
    guarda(im, R + 'fotos/' + (salida or 'editada-' + foto))
    return im


if __name__ == '__main__':
    # la placa de mesa (9x9) en la mano
    pegar('placa-en-mano.jpg', 'placa.png', [(337, 870), (1341, 892), (1351, 1891), (352, 1937)], 'placa', margen=6,
          tapar=(1140, 2004, 1932, 2576))                     # la tarjeta de otra marca que asoma abajo
    # el expositor de pie en la cornisa (la cara de delante, antes de la doblez)
    pegar('expositor-cornisa.jpg', 'stand.png', [(836, 173), (1437, 242), (1610, 1213), (941, 1332)], 'impresa', margen=4)
    print('fotos editadas')
