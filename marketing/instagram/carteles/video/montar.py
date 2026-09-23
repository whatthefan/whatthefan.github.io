"""La ultima del carrusel, en video (8,5 s, 1080x1350): la placa baja girando,
salen cinco estrellas talladas y "Llevas todo el carrusel pensandolo. Te toca.", se da la vuelta y por detras
esta Estrellita con el pulgar arriba ("Aqui no hay nada... Comenta PLACA"). Al volver,
Estrellita asoma la cabeza por detras de la placa, coge impulso, salta por
encima y cae de pie al lado, con el pulgar arriba, junto al "Comenta PLACA". Muy poco texto.

Desde la raiz del repo:
    python3 marketing/instagram/carteles/video/montar.py
    python3 marketing/instagram/carteles/video/musica.py
    FFMPEG=ffmpeg node marketing/instagram/carteles/video/grabar.js
"""
import base64
import math
import re

V = 'marketing/instagram/carteles/video/'
b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
svg = lambda f: 'data:image/svg+xml;base64,' + b64(f)
E = 'public/marca/estrellita/'
PLACA = 'data:image/png;base64,' + b64('marketing/instagram/carrusel-placa/capas/paso5-nfc.png')
CANTO = ''.join(f'<div class="cp" style="transform:translateZ(-{i * 2.2:.1f}px);background:rgba({208 + 2 * i},{224 + i},{222 + i},.98)"></div>'
                for i in range(1, 11))
# la placa por las dos caras (la reflejada del suelo es la misma, a la inversa)
PIEZA = f'''{CANTO}
  <div class="cara"><img src="{PLACA}" style="width:100%;height:100%;display:block">
    <div class="brillo" style="position:absolute;inset:-40%;background:linear-gradient(115deg,transparent 40%,rgba(255,255,255,.4) 48%,transparent 56%)"></div></div>
  <div class="cara detras"><img class="pegatina" src="{svg(E + 'pulgar.svg')}">
    <div class="nota">Aquí no hay nada...<br><b style="color:#B8871F">Comenta PLACA</b></div></div>'''
# el logotipo con sus brazos, pero mas cortos: las barras del centro llegan a 1900 en vez de a 2686,
# los destellos se acercan lo mismo y las rayas de los extremos miden la mitad
LOGO = open('public/marca/marca-plea5e.svg').read()
M = 786                                                             # lo que se acorta cada brazo
LOGO = LOGO.replace('<rect x="-4200.0" y="-760.0" width="998.2" height="100.5"/>', '<rect x="-2915" y="-760.0" width="500" height="100.5"/>')
LOGO = LOGO.replace('<rect x="3201.8" y="-760.0" width="998.2" height="100.5"/>', '<rect x="2415" y="-760.0" width="500" height="100.5"/>')
LOGO = re.sub(r'(<path d="M677\.5 -1259[^"]+")', lambda g: g.group(1).replace('2686.2', '1900'), LOGO)
LOGO = re.sub(r'(<path d="M-2944[^"]+"/>)', rf'<g transform="translate({M} 0)">\1</g>', LOGO)
LOGO = re.sub(r'(<path d="M2944[^"]+"/>)', rf'<g transform="translate(-{M} 0)">\1</g>', LOGO)
LOGO = LOGO.replace('viewBox="-4200 -1290 8400 1680" width="1400" height="280"', 'viewBox="-2960 -1300 5920 1520" width="1480" height="380"')
LOGO = 'data:image/svg+xml;base64,' + base64.b64encode(LOGO.encode()).decode()
def estrella_facetas(i):
    """estrella tallada: cada punta en dos caras (luz y sombra), filo oscuro y un brillo que la cruza"""
    cx, cy, R, r = 50, 52, 47, 20
    pt = lambda k, rad: (cx + rad * math.sin(math.pi * k / 5), cy - rad * math.cos(math.pi * k / 5))
    caras = ''
    for k in range(5):
        (tx, ty), (ax, ay), (bx, by) = pt(2 * k, R), pt(2 * k - 1, r), pt(2 * k + 1, r)
        caras += f'<path d="M{cx} {cy}L{ax:.1f} {ay:.1f}L{tx:.1f} {ty:.1f}Z" fill="#F7D877"/><path d="M{cx} {cy}L{tx:.1f} {ty:.1f}L{bx:.1f} {by:.1f}Z" fill="#D39A22"/>'
    silueta = 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in (pt(j, R if j % 2 == 0 else r) for j in range(10))) + 'Z'
    return (f'<svg viewBox="0 0 100 100" width="92" height="92"><defs><clipPath id="cs{i}"><path d="{silueta}"/></clipPath>'
            f'<linearGradient id="gb{i}" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".75"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
            f'<g clip-path="url(#cs{i})">{caras}<rect class="luz" x="-60" y="-10" width="40" height="120" fill="url(#gb{i})" transform="skewX(-20)"/></g>'
            f'<path d="{silueta}" fill="none" stroke="#9C6F14" stroke-width="2.4" stroke-linejoin="round"/></svg>')


