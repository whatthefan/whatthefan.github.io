"""La ultima del carrusel, en video (8,5 s, 1080x1350): la placa baja girando,
salen cinco estrellas y "Del cielo… a tu mesa." (el carrusel empieza con la estrella en el cielo), se da la vuelta y por detras
esta Estrellita con el pulgar arriba ("Aqui no hay nada... Comenta PLACA"). Al volver,
Estrellita se asoma por el borde, coge impulso, salta fuera y cae de pie al
lado, con el pulgar arriba, junto al "Comenta PLACA". Muy poco texto.

Desde la raiz del repo:
    python3 marketing/instagram/carteles/video/montar.py
    python3 marketing/instagram/carteles/video/musica.py
    FFMPEG=ffmpeg node marketing/instagram/carteles/video/grabar.js
"""
import base64

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
ESTRELLA = ('<svg viewBox="0 0 100 96" width="84" height="80"><path d="M50 3 L61.8 36.2 L97 36.9 L69 58.3 L79.4 92 L50 72 '
            'L20.6 92 L31 58.3 L3 36.9 L38.2 36.2 Z" fill="#E9BC46" stroke="#E9BC46" stroke-width="5" stroke-linejoin="round"/></svg>')

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Mont;font-weight:100 900;src:url(data:font/woff2;base64,{b64('fuente/montserrat-latin.woff2')})}}
@font-face{{font-family:Caveat;font-weight:700;src:url(data:font/woff2;base64,{b64('fuente/caveat-latin.woff2')})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden;font-family:Mont,sans-serif;background:#06080E}}
.abs{{position:absolute}}
/* el fondo: un foco sobre la noche y la estrella de la marca enorme, en linea, girando despacio */
#foco{{inset:0;background:radial-gradient(ellipse 60% 45% at 50% 44%,#1E2638 0%,#0C1019 60%,#06080E 100%)}}
#estrellon{{left:90px;top:120px;width:900px;height:900px;opacity:.09}}
#marca{{left:290px;top:70px;width:500px}}
.escena{{position:absolute;width:600px;height:600px;perspective:2000px}}
.pieza{{position:absolute;inset:0;transform-style:preserve-3d}}
.cp{{position:absolute;inset:0;border-radius:4.2%;border:1px solid rgba(255,255,255,.5)}}
.cara{{position:absolute;inset:0;border-radius:4.2%;backface-visibility:hidden;overflow:hidden}}
.detras{{transform:translateZ(-24px) rotateY(180deg);background:#F4F0E6}}
.pegatina{{position:absolute;left:23%;top:9%;width:54%}}
.nota{{position:absolute;left:0;right:0;bottom:7%;text-align:center;font-family:Caveat;font-weight:700;font-size:64px;line-height:.95;color:#1E2638}}
#suelo{{left:0;right:0;top:872px;height:2px;background:linear-gradient(90deg,transparent,rgba(233,188,70,.25),transparent)}}
#estrellas{{left:0;right:0;top:895px;display:flex;justify-content:center;gap:18px}}
#estrellas svg{{display:block}}
#frase{{left:0;right:0;top:995px;text-align:center;font-weight:900;font-size:62px;letter-spacing:-.01em;color:#F4EDE0;white-space:nowrap}}
#frase b{{color:#E9BC46}}
#bicho{{width:340px;left:680px;transform-origin:50% 100%}}
#cta{{left:0;right:0;top:1118px;display:flex;flex-direction:column;align-items:center;gap:22px}}
#boton{{background:#E9BC46;color:#06080E;font-weight:900;font-size:54px;padding:22px 58px;border-radius:70px}}
#web{{font-weight:800;font-size:30px;letter-spacing:.16em;color:#8A93A6}}
</style></head><body>
<div class="abs" id="foco"></div>
<svg class="abs" id="estrellon" viewBox="0 0 100 100"><path d="M50 3 L61.8 36.2 L97 36.9 L69 58.3 L79.4 92 L50 72 L20.6 92 L31 58.3 L3 36.9 L38.2 36.2 Z"
  fill="none" stroke="#E9BC46" stroke-width=".6" stroke-linejoin="round"/></svg>
<img class="abs" id="marca" src="{svg('public/marca/marca-plea5e.svg')}">
<div class="abs" id="suelo"></div>
<div class="escena" id="esc"><div class="pieza" id="placa">{PIEZA}</div></div>
<img class="abs" id="bicho" src="{svg(E + 'curiosa-izq.svg')}">
<div class="abs" id="estrellas">{''.join(f'<span id="s{i}">{ESTRELLA}</span>' for i in range(5))}</div>
<div class="abs" id="frase">Del cielo… a <b>tu mesa</b>.</div>
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
  const x = 240 - 140 * io(p(t, 4.7, 5.4)), y = 245 + (1 - cae) * -900 + 8 * Math.sin(t * 2) * p(t, 1, 1.5);
  const rx = 10 + 3 * Math.sin(t * .9);
  $('esc').style.left = x + 'px'; $('esc').style.top = y + 'px';
  $('placa').style.transform = `rotateX(${{rx}}deg) rotateY(${{ry}}deg)`;
  const a = ((ry % 360) + 360) % 360;
  document.querySelectorAll('.brillo').forEach(b => b.style.transform = `translateX(${{-60 + (a > 180 ? a - 360 : a) * 1.1}}%)`);
  // las cinco estrellas (una a una) y la frase
  const va = 1;
  for (let i = 0; i < 5; i++) {{ const e = back(p(t, 1.05 + i * .1, 1.4 + i * .1));
    $('s' + i).style.opacity = p(t, 1.05 + i * .1, 1.12 + i * .1) * va; $('s' + i).style.display = 'block';
    $('s' + i).style.transform = `translateY(${{(1 - e) * 50}}px) scale(${{.4 + .6 * e}}) rotate(${{(1 - e) * -70}}deg)`; }}
  const fr = back(p(t, 1.7, 2.1)); $('frase').style.opacity = p(t, 1.7, 1.8) * va;
  $('frase').style.transform = `translateY(${{(1 - fr) * 40}}px)`;
  // Estrellita: se asoma por detras del borde de la placa, coge impulso, salta y cae de pie a su lado
  const b = $('bicho'), h = b.offsetHeight || 300;
  b.style.top = (872 - h) + 'px';
  let dx = 0, dy = 0, sx = 1, sy = 1, rot = 0, z = 1, pose = P.curiosa;
  if (t < 5.35) {{ dx = -250 + 120 * out(p(t, 4.95, 5.3)); }}                              // se asoma
  else if (t < 5.5) {{ const k = Math.sin(Math.PI * p(t, 5.35, 5.5) / 2); dx = -130; sx = 1 + .08 * k; sy = 1 - .14 * k; }}  // coge impulso
  else if (t < 6.0) {{ const s = p(t, 5.5, 6.0); pose = P.salta; z = 3;                    // salta
    dx = -130 + 130 * io(s); dy = -270 * Math.sin(Math.PI * s); rot = 10 * Math.sin(Math.PI * s); sy = 1 + .06 * Math.sin(Math.PI * s); sx = 1 - .04 * Math.sin(Math.PI * s); }}
  else {{ const s = p(t, 6.0, 6.25); z = 3; pose = t < 6.1 ? P.salta : P.pulgar;             // cae y se queda con el pulgar arriba
    const ap = Math.sin(Math.PI * s) * (1 - s); sy = 1 - .16 * ap; sx = 1 + .1 * ap;
    sy *= 1 + .015 * Math.sin((t - 6.25) * 4) * p(t, 6.25, 6.5); }}
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
