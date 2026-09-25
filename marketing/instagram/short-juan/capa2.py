"""Capa de motion design estilo 'premium SaaS' (skill edicion-pro) para el short de Juan."""
import base64, json
R = '/home/user/whatthefan.github.io/'
b64 = lambda f: base64.b64encode(open(R + f, 'rb').read()).decode()
img = lambda f, m: f'data:{m};base64,' + b64(f)
P = json.load(open('plan.json'))
MOTION = open(R + '.claude/skills/edicion-pro/motion.js').read()
A = dict(
    placa=img('marketing/instagram/carrusel-placa/capas/paso5-nfc.png', 'image/png'),
    dplaca=img('marketing/instagram/producto-real/disenos/placa.png', 'image/png'),
    dstand=img('marketing/instagram/producto-real/disenos/stand.png', 'image/png'),
    dtarjeta=img('marketing/instagram/producto-real/disenos/tarjeta.png', 'image/png'),
    foto=img('marketing/guia-resenas/img/placa-mano.jpg', 'image/jpeg'),
    logo=img('public/marca/marca-plea5e.svg', 'image/svg+xml'),
)
F = lambda n, f, w='400': f"@font-face{{font-family:{n};font-weight:{w};src:url(data:font/woff2;base64,{b64('fuente/' + f)})}}"

# tiempos de palabras (salida) para sincronizar
def kw(i, w):
    s = P['seg'][i]
    for sub in P['subs']:
        for x in sub['w']:
            if s['t0'] - .05 <= x['t0'] < s['t1'] and w.lower() in x['w'].lower():
                return round(x['t0'], 3)
    raise KeyError((i, w))
S = lambda i: P['seg'][i]
K = dict(
    s0=S(0)['t0'], s1e=S(1)['t1'], menos=kw(1, 'menos'),
    s4=S(4)['t0'], s4e=S(4)['t1'], rest=kw(4, 'restaurantes'), bares=kw(4, 'bares'), com=kw(4, 'comercios'),
    s9=S(9)['t0'], s10e=S(10)['t1'], acercar=kw(10, 'acercar'),
    s12=S(12)['t0'], s13e=S(13)['t1'],
    s15=S(15)['t0'], s15e=S(15)['t1'], desc=kw(15, 'descargar'), app=kw(15, 'app'), busc=kw(15, 'buscarte'),
    s17=S(17)['t0'], s17e=S(17)['t1'],
    s19=S(19)['t0'], s20e=S(20)['t1'], gratis=kw(20, 'gratis'), impr=kw(20, 'imprime'),
    s21=S(21)['t0'], s22e=S(22)['t1'], cuando=kw(22, 'cuándo'), como=kw(22, 'cómo'), equipo=kw(22, 'equipo'), resenas=kw(22, 'reseñas'),
    s24=S(24)['t0'], s24e=S(24)['t1'], unica=kw(24, 'único'), tuyas=kw(24, 'tuyas'),
    s25=S(25)['t0'], s25e=S(25)['t1'],
    s28=S(28)['t0'], s28e=S(28)['t1'],
    fin=[e for e in P['ev'] if e['k'] == 'final'][0]['t0'],
)
json.dump(K, open('claves.json', 'w'), indent=1)