CHISPA = '<svg viewBox="-10 -10 20 20" width="34" height="34"><path d="M0 -10Q1 -1 10 0Q1 1 0 10Q-1 1 -10 0Q-1 -1 0 -10Z" fill="#FFF3C4"/></svg>'

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Mont;font-weight:100 900;src:url(data:font/woff2;base64,{b64('fuente/montserrat-latin.woff2')})}}
@font-face{{font-family:Caveat;font-weight:700;src:url(data:font/woff2;base64,{b64('fuente/caveat-latin.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden;font-family:Mont,sans-serif;background:#06080E}}
.abs{{position:absolute}}
/* el fondo: un foco sobre la noche y la estrella de la marca enorme, en linea, girando despacio */
#foco{{inset:0;background:radial-gradient(ellipse 60% 45% at 50% 44%,#1E2638 0%,#0C1019 60%,#06080E 100%)}}
#estrellon{{left:90px;top:120px;width:900px;height:900px;opacity:.09}}
#marca{{left:230px;top:22px;width:620px}}
.escena{{position:absolute;width:600px;height:600px;perspective:2000px}}
.pieza{{position:absolute;inset:0;transform-style:preserve-3d}}
.cp{{position:absolute;inset:0;border-radius:4.2%;border:1px solid rgba(255,255,255,.5)}}
.cara{{position:absolute;inset:0;border-radius:4.2%;backface-visibility:hidden;overflow:hidden}}
.detras{{transform:translateZ(-24px) rotateY(180deg);background:#F4F0E6}}
.pegatina{{position:absolute;left:23%;top:9%;width:54%}}
.nota{{position:absolute;left:0;right:0;bottom:7%;text-align:center;font-family:Caveat;font-weight:700;font-size:64px;line-height:.95;color:#1E2638}}
#suelo{{left:0;right:0;top:889px;height:2px;background:linear-gradient(90deg,transparent,rgba(233,188,70,.25),transparent)}}
#estrellas{{left:0;right:0;top:893px;display:flex;justify-content:center;gap:14px}}
.est{{position:relative;display:block;filter:drop-shadow(0 8px 10px rgba(0,0,0,.5))}}
.est svg{{display:block}}
.chispa{{position:absolute;right:-8px;top:-8px;opacity:0}}
#frase{{left:0;right:0;top:998px;text-align:center;white-space:nowrap}}
#f1{{font-weight:800;font-size:44px;color:#C9CEDA}}
#f1 span{{display:inline-block}}
#f2{{margin-top:4px;font-weight:900;font-size:84px;letter-spacing:-.02em;color:#E9BC46;line-height:1}}
#bicho{{width:340px;left:680px;transform-origin:50% 100%}}
#cta{{left:0;right:0;top:1160px;display:flex;flex-direction:column;align-items:center;gap:22px}}
#boton{{background:#E9BC46;color:#06080E;font-weight:900;font-size:54px;padding:22px 58px;border-radius:70px}}
#web{{font-weight:800;font-size:30px;letter-spacing:.16em;color:#8A93A6}}
</style></head><body>
<div class="abs" id="foco"></div>
<svg class="abs" id="estrellon" viewBox="0 0 100 100"><path d="M50 3 L61.8 36.2 L97 36.9 L69 58.3 L79.4 92 L50 72 L20.6 92 L31 58.3 L3 36.9 L38.2 36.2 Z"
  fill="none" stroke="#E9BC46" stroke-width=".6" stroke-linejoin="round"/></svg>
<img class="abs" id="marca" src="{LOGO}">
<div class="abs" id="suelo"></div>
<div class="escena" id="esc"><div class="pieza" id="placa">{PIEZA}</div></div>
<img class="abs" id="bicho" src="{svg(E + 'curiosa-izq.svg')}">
<div class="abs" id="estrellas">{''.join(f'<span class="est" id="s{i}">{estrella_facetas(i)}<i class="chispa" id="ch{i}">{CHISPA}</i></span>' for i in range(5))}</div>
<div class="abs" id="frase"><div id="f1">{''.join(f'<span>{w}</span> ' for w in 'Llevas todo el carrusel pensándolo.'.split())}</div><div id="f2">Te toca.</div></div>
<div class="abs" id="cta"><div id="boton">Comenta PLACA</div><div id="web">PLEA5E.ES</div></div>
<script>
const P = {{ salta: '{svg(E + 'salta.svg')}', curiosa: '{svg(E + 'curiosa-izq.svg')}', pulgar: '{svg(E + 'pulgar-izq.svg')}' }};
const $ = id => document.getElementById(id);
const cl = x => Math.min(1, Math.max(0, x)), p = (t, a, b) => cl((t - a) / (b - a));
const out = x => 1 - Math.pow(1 - x, 3), io = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const back = x => {{ const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); }};
function render(t) {{
  $('estrellon').style.transform = `rotate(${{t * 4}}deg)`;
  $('marca').style.opacity = p(t, .3, .7); $('marca').style.transform = `translateY(${{(1 - out(p(t, .3, .8))) * -30}}px)`;
  // la placa: baja girando (1 s), de frente; a los 2,6 s se da la vuelta; a los 4,6 vuelve y se aparta a la izquierda
  const cae = out(p(t, 0, 1.05));
  let ry = -540 * (1 - cae) + 180 * io(p(t, 2.6, 3.3)) + 180 * io(p(t, 4.6, 5.3));
  ry += 6 * Math.sin(t * 1.4) * p(t, 5.3, 6);
  const x = 240 - 140 * io(p(t, 4.7, 5.4)), y = 262 + (1 - cae) * -900 + 8 * Math.sin(t * 2) * p(t, 1, 1.5);
  const rx = 10 + 3 * Math.sin(t * .9);
  $('esc').style.left = x + 'px'; $('esc').style.top = y + 'px';
  $('placa').style.transform = `rotateX(${{rx}}deg) rotateY(${{ry}}deg)`;
  const a = ((ry % 360) + 360) % 360;
  document.querySelectorAll('.brillo').forEach(b => b.style.transform = `translateX(${{-60 + (a > 180 ? a - 360 : a) * 1.1}}%)`);
  // las cinco estrellas (una a una) y la frase
  const va = 1;
  for (let i = 0; i < 5; i++) {{
    const a0 = 1.0 + i * .12, e = back(p(t, a0, a0 + .38)), st = $('s' + i);
    // cae girando; luego, cada 1,6 s, una ola que las va levantando una detras de otra
    const ola = t > 2.4 ? Math.max(0, Math.sin(((t - 2.4 - i * .09) % 1.6) / .35 * Math.PI)) * ((t - 2.4 - i * .09) % 1.6 < .35) : 0;
    st.style.opacity = p(t, a0, a0 + .06) * va;
    st.style.transform = `translateY(${{(1 - e) * -70 - 14 * ola}}px) scale(${{(.3 + .7 * e) * (1 + .06 * ola)}}) rotate(${{(1 - e) * -144}}deg)`;
    // el brillo cruza cada estrella al caer y luego de vez en cuando
    const lz = ((t - a0 - .25) % 2.4) / .5;
    st.querySelector('.luz').setAttribute('x', -60 + 190 * cl(lz));
    // la chispa al aterrizar
    const c = p(t, a0 + .28, a0 + .6); $('ch' + i).style.opacity = Math.sin(Math.PI * c);
    $('ch' + i).style.transform = `scale(${{.4 + c}}) rotate(${{c * 90}}deg)`;
  }}
  // la frase: palabra a palabra, y "Te toca." de golpe
  [...$('f1').children].forEach((w, i) => {{ const e = out(p(t, 1.75 + i * .08, 2.05 + i * .08));
    w.style.opacity = e; w.style.transform = `translateY(${{(1 - e) * 24}}px)`; }});
  const tt = back(p(t, 2.3, 2.6)); $('f2').style.opacity = p(t, 2.3, 2.36);
  $('f2').style.transform = `scale(${{1.8 - .8 * tt}})`;
  // Estrellita: se asoma por detras del borde de la placa, coge impulso, salta y cae de pie a su lado
  const b = $('bicho'), h = b.offsetHeight || 300;
  b.style.top = (889 - h) + 'px';
  let dx = 0, dy = 0, sx = 1, sy = 1, rot = 0, z = 1, pose = P.curiosa;
  // sale de detras de la placa: asoma la cabeza por arriba, coge impulso y salta por encima
  const DX = -470, DY = -445;
  if (t < 5.35) {{ dx = DX; dy = DY + 380 * (1 - out(p(t, 4.95, 5.3))); }}                          // se asoma
  else if (t < 5.5) {{ const k = Math.sin(Math.PI * p(t, 5.35, 5.5) / 2); dx = DX; dy = DY; sx = 1 + .06 * k; sy = 1 - .09 * k; }}  // coge impulso
  else if (t < 6.05) {{ const s = p(t, 5.5, 6.05); pose = P.salta; z = 3;                               // salta
    dx = DX * (1 - io(s)); dy = DY * (1 - s) - 130 * Math.sin(Math.PI * s); rot = 12 * Math.sin(Math.PI * s);
    sy = 1 + .06 * Math.sin(Math.PI * s); sx = 1 - .04 * Math.sin(Math.PI * s); }}
  else {{ const s = p(t, 6.05, 6.3); z = 3; pose = t < 6.12 ? P.salta : P.pulgar;                     // cae y se queda con el pulgar arriba
    const ap = Math.sin(Math.PI * s) * (1 - s); sy = 1 - .16 * ap; sx = 1 + .1 * ap;
    sy *= 1 + .015 * Math.sin((t - 6.3) * 4) * p(t, 6.3, 6.5); }}
  b.style.opacity = t > 4.95 ? 1 : 0; b.style.zIndex = z; $('esc').style.zIndex = 2;
  if (b.dataset.pose !== pose) {{ b.src = pose; b.dataset.pose = pose; }}
  b.style.transform = `translate(${{dx}}px,${{dy}}px) rotate(${{rot}}deg) scale(${{sx}},${{sy}})`;
  // la llamada
  const c = back(p(t, 6.1, 6.6)); $('cta').style.opacity = p(t, 6.1, 6.25);
  $('cta').style.transform = `translateY(${{(1 - c) * 60}}px)`;
  $('boton').style.transform = `scale(${{1 + .03 * Math.sin((t - 6.6) * 6) * p(t, 6.6, 6.8)}})`;
}}
window.render = render; render(0);
</script></body></html>'''
open(V + 'escena.html', 'w').write(html)
print('escena.html')
