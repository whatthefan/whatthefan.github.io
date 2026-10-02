"""Publicacion "notificaciones" (1080x1350, se exporta a 2160x2700), al estilo de la
referencia de las hamburguesas: dos fotos de producto, una arriba y otra abajo, y en
medio un titulo y tres notificaciones del movil (resenas de Google e Instagram).

  arriba: la placa sobre la mesa de marmol (la foto de Flow, recortada: sin el cafe,
          el azucar ni la cuchara)
  abajo:  el expositor de pie en la cornisa al sol (la foto de verdad, ya con el
          diseno pegado: ../producto-real/pegar.py) y, a un lado, unas tarjetas de
          mano abiertas en abanico en el suelo, en perspectiva y con su sombra

El titulo va en 3D, como las letras del OYEEEE: cara blanca, volumen verde de la
marca, filo, sombra y un moteado fino.

Desde la raiz del repo:  python3 marketing/instagram/notificaciones/construir.py
y despues:               node marketing/instagram/notificaciones/hacer-png.js
"""
import base64

N = 'marketing/instagram/notificaciones/'
P = 'marketing/instagram/producto-real/'
b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
MARMOL = 'data:image/jpeg;base64,' + b64(P + 'fotos/placa-marmol.jpg')                  # 1438x2576
STAND = 'data:image/jpeg;base64,' + b64(P + 'fotos/editada-expositor-cornisa.jpg')      # 2576x1932
TARJ = 'data:image/png;base64,' + b64(P + 'disenos/tarjeta.png')                         # 1600x1016
W, H = 1080, 1350

KM = W / 1438                    # la foto del marmol, a lo ancho
PLACA_Y = 170                    # donde empieza la placa (en la foto esta en y=702)
KS, SX = .43, -14                # la del expositor: escala y desplazamiento
STAND_T = 780                    # donde empieza la foto del expositor
AVISOS_Y = 600

# ── el titulo en 3D ──
def titulo(lineas, y0, tam):
    capas = 12
    out = ''
    for n, t in enumerate(lineas):
        y = y0 + n * tam * 1.05
        txt = lambda fill, extra='': (f'<text x="540" y="{y:.0f}" text-anchor="middle" font-family="Mont" font-weight="800" '
                                      f'font-size="{tam}" letter-spacing="-1.5" fill="{fill}" {extra}>{t}</text>')
        out += ''.join(f'<g transform="translate({i * .45:.1f} {i * .7:.1f})">{txt("#123A2A")}</g>' for i in range(capas, 0, -1))
        out += txt('#FFFFFF', 'stroke="#0C2A1E" stroke-width="2.5" paint-order="stroke"')
        out += f'<g filter="url(#moteado)">{txt("#FFFFFF")}</g>'
    return (f'''<svg class="abs" style="left:0;top:0" width="{W}" height="400"><defs>
<filter id="sombra" x="-10%" y="-30%" width="120%" height="180%"><feDropShadow dx="4" dy="16" stdDeviation="12" flood-color="#0b1a12" flood-opacity=".45"/></filter>
<filter id="moteado"><feTurbulence type="fractalNoise" baseFrequency="1.3" numOctaves="2" seed="7"/>
  <feColorMatrix values="0 0 0 0 .55  0 0 0 0 .5  0 0 0 0 .42  0 0 0 -1.7 1.1"/><feComposite in2="SourceGraphic" operator="in"/>
  <feComponentTransfer><feFuncA type="linear" slope=".35"/></feComponentTransfer></filter></defs>
<g filter="url(#sombra)">{out}</g></svg>''')


# ── los logos, en vector ──
G = '''<svg viewBox="0 0 48 48" width="40" height="40"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
<path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
<path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
<path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>'''
ICO_G = f'<div class="ico" style="background:#fff">{G}</div>'
ICO_IG = ('<div class="ico" style="background:radial-gradient(circle at 30% 107%,#fdf497 0%,#fdf497 5%,#fd5949 45%,#d6249f 60%,#285AEB 90%)">'
          '<svg viewBox="0 0 24 24" width="38" height="38"><rect x="2.8" y="2.8" width="18.4" height="18.4" rx="5.6" fill="none" stroke="#fff" stroke-width="2"/>'
          '<circle cx="12" cy="12" r="4.3" fill="none" stroke="#fff" stroke-width="2"/><circle cx="17.4" cy="6.6" r="1.25" fill="#fff"/></svg></div>')
EST = '<span class="est">★★★★★</span>'


def aviso(ico, app, cuando, titulo_, cuerpo):
    return f'''<div class="aviso">{ico}<div class="txt">
  <div class="cab"><b>{titulo_}</b><span>{cuando}</span></div><div class="cuerpo">{cuerpo}</div></div></div>'''


# ── las tarjetas en el suelo, en perspectiva ──
TW, TH = 300, 190
ABANICO = ''.join(
    f'<div class="tarjeta" style="left:{-TW / 2 + dx}px;top:{-TH / 2 + dy}px;transform:rotate({g}deg)"><img src="{TARJ}"><div class="brillo"></div></div>'
    for g, dx, dy in ((-38, -40, 30), (-19, -18, 8), (0, 0, 0), (19, 18, 8), (38, 40, 30)))

