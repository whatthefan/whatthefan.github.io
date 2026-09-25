"""Genera capa.html: la capa de graficos y subtitulos (1080x1920, fondo transparente) con render(t)."""
import base64, json
R = '/home/user/whatthefan.github.io/'
b64 = lambda f: base64.b64encode(open(R + f, 'rb').read()).decode()
img = lambda f, m: f'data:{m};base64,' + b64(f)
P = json.load(open('plan.json'))
A = dict(
    placa=img('marketing/instagram/carrusel-placa/capas/paso5-nfc.png', 'image/png'),
    dplaca=img('marketing/instagram/producto-real/disenos/placa.png', 'image/png'),
    dstand=img('marketing/instagram/producto-real/disenos/stand.png', 'image/png'),
    dtarjeta=img('marketing/instagram/producto-real/disenos/tarjeta.png', 'image/png'),
    foto=img('marketing/guia-resenas/img/placa-mano.jpg', 'image/jpeg'),
    guia=img('marketing/guia-resenas/paginas/01.png', 'image/png'),
    logo=img('public/marca/marca-plea5e.svg', 'image/svg+xml'),
)
for p in ['gota', 'pulgar', 'tachan-izq', 'megafono-izq', 'guino', 'curiosa', 'saluda-izq']:
    A['b_' + p] = img(f'marketing/instagram/personaje/svg/{p}.svg', 'image/svg+xml')
F = lambda n, f, w='400': f"@font-face{{font-family:{n};font-weight:{w};src:url(data:font/woff2;base64,{b64('fuente/' + f)})}}"
G = ('<svg viewBox="0 0 48 48" width="{s}" height="{s}"><path fill="#4285F4" d="M45.1 24.5c0-1.6-.1-2.8-.4-4.1H24v7.4h12.1c-.2 1.8-1.6 4.6-4.5 6.5l6.9 5.3c4.1-3.8 6.6-9.4 6.6-15.1z"/>'
     '<path fill="#34A853" d="M24 46c5.9 0 10.9-2 14.5-5.3l-6.9-5.3c-1.8 1.3-4.3 2.2-7.6 2.2-5.8 0-10.7-3.8-12.5-9.1l-7.1 5.5C8 41 15.4 46 24 46z"/>'
     '<path fill="#FBBC05" d="M11.5 28.5c-.5-1.4-.8-2.9-.8-4.5s.3-3.1.7-4.5l-7.1-5.5C2.8 17 2 20.4 2 24s.8 7 2.3 10z"/>'
     '<path fill="#EA4335" d="M24 10.2c4.1 0 6.9 1.8 8.5 3.3l6.2-6C34.9 4 29.9 2 24 2 15.4 2 8 7 4.3 14l7.1 5.5c1.8-5.3 6.8-9.3 12.6-9.3z"/></svg>')
