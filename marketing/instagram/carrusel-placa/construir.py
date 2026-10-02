"""Carrusel "Desliza para agregar": la placa de ejemplo montada paso a paso,
al estilo de los del cuenco (foto cenital sobre negro, el producto llenando
la imagen y cada foto con algo nuevo que se ve de un vistazo).

Toma las capas que saca capas.js y monta 7 diapositivas de 1080x1350 (el
4:5 del carrusel) en diapositivas/NN.html; hacer-png.js les hace la foto.
Negocio y logo son INVENTADOS (Bar La Plaza).

La placa se dibuja "de verdad": el metacrilato con su canto de 4 mm (la
silueta repetida hacia abajo, con el borde claro que tiene el acrilico
cortado), el brillo de la superficie, una sombra de contacto y otra
suave, y un foco de luz sobre el negro. Un poco inclinada hacia atras
(rotateX) para que el canto se vea, como en una foto hecha desde arriba.

Desde la raiz del repo:  python3 marketing/instagram/carrusel-placa/construir.py
"""
import base64
import os
import re

C = 'marketing/instagram/carrusel-placa/'
b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
png = lambda f: f'data:image/png;base64,{b64(f)}'

ico = open('public/icono.svg').read()
STAR = re.search(r'<path fill="#E9BC46" d="([^"]+)"', ico).group(1)
FIVE = re.search(r'<path fill="#0A0E16" transform="[^"]+" d="([^"]+)"', ico).group(1)
SELLO = (f'<svg viewBox="0 0 1024 900" width="52" height="46"><path fill="#E9BC46" d="{STAR}"/>'
         f'<path fill="#06080E" transform="translate(407.2 677.2) scale(.42)" d="{FIVE}"/></svg>')

LADO = 960                       # la placa, en pixeles de la foto
X0, Y0 = (1080 - LADO) // 2, 318
GROSOR = 16                      # el canto de 4 mm a esta escala

CSS = f'''
@font-face{{font-family:Mont;font-weight:100 900;src:url(data:font/woff2;base64,{b64('fuente/montserrat-latin.woff2')})}}
@font-face{{font-family:Caveat;font-weight:700;src:url(data:font/woff2;base64,{b64('fuente/caveat-latin.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden;font-family:Mont,sans-serif;color:#F4EDE0;
  background:radial-gradient(ellipse 70% 55% at 50% 60%,#171b24 0%,#0a0c12 55%,#040507 100%)}}
.cab{{position:absolute;top:44px;left:0;right:0;text-align:center;z-index:5}}
.cab .a{{font-weight:800;font-size:64px;letter-spacing:1px;color:#F7F1E3}}
.cab .b{{font-family:Caveat;font-weight:700;font-size:134px;line-height:1.02;color:#E9BC46}}
.mesa{{position:absolute;left:{X0}px;top:{Y0}px;width:{LADO}px;height:{LADO}px;
  transform:perspective(2600px) rotateX(9deg);transform-origin:50% 100%}}
.capa{{position:absolute;inset:0;border-radius:4.2%}}
.capa img{{position:absolute;inset:0;width:100%;height:100%;border-radius:4.2%}}
.sombra{{position:absolute;left:{X0 + 30}px;top:{Y0 + LADO - 40}px;width:{LADO - 60}px;height:90px;border-radius:50%;
  background:rgba(0,0,0,.85);filter:blur(30px)}}
.contacto{{position:absolute;left:{X0 + 10}px;top:{Y0 + LADO + 4}px;width:{LADO - 20}px;height:16px;border-radius:50%;
  background:rgba(0,0,0,.95);filter:blur(6px)}}
.marca{{position:absolute;border:6px solid #E9BC46;border-radius:22px;box-shadow:0 0 34px rgba(233,188,70,.75),inset 0 0 18px rgba(233,188,70,.35)}}
.marca span{{position:absolute;top:-30px;left:18px;background:#E9BC46;color:#100B00;font-weight:800;font-size:28px;
  padding:6px 16px;border-radius:30px;white-space:nowrap}}
.pie{{position:absolute;left:0;right:0;bottom:22px;display:flex;justify-content:center;align-items:center;gap:10px;
  font-weight:800;font-size:22px;letter-spacing:6px;color:#4A5263}}
'''


def canto(vacia=False):
    """el grosor: la silueta repetida hacia abajo. El acrilico cortado tiene
    el canto mas claro que la cara, y con la placa vacia se ve a traves"""
    capas = ''
    for i in range(GROSOR, 0, -1):
        k = i / GROSOR
        fondo = 'transparent' if vacia else f'rgba({int(180 + 40 * k)},{int(200 + 30 * k)},{int(200 + 30 * k)},.9)'
        borde = f'rgba(255,255,255,{.10 + .25 * (1 - k):.2f})'
        capas += f'<div class="capa" style="transform:translateY({i}px);background:{fondo};border:1.5px solid {borde}"></div>'
    return capas


def brillo():
    """el brillo del metacrilato por encima de lo impreso"""
    return ('<div class="capa" style="background:linear-gradient(118deg,rgba(255,255,255,0) 22%,rgba(255,255,255,.13) 30%,'
            'rgba(255,255,255,0) 40%,rgba(255,255,255,0) 64%,rgba(255,255,255,.07) 70%,rgba(255,255,255,0) 76%);'
            'box-shadow:inset 0 2px 0 rgba(255,255,255,.55),inset 2px 0 0 rgba(255,255,255,.25),inset 0 -2px 0 rgba(0,0,0,.25)"></div>')


