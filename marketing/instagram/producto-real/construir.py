"""Carrusel "producto real" (3 fotos de 1080x1350) con las fotos de verdad editadas
(pegar.py), al estilo de la referencia de la hamburguesa:

  1. La placa en la mano y un anillo de letras finas alrededor ("5 estrellas •").
  2 y 3. Una panoramica: el expositor en la cornisa, partido justo por la mitad
     entre las dos fotos, asi al deslizar la placa "sigue". Poco texto.

Desde la raiz del repo:  python3 marketing/instagram/producto-real/construir.py
y despues:               node marketing/instagram/producto-real/hacer-png.js
"""
import base64
import os

R = 'marketing/instagram/producto-real/'
b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
MANO = 'data:image/jpeg;base64,' + b64(R + 'fotos/editada-placa-en-mano.jpg')
PANO = 'data:image/jpeg;base64,' + b64(R + 'fotos/editada-expositor-cornisa.jpg')
ico = open('public/icono.svg').read()

CSS = f'''
@font-face{{font-family:Mont;font-weight:100 900;src:url(data:font/woff2;base64,{b64('fuente/montserrat-latin.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden;font-family:Mont,sans-serif;background:#000}}
.abs{{position:absolute}}
.foto{{position:absolute;filter:contrast(1.06) saturate(1.08) brightness(1.02)}}
.vineta{{position:absolute;inset:0;background:radial-gradient(ellipse 80% 70% at 50% 50%,transparent 55%,rgba(0,0,0,.35))}}
.grano{{position:absolute;inset:0;opacity:.35;mix-blend-mode:overlay;
  background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='r'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .5 0'/></filter><rect width='300' height='300' filter='url(%23r)'/></svg>")}}
.titulo{{position:absolute;color:#fff;font-weight:800;letter-spacing:-.02em;line-height:1;text-shadow:0 4px 24px rgba(0,30,60,.35)}}
.fino{{position:absolute;color:#fff;font-weight:500;letter-spacing:.3em;text-transform:lowercase;text-shadow:0 2px 12px rgba(0,0,0,.35)}}
'''


def diapo(n, cuerpo):
    os.makedirs(R + 'diapositivas', exist_ok=True)
    open(f'{R}diapositivas/{n}.html', 'w').write(
        f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{cuerpo}'
        '<div class="vineta"></div><div class="grano"></div></body></html>')


# 1 · la placa en la mano con el anillo de letras. La foto (1932x2576) se escala a 0,64 y se
# coloca para que el centro de la placa (846, 1400 en la foto) caiga en el centro de la foto
K = .64
CX, CY, RAD = 540, 675, 480
IX, IY = CX - 846 * K, CY - 1400 * K
anillo = ' • '.join(['5 estrellas'] * 5) + ' • '
# el fondo se desenfoca mas (como un objetivo abierto), sin tocar la placa ni el centro
# de la mano: una copia borrosa encima, con un agujero redondo alrededor de la placa
FOCO = 'radial-gradient(ellipse 680px 780px at 500px 760px, transparent 70%, #000 100%)'
diapo(1, f'''<div class="abs" style="inset:0;filter:contrast(1.1) saturate(1.22) brightness(.96) sepia(.1)">
  <img class="abs" src="{MANO}" style="left:{IX:.0f}px;top:{IY:.0f}px;width:{1932 * K:.0f}px">
  <img class="abs" src="{MANO}" style="left:{IX:.0f}px;top:{IY:.0f}px;width:{1932 * K:.0f}px;filter:blur(4px);
    -webkit-mask-image:{FOCO}"></div>
<div class="abs" style="inset:0;mix-blend-mode:soft-light;background:radial-gradient(ellipse 90% 70% at 85% 5%,rgba(255,190,110,.75),transparent 60%),
  linear-gradient(180deg,rgba(40,90,160,.35),transparent 35%)"></div>
<div class="abs" style="inset:0;background:radial-gradient(ellipse 70% 60% at 50% 50%,transparent 60%,rgba(10,14,22,.35) 100%)"></div>
<svg class="abs" style="left:0;top:0" width="1080" height="1350">
  <defs><path id="aro" d="M{CX - RAD:.0f} {CY:.0f} a{RAD} {RAD} 0 1 1 {2 * RAD} 0 a{RAD} {RAD} 0 1 1 {-2 * RAD} 0"/>
  <filter id="s"><feDropShadow dx="0" dy="2" stdDeviation="5" flood-color="#000" flood-opacity=".35"/></filter></defs>
  <g transform="rotate(-100 {CX:.0f} {CY:.0f})" filter="url(#s)">
  <text font-family="Mont" font-weight="500" font-size="44" fill="#fff" letter-spacing="9">
    <textPath href="#aro" textLength="{2 * 3.14159 * RAD - 30:.0f}" lengthAdjust="spacing">{anillo}</textPath></text></g>
</svg>''')

# 2 y 3 · la panoramica. La foto (2576x1932) se recorta 2400x1500 desde (20, 60) y se escala
# a 2160x1350 (factor 0,9): el expositor (centro en x=1220 de la foto) cae en x=1080, el corte.
for n, izq in ((2, 0), (3, -1080)):
    texto = ('''<div class="titulo" style="left:70px;top:80px;font-size:104px">Tu bar,</div>
<div class="fino" style="left:74px;top:210px;font-size:30px">tu marca · tus colores</div>''' if n == 2 else
             '''<div class="titulo" style="right:70px;top:80px;font-size:104px;text-align:right">en 5 estrellas.</div>
<div class="fino" style="right:70px;top:210px;font-size:30px;text-align:right">toca o escanea · sin apps</div>
<div class="abs" style="right:70px;bottom:90px;display:flex;align-items:center;gap:22px">
  <div style="background:#E9BC46;color:#06080E;font-weight:900;font-size:42px;padding:18px 40px;border-radius:60px;box-shadow:0 10px 30px rgba(0,0,0,.3)">Comenta PLACA</div>
  <div style="color:#fff;font-weight:800;font-size:30px;letter-spacing:.12em;text-shadow:0 2px 12px rgba(0,0,0,.5)">PLEA5E.ES</div></div>''')
    diapo(n, f'<img class="foto" src="{PANO}" style="left:{izq - 20 * .9:.0f}px;top:{-60 * .9:.0f}px;width:{2576 * .9:.0f}px">' + texto)
print('3 diapositivas')