FOTOS_A = f'''<!-- arriba: la placa en el marmol -->
<div class="panel" style="top:0;height:{STAND_T + 100}px">
  <img class="abs" src="{MARMOL}" style="left:0;top:{PLACA_Y - 702 * KM:.0f}px;width:{W}px;filter:contrast(1.04) saturate(1.05)">
</div>
<!-- abajo: el expositor al sol, fundido por arriba con la de la placa -->
<div class="panel" style="top:{STAND_T}px;height:{H - STAND_T}px;-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 100px)">
  <img class="abs" src="{STAND}" style="left:{SX}px;top:-44px;width:{2576 * KS:.0f}px;filter:contrast(1.04) saturate(1.08)">
</div>
<div class="suelo">{ABANICO}</div>
'''
# la version B, al reves: el expositor arriba (grande, al sol) y la placa abajo en el marmol,
# con las tarjetas en abanico encima del marmol, a la derecha
FOTOS_B = f'''<img class="abs" src="{MARMOL}" style="left:0;top:-300px;width:{W}px;filter:blur(3px) brightness(1.05)">
<div class="panel" style="top:0;height:880px;-webkit-mask-image:linear-gradient(180deg,transparent 60px,#000 190px)">
  <img class="abs" src="{STAND}" style="left:-192px;top:70px;width:{2576 * .6:.0f}px;filter:contrast(1.04) saturate(1.08)">
</div>
<div class="panel" style="top:780px;height:{H - 780}px;-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 100px)">
  <img class="abs" src="{MARMOL}" style="left:0;top:{880 - 780 - 545 * KM:.0f}px;width:{W}px;filter:contrast(1.04) saturate(1.05)">
</div>
<div class="suelo" style="left:130px;top:1290px;transform:perspective(900px) rotateX(58deg) rotateZ(-20deg) scale(.85)">{ABANICO}</div>'''
for VAR, FOTOS in (('', FOTOS_A), ('-b', FOTOS_B)):
  html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Mont;font-weight:100 900;src:url(data:font/woff2;base64,{b64('fuente/montserrat-latin.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;font-family:Mont,sans-serif;background:#ddd6cc}}
.abs{{position:absolute}}
.panel{{position:absolute;left:0;width:{W}px;overflow:hidden}}
/* las tarjetas: un plano tumbado en el suelo, y encima el abanico */
.suelo{{position:absolute;left:150px;top:1250px;width:0;height:0;transform-style:preserve-3d;
  transform:perspective(900px) rotateX(64deg) rotateZ(-18deg)}}
.tarjeta{{position:absolute;width:{TW}px;height:{TH}px;border-radius:14px;transform-origin:50% 160%;
  box-shadow:0 1px 0 rgba(255,255,255,.6) inset, 0 6px 5px rgba(40,30,20,.45), 0 24px 30px rgba(40,30,20,.35)}}
.tarjeta img{{width:100%;height:100%;border-radius:14px;display:block}}
.tarjeta .brillo{{position:absolute;inset:0;border-radius:14px;background:linear-gradient(125deg,rgba(255,255,255,0) 30%,rgba(255,255,255,.35) 42%,rgba(255,255,255,0) 55%)}}
/* las notificaciones, como las del iPhone: cristal oscuro con desenfoque */
.avisos{{position:absolute;left:110px;right:110px;top:{AVISOS_Y}px;display:flex;flex-direction:column;gap:14px}}
.aviso{{display:flex;align-items:center;gap:20px;padding:18px 24px 18px 18px;border-radius:32px;
  background:rgba(30,30,32,.72);backdrop-filter:blur(26px) saturate(1.7);-webkit-backdrop-filter:blur(26px) saturate(1.7);
  box-shadow:0 1px 0 rgba(255,255,255,.12) inset,0 22px 44px rgba(0,0,0,.32);color:#fff}}
.ico{{flex:none;width:64px;height:64px;border-radius:15px;display:flex;align-items:center;justify-content:center;
  box-shadow:0 0 0 1px rgba(0,0,0,.08)}}
.txt{{flex:1;min-width:0}}
.cab{{display:flex;justify-content:space-between;align-items:baseline;font-size:25px;line-height:1.2}}
.cab b{{font-weight:700}}
.cab span{{font-weight:500;font-size:21px;color:rgba(235,235,245,.6)}}
.cuerpo{{margin-top:3px;font-weight:500;font-size:23px;line-height:1.3;color:rgba(255,255,255,.92)}}
.est{{color:#FFC93C;letter-spacing:1px}}
.grano{{position:absolute;inset:0;opacity:.3;mix-blend-mode:overlay;pointer-events:none;
  background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='r'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .5 0'/></filter><rect width='300' height='300' filter='url(%23r)'/></svg>")}}
</style></head><body>
{FOTOS}
{titulo(['Las únicas notificaciones', 'que quiero ver:'], 88, 58)}
<div class="avisos">
  {aviso(ICO_G, 'Google', 'ahora', 'Google Maps · Nueva reseña', f'{EST} «¡Trato de diez! Volveremos.»')}
  {aviso(ICO_IG, 'Instagram', 'hace 2 min', 'lucia.gr', 'Te ha mencionado en su historia: «el mejor desayuno de Córdoba»')}
  {aviso(ICO_G, 'Google', 'hace 5 min', 'Google Maps · Nueva reseña', f'{EST} «Nos lo dijo la placa de la mesa.»')}
</div>
<div class="grano"></div>
</body></html>'''
  open(N + f'notificaciones{VAR}.html', 'w').write(html)
  print(f'notificaciones{VAR}.html')