EST = '<svg viewBox="-1 -1 22 22" class="st"><path d="M10 0L12.5 6.9 20 7.3 14.1 11.9 16.2 19.1 10 15 3.8 19.1 5.9 11.9 0 7.3 7.5 6.9Z"/></svg>'
WA = '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path fill="#fff" d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm5.8 14.1c-.2.7-1.4 1.3-2 1.4-.5.1-1.2.1-1.9-.1-.4-.1-1-.3-1.8-.6-3.1-1.3-5.1-4.4-5.3-4.6-.1-.2-1.2-1.6-1.2-3s.7-2.1 1-2.4c.3-.3.6-.4.8-.4h.6c.2 0 .5-.1.7.5l1 2.4c.1.2.1.4 0 .6l-.4.5-.3.4c-.1.1-.3.3-.1.6.1.3.6 1.1 1.4 1.8 1 .9 1.8 1.1 2 1.3.3.1.4.1.6-.1l.8-1c.2-.2.4-.2.6-.1l2.2 1.1c.3.1.5.2.5.4 0 .1 0 .6-.2 1.3z"/></svg>'

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
{F('Anton', 'anton-latin.woff2')}{F('Mont', 'montserrat-latin.woff2', '100 900')}{F('Caveat', 'caveat-latin.woff2', '400 700')}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:transparent}}
.abs{{position:absolute}}
#panel{{position:absolute;left:0;top:0;width:1080px;height:960px;overflow:hidden;
  background:radial-gradient(ellipse 80% 70% at 50% 45%,#1B2440 0%,#0C1120 55%,#06080E 100%)}}
#panel::after{{content:"";position:absolute;inset:0;opacity:.35;mix-blend-mode:overlay;
  background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='r'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .5 0'/></filter><rect width='300' height='300' filter='url(%23r)'/></svg>")}}
#costura{{position:absolute;left:0;top:954px;width:1080px;height:12px;background:linear-gradient(90deg,#9A6A00,#E9BC46,#FFE08A,#E9BC46,#9A6A00);box-shadow:0 0 30px rgba(233,188,70,.6)}}
#logoPanel{{position:absolute;top:56px;left:50%;transform:translateX(-50%);height:44px;opacity:.9}}
#barra{{position:absolute;left:0;top:0;height:10px;background:#E9BC46;box-shadow:0 0 12px rgba(233,188,70,.8)}}
/* subtitulos */
#sub{{position:absolute;left:40px;right:40px;text-align:center;font-family:Mont;font-weight:900;font-size:92px;line-height:1.05;text-transform:uppercase;letter-spacing:-1px}}
#sub span{{display:inline-block;margin:0 10px;color:#fff;-webkit-text-stroke:14px #06080E;paint-order:stroke fill;
  text-shadow:0 10px 0 #06080E,0 14px 24px rgba(0,0,0,.55)}}
#sub span.on{{color:#FFD23A}}
.g{{position:absolute;opacity:0;will-change:transform,opacity}}
.card{{background:#fff;border-radius:34px;box-shadow:0 30px 60px rgba(0,0,0,.45)}}
.chip{{position:absolute;font-family:Mont;font-weight:900;font-size:54px;color:#06080E;background:#FFD23A;padding:14px 34px;border-radius:999px;box-shadow:0 12px 0 #9A6A00,0 24px 40px rgba(0,0,0,.4);white-space:nowrap}}
.tit{{font-family:Anton;color:#fff;text-transform:uppercase;line-height:1;text-shadow:0 8px 0 #06080E,0 16px 40px rgba(0,0,0,.6);-webkit-text-stroke:10px #06080E;paint-order:stroke fill}}
.oro{{color:#FFD23A}}
.st{{width:1em;height:1em;fill:#FFD23A;filter:drop-shadow(0 6px 0 #9A6A00)}}
.bicho{{position:absolute;filter:drop-shadow(0 20px 20px rgba(0,0,0,.45))}}
/* movil */
.movil{{position:absolute;width:420px;height:860px;border-radius:64px;background:#0E0E10;padding:16px;box-shadow:0 40px 80px rgba(0,0,0,.6),inset 0 0 0 4px #333}}
.pant{{width:100%;height:100%;border-radius:50px;background:#fff;overflow:hidden;position:relative;font-family:Mont;color:#202124}}
.isla{{position:absolute;top:28px;left:50%;transform:translateX(-50%);width:120px;height:34px;border-radius:20px;background:#000;z-index:2}}
.pcab{{display:flex;gap:18px;align-items:center;padding:96px 34px 26px;border-bottom:3px solid #eee}}
.pcab b{{display:block;font-size:30px}} .pcab small{{font-size:22px;color:#5f6368}}
.pq{{text-align:center;font-weight:800;font-size:30px;margin:44px 0 26px}}
.pe{{display:flex;justify-content:center;gap:10px}}
.pe svg{{width:58px;height:58px;fill:#DADCE0;filter:none}}
.pe svg.on{{fill:#FBBC04}}
.pc{{margin:40px 34px 0;border:3px solid #DADCE0;border-radius:18px;min-height:210px;padding:20px;font-size:26px;line-height:1.35;text-align:left}}
.pb{{margin:30px auto 0;width:200px;text-align:center;padding:16px 0;border-radius:40px;background:#E8EAED;color:#9AA0A6;font-weight:800;font-size:26px}}
.pb.on{{background:#1A73E8;color:#fff}}
</style></head><body>
<div id="panel"><img id="logoPanel" src="{A['logo']}"></div>
<div id="costura"></div>

<!-- placa (gancho) -->
<div class="g" id="g_placa" style="left:290px;top:150px;width:500px;height:500px">
  <div style="position:absolute;inset:0;border-radius:24px;background:#d9dcdc;transform:translate(10px,14px)"></div>
  <img src="{A['placa']}" style="position:absolute;inset:0;width:100%;height:100%;border-radius:22px;box-shadow:0 40px 70px rgba(0,0,0,.55)">
  <div id="brillo" style="position:absolute;inset:0;border-radius:22px;background:linear-gradient(115deg,transparent 35%,rgba(255,255,255,.55) 48%,transparent 60%);background-size:300% 100%"></div>
</div>
<div class="g" id="g_badge10" style="left:600px;top:560px">
  <div class="tit" style="font-size:120px;transform:rotate(-6deg)"><span class="oro">&lt;10</span> SEG</div>
</div>
<!-- nombre -->
<div class="g" id="g_nombre" style="left:60px;top:1060px">
  <div style="display:flex;align-items:center;gap:22px;background:#06080E;border:4px solid #E9BC46;border-radius:26px;padding:22px 34px;box-shadow:0 20px 40px rgba(0,0,0,.5)">
    <div style="font-family:Mont;font-weight:900;font-size:58px;color:#fff">JUAN</div>
    <div style="width:4px;height:60px;background:#E9BC46"></div>
    <img src="{A['logo']}" style="height:54px">
  </div>
</div>
<!-- negocios -->
<div class="g" id="g_negocios" style="left:0;top:0;width:1080px;height:960px">
  <div class="tit abs" style="left:0;right:0;top:170px;text-align:center;font-size:84px">PLACAS PARA</div>
  <div class="chip" id="n0" style="left:90px;top:360px">RESTAURANTES</div>
  <div class="chip" id="n1" style="left:600px;top:520px">BARES</div>
  <div class="chip" id="n2" style="left:170px;top:680px">COMERCIOS LOCALES</div>
</div>
<!-- estrellas (full) -->
<div class="g" id="g_estrellas" style="left:0;right:0;top:170px;width:1080px;text-align:center;font-size:120px">{EST * 5}</div>
<!-- cero (full) -->
<div class="g" id="g_cero" style="left:190px;top:170px;width:700px">
  <div class="card" style="padding:34px 40px;display:flex;align-items:center;gap:28px">
    {G.format(s=90)}
    <div style="font-family:Mont"><div style="font-weight:900;font-size:66px;color:#202124">0 reseñas</div><div style="font-size:34px;color:#70757a;font-weight:600">esta semana</div></div>
  </div>
</div>
<!-- bicho (full) -->
<img class="g bicho" id="g_bicho" src="{A['b_gota']}" style="left:700px;top:180px;width:330px">
<!-- foto placa -->
<div class="g" id="g_foto" style="left:120px;top:150px;width:520px;height:700px">
  <img src="{A['foto']}" style="width:100%;height:100%;object-fit:cover;border-radius:40px;border:8px solid #fff;box-shadow:0 40px 70px rgba(0,0,0,.55)">
</div>
<!-- movil -->
<div class="g" id="g_movil" style="left:600px;top:120px;transform-origin:50% 50%">
  <div class="movil"><div class="isla"></div><div class="pant">
    <div class="pcab">{G.format(s=64)}<div><b>Tu negocio</b><small>Escribe una reseña</small></div></div>
    <div class="pq">¿Qué te ha parecido?</div>
    <div class="pe" id="pe">{EST * 5}</div>
    <div class="pc" id="pc"></div>
    <div class="pb" id="pb">Publicar</div>
  </div></div>
</div>
<!-- boom (full) -->
<div class="g" id="g_boom" style="left:0;top:0;width:1080px;height:1920px">
  <div id="flash" style="position:absolute;inset:0;background:#fff"></div>
  <div class="tit abs" style="left:0;right:0;top:230px;text-align:center;font-size:260px"><span class="oro">¡BOOM!</span></div>
</div>
<!-- pregunta (full) -->
<div class="g tit" id="g_pregunta" style="left:0;right:0;top:120px;width:1080px;text-align:center;font-size:380px"><span class="oro">?</span></div>
<!-- lista -->
<div class="g" id="g_lista" style="left:0;top:0;width:1080px;height:960px">
  <div class="tit abs" style="left:0;right:0;top:150px;text-align:center;font-size:80px">SIN NADA DE ESTO</div>
  {''.join(f'<div class="abs" id="l{i}" style="left:130px;top:{300 + i * 190}px;display:flex;align-items:center;gap:30px;font-family:Mont;font-weight:900;font-size:62px;color:#fff"><span style="display:inline-grid;place-items:center;width:110px;height:110px;border-radius:50%;background:#E4574B;color:#fff;font-size:76px;box-shadow:0 10px 0 #8A2A1E">✕</span>{t}</div>' for i, t in enumerate(['Descargar nada', 'Instalar apps', 'Buscarte en Google']))}
</div>
<!-- qr -->
<div class="g" id="g_qr" style="left:190px;top:130px;width:700px;height:700px;overflow:hidden;border-radius:36px;box-shadow:0 40px 70px rgba(0,0,0,.55)">
  <img id="qrimg" src="{A['placa']}" style="position:absolute;width:1400px;height:1400px;left:-700px;top:-560px">
  <div class="chip" style="left:230px;top:590px;font-size:48px">+ QR</div>
</div>
<!-- tres (full) -->
<div class="g" id="g_tres" style="left:0;top:110px;width:1080px;text-align:center">
  <div class="tit" style="font-size:300px"><span class="oro">3</span></div><div class="tit" style="font-size:96px;margin-top:-20px">MOTIVOS</div>
</div>
<!-- motivo 1 -->
<div class="g" id="g_motivo1" style="left:0;top:0;width:1080px;height:960px">
  <div class="tit abs" style="left:70px;top:150px;font-size:74px"><span class="oro">1 ·</span> TU LOGO, TUS COLORES</div>
  <img id="m1a" class="abs" src="{A['dtarjeta']}" style="left:40px;top:330px;width:440px;transform:rotate(-10deg);filter:drop-shadow(0 30px 30px rgba(0,0,0,.5))">
  <img id="m1b" class="abs" src="{A['dplaca']}" style="left:360px;top:290px;width:380px;filter:drop-shadow(0 30px 30px rgba(0,0,0,.5))">
  <img id="m1c" class="abs" src="{A['dstand']}" style="left:760px;top:300px;width:270px;transform:rotate(8deg);filter:drop-shadow(0 30px 30px rgba(0,0,0,.5))">
  <div id="m1g" class="chip" style="left:130px;top:760px;font-size:64px;transform:rotate(-4deg)">DISEÑO GRATIS</div>
  <div id="m1v" class="chip" style="left:600px;top:790px;font-size:40px;background:#fff">✓ TÚ LO APRUEBAS</div>
</div>
<!-- motivo 2 -->
<div class="g" id="g_motivo2" style="left:0;top:0;width:1080px;height:960px">
  <div class="tit abs" style="left:70px;top:150px;font-size:74px"><span class="oro">2 ·</span> TE ENSEÑAMOS</div>
  <img id="m2g" class="abs" src="{A['guia']}" style="left:120px;top:290px;width:420px;border-radius:16px;transform:rotate(-6deg);box-shadow:0 40px 60px rgba(0,0,0,.6)">
  <div class="abs" style="left:590px;top:360px;width:430px;font-family:Mont;font-weight:900;font-size:52px;line-height:1.15;color:#fff">A TI Y A TU EQUIPO:<br><span class="oro">CUÁNDO Y CÓMO PEDIRLA</span></div>
  <img class="abs bicho" src="{A['b_guino']}" style="left:700px;top:640px;width:250px">
</div>
<!-- motivo 3 -->
<div class="g" id="g_motivo3" style="left:0;top:0;width:1080px;height:960px">
  <div class="tit abs" style="left:70px;top:150px;font-size:74px"><span class="oro">3 ·</span> PAGO ÚNICO</div>
  <div class="abs" style="left:110px;top:320px;width:860px;height:430px;border-radius:40px;background:#fff;box-shadow:0 40px 70px rgba(0,0,0,.5);display:flex;align-items:center;gap:40px;padding:40px 50px">
    <img src="{A['dplaca']}" style="width:300px;filter:drop-shadow(0 20px 20px rgba(0,0,0,.3))">
    <div style="font-family:Mont"><div style="font-weight:900;font-size:64px;color:#06080E;line-height:1.05">LA PAGAS<br>UNA VEZ</div>
      <div id="m3t" style="margin-top:22px;display:inline-block;font-weight:900;font-size:60px;color:#06080E;background:#FFD23A;padding:8px 26px;border-radius:14px;transform:rotate(-4deg)">Y ES TUYA</div></div>
  </div>
</div>
<!-- whatsapp -->
<div class="g" id="g_whatsapp" style="left:120px;top:190px;width:840px">
  <div style="display:flex;align-items:center;gap:26px;background:#fff;border-radius:40px;padding:34px 40px;box-shadow:0 40px 70px rgba(0,0,0,.5)">
    <div style="width:130px;height:130px;border-radius:32px;background:#25D366;display:grid;place-items:center;flex:none">{WA.format(s=86)}</div>
    <div style="font-family:Mont"><div style="font-weight:900;font-size:44px;color:#111">Juan · PLEA5E</div><div style="font-size:38px;color:#444;margin-top:6px">¡Hola! Te paso el diseño 👇</div></div>
  </div>
  <div class="tit" style="font-size:78px;text-align:center;margin-top:90px">HABLAS <span class="oro">CONMIGO</span></div>
</div>
<!-- espana (full) -->
<div class="g" id="g_espana" style="left:0;top:160px;width:1080px;text-align:center">
  <div class="chip" style="position:relative;display:inline-block;font-size:60px">📍 CÓRDOBA → TODA ESPAÑA</div>
</div>
<!-- comenta -->
<div class="g" id="g_comenta" style="left:90px;top:220px;width:900px">
  <div style="background:#fff;border-radius:36px;padding:34px 40px;box-shadow:0 40px 70px rgba(0,0,0,.5);font-family:Mont">
    <div style="font-size:34px;color:#666;font-weight:700">Añade un comentario…</div>
    <div style="font-size:110px;font-weight:900;color:#06080E;margin-top:10px"><span id="ctxt"></span><span id="ccur" style="color:#1A73E8">|</span></div>
  </div>
  <div class="tit" style="font-size:84px;text-align:center;margin-top:70px">COMENTA <span class="oro">«PLACA»</span></div>
</div>
<img class="g bicho" id="g_megafono" src="{A['b_megafono-izq']}" style="left:760px;top:560px;width:300px">
<!-- final -->
<div class="g" id="g_final" style="left:0;top:0;width:1080px;height:960px">
  <img src="{A['placa']}" class="abs" style="left:350px;top:170px;width:380px;border-radius:18px;transform:rotate(-5deg);box-shadow:0 40px 60px rgba(0,0,0,.55)">
  <div class="tit abs" style="left:0;right:0;top:620px;text-align:center;font-size:88px">TE MANDO <span class="oro">TU DISEÑO</span></div>
  <div class="abs" style="left:0;right:0;top:760px;text-align:center;font-family:Mont;font-weight:800;font-size:46px;color:#fff">plea5e.es</div>
  <img class="abs bicho" id="fb" src="{A['b_tachan-izq']}" style="left:40px;top:360px;width:280px">
</div>

<div id="sub"></div>
<div id="barra"></div>
<script>
const P = {json.dumps(dict(total=P['total'], seg=P['seg'], subs=P['subs'], ev=P['ev']), ensure_ascii=False)};
const $ = id => document.getElementById(id);
const cl = (x,a=0,b=1) => Math.min(b, Math.max(a, x));
const eo = x => 1 - Math.pow(1 - cl(x), 3);
const back = x => {{ x = cl(x); const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); }};
function segAt(t) {{ for (const s of P.seg) if (t < s.t1) return s; return P.seg[P.seg.length - 1]; }}
function show(el, e, t, how) {{
  const u = t - e.t0, left = e.t1 - t;
  if (u < 0 || left < 0) {{ el.style.opacity = 0; return null; }}
  const inn = cl(u / .28), out = cl(left / .14);
  el.style.opacity = Math.min(1, inn * 3, out);
  let tr = '';
  if (how === 'pop') tr = `scale(${{.4 + .6 * back(u / .32)}})`;
  else if (how === 'down') tr = `translateY(${{(1 - eo(u / .3)) * -140}}px)`;
  else if (how === 'left') tr = `translateX(${{(1 - eo(u / .3)) * -700}}px)`;
  else if (how === 'up') tr = `translateY(${{(1 - eo(u / .3)) * 260}}px)`;
  el.style.transform = tr;
  return u;
}}
const pops = (ids, ts, t) => ids.forEach((id, k) => {{ const u = t - ts[k]; const el = $(id);
  el.style.opacity = u < 0 ? 0 : 1; el.style.transform = (el.dataset.r || '') + ` scale(${{u < 0 ? .3 : .3 + .7 * back(u / .3)}})`; }});
window.render = function(t) {{
  const s = segAt(t), split = s.lay === 'split';
  $('panel').style.opacity = split ? 1 : 0; $('costura').style.opacity = split ? 1 : 0;
  $('barra').style.width = (t / P.total * 1080) + 'px';
  // subtitulos
  const pg = P.subs.find(p => t >= p.t0 && t < p.t1);
  const sub = $('sub');
  if (pg) {{
    sub.style.top = split ? '905px' : '1330px';
    if (sub.dataset.k != pg.t0) {{ sub.innerHTML = pg.w.map(w => `<span>${{w.w}}</span>`).join(''); sub.dataset.k = pg.t0; }}
    const u = t - pg.t0; sub.style.transform = `scale(${{.75 + .25 * back(u / .18)}})`;
    [...sub.children].forEach((sp, k) => sp.classList.toggle('on', t >= pg.w[k].t0 && t < pg.w[k].t1 + .05));
  }} else sub.innerHTML = '';
  // graficos
  const E = k => P.ev.filter(e => e.k === k);
  const one = (k, how, id) => {{ let r = null; for (const e of E(k)) {{ const v = show($(id || 'g_' + k), e, t, how); if (v !== null) r = [v, e]; }} if (!r) $(id || 'g_' + k).style.opacity = 0; return r; }};
  let r;
  if ((r = one('placa', 'pop'))) {{ const [u] = r; const el = $('g_placa');
    const tS = P.seg[1].t0; const sh = cl((t - tS) / .4);
    el.style.transform += ` rotate(${{-6 + Math.sin(u * 2) * 2}}deg) translate(${{-sh * 170}}px, ${{-sh * 20}}px) scale(${{1 - sh * .22}})`;
    $('brillo').style.backgroundPosition = `${{(1 - (u % 2.2) / 1.2) * 150}}% 0`; }}
  one('badge10', 'pop');
  one('nombre', 'left');
  if ((r = one('negocios', ''))) pops(['n0', 'n1', 'n2'], r[1].pops, t);
  if ((r = one('estrellas', ''))) [...$('g_estrellas').children].forEach((st, k) => {{ const u = r[0] - k * .09;
    st.style.transform = `scale(${{u < 0 ? 0 : back(u / .3)}}) rotate(${{(1 - cl(u / .3)) * -90}}deg)`; }});
  one('cero', 'down');
  one('bicho', 'up');
  one('foto', 'left');
  for (const e of E('movil')) {{ }}
  const mv = E('movil').find(e => t >= e.t0 && t < e.t1);
  const gm = $('g_movil');
  if (mv) {{
    const u = t - mv.t0; gm.style.opacity = Math.min(1, u / .15, (mv.t1 - t) / .12);
    if (mv.fase === 'llega') {{ gm.style.left = '640px'; gm.style.transform = `translate(${{(1 - eo(u / .9)) * 500}}px, ${{(1 - eo(u / .9)) * 300}}px) rotate(${{-14 + eo(u / .9) * 4}}deg) scale(.95)`;
      [...$('pe').children].forEach(x => x.classList.remove('on')); $('pc').textContent = ''; $('pb').classList.remove('on'); }}
    else {{ gm.style.left = '330px'; gm.style.transform = `translateY(${{(1 - eo(u / .35)) * 500}}px) scale(.98)`;
      const nS = Math.floor(cl((u - 1.1) / .9) * 5 + .001); [...$('pe').children].forEach((x, k) => x.classList.toggle('on', k < nS));
      const txt = 'Todo buenísimo y el trato, de 10. ¡Volveremos!'; const nc = Math.floor(cl((u - 2.3) / 1.9) * txt.length);
      $('pc').textContent = txt.slice(0, nc); $('pb').classList.toggle('on', nc >= txt.length); }}
  }} else gm.style.opacity = 0;
  if ((r = one('boom', ''))) {{ $('flash').style.opacity = cl(1 - r[0] / .18); $('g_boom').children[1].style.transform = `scale(${{.3 + .7 * back(r[0] / .25)}}) rotate(-5deg)`; }}
  one('pregunta', 'pop');
  if ((r = one('lista', ''))) ['l0', 'l1', 'l2'].forEach((id, k) => {{ const u = t - r[1].pops[k]; const el = $(id);
    el.style.opacity = u < 0 ? .0 : 1; el.style.transform = `translateX(${{u < 0 ? -80 : (1 - eo(u / .25)) * -80}}px)`; }});
  if ((r = one('qr', 'pop'))) {{ const u = r[0]; $('qrimg').style.transform = `scale(${{1 + eo(u / 1.4) * .12}})`; }}
  one('tres', 'pop');
  if ((r = one('motivo1', ''))) {{ const u = r[0], e = r[1];
    ['m1a', 'm1b', 'm1c'].forEach((id, k) => {{ const v = u - k * .12; const el = $(id); el.style.opacity = v < 0 ? 0 : 1;
      el.style.transform = `translateY(${{(1 - eo(v / .35)) * 400}}px) rotate(${{[-10, 0, 8][k]}}deg)`; }});
    const g = t - e.gratis; $('m1g').style.opacity = g < 0 ? 0 : 1; $('m1g').style.transform = `rotate(-4deg) scale(${{g < 0 ? .3 : .3 + .7 * back(g / .3)}})`;
    const v = t - e.guste; $('m1v').style.opacity = v < 0 ? 0 : 1; $('m1v').style.transform = `scale(${{v < 0 ? .3 : .3 + .7 * back(v / .3)}})`; }}
  if ((r = one('motivo2', ''))) {{ $('m2g').style.transform = `rotate(-6deg) translateY(${{(1 - eo(r[0] / .4)) * 500}}px)`; }}
  if ((r = one('motivo3', ''))) {{ const v = t - r[1].tuya; $('m3t').style.transform = `rotate(-4deg) scale(${{v < 0 ? 1 : 1 + .25 * Math.sin(cl(v / .35) * Math.PI)}})`; }}
  one('whatsapp', 'down');
  one('espana', 'pop');
  if ((r = one('comenta', 'pop'))) {{ const u = r[0]; const w = 'PLACA'; $('ctxt').textContent = w.slice(0, Math.floor(cl((u - .25) / .5) * w.length));
    $('ccur').style.opacity = (Math.floor(u * 3) % 2) ? 0 : 1; }}
  const cm = E('comenta')[0]; show($('g_megafono'), {{t0: cm.t0 + .2, t1: cm.t1}}, t, 'up');
  if ((r = one('final', ''))) {{ $('fb').style.transform = `translateY(${{Math.abs(Math.sin(r[0] * 5)) * -30}}px)`; }}
}};
window.LISTO = true;
</script></body></html>'''
open('capa.html', 'w').write(html)
print('capa.html', len(html) // 1024, 'KB')
