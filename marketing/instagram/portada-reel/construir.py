"""Portada generica para los reels (1080x1920) de Estrellita ensenando la placa.

Fondo de restaurante de noche desenfocado (luces calidas en bokeh, pared oscura y la
mesa de madera), Estrellita senalando la placa y un titular enorme en letra
aterciopelada: cara con degradado suave, brillo en los bordes, pelusa fina (moteado),
volumen en 3D y sombra.

Lo importante (titular, placa y Estrellita) cae dentro del recorte 3:4 que ensena el
perfil (de y=240 a y=1680).

Desde la raiz del repo:  python3 marketing/instagram/portada-reel/construir.py
y despues:               node marketing/instagram/portada-reel/hacer-png.js
"""
import base64
import math
import random

P = 'marketing/instagram/portada-reel/'
b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
svg = lambda f: 'data:image/svg+xml;base64,' + b64(f)
PLACA = 'data:image/png;base64,' + b64('marketing/instagram/carrusel-placa/capas/paso5-nfc.png')
BICHO = svg('marketing/instagram/personaje/svg/senala.svg')
W, H = 1080, 1920

# las luces del restaurante (bokeh): circulos calidos desenfocados
rnd = random.Random(5)
LUCES = ''
for _ in range(38):
    x, y = rnd.uniform(-60, W + 60), rnd.uniform(-40, 1250)
    r = rnd.uniform(30, 120)
    c = rnd.choice(['255,196,110', '255,170,80', '255,220,150', '240,150,70'])
    a = rnd.uniform(.10, .38) * (1.15 - y / 1500)
    bl = rnd.uniform(3, 14)
    LUCES += (f'<div class="abs" style="left:{x - r:.0f}px;top:{y - r:.0f}px;width:{2 * r:.0f}px;height:{2 * r:.0f}px;border-radius:50%;'
              f'background:radial-gradient(circle,rgba({c},{a:.2f}) 0%,rgba({c},{a * .8:.2f}) 55%,rgba({c},{a * .25:.2f}) 72%,transparent 74%);'
              f'filter:blur({bl:.0f}px)"></div>')

DEFS = '''<defs>
<linearGradient id="gBlanco" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="#FFF6E6"/><stop offset="1" stop-color="#F1DDBE"/></linearGradient>
<linearGradient id="gOro" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD84A"/><stop offset=".5" stop-color="#F2B92A"/><stop offset="1" stop-color="#D08A10"/></linearGradient>
<filter id="sombra" x="-20%" y="-30%" width="140%" height="180%"><feDropShadow dx="6" dy="22" stdDeviation="16" flood-color="#000" flood-opacity=".6"/></filter>
<!-- terciopelo: los bordes cogen luz (el pelo de la tela) y el centro se queda mate -->
<filter id="terciopelo" x="-5%" y="-5%" width="110%" height="110%">
  <feMorphology in="SourceAlpha" operator="erode" radius="7" result="dentro"/>
  <feGaussianBlur in="dentro" stdDeviation="7" result="dentroB"/>
  <feComposite in="SourceAlpha" in2="dentroB" operator="out" result="borde"/>
  <feFlood flood-color="#FFF4DC" flood-opacity=".38"/><feComposite in2="borde" operator="in" result="brillo"/>
  <feTurbulence type="fractalNoise" baseFrequency="1.8" numOctaves="2" seed="11" result="ruido"/>
  <feColorMatrix in="ruido" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2 1.25" result="pelusa"/>
  <feComposite in="pelusa" in2="SourceAlpha" operator="in" result="pelusaD"/>
  <feComponentTransfer in="pelusaD" result="pelusaS"><feFuncA type="linear" slope=".28"/></feComponentTransfer>
  <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="brillo"/><feMergeNode in="pelusaS"/></feMerge>
</filter>
</defs>'''


def titulo(texto, x, y, tam, cara, lado, filo, giro=0):
    t = lambda fill, extra='': (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Titan" font-size="{tam}" '
                                f'letter-spacing="{tam * .01:.1f}" fill="{fill}" {extra}>{texto}</text>')
    capas = int(tam * .11)
    vol = ''.join(f'<g transform="translate({i * .45:.1f} {i * .85:.1f})">{t(lado)}</g>' for i in range(capas, 0, -1))
    trazo = f'stroke="{filo}" stroke-width="{tam * .05:.1f}" stroke-linejoin="round"'
    return (f'<g transform="rotate({giro} {x} {y})"><g filter="url(#sombra)">{vol}</g>'
            f'{t(filo, trazo)}'
            f'<g filter="url(#terciopelo)">{t(cara)}</g></g>')


