"""Carrusel "Desliza para agregar": la placa de ejemplo montada paso a paso.

Toma las capas que saca capas.js y monta 7 diapositivas de 1080x1350
(el 4:5 del carrusel de Instagram) en diapositivas/NN.html; hacer-png.js
les hace la foto. Negocio y logo son INVENTADOS (Bar La Plaza).

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
SELLO = (f'<svg viewBox="0 0 1024 900" width="46" height="40"><path fill="#E9BC46" d="{STAR}"/>'
         f'<path fill="#06080E" transform="translate(407.2 677.2) scale(.42)" d="{FIVE}"/></svg>')

CSS = f'''
@font-face{{font-family:Mont;font-weight:100 900;src:url(data:font/woff2;base64,{b64('fuente/montserrat-latin.woff2')})}}
@font-face{{font-family:Caveat;font-weight:700;src:url(data:font/woff2;base64,{b64('fuente/caveat-latin.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden;background:#06080E;font-family:Mont,sans-serif;color:#F4EDE0}}
.cab{{position:absolute;top:62px;left:0;right:0;text-align:center}}
.cab .a{{font-weight:800;font-size:62px;letter-spacing:1px;color:#F7F1E3}}
.cab .b{{font-family:Caveat;font-weight:700;font-size:128px;line-height:1.05;color:#E9BC46}}
.placa{{position:absolute;left:130px;top:360px;width:820px;height:820px}}
.placa .canto{{position:absolute;inset:0;border-radius:4.2%}}
.placa img{{position:absolute;inset:0;width:100%;height:100%}}
.sombra{{position:absolute;left:150px;top:1150px;width:780px;height:60px;border-radius:50%;background:rgba(0,0,0,.8);filter:blur(22px)}}
.nota{{position:absolute;left:0;right:0;top:1222px;text-align:center;font-weight:600;font-size:30px;color:#8B95AB}}
.nota b{{color:#E9BC46}}
.firma{{position:absolute;left:0;right:0;bottom:30px;display:flex;justify-content:center;align-items:center;gap:10px;
       font-weight:800;font-size:24px;letter-spacing:5px;color:#5D6679}}
'''


def canto(transparente=False):
    """el grosor del metacrilato: la silueta repetida hacia abajo a la derecha.
    Con la placa ya impresa el vinilo lo tapa todo y solo asoma el canto;
    vacia se ve a traves, asi que ahi solo se pintan los bordes."""
    capas = ''
    for i in range(10, 0, -1):
        relleno = 'transparent' if transparente else f'rgba(214,226,232,{.10 + .012 * i:.3f})'
        capas += (f'<div class="canto" style="transform:translate({i * .9:.1f}px,{i * 1.4:.1f}px);'
                  f'background:{relleno};border:1px solid rgba(255,255,255,{.05 if transparente else .10})"></div>')
    return capas


def vidrio():
    return ('<div class="canto" style="background:linear-gradient(135deg,rgba(255,255,255,.10),rgba(255,255,255,.02) 42%,'
            'rgba(255,255,255,.01) 58%,rgba(255,255,255,.06));border:3px solid rgba(255,255,255,.55);'
            'box-shadow:inset 0 0 40px rgba(255,255,255,.08)"></div>'
            '<div class="canto" style="background:linear-gradient(115deg,transparent 18%,rgba(255,255,255,.18) 22%,'
            'transparent 30%,transparent 62%,rgba(255,255,255,.10) 66%,transparent 70%)"></div>')


def diapo(num, arriba, grande, placa_html, extra='', nota='', tam=128, vacia=False):
    html = f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="cab"><div class="a">{arriba}</div><div class="b" style="font-size:{tam}px">{grande}</div></div>
<div class="sombra"></div>
<div class="placa">{canto(vacia)}{placa_html}</div>
{extra}
<div class="nota">{nota}</div>
<div class="firma">{SELLO}PLEA5E</div>
</body></html>'''
    os.makedirs(C + 'diapositivas', exist_ok=True)
    open(f'{C}diapositivas/{num:02d}.html', 'w').write(html)


capa = lambda n: f'<img src="{png(C + "capas/" + n + ".png")}">'

LUPA = f'''<svg style="position:absolute;left:0;top:0" width="1080" height="1350">
  <line x1="570" y1="1010" x2="780" y2="930" stroke="#E9BC46" stroke-width="4"/>
  <circle cx="555" cy="1012" r="22" fill="none" stroke="#E9BC46" stroke-width="4"/></svg>
<div style="position:absolute;left:760px;top:730px;width:260px;height:260px;border-radius:50%;border:8px solid #E9BC46;
  background:#F7F7F7 url({png(C + 'logo-ejemplo.png')}) center/78% no-repeat;box-shadow:0 12px 30px rgba(0,0,0,.6)"></div>'''

CHIP = '''<svg style="position:absolute;left:130px;top:360px" width="820" height="820" viewBox="0 0 820 820">
  <g opacity=".95">
    <rect x="150" y="270" width="300" height="300" rx="26" fill="none" stroke="#C98A3A" stroke-width="9"/>
    <rect x="172" y="292" width="256" height="256" rx="20" fill="none" stroke="#C98A3A" stroke-width="9"/>
    <rect x="194" y="314" width="212" height="212" rx="16" fill="none" stroke="#C98A3A" stroke-width="9"/>
    <rect x="270" y="390" width="60" height="60" rx="6" fill="#1b1b1b" stroke="#C98A3A" stroke-width="5"/>
  </g></svg>
<div style="position:absolute;left:60px;top:1060px;background:#E9BC46;color:#100B00;font-weight:800;font-size:30px;
  padding:14px 26px;border-radius:40px">Programado con tu ficha de Google ✓</div>'''

MOVIL = f'''<div style="position:absolute;left:745px;top:640px;width:285px;height:552px;border-radius:42px;background:#10141d;
  border:11px solid #2A3448;transform:rotate(-10deg);overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.7)">
  <div style="position:absolute;inset:0;background:#fff;color:#1f1f1f;font-family:Mont">
    <div style="height:150px;background:#1F4D3A;padding:52px 26px 0"><div style="font-weight:800;font-size:30px;color:#fff">Bar La Plaza</div>
      <div style="font-weight:600;font-size:20px;color:#E9C46A;margin-top:4px">Reseña en Google</div></div>
    <div style="padding:34px 20px;text-align:center"><div style="font-weight:700;font-size:23px">¿Qué tal tu visita?</div>
      <div style="margin-top:26px;font-size:50px;letter-spacing:1px;color:#FBBC05">★★★★★</div>
      <div style="margin:26px auto 0;height:120px;border:3px solid #e2e5ea;border-radius:14px;text-align:left;padding:14px;font-size:20px;color:#1f1f1f">¡Trato de diez! Volveremos.</div></div>
  </div></div>
<svg style="position:absolute;left:672px;top:760px" width="110" height="170" viewBox="0 0 110 170">
  <path d="M15 50 a45 45 0 0 1 0 70" fill="none" stroke="#E9BC46" stroke-width="10" stroke-linecap="round"/>
  <path d="M45 30 a75 75 0 0 1 0 110" fill="none" stroke="#E9BC46" stroke-width="10" stroke-linecap="round" opacity=".7"/>
  <path d="M75 10 a105 105 0 0 1 0 150" fill="none" stroke="#E9BC46" stroke-width="10" stroke-linecap="round" opacity=".4"/></svg>
<div style="position:absolute;left:0;right:0;top:1195px;text-align:center">
  <span style="display:inline-block;background:#E9BC46;color:#100B00;font-weight:800;font-size:34px;padding:16px 34px;border-radius:44px">Comenta PLACA y te hacemos la tuya</span></div>'''

D = 'DESLIZA PARA AGREGAR'
diapo(1, D, 'TU NOMBRE', vidrio(), nota='Metacrilato de <b>4 mm</b> · 90 × 90 mm', vacia=True)
diapo(2, D, 'TU LOGO', capa('paso1-nombre'), nota='El nombre de tu local, con tu lema')
diapo(3, D, 'TUS COLORES', capa('paso2-logo'), LUPA, nota='Tu logo, tal cual lo tienes')
diapo(4, D, 'EL CÓDIGO QR', capa('paso3-colores'), nota='Los colores de tu marca')
diapo(5, D, 'EL CHIP NFC', capa('paso4-qr'), nota='Lleva a <b>tu ficha de Google</b>, directo a escribir')
diapo(6, 'DESLIZA PARA', 'PROBARLA', f'<div style="position:absolute;inset:0;opacity:.55">{capa("paso5-nfc")}</div>', CHIP,
      nota='El chip va dentro: se acerca el móvil y listo')
diapo(7, '¡LISTA PARA TU MESA!', '5 ★ en 10 segundos', capa('paso5-nfc'), MOVIL, tam=104)
print('7 diapositivas')
