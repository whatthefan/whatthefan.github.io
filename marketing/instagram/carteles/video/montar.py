"""La ultima del carrusel, en video (8,5 s, 1080x1350). Arriba, en grande y en
blanco (Anton): "LLEVAS TODO EL CARRUSEL PENSANDOLO.". La placa baja girando,
caen cinco estrellas talladas y "Te toca.". La placa se da la vuelta: detras
esta Estrellita pegada, con "Aqui no hay nada... Comenta PLACA". Estrellita se
despega (se levanta de una esquina, como una pegatina), coge impulso, salta
hacia delante y cae de pie al lado de la placa, que vuelve de frente. Cierra
con Comenta PLACA.

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
  <div class="cara detras"><div class="hueco"></div><img class="pegatina" src="{svg(E + 'pulgar.svg')}">
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
@font-face{{font-family:Anton;src:url(data:font/woff2;base64,{b64('fuente/anton-latin.woff2')})}}
@font-face{{font-family:Caveat;font-weight:700;src:url(data:font/woff2;base64,{b64('fuente/caveat-latin.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden;font-family:Mont,sans-serif;background:#06080E}}
.abs{{position:absolute}}
/* el fondo: un foco sobre la noche y la estrella de la marca enorme, en linea, girando despacio */
#foco{{inset:0;background:radial-gradient(ellipse 60% 45% at 50% 46%,#1E2638 0%,#0C1019 60%,#06080E 100%)}}
#estrellon{{left:90px;top:150px;width:900px;height:900px;opacity:.09}}
#titulo{{left:0;right:0;top:48px;text-align:center;font-family:Anton;color:#fff;text-transform:uppercase;line-height:1.1}}
#titulo div{{white-space:nowrap}}
#titulo span{{display:inline-block}}
#t1{{font-size:98px;letter-spacing:.01em}}
#t2{{font-size:142px;letter-spacing:.02em}}
.escena{{position:absolute;width:540px;height:540px;perspective:2000px}}
.pieza{{position:absolute;inset:0;transform-style:preserve-3d}}
.cp{{position:absolute;inset:0;border-radius:4.2%;border:1px solid rgba(255,255,255,.5)}}
.cara{{position:absolute;inset:0;border-radius:4.2%;backface-visibility:hidden;overflow:hidden}}
.detras{{transform:translateZ(-24px) rotateY(180deg);background:#F4F0E6}}
.pegatina{{position:absolute;left:23%;top:9%;width:54%}}
.hueco{{position:absolute;left:23%;top:9%;width:54%;height:48%;border:4px dashed rgba(30,38,56,.18);border-radius:24px;opacity:0}}
.nota{{position:absolute;left:0;right:0;bottom:7%;text-align:center;font-family:Caveat;font-weight:700;font-size:58px;line-height:.95;color:#1E2638}}
#suelo{{left:0;right:0;top:895px;height:2px;background:linear-gradient(90deg,transparent,rgba(233,188,70,.25),transparent)}}
#estrellas{{left:0;right:0;top:905px;display:flex;justify-content:center;gap:14px}}
.est{{position:relative;display:block;filter:drop-shadow(0 8px 10px rgba(0,0,0,.5))}}
.est svg{{display:block}}
.chispa{{position:absolute;right:-8px;top:-8px;opacity:0}}
#toca{{left:0;right:0;top:1010px;text-align:center;font-weight:900;font-size:84px;letter-spacing:-.02em;color:#E9BC46;line-height:1}}
#bicho{{left:0;top:0;width:340px;transform-origin:50% 100%;filter:drop-shadow(0 14px 14px rgba(0,0,0,.45))}}
#cta{{left:0;right:0;top:1128px;display:flex;flex-direction:column;align-items:center;gap:20px}}
#boton{{background:#E9BC46;color:#06080E;font-weight:900;font-size:54px;padding:22px 58px;border-radius:70px}}
#web{{font-weight:800;font-size:30px;letter-spacing:.16em;color:#8A93A6}}
</style></head><body>
<div class="abs" id="foco"></div>
<svg class="abs" id="estrellon" viewBox="0 0 100 100"><path d="M50 3 L61.8 36.2 L97 36.9 L69 58.3 L79.4 92 L50 72 L20.6 92 L31 58.3 L3 36.9 L38.2 36.2 Z"
  fill="none" stroke="#E9BC46" stroke-width=".6" stroke-linejoin="round"/></svg>
<div class="abs" id="titulo"><div id="t1">{''.join(f'<span>{w}</span> ' for w in 'Llevas todo el carrusel'.split())}</div><div id="t2"><span>pensándolo.</span></div></div>
<div class="abs" id="suelo"></div>
<div class="escena" id="esc"><div class="pieza" id="placa">{PIEZA}</div></div>
<img class="abs" id="bicho" src="{svg(E + 'pulgar.svg')}">
<div class="abs" id="estrellas">{''.join(f'<span class="est" id="s{i}">{estrella_facetas(i)}<i class="chispa" id="ch{i}">{CHISPA}</i></span>' for i in range(5))}</div>
<div class="abs" id="toca">Te toca.</div>
<div class="abs" id="cta"><div id="boton">Comenta PLACA</div><div id="web">PLEA5E.ES</div></div>
<script>
const P = {{ pegada: '{svg(E + 'pulgar.svg')}', salta: '{svg(E + 'salta.svg')}', pulgar: '{svg(E + 'pulgar-izq.svg')}' }};
const $ = id => document.getElementById(id);
const cl = x => Math.min(1, Math.max(0, x)), p = (t, a, b) => cl((t - a) / (b - a));
const out = x => 1 - Math.pow(1 - x, 3), io = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const back = x => {{ const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); }};
const L = 540, X0 = 270, X1 = 110, Y = 330;                   // la placa: lado, sitio al principio y al final
function render(t) {{
  $('estrellon').style.transform = `rotate(${{t * 4}}deg)`;
  // el titulo, palabra a palabra, y PENSANDOLO de golpe
  [...$('t1').children].forEach((w, i) => {{ const e = back(p(t, .25 + i * .1, .6 + i * .1));
    w.style.opacity = p(t, .25 + i * .1, .32 + i * .1); w.style.transform = `translateY(${{(1 - e) * 50}}px)`; }});
  const tp = back(p(t, .75, 1.1)); $('t2').style.opacity = p(t, .75, .8); $('t2').style.transform = `scale(${{1.5 - .5 * tp}})`;
  // la placa: baja girando; a los 2,5 s se da la vuelta (detras esta Estrellita pegada);
  // Estrellita se despega y salta; la placa se aparta a la izquierda y vuelve de frente
  const cae = out(p(t, .2, 1.25));
  let ry = -540 * (1 - cae) + 180 * io(p(t, 2.5, 3.2)) + 180 * io(p(t, 5.1, 5.8));
  ry += 5 * Math.sin(t * 1.4) * p(t, 5.8, 6.4);
  const x = X0 - (X0 - X1) * io(p(t, 4.35, 5.0)), y = Y + (1 - cae) * -1000;
  const rx = 8 + 3 * Math.sin(t * .9);
  $('esc').style.left = x + 'px'; $('esc').style.top = y + 'px';
  $('placa').style.transform = `rotateX(${{rx}}deg) rotateY(${{ry}}deg)`;
  const a = ((ry % 360) + 360) % 360;
  document.querySelectorAll('.brillo').forEach(b => b.style.transform = `translateX(${{-60 + (a > 180 ? a - 360 : a) * 1.1}}%)`);
  // la pegatina de detras: esta hasta que se despega; queda el hueco marcado
  document.querySelectorAll('#placa .pegatina').forEach(g => g.style.opacity = t < 3.85 ? 1 : 0);
  document.querySelectorAll('#placa .hueco').forEach(g => g.style.opacity = t < 3.85 ? 0 : 1);
  // las cinco estrellas
  for (let i = 0; i < 5; i++) {{
    const a0 = 1.3 + i * .12, e = back(p(t, a0, a0 + .38)), st = $('s' + i);
    const ola = t > 2.6 ? Math.max(0, Math.sin(((t - 2.6 - i * .09) % 1.6) / .35 * Math.PI)) * ((t - 2.6 - i * .09) % 1.6 < .35) : 0;
    st.style.opacity = p(t, a0, a0 + .06);
    st.style.transform = `translateY(${{(1 - e) * -70 - 14 * ola}}px) scale(${{(.3 + .7 * e) * (1 + .06 * ola)}}) rotate(${{(1 - e) * -144}}deg)`;
    const lz = ((t - a0 - .25) % 2.4) / .5;
    st.querySelector('.luz').setAttribute('x', -60 + 190 * cl(lz));
    const c = p(t, a0 + .28, a0 + .6); $('ch' + i).style.opacity = Math.sin(Math.PI * c);
    $('ch' + i).style.transform = `scale(${{.4 + c}}) rotate(${{c * 90}}deg)`;
  }}
  const tt = back(p(t, 2.1, 2.4)); $('toca').style.opacity = p(t, 2.1, 2.16); $('toca').style.transform = `scale(${{1.8 - .8 * tt}})`;
  // Estrellita: sale del sitio exacto de la pegatina, se despega (se levanta de una esquina y se suelta),
  // coge impulso, salta hacia delante y cae de pie al lado de la placa
  const b = $('bicho'), h = b.offsetHeight || 300;
  const PX = X0 + .23 * L, PY = Y + .09 * L, PS = .54 * L / 340;     // donde esta pegada (arriba-izquierda y escala)
  const FX = 690, FY = 895 - h;                                    // donde cae
  let bx = PX - 340 * (1 - PS) / 2, by = PY - h * (1 - PS), sx = PS, sy = PS, rot = 0, pose = P.pegada;
  if (t >= 3.85 && t < 4.2) {{ const k = out(p(t, 3.85, 4.2));                                  // se despega
    rot = -14 * k; by -= 40 * k; sx = PS * (1 + .06 * k); sy = PS * (1 + .06 * k); }}
  else if (t >= 4.2 && t < 4.32) {{ const k = Math.sin(Math.PI * p(t, 4.2, 4.32) / 2);           // coge impulso
    rot = -14 * (1 - k); by -= 40; sx = PS * 1.06 * (1 + .06 * k); sy = PS * 1.06 * (1 - .1 * k); }}
  else if (t >= 4.32 && t < 4.95) {{ const s = p(t, 4.32, 4.95); pose = P.salta;                // salta hacia delante
    const x0 = bx, y0 = by - 40;
    bx = x0 + (FX - x0) * io(s); by = y0 + (FY - y0) * s - 230 * Math.sin(Math.PI * s);
    const e = PS * 1.06 + (1 - PS * 1.06) * io(s); sx = e * (1 - .04 * Math.sin(Math.PI * s)); sy = e * (1 + .06 * Math.sin(Math.PI * s));
    rot = 360 * io(s) * .0 + 10 * Math.sin(Math.PI * s); }}
  else if (t >= 4.95) {{ const s = p(t, 4.95, 5.2); pose = t < 5.02 ? P.salta : P.pulgar;         // cae de pie y pulgar arriba
    bx = FX; by = FY; const ap = Math.sin(Math.PI * s) * (1 - s); sx = 1 + .1 * ap; sy = (1 - .16 * ap) * (1 + .015 * Math.sin((t - 5.2) * 4) * p(t, 5.2, 5.4)); }}
  b.style.opacity = t >= 3.85 ? 1 : 0; b.style.zIndex = 3; $('esc').style.zIndex = 2;
  if (b.dataset.pose !== pose) {{ b.src = pose; b.dataset.pose = pose; }}
  b.style.transformOrigin = t < 4.32 ? '100% 100%' : '50% 100%';
  b.style.transform = `translate(${{bx}}px,${{by}}px) rotate(${{rot}}deg) scale(${{sx}},${{sy}})`;
  // la llamada
  const c = back(p(t, 5.9, 6.4)); $('cta').style.opacity = p(t, 5.9, 6.05);
  $('cta').style.transform = `translateY(${{(1 - c) * 60}}px)`;
  $('boton').style.transform = `scale(${{1 + .03 * Math.sin((t - 6.4) * 6) * p(t, 6.4, 6.6)}})`;
}}
window.render = render; render(0);
</script></body></html>'''
open(V + 'escena.html', 'w').write(html)
print('escena.html')