def vacia():
    return ('<div class="capa" style="background:linear-gradient(135deg,rgba(255,255,255,.07),rgba(255,255,255,.015) 45%,'
            'rgba(255,255,255,.04));border:3px solid rgba(255,255,255,.6);box-shadow:inset 0 0 50px rgba(255,255,255,.06)"></div>'
            '<div class="capa" style="background:linear-gradient(118deg,transparent 20%,rgba(255,255,255,.22) 26%,'
            'transparent 34%,transparent 62%,rgba(255,255,255,.12) 67%,transparent 72%)"></div>'
            # los cuatro taladros no: esta placa va pegada con adhesivo 3M
            )


capa = lambda n: f'<div class="capa"><img src="{png(C + "capas/" + n + ".png")}"></div>'


def marca(x0, y0, x1, y1, texto):
    """el recuadro dorado de lo que se acaba de anadir (fracciones de la placa)"""
    m = 18
    return (f'<div class="marca" style="left:{x0 * LADO - m:.0f}px;top:{y0 * LADO - m:.0f}px;'
            f'width:{(x1 - x0) * LADO + 2 * m:.0f}px;height:{(y1 - y0) * LADO + 2 * m:.0f}px"><span>{texto}</span></div>')


def diapo(num, arriba, grande, cara, extra='', tam=134, vacia_=False, sobre=''):
    """sobre: lo que va encima de la placa y se inclina con ella (recuadros, chip)"""
    html = f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="cab"><div class="a">{arriba}</div><div class="b" style="font-size:{tam}px">{grande}</div></div>
<div class="sombra"></div><div class="contacto"></div>
<div class="mesa">{canto(vacia_)}{cara}{'' if vacia_ else brillo()}{sobre}</div>
{extra}
<div class="pie">{SELLO}PLEA5E</div>
</body></html>'''
    os.makedirs(C + 'diapositivas', exist_ok=True)
    open(f'{C}diapositivas/{num:02d}.html', 'w').write(html)


CHIP = f'''<svg style="position:absolute;left:0;top:0" width="{LADO}" height="{LADO}" viewBox="0 0 1000 1000">
  {''.join(f'<rect x="{200 + 22 * i}" y="{420 + 22 * i}" width="{300 - 44 * i}" height="{300 - 44 * i}" rx="{24 - 4 * i}" fill="none" stroke="#D4933F" stroke-width="10"/>' for i in range(4))}
  <rect x="320" y="540" width="60" height="60" rx="6" fill="#1b1b1b" stroke="#D4933F" stroke-width="5"/></svg>'''

MOVIL = f'''<div style="position:absolute;left:720px;top:600px;width:320px;height:620px;border-radius:46px;background:#10141d;
  border:12px solid #2A3448;transform:rotate(-12deg);overflow:hidden;box-shadow:0 40px 70px rgba(0,0,0,.8);z-index:4">
  <div style="position:absolute;inset:0;background:#fff;color:#1f1f1f;font-family:Mont">
    <div style="height:160px;background:#1F4D3A;padding:56px 26px 0"><div style="font-weight:800;font-size:31px;color:#fff">Bar La Plaza</div>
      <div style="font-weight:600;font-size:21px;color:#E9C46A;margin-top:4px">Reseña en Google</div></div>
    <div style="padding:34px 20px;text-align:center"><div style="font-weight:700;font-size:24px">¿Qué tal tu visita?</div>
      <div style="margin-top:26px;font-size:54px;letter-spacing:1px;color:#FBBC05">★★★★★</div>
      <div style="margin:26px auto 0;height:130px;border:3px solid #e2e5ea;border-radius:14px;text-align:left;padding:14px;font-size:21px">¡Trato de diez! Volveremos.</div></div>
  </div></div>
<svg style="position:absolute;left:630px;top:760px;z-index:4" width="120" height="190" viewBox="0 0 120 190">
  <path d="M15 60 a45 45 0 0 1 0 70" fill="none" stroke="#E9BC46" stroke-width="11" stroke-linecap="round"/>
  <path d="M48 38 a78 78 0 0 1 0 114" fill="none" stroke="#E9BC46" stroke-width="11" stroke-linecap="round" opacity=".7"/>
  <path d="M82 16 a110 110 0 0 1 0 158" fill="none" stroke="#E9BC46" stroke-width="11" stroke-linecap="round" opacity=".4"/></svg>'''

D = 'DESLIZA PARA AGREGAR'
diapo(1, D, 'TUS COLORES', vacia(), vacia_=True)
diapo(2, D, 'TU MENSAJE', capa('paso1-colores'))
diapo(3, D, 'TU LOGO Y NOMBRE', capa('paso2-mensaje'), sobre=marca(.28, .07, .72, .345, '+ mensaje'), tam=120)
diapo(4, D, 'EL CÓDIGO QR', capa('paso3-cliente'), sobre=marca(.27, .755, .73, .875, '+ logo y nombre'))
diapo(5, D, 'EL CHIP NFC', capa('paso4-qr'), sobre=marca(.29, .38, .83, .745, '+ código QR'))
diapo(6, 'DESLIZA PARA', 'PROBARLA',
      f'<div class="capa" style="opacity:.5">{capa("paso5-nfc")}</div>',
      sobre=CHIP + marca(.17, .39, .52, .65, '+ chip NFC programado'))
diapo(7, '¡LISTA PARA TU MESA!', '5 ★ en 10 segundos', capa('paso5-nfc'), MOVIL, tam=110)
print('7 diapositivas')
