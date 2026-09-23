"""Video "Piedra, papel... ¡reseñas!" (9,5 s, 1080x1920): el juego de
toda la vida, pero la tijera se tacha y la jugada que gana es la mano con
el movil tocando la placa. Monta video/escena.html; lo graban
video/grabar.js (imagen) y video/musica.py (sonido).

Desde la raiz del repo:
    python3 marketing/instagram/piedra-papel-resenas/video.py
    python3 marketing/instagram/piedra-papel-resenas/video/musica.py
    FFMPEG=ffmpeg node marketing/instagram/piedra-papel-resenas/video/grabar.js
"""
import base64
import os
import re
import sys

sys.path.insert(0, 'marketing/instagram/piedra-papel-resenas')
P = 'marketing/instagram/piedra-papel-resenas/'
# lo mismo que usan las fotos del carrusel: manos, estrella, placa, letras
fuente = open(P + 'construir.py').read().split("CSS = f'''")[0]
exec(fuente)                                           # mano(), ESTRELLA, PLACA, b64, svg_uri
tijera = svg_uri(open(P + 'manos/tijera.svg').read())

ESTRELLAS = ''.join(f'<img class="est" id="e{i}" src="{ESTRELLA}" style="left:{x}px;top:{y}px;width:{w}px">'
                    for i, (x, y, w) in enumerate(((120, 700, 130), (290, 620, 150), (465, 590, 160), (645, 620, 150), (830, 700, 130))))
