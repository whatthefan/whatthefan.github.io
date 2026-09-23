"""Los carteles de PLEA5E (el diseno plano, listo para imprimir o para
ponerlo en una escena). Estilo de la referencia de BRUTO: fondo claro,
letra negra muy gruesa arriba y abajo, el producto en medio como foto de
producto, una linea de "ingredientes" y una firma pequena.

Saca carteles/NOMBRE.html; hacer-png.js les hace la foto (a 2x).
La placa es la de ejemplo (Bar La Plaza, INVENTADO) del carrusel.

Desde la raiz del repo:  python3 marketing/instagram/carteles/carteles.py
"""
import base64
import re

C = 'marketing/instagram/carteles/'
b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
PLACA = 'data:image/png;base64,' + b64('marketing/instagram/carrusel-placa/capas/paso5-nfc.png')
ico = open('public/icono.svg').read()
STAR = re.search(r'<path fill="#E9BC46" d="([^"]+)"', ico).group(1)
FIVE = re.search(r'<path fill="#0A0E16" transform="[^"]+" d="([^"]+)"', ico).group(1)


def sello(tam, estrella='#E9BC46', cinco='#06080E'):
    return (f'<svg viewBox="0 0 1024 900" width="{tam}" height="{tam * .88:.0f}"><path fill="{estrella}" d="{STAR}"/>'
            f'<path fill="{cinco}" transform="translate(407.2 677.2) scale(.42)" d="{FIVE}"/></svg>')


CSS = f'''
@font-face{{font-family:Mont;font-weight:100 900;src:url(data:font/woff2;base64,{b64('fuente/montserrat-latin.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:Mont,sans-serif;overflow:hidden}}
.c{{position:relative;overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.ref{{font-weight:600;letter-spacing:.06em}}
.gordo{{font-weight:900;letter-spacing:-.035em;line-height:.9;text-align:center;white-space:nowrap}}
.linea{{font-weight:700;letter-spacing:.02em;white-space:nowrap}}
.firma{{font-weight:800;letter-spacing:.04em}}
'''


def placa_foto(lado, giro_x=24, giro_z=-8, sombra='rgba(20,15,5,.45)'):
    """la placa como foto de producto: tumbada un poco hacia atras, con su canto
    de metacrilato de 4 mm y la sombra en el suelo"""
    canto = ''.join(f'<div style="position:absolute;inset:0;border-radius:4.2%;transform:translateZ(-{i * 1.6:.1f}px);'
                    f'background:rgba({205 + 2 * i},{222 + i},{220 + i},.97);border:1px solid rgba(255,255,255,.4)"></div>'
                    for i in range(14, 0, -1))
    return f'''<div style="position:relative;width:{lado}px;height:{lado}px;perspective:{lado * 3}px">
  <div style="position:absolute;left:6%;right:6%;bottom:-5%;height:22%;border-radius:50%;background:{sombra};filter:blur({lado * .05:.0f}px)"></div>
  <div style="position:absolute;inset:0;transform-style:preserve-3d;transform:rotateX({giro_x}deg) rotateZ({giro_z}deg)">
    {canto}
    <img src="{PLACA}" style="position:absolute;inset:0;width:100%;height:100%;border-radius:4.2%">
    <div style="position:absolute;inset:0;border-radius:4.2%;background:linear-gradient(118deg,transparent 22%,rgba(255,255,255,.28) 30%,transparent 40%,transparent 64%,rgba(255,255,255,.12) 70%,transparent 76%);
      box-shadow:inset 0 3px 0 rgba(255,255,255,.7)"></div>
  </div></div>'''