EST = '<svg viewBox="0 0 20 20" class="st"><path d="M10 0L12.5 6.9 20 7.3 14.1 11.9 16.2 19.1 10 15 3.8 19.1 5.9 11.9 0 7.3 7.5 6.9Z"/></svg>'
G = ('<svg viewBox="0 0 48 48" width="{s}" height="{s}"><path fill="#4285F4" d="M45.1 24.5c0-1.6-.1-2.8-.4-4.1H24v7.4h12.1c-.2 1.8-1.6 4.6-4.5 6.5l6.9 5.3c4.1-3.8 6.6-9.4 6.6-15.1z"/>'
     '<path fill="#34A853" d="M24 46c5.9 0 10.9-2 14.5-5.3l-6.9-5.3c-1.8 1.3-4.3 2.2-7.6 2.2-5.8 0-10.7-3.8-12.5-9.1l-7.1 5.5C8 41 15.4 46 24 46z"/>'
     '<path fill="#FBBC05" d="M11.5 28.5c-.5-1.4-.8-2.9-.8-4.5s.3-3.1.7-4.5l-7.1-5.5C2.8 17 2 20.4 2 24s.8 7 2.3 10z"/>'
     '<path fill="#EA4335" d="M24 10.2c4.1 0 6.9 1.8 8.5 3.3l6.2-6C34.9 4 29.9 2 24 2 15.4 2 8 7 4.3 14l7.1 5.5c1.8-5.3 6.8-9.3 12.6-9.3z"/></svg>')
ICO = {  # iconos de linea (restaurante, bar, tienda)
    'rest': '<path d="M14 6v14a4 4 0 0 0 4 4v18M22 6v14a4 4 0 0 1-4 4M18 6v12M34 42V6c-4 2-6 8-6 14 0 3 2 5 6 5"/>',
    'bar': '<path d="M12 8h24l-10 16v14h6M26 38h-10M22 24L12 8"/>',
    'com': '<path d="M10 16h28l-3 24H13zM18 16v-4a6 6 0 0 1 12 0v4"/>',
}
ico = lambda k: f'<svg viewBox="0 0 48 48" width="70" height="70" fill="none" stroke="#E9BC46" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{ICO[k]}</svg>'
CUR = '<svg viewBox="0 0 24 24" width="64" height="64"><path d="M5 3l14 8-6 1.5 3.5 7-2.6 1.3-3.5-7L6 18z" fill="#fff" stroke="#000" stroke-width="1.2" stroke-linejoin="round"/></svg>'

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
{F('Inter', 'inter-latin.woff2', '100 900')}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:transparent;font-family:Inter;color:#EDEDF0;-webkit-font-smoothing:antialiased}}
.abs{{position:absolute}}
#panel{{position:absolute;left:0;top:0;width:1080px;height:960px;overflow:hidden;background:radial-gradient(ellipse 70% 60% at 50% 42%,#15161C 0%,#0B0C10 60%,#07080B 100%)}}
#arco{{position:absolute;left:-200px;right:-200px;top:780px;height:600px;border-radius:50%;border-top:2px solid rgba(233,188,70,.55);
  box-shadow:0 -30px 90px rgba(233,188,70,.18),inset 0 30px 90px rgba(233,188,70,.10)}}
