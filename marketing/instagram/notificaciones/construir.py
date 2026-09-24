"""Publicacion "notificaciones" (1080x1350), al estilo de la referencia de las
hamburguesas: dos fotos de producto, una arriba y otra abajo, y en medio un titulo y
tres notificaciones del movil. Aqui son resenas de Google e Instagram.

  arriba: la placa sobre la mesa de marmol (la foto de Flow, recortada: sin el cafe,
          el azucar ni la cuchara)
  abajo:  un abanico de tarjetas de mano sobre el mismo marmol (el trozo de mesa de
          arriba de esa foto), con sus sombras y el brillo del plastico

Desde la raiz del repo:  python3 marketing/instagram/notificaciones/construir.py
y despues:               node marketing/instagram/notificaciones/hacer-png.js
"""
import base64
import os

N = 'marketing/instagram/notificaciones/'
P = 'marketing/instagram/producto-real/'
b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
FOTO = 'data:image/jpeg;base64,' + b64(P + 'fotos/placa-marmol.jpg')          # 1438x2576
TARJ = 'data:image/png;base64,' + b64(P + 'disenos/tarjeta.png')               # 1600x1016
W, H = 1080, 1350
K = W / 1438                     # la foto a lo ancho de la publicacion
CORTE = 900                      # donde acaba la foto de arriba y empieza la de abajo

# el abanico: cinco tarjetas giradas alrededor de un punto de abajo, como una mano de cartas
TW, TH = 420, 267
ABANICO = ''.join(
    f'''<div class="tarjeta" style="left:{540 - TW / 2 + dx}px;top:{1075 + dy}px;transform:rotate({g}deg)">
  <img src="{TARJ}"><div class="brillo"></div></div>'''
    for g, dx, dy in ((-28, -170, 60), (28, 170, 60), (-14, -88, 18), (14, 88, 18), (0, 0, 0)))   # la del centro, encima

G = f'<div class="ico" style="background:#fff url({TARJ}) no-repeat;background-size:1060px 673px;background-position:-743px -123px"></div>'
IG = ('<div class="ico" style="background:radial-gradient(circle at 30% 107%,#fdf497 0%,#fdf497 5%,#fd5949 45%,#d6249f 60%,#285AEB 90%)">'
      '<svg viewBox="0 0 24 24" width="46" height="46" style="margin:15px"><rect x="3" y="3" width="18" height="18" rx="5.5" fill="none" stroke="#fff" stroke-width="2.2"/>'
      '<circle cx="12" cy="12" r="4.2" fill="none" stroke="#fff" stroke-width="2.2"/><circle cx="17.3" cy="6.7" r="1.3" fill="#fff"/></svg></div>')
ESTR = '<span class="est">★★★★★</span>'


def aviso(ico, app, texto):
    return f'''<div class="aviso">{ico}<div class="txt"><div class="app">{app}<span>Ahora</span></div>{texto}</div></div>'''


html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Mont;font-weight:100 900;src:url(data:font/woff2;base64,{b64('fuente/montserrat-latin.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;font-family:Mont,sans-serif;background:#e9e6e1}}
.abs{{position:absolute}}
.panel{{position:absolute;left:0;width:{W}px;overflow:hidden}}
.panel img.f{{position:absolute;left:0;width:{W}px}}
.tarjeta{{position:absolute;width:{TW}px;height:{TH}px;transform-origin:50% 230%;border-radius:18px;
  filter:drop-shadow(0 3px 3px rgba(60,40,20,.35)) drop-shadow(0 18px 26px rgba(60,40,20,.28))}}
.tarjeta img{{width:100%;height:100%;border-radius:22px;display:block}}
.tarjeta .brillo{{position:absolute;inset:0;border-radius:22px;background:linear-gradient(115deg,rgba(255,255,255,0) 35%,rgba(255,255,255,.28) 45%,rgba(255,255,255,0) 58%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.7)}}
h1{{position:absolute;left:0;right:0;top:40px;text-align:center;font-weight:800;font-size:56px;line-height:1.06;letter-spacing:-.02em;color:#161616}}
.avisos{{position:absolute;left:130px;right:130px;top:{CORTE - 170}px;display:flex;flex-direction:column;gap:14px}}
.aviso{{display:flex;align-items:center;gap:20px;padding:16px 24px;border-radius:30px;background:rgba(34,34,36,.92);color:#fff;
  box-shadow:0 18px 40px rgba(0,0,0,.28);backdrop-filter:blur(10px)}}
.ico{{flex:none;width:68px;height:68px;border-radius:16px;overflow:hidden}}
.txt{{flex:1;font-weight:500;font-size:24px;line-height:1.28}}
.app{{display:flex;justify-content:space-between;font-weight:700;font-size:23px;color:#fff;margin-bottom:4px}}
.app span{{font-weight:500;color:#9a9aa0}}
.est{{color:#F6C343;letter-spacing:2px;font-size:25px}}
</style></head><body>
<div class="panel" style="top:0;height:{CORTE}px">
  <img class="f" src="{FOTO}" style="top:{195 - 702 * K:.0f}px">
</div>
<div class="panel" style="top:{CORTE - 160}px;height:{H - CORTE + 160}px;-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 160px)">
  <img class="f" src="{FOTO}" style="left:{-400 * 1.04:.0f}px;top:{-150 * 1.04 - 160:.0f}px;width:{1438 * 1.04:.0f}px;filter:brightness(1.06) sepia(.06)">
</div>
<div class="panel" style="top:0;height:{H}px">{ABANICO}
</div>
<h1>Las únicas notificaciones<br>que quiero ver:</h1>
<div class="avisos">
  {aviso(G, 'Google', f'Nueva reseña {ESTR}<br>«¡Trato de diez! Volveremos.»')}
  {aviso(IG, 'Instagram', '@lucia.gr te ha mencionado en su historia:<br>«el mejor desayuno de Córdoba»')}
  {aviso(G, 'Google', f'Nueva reseña {ESTR}<br>«Nos lo dijo la placa de la mesa.»')}
</div>
</body></html>'''
open(N + 'notificaciones.html', 'w').write(html)
print('notificaciones.html')