CANTO = ''.join(f'<div style="position:absolute;inset:0;border-radius:4.2%;transform:translateY({i}px);'
                f'background:rgba({200 + 3 * i},{215 + 2 * i},{212 + 2 * i},.95);border:1px solid rgba(255,255,255,.3)"></div>'
                for i in range(10, 0, -1))

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Mont;font-weight:100 900;src:url(data:font/woff2;base64,{b64('fuente/montserrat-latin.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;font-family:Mont,sans-serif;
  background:radial-gradient(ellipse 80% 60% at 50% 45%,#E7DAC8 0%,#DCCBB4 60%,#CDBBA2 100%)}}
.abs{{position:absolute}}
.palabra{{position:absolute;left:0;right:0;top:380px;text-align:center;font-weight:800;font-size:190px;letter-spacing:-3px;color:#8A6534}}
.mano{{position:absolute;filter:drop-shadow(0 40px 44px rgba(90,60,30,.3))}}
.est{{position:absolute;filter:drop-shadow(0 12px 14px rgba(120,80,20,.35))}}
.frase{{position:absolute;left:0;right:0;text-align:center;font-weight:700;font-size:58px;color:#6E5130}}
.frase b{{color:#8A6534;font-weight:800}}
</style></head><body>
<div class="frase" id="jugamos" style="top:220px;font-size:46px;letter-spacing:6px;font-weight:800;color:#A58E6E">¿JUGAMOS?</div>
<div class="palabra" id="w0">Piedra</div>
<div class="palabra" id="w1">Papel</div>
<div class="palabra" id="w2">¿Tijera?</div>
<div class="palabra" id="w3" style="font-size:176px">¡Reseñas!</div>
<img class="mano" id="h0" src="{mano('piedra')[0]}" style="left:240px;top:760px;width:600px">
<img class="mano" id="h1" src="{mano('papel')[0]}" style="left:230px;top:740px;width:620px">
<img class="mano" id="h2" src="{tijera}" style="left:240px;top:720px;width:600px">
<svg class="abs" id="equis" style="left:190px;top:700px" width="700" height="700" viewBox="0 0 100 100">
  <path id="x1" d="M14 14 L86 86" stroke="#D9383F" stroke-width="11" stroke-linecap="round" fill="none" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
  <path id="x2" d="M86 14 L14 86" stroke="#D9383F" stroke-width="11" stroke-linecap="round" fill="none" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>
<div class="abs" id="placa" style="left:60px;top:870px;width:560px;height:560px;filter:drop-shadow(0 34px 34px rgba(90,60,30,.35))">{CANTO}
  <img src="{PLACA}" style="position:absolute;inset:0;width:100%;height:100%;border-radius:4.2%">
  <div style="position:absolute;inset:0;border-radius:4.2%;background:linear-gradient(118deg,transparent 25%,rgba(255,255,255,.18) 32%,transparent 42%)"></div></div>
<svg class="abs" id="ondas" style="left:600px;top:970px" width="150" height="240" viewBox="0 0 130 200">
  <path id="o1" d="M18 70 a45 45 0 0 1 0 60" fill="none" stroke="#B98B2E" stroke-width="11" stroke-linecap="round"/>
  <path id="o2" d="M52 45 a80 80 0 0 1 0 110" fill="none" stroke="#B98B2E" stroke-width="11" stroke-linecap="round"/>
  <path id="o3" d="M88 20 a115 115 0 0 1 0 160" fill="none" stroke="#B98B2E" stroke-width="11" stroke-linecap="round"/></svg>
<img class="mano" id="h3" src="{mano('resenas')[0]}" style="left:450px;top:800px;width:640px">
{ESTRELLAS}
<div class="frase" id="gana" style="top:1545px">…y esta <b>gana siempre</b></div>
<div class="abs" id="cta" style="left:140px;top:1560px;width:800px;padding:22px 0;border-radius:60px;background:#8A6534;color:#F7F1E3;text-align:center;font-weight:800;font-size:46px">Comenta <span style="color:#F2C95B">PLACA</span> · plea5e.es</div>
<script>
const $ = id => document.getElementById(id);
const cl = x => Math.min(1, Math.max(0, x));
const p = (t, a, b) => cl((t - a) / (b - a));
const out = x => 1 - Math.pow(1 - x, 3);
const back = x => {{ const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); }};
function T(el, o) {{ el = $(el); el.style.transform = `translate(${{o.x || 0}}px,${{o.y || 0}}px) scale(${{o.s ?? 1}}) rotate(${{o.r || 0}}deg)`; el.style.opacity = o.o ?? 1; }}
function pop(el, t, a, z, dy = 60) {{
  const i = back(p(t, a, a + .3)), f = z ? p(t, z, z + .15) : 0;
  T(el, {{ y: (1 - i) * dy, s: .6 + .4 * i + .1 * f, o: cl(p(t, a, a + .12)) * (1 - f) }});
}}
// cada mano: aparece de un golpe (baja y rebota, como al jugar) y se va
function golpe(el, t, a, z) {{
  const b = p(t, a - .18, a), r = back(p(t, a, a + .3)), f = z ? p(t, z, z + .15) : 0;
  const alto = b < 1 ? -180 * Math.sin(Math.PI * b * .5 + Math.PI * .5) : 0;
  T(el, {{ y: alto + (1 - r) * 30, s: (.9 + .1 * r) * (1 - .15 * f), r: -6 * (1 - r), o: cl(p(t, a - .18, a - .08)) * (1 - f) }});
}}
function render(t) {{
  pop('jugamos', t, .05, 3.5);
  pop('w0', t, .3, 1.15); golpe('h0', t, .3, 1.15);
  pop('w1', t, 1.3, 2.15); golpe('h1', t, 1.3, 2.15);
  pop('w2', t, 2.3, 3.45); golpe('h2', t, 2.3, 3.45);
  $('x1').style.strokeDashoffset = 1 - out(p(t, 2.85, 3.0)); $('x2').style.strokeDashoffset = 1 - out(p(t, 3.0, 3.15));
  $('equis').style.opacity = 1 - p(t, 3.45, 3.6);
  pop('w3', t, 3.6, null, 80);
  const pl = out(p(t, 3.65, 4.05)); T('placa', {{ x: (1 - pl) * -700, r: -6, o: pl }});
  const mv = out(p(t, 3.8, 4.25)), toca = Math.sin(Math.PI * p(t, 4.25, 4.55));
  T('h3', {{ x: (1 - mv) * 700 - 40 * toca, r: -22 - 4 * toca, o: mv }});
  const onda = t > 4.3 && t < 5.4;
  ['o1', 'o2', 'o3'].forEach((o, i) => {{ $(o).style.opacity = onda ? cl(Math.sin((t - 4.3 - i * .1) * 7)) : 0; }});
  for (let i = 0; i < 5; i++) {{
    const a = 4.55 + i * .18, e = back(p(t, a, a + .35));
    T('e' + i, {{ y: (1 - e) * 300 + 8 * Math.sin((t - a) * 5), s: .2 + .8 * e, r: (i - 2) * 8 * e, o: p(t, a, a + .1) }});
  }}
  pop('gana', t, 5.8, 7.0);
  pop('cta', t, 7.1, null, 40);
  if (t > 7.5) $('cta').style.transform += ` scale(${{1 + .03 * Math.sin((t - 7.5) * 6)}})`;
}}
window.render = render; render(0);
</script></body></html>'''
os.makedirs(P + 'video', exist_ok=True)
open(P + 'video/escena.html', 'w').write(html)
print('video/escena.html')