#costura{{position:absolute;left:0;top:958px;width:1080px;height:2px;background:linear-gradient(90deg,transparent,rgba(233,188,70,.7),transparent)}}
.esc{{position:absolute;left:0;top:0;width:1080px;height:960px;opacity:0}}
.tit{{font-size:44px;font-weight:500;letter-spacing:-.5px;color:rgba(237,237,240,.92);text-align:center}}
.peq{{font-size:30px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:rgba(237,237,240,.45)}}
.acento{{color:#E9BC46}}
.rojo{{color:#E5484D}}
.glass{{background:linear-gradient(180deg,rgba(255,255,255,.07),rgba(255,255,255,.03));border:1px solid rgba(255,255,255,.10);border-radius:28px;
  box-shadow:0 30px 80px rgba(0,0,0,.55),inset 0 1px 0 rgba(255,255,255,.08)}}
.brillo{{box-shadow:0 0 0 1px rgba(233,188,70,.55),0 0 60px rgba(233,188,70,.35),0 30px 80px rgba(0,0,0,.6)}}
.st{{width:1em;height:1em;fill:#3A3B42}}
.st.on{{fill:#FBBC04;filter:drop-shadow(0 0 10px rgba(251,188,4,.6))}}
.caret{{color:#E9BC46;font-weight:300}}
#cur{{position:absolute;left:0;top:0;opacity:0;filter:drop-shadow(0 6px 10px rgba(0,0,0,.5));z-index:20}}
/* subtitulos discretos */
#sub{{position:absolute;left:60px;right:60px;text-align:center;font-weight:650;font-size:60px;line-height:1.15;letter-spacing:-.5px;color:#fff;
  text-shadow:0 2px 3px rgba(0,0,0,.6),0 8px 30px rgba(0,0,0,.55)}}
#sub .on{{color:#E9BC46}}
#subfondo{{position:absolute;left:0;right:0;height:260px;background:linear-gradient(180deg,transparent,rgba(0,0,0,.45),transparent);opacity:0}}
#marca{{position:absolute;left:0;right:0;top:92px;text-align:center;font-size:26px;font-weight:600;letter-spacing:.06em;color:rgba(255,255,255,.75)}}
#negro{{position:absolute;inset:0;background:#000;opacity:0}}
</style></head><body>
<div id="panel">
  <div id="arco"></div>
  <img src="{A['logo']}" class="abs" style="left:50%;top:44px;height:34px;transform:translateX(-50%);opacity:.8">

  <!-- 0 · la placa -->
  <div class="esc" id="e_placa">
    <div class="abs" id="placa3d" style="left:300px;top:140px;width:480px;height:480px;transform-style:preserve-3d">
      <div class="abs brillo" style="inset:0;border-radius:26px;overflow:hidden">
        <img src="{A['placa']}" style="width:100%;height:100%;display:block">
        <div id="barrido" class="abs" style="inset:0;background:linear-gradient(110deg,transparent 40%,rgba(255,255,255,.45) 50%,transparent 60%);background-size:260% 100%"></div>
      </div>
    </div>
    <div class="abs tit" id="t_placa" style="left:0;right:0;top:680px"></div>
    <div class="abs" id="anillo" style="left:790px;top:520px;width:170px;height:170px">
      <svg viewBox="0 0 100 100" width="170" height="170"><circle cx="50" cy="50" r="44" fill="rgba(10,11,15,.8)" stroke="rgba(255,255,255,.1)" stroke-width="3"/>
      <circle id="arcoT" cx="50" cy="50" r="44" fill="none" stroke="#E9BC46" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="276" stroke-dashoffset="276" transform="rotate(-90 50 50)"/></svg>
      <div id="num" class="abs" style="inset:0;display:grid;place-items:center;font-size:52px;font-weight:600;color:#fff">0s</div>
    </div>
  </div>

  <!-- 4 · negocios (fila de circulos que se desliza) -->
  <div class="esc" id="e_neg">
    <div class="abs peq" style="left:0;right:0;top:190px;text-align:center">Placas para</div>
    <div class="abs" id="fila" style="left:0;top:330px;width:1080px;height:360px">
      {''.join(f'<div class="abs" id="n{i}" style="left:{130 + i * 290}px;top:0;width:240px;text-align:center"><div class="glass" style="width:190px;height:190px;border-radius:50%;margin:0 auto;display:grid;place-items:center">{ico(k)}</div><div style="margin-top:26px;font-size:36px;font-weight:500">{t}</div></div>' for i, (k, t) in enumerate([('rest', 'Restaurantes'), ('bar', 'Bares'), ('com', 'Comercios')]))}
    </div>
  </div>

  <!-- 9-10 · la placa en la mesa + el movil que llega -->
  <div class="esc" id="e_mesa">
    <div class="abs" id="foto3d" style="left:130px;top:130px;width:470px;height:640px">
      <img src="{A['foto']}" class="brillo" style="width:100%;height:100%;object-fit:cover;border-radius:34px">
    </div>
    <div class="abs" id="movilL" style="left:640px;top:170px;width:300px;height:600px;border-radius:48px;background:#0E0F13;border:1px solid rgba(255,255,255,.14);box-shadow:0 30px 80px rgba(0,0,0,.7);padding:12px">
      <div style="width:100%;height:100%;border-radius:38px;background:linear-gradient(160deg,#1C2233,#0C0F18);display:grid;place-items:center">
        <div style="width:150px;height:150px;border-radius:50%;border:2px solid rgba(233,188,70,.5);display:grid;place-items:center;box-shadow:0 0 50px rgba(233,188,70,.3)">
          <svg viewBox="0 0 48 48" width="80" height="80" fill="none" stroke="#E9BC46" stroke-width="2.4" stroke-linecap="round"><path d="M18 16a12 12 0 0 1 0 16M24 11a19 19 0 0 1 0 26M30 6a26 26 0 0 1 0 36"/></svg></div></div>
    </div>
  </div>

  <!-- 12-13 · la pantalla de Google -->
  <div class="esc" id="e_rev">
    <div class="abs" id="rev3d" style="left:250px;top:110px;width:580px;height:760px">
      <div class="brillo" style="width:100%;height:100%;border-radius:40px;background:#fff;overflow:hidden;color:#202124;font-family:Inter">
        <div style="display:flex;gap:22px;align-items:center;padding:44px 40px 30px;border-bottom:1px solid #eee">{G.format(s=70)}<div><div style="font-size:34px;font-weight:700">Tu negocio</div><div style="font-size:24px;color:#5f6368">Escribe una reseña</div></div></div>
        <div style="text-align:center;font-size:32px;font-weight:600;margin:40px 0 24px">¿Qué te ha parecido?</div>
        <div id="revEst" style="display:flex;justify-content:center;gap:12px;font-size:70px">{EST * 5}</div>
        <div id="revTxt" style="margin:40px 40px 0;border:2px solid #DADCE0;border-radius:18px;min-height:200px;padding:22px;font-size:28px;line-height:1.4;color:#202124"></div>
        <div id="revBtn" style="margin:30px auto 0;width:220px;text-align:center;padding:18px 0;border-radius:40px;background:#E8EAED;color:#9AA0A6;font-weight:700;font-size:28px">Publicar</div>
      </div>
    </div>
  </div>

  <!-- 15 · lo que NO hace falta -->
  <div class="esc" id="e_lista">
    <div class="abs peq" style="left:0;right:0;top:180px;text-align:center">No hace falta</div>
    {''.join(f'<div class="abs" id="l{i}" style="left:0;right:0;top:{310 + i * 150}px;text-align:center"><span style="position:relative;display:inline-block;font-size:56px;font-weight:500">{t}<span class="tach" style="position:absolute;left:-10px;top:52%;height:4px;width:0;background:#E5484D;box-shadow:0 0 18px rgba(229,72,77,.7)"></span></span></div>' for i, t in enumerate(['Descargar nada', 'Instalar una app', 'Buscarte en Google']))}
  </div>

  <!-- 17 · el QR -->
  <div class="esc" id="e_qr">
    <div class="abs brillo" style="left:240px;top:120px;width:600px;height:600px;border-radius:30px;overflow:hidden">
      <img id="qrImg" src="{A['placa']}" style="position:absolute;width:1300px;height:1300px;left:-640px;top:-520px">
      <div id="scan" class="abs" style="left:0;right:0;height:6px;background:#E9BC46;box-shadow:0 0 30px 8px rgba(233,188,70,.6)"></div>
    </div>
    <div class="abs tit" id="t_qr" style="left:0;right:0;top:770px"></div>
  </div>

  <!-- 19-20 · 01 tu logo -->
  <div class="esc" id="e_m1">
    <div class="abs peq" style="left:0;right:0;top:150px;text-align:center"><span class="acento">01</span> — Tu logo, tus colores</div>
    <img id="c1" src="{A['dtarjeta']}" class="abs" style="left:110px;top:300px;width:420px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))">
    <img id="c2" src="{A['dplaca']}" class="abs" style="left:370px;top:260px;width:360px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))">
    <img id="c3" src="{A['dstand']}" class="abs" style="left:720px;top:280px;width:250px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.6))">
    <div id="pill" class="abs brillo" style="left:50%;top:700px;transform:translateX(-50%);padding:18px 40px;border-radius:40px;background:linear-gradient(180deg,#F2CB5C,#C99A22);color:#0A0B0F;font-size:40px;font-weight:700;white-space:nowrap">Diseño gratis</div>
    <div id="okT" class="abs tit" style="left:0;right:0;top:820px;font-size:34px;color:rgba(237,237,240,.6)"></div>
  </div>

  <!-- 21-22 · 02 te ensenamos (orbitas) -->
  <div class="esc" id="e_m2">
    <div class="abs peq" style="left:0;right:0;top:150px;text-align:center"><span class="acento">02</span> — Te enseñamos</div>
    <svg class="abs" style="left:0;top:0" width="1080" height="960"><g id="lineas" stroke="rgba(233,188,70,.5)" stroke-width="2" stroke-dasharray="8 10" fill="none">
      <path id="ln0" d="M230 420 L540 560"/><path id="ln1" d="M850 420 L540 560"/><path id="ln2" d="M540 800 L540 560"/></g></svg>
    {''.join(f'<div class="abs" id="o{i}" style="left:{x - 110}px;top:{y - 110}px;width:220px;height:220px;display:grid;place-items:center;font-size:40px;font-weight:500"><div class="ring abs" style="inset:0;border-radius:50%;border:1.5px dashed rgba(255,255,255,.28)"></div><span style="position:relative">{t}</span></div>' for i, (x, y, t) in enumerate([(230, 420, 'Cuándo'), (850, 420, 'Cómo'), (540, 800, 'Tu equipo')]))}
    <div class="abs" id="m2placa" style="left:390px;top:300px;width:300px;height:300px"><img src="{A['placa']}" class="brillo" style="width:100%;height:100%;border-radius:18px"></div>
    <div class="abs tit" id="t_m2" style="left:0;right:0;top:660px"></div>
    <div class="abs" id="oC" style="left:400px;top:420px;width:280px;height:280px;border-radius:50%;border:2px solid #E9BC46;display:grid;place-items:center;font-size:48px;font-weight:600;color:#E9BC46;background:rgba(233,188,70,.06);box-shadow:0 0 80px rgba(233,188,70,.25)">Reseñas</div>
  </div>

  <!-- 24 · 03 pago unico (boton que brilla) -->
  <div class="esc" id="e_m3">
    <div class="abs peq" style="left:0;right:0;top:150px;text-align:center"><span class="acento">03</span> — Pago único</div>
    <div id="btn" class="abs" style="left:50%;top:380px;transform:translateX(-50%);padding:34px 80px;border-radius:30px;font-size:64px;font-weight:600;color:#fff;white-space:nowrap;
      background:linear-gradient(180deg,#D8AC3A,#9C7414);border:1px solid rgba(255,230,160,.6);box-shadow:0 0 0 1px rgba(233,188,70,.5),0 0 70px rgba(233,188,70,.45),inset 0 2px 0 rgba(255,255,255,.35)">Pago único</div>
    <div class="abs tit" id="t_m3" style="left:0;right:0;top:620px"></div>
  </div>

  <!-- 25 · whatsapp: notificaciones que se apilan -->
  <div class="esc" id="e_wa">
    {''.join(f'<div class="abs glass" id="w{i}" style="left:130px;width:820px;top:{250 + i * 190}px;padding:30px 34px;display:flex;gap:26px;align-items:center"><div style="width:90px;height:90px;border-radius:24px;background:#25D366;flex:none;display:grid;place-items:center"><svg viewBox="0 0 24 24" width="56" height="56"><path fill="#fff" d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2z"/></svg></div><div><div style="font-size:32px;font-weight:650">Juan · PLEA5E <span style="font-weight:400;color:rgba(255,255,255,.45);font-size:26px">ahora</span></div><div style="font-size:32px;color:rgba(255,255,255,.75);margin-top:6px">{t}</div></div></div>' for i, t in enumerate(['¡Hola! Te paso tu diseño 👇', 'Si quieres cambiar algo, me dices']))}
  </div>

  <!-- 28 · comenta PLACA -->
  <div class="esc" id="e_com">
    <div class="abs peq" style="left:0;right:0;top:220px;text-align:center">Comenta</div>
    <div class="abs glass" style="left:120px;width:840px;top:340px;height:170px;display:flex;align-items:center;padding:0 40px;gap:24px">
      <div id="comTxt" style="flex:1;font-size:72px;font-weight:650;letter-spacing:1px"></div>
      <div id="send" style="width:100px;height:100px;border-radius:50%;background:#2A2B31;display:grid;place-items:center">
        <svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg></div>
    </div>
    <div class="abs tit" id="t_com" style="left:0;right:0;top:600px"></div>
  </div>
</div>
<div id="costura"></div>
<div id="subfondo"></div>
<div id="sub"></div>
<div id="marca"><span style="color:#E9BC46">PLEA5E</span>.es</div>
<div id="cur">{CUR}</div>
<div id="negro"></div>
<script>
{MOTION}
const P = {json.dumps(dict(total=P['total'], seg=P['seg'], subs=P['subs']), ensure_ascii=False)};
const K = {json.dumps(K)};
const $ = id => document.getElementById(id);
const {{cl, lerp, ease, p}} = M;
function segAt(t) {{ for (const s of P.seg) if (t < s.t1) return s; return P.seg[P.seg.length - 1]; }}
window.render = function(t) {{
  const s = segAt(t), split = s.lay === 'split', fin = t >= K.fin;
  $('panel').style.opacity = split && !fin ? 1 : 0; $('costura').style.opacity = split && !fin ? 1 : 0;
  $('arco').style.transform = `translateY(${{Math.sin(t * .6) * 8}}px)`;
  // subtitulos
  const pg = fin ? null : P.subs.find(q => t >= q.t0 && t < q.t1);
  const sub = $('sub');
  if (pg) {{
    const y = split ? 990 : 1440; sub.style.top = y + 'px'; $('subfondo').style.top = (y - 80) + 'px'; $('subfondo').style.opacity = 1;
    if (sub.dataset.k != pg.t0) {{ sub.innerHTML = pg.w.map(w => `<span class="w">${{w.w}}</span>`).join(' '); sub.dataset.k = pg.t0; }}
    [...sub.children].forEach((sp, k) => {{ const w = pg.w[k]; const e = ease.outExpo(p(t, w.t0 - .05, .25));
      sp.style.display = 'inline-block'; sp.style.opacity = e; sp.style.filter = `blur(${{(1 - e) * 8}}px)`; sp.style.transform = `translateY(${{(1 - e) * 10}}px)`;
      sp.classList.toggle('on', t >= w.t0 && t < w.t1 + .05); }});
  }} else {{ sub.innerHTML = ''; sub.dataset.k = ''; $('subfondo').style.opacity = 0; }}
  $('marca').style.opacity = fin ? 0 : 1;
  $('negro').style.opacity = fin ? 1 : 0;
  $('cur').style.opacity = 0;

  // 0-1 · placa
  let v = M.blurIO($('e_placa'), t, K.s0, K.s1e);
  if (v.vis) {{ M.tilt($('placa3d'), t, K.s0, {{rx: 26, ry: -34, d: 1.2}});
    $('barrido').style.backgroundPosition = `${{(1 - ((t - K.s0) % 2.4) / 1.4) * 160}}% 0`;
    M.palabras($('t_placa'), 'Reseñas en Google en *10* segundos', t, K.s0 + .3, K.s1e);
    const a = $('anillo'); const k = ease.outExpo(p(t, K.menos, .5)); a.style.opacity = t >= K.menos ? k : 0; a.style.transform = `scale(${{lerp(.7, 1, k)}})`;
    const q = ease.outCubic(p(t, K.menos, 1.2)); $('arcoT').setAttribute('stroke-dashoffset', 276 * (1 - q)); $('num').textContent = Math.round(q * 10) + 's'; }}
  // 4 · negocios
  v = M.blurIO($('e_neg'), t, K.s4, K.s4e);
  if (v.vis) {{ $('fila').style.transform = `translateX(${{(1 - ease.outExpo(p(t, K.s4, 1.2))) * 500 - (t - K.s4) * 12}}px)`;
    [K.rest, K.bares, K.com].forEach((tk, i) => {{ const e = ease.outExpo(p(t, tk - .1, .5)); const n = $('n' + i);
      n.style.opacity = e; n.style.filter = `blur(${{(1 - e) * 12}}px)`; n.style.transform = `translateY(${{(1 - e) * 30}}px) scale(${{lerp(.85, 1, e)}})`; }}); }}
  // 9-10 · mesa + movil
  v = M.blurIO($('e_mesa'), t, K.s9, K.s10e);
  if (v.vis) {{ M.tilt($('foto3d'), t, K.s9, {{rx: 10, ry: 24}});
    const m = $('movilL'); const e = ease.outExpo(p(t, K.acercar - .1, .7));
    m.style.opacity = t >= K.acercar - .1 ? 1 : 0; m.style.filter = `blur(${{(1 - e) * 16}}px)`;
    m.style.transform = `translateX(${{(1 - e) * 500 - e * 60}}px) rotate(${{lerp(18, -8, e)}}deg)`; }}
  // 12-13 · pantalla de Google
  v = M.blurIO($('e_rev'), t, K.s12, K.s13e, {{dy: 60}});
  if (v.vis) {{ M.tilt($('rev3d'), t, K.s12, {{rx: 30, ry: 20, d: 1.3}});
    const u = t - K.s12; const nS = Math.floor(cl((u - 1.0) / 1.0) * 5 + .001);
    [...$('revEst').children].forEach((x, k) => x.classList.toggle('on', k < nS));
    const done = M.teclea($('revTxt'), 'Todo buenísimo y el trato, de 10. ¡Volveremos!', t, K.s12 + 2.2, 17);
    const b = $('revBtn'); b.style.background = done ? '#1A73E8' : '#E8EAED'; b.style.color = done ? '#fff' : '#9AA0A6'; b.style.boxShadow = done ? '0 0 40px rgba(26,115,232,.5)' : 'none'; }}
  // 15 · lista tachada
  v = M.blurIO($('e_lista'), t, K.s15, K.s15e);
  if (v.vis) [K.desc, K.app, K.busc].forEach((tk, i) => {{ const e = ease.outExpo(p(t, tk - .15, .45)); const l = $('l' + i);
    l.style.opacity = e; l.style.filter = `blur(${{(1 - e) * 10}}px)`; l.style.transform = `translateY(${{(1 - e) * 20}}px)`;
    l.querySelector('.tach').style.width = `calc(${{ease.inOutCubic(p(t, tk + .35, .4)) * 100}}% + 20px)`; }});
  // 17 · QR
  v = M.blurIO($('e_qr'), t, K.s17, K.s17e);
  if (v.vis) {{ $('qrImg').style.transform = `scale(${{1 + (t - K.s17) * .05}})`; $('scan').style.top = (Math.abs(Math.sin((t - K.s17) * 2.2)) * 590) + 'px';
    M.palabras($('t_qr'), 'Y si no lee NFC, el *QR*', t, K.s17 + .2, K.s17e); }}
  // 19-20 · 01
  v = M.blurIO($('e_m1'), t, K.s19, K.s20e);
  if (v.vis) {{ [['c1', -12, 0], ['c2', 0, .15], ['c3', 10, .3]].forEach(([id, r, d]) => {{ const e = ease.outExpo(p(t, K.s19 + d, .8)); const c = $(id);
      c.style.opacity = e; c.style.transform = `translateY(${{(1 - e) * -420}}px) rotate(${{r + (1 - e) * 25}}deg)`; }});
    const g = ease.back(p(t, K.gratis - .05, .45)); $('pill').style.opacity = t >= K.gratis - .05 ? 1 : 0; $('pill').style.transform = `translateX(-50%) scale(${{lerp(.6, 1, g)}})`;
    M.palabras($('okT'), 'Nada se imprime sin tu *OK*', t, K.impr, K.s20e); }}
  // 21-22 · 02 orbitas
  v = M.blurIO($('e_m2'), t, K.s21, K.s22e);
  if (v.vis) {{ const sal = K.cuando - .15;
    const mp = M.blurIO($('m2placa'), t, K.s21, sal, {{dy: 30}}); M.palabras($('t_m2'), 'No solo *una* *placa*', t, K.s21 + .2, sal);
    [K.cuando, K.como, K.equipo].forEach((tk, i) => {{ const e = ease.outExpo(p(t, tk - .1, .5)); const o = $('o' + i);
      o.style.opacity = e; o.style.transform = `scale(${{lerp(.6, 1, e)}})`; o.querySelector('.ring').style.transform = `rotate(${{(t - K.s21) * (i % 2 ? -14 : 14)}}deg)`;
      const ln = $('ln' + i); ln.style.opacity = ease.outCubic(p(t, tk + .1, .4)); ln.style.strokeDashoffset = -(t * 40); }});
    const c = ease.back(p(t, K.resenas - .1, .5)); $('oC').style.opacity = t >= K.resenas - .1 ? 1 : .0; $('oC').style.transform = `scale(${{lerp(.5, 1, c)}})`; }}
  // 24 · 03 boton
  v = M.blurIO($('e_m3'), t, K.s24, K.s24e);
  if (v.vis) {{ const tc = K.unica + .3; M.cursor($('cur'), t, K.s24 + .2, [980, 900], [590, 470], tc);
    const pr = Math.abs(t - tc) < .12 ? .95 : 1; const glow = t >= tc ? 1 : .5;
    $('btn').style.transform = `translateX(-50%) scale(${{pr}})`; $('btn').style.boxShadow = `0 0 0 1px rgba(233,188,70,.5),0 0 ${{70 + glow * 60}}px rgba(233,188,70,${{.3 + glow * .3}}),inset 0 2px 0 rgba(255,255,255,.35)`;
    M.palabras($('t_m3'), 'La pagas una vez. Es *tuya.*', t, tc + .1, K.s24e); }}
  // 25 · whatsapp
  v = M.blurIO($('e_wa'), t, K.s25, K.s25e);
  if (v.vis) [0, 1].forEach(i => {{ const e = ease.outExpo(p(t, K.s25 + .15 + i * .7, .6)); const w = $('w' + i);
    w.style.opacity = e; w.style.transform = `translateY(${{(1 - e) * -120}}px) scale(${{lerp(.9, 1, e)}})`; w.style.filter = `blur(${{(1 - e) * 10}}px)`; }});
  // 28 · comenta
  v = M.blurIO($('e_com'), t, K.s28, K.s28e);
  if (v.vis) {{ const ok = M.teclea($('comTxt'), 'PLACA', t, K.s28 + .25, 9); const tc = K.s28 + 1.0;
    M.cursor($('cur'), t, K.s28 + .45, [1000, 900], [860, 410], tc);
    $('send').style.background = t >= tc ? '#E9BC46' : '#2A2B31'; $('send').style.boxShadow = t >= tc ? '0 0 50px rgba(233,188,70,.6)' : 'none';
    M.palabras($('t_com'), 'y te mando *tu* *diseño*', t, tc, K.s28e + 3); }}
}};
window.LISTO = true;
</script></body></html>'''
open('capa.html', 'w').write(html)
print('capa.html', len(html) // 1024, 'KB')
