"""Carrusel "Piedra, papel y... reseñas" (3 fotos de 1080x1350).

La broma: es piedra, papel o tijera, pero la tercera jugada no es la
tijera, es la mano con el movil tocando una placa PLEA5E. Y esa gana
siempre. Estilo de la referencia: fondo beige liso, una palabra grande
arriba y la mano en el centro.

Las manos son de Fluent Emoji (Microsoft, licencia MIT: uso comercial
libre), en vector, asi que se agrandan sin perder nada. A la del movil se
le cambia la manga rosa por los azules de PLEA5E. La placa es la de
ejemplo del otro carrusel (../carrusel-placa/capas/paso5-nfc.png).

Si se quieren fotos de una mano de verdad: fotos/piedra.jpg, papel.jpg y
resenas.jpg (ver LEEME.md); si estan, se usan en vez de las dibujadas.

Desde la raiz del repo:  python3 marketing/instagram/piedra-papel-resenas/construir.py
"""
import base64
import os
import re

P = 'marketing/instagram/piedra-papel-resenas/'
b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
svg_uri = lambda s: 'data:image/svg+xml;base64,' + base64.b64encode(s.encode()).decode()

MANGA = {'#FF99B6': '#3A4866', '#E24C86': '#2A3448', '#D56274': '#1C2536', '#BA2083': '#0F1522'}


def mano(nombre):
    """la mano: la foto de verdad si esta en fotos/, si no, la dibujada"""
    for ext in ('jpg', 'jpeg', 'png'):
        foto = f'{P}fotos/{nombre}.{ext}'
        if os.path.exists(foto):
            return f'data:image/{"png" if ext == "png" else "jpeg"};base64,{b64(foto)}', True
    s = open(f'{P}manos/{ {"piedra": "puno", "papel": "mano", "resenas": "movil"}[nombre] }.svg').read()
    for a, b in MANGA.items():
        s = s.replace(a, b)
    # la sombra de dentro de la manga va en un filtro, en rojo: tambien a azul noche
    s = s.replace('values="0 0 0 0 0.713726 0 0 0 0 0.121569 0 0 0 0 0.254902 0 0 0 1 0"',
                  'values="0 0 0 0 0.04 0 0 0 0 0.06 0 0 0 0 0.10 0 0 0 1 0"')
    return svg_uri(s), False


ESTRELLA = svg_uri(open(P + 'manos/estrella.svg').read())
PLACA = 'data:image/png;base64,' + b64('marketing/instagram/carrusel-placa/capas/paso5-nfc.png')
ico = open('public/icono.svg').read()
STAR = re.search(r'<path fill="#E9BC46" d="([^"]+)"', ico).group(1)
FIVE = re.search(r'<path fill="#0A0E16" transform="[^"]+" d="([^"]+)"', ico).group(1)
SELLO = (f'<svg viewBox="0 0 1024 900" width="44" height="39"><path fill="#B98B2E" d="{STAR}"/>'
         f'<path fill="#E2D3BE" transform="translate(407.2 677.2) scale(.42)" d="{FIVE}"/></svg>')

CSS = f'''
@font-face{{font-family:Mont;font-weight:100 900;src:url(data:font/woff2;base64,{b64('fuente/montserrat-latin.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden;font-family:Mont,sans-serif;
  background:radial-gradient(ellipse 75% 60% at 50% 45%,#E7DAC8 0%,#DCCBB4 60%,#CDBBA2 100%)}}
.palabra{{position:absolute;left:0;right:0;top:250px;text-align:center;font-weight:800;font-size:170px;
  letter-spacing:-2px;color:#8A6534}}
.mano{{position:absolute;filter:drop-shadow(0 34px 38px rgba(90,60,30,.28))}}
.foto{{position:absolute;inset:0;background-size:cover;background-position:center}}
.frase{{position:absolute;left:0;right:0;text-align:center;font-weight:700;font-size:44px;color:#6E5130}}
.frase b{{color:#8A6534;font-weight:800}}
.pie{{position:absolute;left:0;right:0;bottom:34px;display:flex;justify-content:center;align-items:center;gap:10px;
  font-weight:800;font-size:22px;letter-spacing:6px;color:#A58E6E}}
'''


def placa(x, y, lado, giro):
    """la placa con su canto de metacrilato y su sombra"""
    canto = ''.join(f'<div style="position:absolute;inset:0;border-radius:4.2%;transform:translateY({i}px);'
                    f'background:rgba({200 + 3 * i},{215 + 2 * i},{212 + 2 * i},.95);border:1px solid rgba(255,255,255,.3)"></div>'
                    for i in range(9, 0, -1))
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{lado}px;height:{lado}px;transform:rotate({giro}deg);'
            f'filter:drop-shadow(0 30px 30px rgba(90,60,30,.35))">{canto}'
            f'<img src="{PLACA}" style="position:absolute;inset:0;width:100%;height:100%;border-radius:4.2%">'
            f'<div style="position:absolute;inset:0;border-radius:4.2%;background:linear-gradient(118deg,transparent 25%,'
            f'rgba(255,255,255,.18) 32%,transparent 42%)"></div></div>')


def diapo(num, palabra, cuerpo, frase=''):
    html = f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
{cuerpo}
<div class="palabra">{palabra}</div>
{frase}
<div class="pie">{SELLO}PLEA5E</div>
</body></html>'''
    os.makedirs(P + 'diapositivas', exist_ok=True)
    open(f'{P}diapositivas/{num}.html', 'w').write(html)


def con_mano(nombre, x, y, ancho, giro=0):
    src, foto = mano(nombre)
    if foto:   # la foto de verdad ocupa la foto entera, y la palabra va encima
        return f'<div class="foto" style="background-image:url({src})"></div>'
    return f'<img class="mano" src="{src}" style="left:{x}px;top:{y}px;width:{ancho}px;transform:rotate({giro}deg)">'


ONDAS = '''<svg style="position:absolute;left:505px;top:745px" width="130" height="200" viewBox="0 0 130 200">
  <path d="M18 70 a45 45 0 0 1 0 60" fill="none" stroke="#B98B2E" stroke-width="11" stroke-linecap="round"/>
  <path d="M52 45 a80 80 0 0 1 0 110" fill="none" stroke="#B98B2E" stroke-width="11" stroke-linecap="round" opacity=".7"/>
  <path d="M88 20 a115 115 0 0 1 0 160" fill="none" stroke="#B98B2E" stroke-width="11" stroke-linecap="round" opacity=".4"/></svg>'''

# cinco estrellas en arco por encima de la placa y el movil
ESTRELLAS = ''.join(
    f'<img src="{ESTRELLA}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;transform:rotate({r}deg);'
    f'filter:drop-shadow(0 10px 12px rgba(120,80,20,.35))">'
    for x, y, w, r in ((150, 520, 96, -14), (285, 468, 112, -6), (440, 450, 124, 0), (605, 468, 112, 6), (755, 520, 96, 14)))

diapo(1, 'Piedra', con_mano('piedra', 250, 560, 580))
diapo(2, 'Papel', con_mano('papel', 240, 540, 600))
_, foto3 = mano('resenas')
if foto3:
    diapo(3, 'Reseñas', con_mano('resenas', 0, 0, 0),
          '<div class="frase" style="top:1170px">…y esta <b>gana siempre</b></div>')
else:
    diapo(3, 'Reseñas',
          placa(70, 700, 440, -6) + ONDAS + con_mano('resenas', 330, 640, 580, -24) + ESTRELLAS,
          '<div class="frase" style="top:1195px">…y esta <b>gana siempre</b></div>')
print('3 diapositivas')