def estrellas(cx, y, tam, hueco=16):
    pt = lambda ex, k, r: (ex + r * math.sin(math.pi * k / 5), y - r * math.cos(math.pi * k / 5))
    x0 = cx - (5 * tam + 4 * hueco) / 2
    out = ''
    for i in range(5):
        ex = x0 + i * (tam + hueco) + tam / 2
        d = 'M' + 'L'.join(f'{a:.1f} {b:.1f}' for a, b in (pt(ex, j, tam / 2 if j % 2 == 0 else tam / 4.6) for j in range(10))) + 'Z'
        vol = ''.join(f'<path d="{d}" fill="#8A5A00" transform="translate({k * .45:.1f} {k * .85:.1f})"/>' for k in range(7, 0, -1))
        out += (f'<g transform="rotate({(i - 2) * 5} {ex} {y})"><g filter="url(#sombra)">{vol}</g>'
                f'<path d="{d}" fill="#5A3A00" stroke="#5A3A00" stroke-width="6" stroke-linejoin="round"/>'
                f'<g filter="url(#terciopelo)"><path d="{d}" fill="url(#gOro)"/></g></g>')
    return out


BL = ('url(#gBlanco)', '#5B2E12', '#3A1C0A')
ORO = ('url(#gOro)', '#7A4E00', '#4A2E00')

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Titan;src:url(data:font/woff2;base64,{b64('fuente/titan-one-latin.woff2')})}}
@font-face{{font-family:Caveat;font-weight:700;src:url(data:font/woff2;base64,{b64('fuente/caveat-latin.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
/* la pared del restaurante: noche calida, mas clara donde estan las lamparas */
body{{background:radial-gradient(ellipse 90% 55% at 50% 30%,#4A2A18 0%,#2A170E 45%,#120A08 80%,#06080E 100%)}}
.abs{{position:absolute}}
/* la mesa de madera, desenfocada */
.mesa{{position:absolute;left:-40px;right:-40px;top:1330px;bottom:0;
  background:
    repeating-linear-gradient(178deg,rgba(0,0,0,0) 0 26px,rgba(0,0,0,.10) 26px 30px,rgba(255,200,140,.05) 30px 44px),
    linear-gradient(180deg,#7A4A2A 0%,#5E3720 30%,#3A2214 100%);
  filter:blur(3px);box-shadow:0 -30px 60px rgba(0,0,0,.45)}}
.mesa::before{{content:"";position:absolute;left:0;right:0;top:0;height:16px;background:linear-gradient(180deg,rgba(255,210,150,.35),transparent)}}
.grano{{position:absolute;inset:0;pointer-events:none;opacity:.35;mix-blend-mode:overlay;
  background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='r'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .55 0'/></filter><rect width='300' height='300' filter='url(%23r)'/></svg>")}}
.vineta{{position:absolute;inset:0;background:radial-gradient(ellipse 80% 70% at 50% 45%,transparent 55%,rgba(0,0,0,.55) 100%)}}
.foco{{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,220,140,.30) 0%,rgba(255,200,110,.10) 40%,transparent 70%)}}
.bicho{{position:absolute}}
.bicho img{{display:block;width:100%;filter:drop-shadow(0 24px 22px rgba(0,0,0,.55))}}
.sub{{position:absolute;left:0;right:0;text-align:center;font:700 64px Caveat;color:#FFF3DC;
  text-shadow:0 3px 0 #3A1C0A,0 8px 18px rgba(0,0,0,.6)}}
</style></head><body>
{LUCES}
<div class="mesa"></div>
<div class="foco" style="left:430px;top:780px;width:620px;height:620px"></div>

<!-- la placa, de pie sobre la mesa, un poco girada -->
<div class="abs" style="left:560px;top:880px;width:430px;height:430px;transform:rotate(7deg);filter:drop-shadow(0 34px 30px rgba(0,0,0,.6))">
  {''.join(f'<div style="position:absolute;inset:0;border-radius:4.2%;transform:translateY({i}px);background:rgba({200 + 2 * i},{214 + i},{214 + i},.98)"></div>' for i in range(12, 0, -1))}
  <img src="{PLACA}" style="position:absolute;inset:0;width:100%;height:100%;border-radius:4.2%">
  <div style="position:absolute;inset:0;border-radius:4.2%;background:linear-gradient(125deg,rgba(255,255,255,.28) 0%,transparent 35%,transparent 70%,rgba(255,255,255,.10) 100%)"></div>
</div>
<!-- su sombra en la mesa -->
<div class="abs" style="left:570px;top:1318px;width:440px;height:40px;border-radius:50%;background:rgba(0,0,0,.45);filter:blur(12px)"></div>

<!-- Estrellita senalando la placa -->
<div class="bicho" style="left:20px;top:800px;width:620px;transform:rotate(-4deg)"><img src="{BICHO}"></div>

<svg class="abs" style="left:0;top:0" width="{W}" height="{H}">{DEFS}
{titulo('¡MIRA LO', 540, 470, 190, *BL, -3)}
{titulo('QUE TE', 540, 640, 170, *BL, 2)}
{titulo('TRAIGO!', 540, 830, 210, *ORO, -2)}
{estrellas(540, 1575, 84)}
</svg>
<div class="sub" style="top:1625px">tu placa de reseñas de Google</div>
<div class="vineta"></div>
<div class="grano"></div>
</body></html>'''
open(P + 'portada.html', 'w').write(html)
print('portada.html')