def cartel(nombre, ancho, alto, cuerpo, fondo):
    open(f'{C}{nombre}.html', 'w').write(f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
html,body{{width:{ancho}px;height:{alto}px}}</style></head><body>
<div class="c" style="width:{ancho}px;height:{alto}px;background:{fondo}">{cuerpo}</div></body></html>''')


# 1. La lona de fachada (2:3). "QUE HABLEN · [la placa] · DE TU BAR"
cartel('lona-que-hablen', 1600, 2400, f'''
<div class="ref" style="font-size:44px;color:#1a1a1a">PL-005 / NFC + QR</div>
<div class="gordo" style="margin-top:50px;font-size:208px;color:#0b0b0b">QUE HABLEN</div>
<div style="margin-top:90px">{placa_foto(860, 16, -5)}</div>
<div style="display:flex;align-items:center;gap:26px;margin-top:80px">{sello(100)}
  <span class="gordo" style="font-size:120px;color:#0b0b0b;letter-spacing:-.02em">PLEA5E</span><sup style="font-weight:800;font-size:40px;align-self:flex-start;margin-top:6px">®</sup></div>
<div class="gordo" style="margin-top:40px;font-size:208px;color:#0b0b0b">DE TU BAR</div>
<div class="linea" style="margin-top:80px;font-size:36px;color:#1a1a1a">NFC // QR // GOOGLE // 5 ESTRELLAS // 10 SEGUNDOS // SIN APPS</div>
<div class="firma" style="margin-top:44px;font-size:40px;color:#1a1a1a">HECHO PARA QUE TE VALOREN.</div>
''', 'linear-gradient(180deg,#F6F3EC,#EFEBE2)')

# 2. El mupi de la parada (1:1,47, va retroiluminado). Fondo crema (de noche brilla), letra negra y oro.
cartel('mupi-te-buscan', 1200, 1760, f'''
<div class="ref" style="font-size:34px;color:#5A6272">PL-005 / RESEÑAS EN GOOGLE</div>
<div class="gordo" style="margin-top:34px;font-size:102px;color:#0b0b0b">ANTES DE ENTRAR,</div>
<div class="gordo" style="margin-top:8px;font-size:132px;color:#B8871F">TE BUSCAN.</div>
<div style="margin-top:70px">{placa_foto(640, 14, 5)}</div>
<div class="gordo" style="margin-top:70px;font-size:62px;color:#0b0b0b;letter-spacing:-.02em">QUE LO QUE LEAN SEA BUENO.</div>
<div class="linea" style="margin-top:48px;font-size:28px;color:#3a3f4a">TOCA // ESCANEA // 5 ESTRELLAS // 10 SEGUNDOS</div>
<div style="display:flex;align-items:center;gap:18px;margin-top:50px">{sello(70)}
  <span class="gordo" style="font-size:64px;color:#0b0b0b;letter-spacing:-.01em">PLEA5E</span>
  <span class="firma" style="font-size:28px;color:#3a3f4a;margin-left:14px">plea5e.es</span></div>
''', 'linear-gradient(180deg,#F7F3EB,#EEE8DC)')

# 3. El ticket de caja del bar (papel termico, 80 mm): al final, la llamada a la placa.
# Bar, direccion y precios son INVENTADOS, como la placa de ejemplo.
T = lambda a, b='': f'<div style="display:flex;justify-content:space-between"><span>{a}</span><span>{b}</span></div>'
cartel('ticket-bar', 600, 1180, f'''
<div style="width:100%;height:100%;padding:70px 48px;font-family:'Liberation Mono','DejaVu Sans Mono',monospace;font-size:27px;line-height:1.45;color:#2a2a2a">
<div style="text-align:center;font-weight:700;font-size:40px;letter-spacing:.06em">BAR LA PLAZA</div>
<div style="text-align:center">Tapas · Cañas · Terraza</div>
<div style="text-align:center">Pza. de la Corredera · Córdoba</div>
<div style="margin:22px 0;border-top:3px dashed #555"></div>
{T('Mesa 4', '23/09  21:14')}
<div style="margin:22px 0;border-top:3px dashed #555"></div>
{T('2 CAÑA', '4,00')}{T('1 TINTO VERANO', '2,80')}{T('1 SALMOREJO', '6,50')}{T('1 FLAMENQUÍN', '9,00')}
<div style="margin:22px 0;border-top:3px dashed #555"></div>
<div style="font-weight:700;font-size:36px">{T('TOTAL', '22,30 €')}</div>
<div>IVA incluido</div>
<div style="margin:22px 0;border-top:3px dashed #555"></div>
<div style="text-align:center;font-weight:700;font-size:32px">¿Qué tal todo?</div>
<div style="text-align:center;margin-top:10px">Si te hemos tratado bien,<br>acerca el móvil a la placa<br>de la mesa. Son 10 segundos.</div>
<div style="text-align:center;font-size:52px;letter-spacing:.2em;margin-top:14px">★★★★★</div>
<div style="text-align:center;margin-top:18px">¡Gracias por venir!</div>
<div style="margin:22px 0;border-top:3px dashed #555"></div>
<div style="text-align:center;font-size:22px">Reseñas con PLEA5E · plea5e.es</div>
</div>''', '#F4F2EE')

# 4. La ultima foto del carrusel "en todas partes": el producto de verdad y el gancho.
# Antes van las fotos de ambientes (nubes, moneda, arena...: ver PROMPTS.md).
cartel('final-producto', 1080, 1350, f'''
<div class="firma" style="font-size:40px;color:#F4EDE0;letter-spacing:.02em;text-align:center;line-height:1.25">NO HACE FALTA<br>ESCRIBIRLO EN EL CIELO.</div>
<div class="gordo" style="margin-top:22px;font-size:84px;color:#E9BC46;letter-spacing:-.02em;line-height:1">BASTA CON UNA</div>
<div class="gordo" style="font-size:84px;color:#E9BC46;letter-spacing:-.02em;line-height:1.05">PLACA EN LA MESA.</div>
<div style="margin-top:46px">{placa_foto(600, 18, -6, 'rgba(0,0,0,.75)')}</div>
<div class="linea" style="margin-top:50px;font-size:30px;color:#C9CEDA;white-space:normal;text-align:center;line-height:1.35;font-weight:600">
  Tu cliente acerca el móvil y te deja la reseña en 10 segundos.<br>Toca o escanea. Sin apps.</div>
<div style="margin-top:40px;display:flex;align-items:center;gap:26px">
  <div style="background:#E9BC46;color:#06080E;font-weight:900;font-size:42px;padding:20px 44px;border-radius:60px">Comenta PLACA</div>
  <div style="display:flex;align-items:center;gap:12px">{sello(52)}<span class="firma" style="font-size:30px;color:#F4EDE0">plea5e.es</span></div></div>
''', 'radial-gradient(ellipse 75% 55% at 50% 52%,#1A2130 0%,#0B0F18 60%,#06080E 100%)')

print('carteles hechos')
