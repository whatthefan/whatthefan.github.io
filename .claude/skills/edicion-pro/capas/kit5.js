/* kit5.js — transiciones de editor y cara real a pantalla completa (sobre kit.js + kit2.js). */
const pad4 = i => String(i).padStart(4, '0');
/* cara real: fotogramas del vídeo (ya en espejo); objectPosition por tramo */
K.caraReal = (dir, N) => { K._cf = { img: $('caraF').querySelector('img'), dir, N }; };
K.caraRealFrame = async t => { const C = K._cf, i = Math.max(1, Math.min(C.N, Math.round(t * 30) + 1));
  if (C.img._i !== i) { C.img.src = `${C.dir}/${pad4(i)}.jpg`; try { await C.img.decode(); } catch (e) {} C.img._i = i; } };
/* zoom de cara: empuje lento + «punch-in» instantáneo en palabras clave: golpes [[t, escala]] (se queda hasta el final del tramo) */
K.caraZoom = (t, a, b, golpes = [], pos = '50% 38%') => { const img = K._cf.img; img.style.objectPosition = pos;
  let s = 1 + .04 * p(t, a, b - a); golpes.forEach(([tg, e]) => { if (t >= tg && tg >= a && tg < b) s *= e; });
  const [sx, sy] = K.sacude(t, golpes.filter(g => g[0] >= a && g[0] < b).map(g => [g[0], 10]));
  img.style.transform = `translate(${sx}px,${sy}px) scale(${s})`; };

/* ---------- transiciones: devuelven estilo para [saliente, entrante] según k (0→1) ---------- */
/* tinta: manchas que crecen con borde irregular (clip-path con varias subrutas) */
function ruido(a, s) { return Math.sin(a * 3 + s) * .5 + Math.sin(a * 7 + s * 2.3) * .3 + Math.sin(a * 13 + s * .7) * .2; }
K.tinta = (k, semillas = [[300, 700, 1], [760, 1200, 1.3], [520, 400, .8], [180, 1500, .9], [900, 500, .7]]) => {
  let d = ''; semillas.forEach(([cx, cy, f], j) => { const R = Math.max(0, (k * 1.35 - j * .07)) * 1400 * f; if (R <= 1) return;
    for (let i = 0; i <= 48; i++) { const a = i / 48 * Math.PI * 2, r = R * (1 + .16 * ruido(a, j * 5 + k * 3)); d += (i ? 'L' : 'M') + (cx + Math.cos(a) * r).toFixed(1) + ' ' + (cy + Math.sin(a) * r).toFixed(1); } d += 'Z'; });
  return d ? `path('${d}')` : 'circle(0px at 50% 50%)'; };
/* aplica transición de entrada a una escena (el contenedor .esc) en [a, a+d] */
K.entrada = (el, t, a, tipo, d) => { el.style.clipPath = ''; el.style.transform = ''; el.style.filter = ''; el.style.opacity = '';
  if (t >= a + d || t < a) return;
  const k = p(t, a, d);
  if (tipo === 'tinta') el.style.clipPath = K.tinta(ease.inOut(k));
  if (tipo === 'iris') el.style.clipPath = `circle(${ease.inCubic(k) * 1300}px at 50% 48%)`;
  if (tipo === 'latigo') { const e = ease.outExpo(k); el.style.transform = `translateX(${(1 - e) * 1080}px)`; el.style.filter = `blur(${(1 - e) * 28}px)`; }
  if (tipo === 'zoom') { const e = ease.outExpo(k); el.style.transform = `scale(${.72 + .28 * e})`; el.style.filter = `blur(${(1 - e) * 18}px)`; el.style.opacity = Math.min(1, k * 3); }
};
/* capa global para el saliente del látigo / zoom (se dibuja sobre la escena anterior con desenfoque) */
K.efectos = (t, EV) => { // EV: [[t, 'fuga'|'estrobo'|'flash']]
  let fu = 0, es = null;
  EV.forEach(([t0, tipo]) => { const u = t - t0;
    if (tipo === 'fuga' && u > -.1 && u < .45) fu = Math.max(fu, u < .08 ? (u + .1) / .18 : 1 - (u - .08) / .37);
    if (tipo === 'estrobo' && u >= 0 && u < .2) { const f = Math.floor(u * 30); es = ['#fff', '#0b0b0b', '#8f8f8f', '#fff', '#0b0b0b', '#dcdcdc'][f % 6]; } });
  $('fuga').style.opacity = Math.max(0, Math.min(1, fu)); $('fuga').style.transform = `translateX(${(t * 180) % 300 - 150}px)`;
  $('estrobo').style.opacity = es ? 1 : 0; if (es) $('estrobo').style.background = es; };
/* cinético 3D: número/palabra gigante que gira en perspectiva (como el «01» de las referencias) */
K.gira = (el, t, t0, o = {}) => { const { ry = -38, rx = 12, desde = 70 } = o; const k = muelle(t, t0, 1.6, .6), e = ease.outExpo(p(t, t0, .35));
  el.style.opacity = t < t0 ? 0 : e; el.style.transform = `perspective(1400px) rotateY(${ry + (desde) * (1 - k)}deg) rotateX(${rx * (1 - k * .3)}deg) scale(${.8 + .2 * k})`;
  el.style.filter = `blur(${(1 - e) * 16}px)`; };
/* controlador de escenas v5: ESC = [[id, a, b, {ent:'tinta'|'iris'|'latigo'|'zoom'|'corte', d, sal:'blur'|'corte', empuje, golpes}]] */
K.escenas5 = (ESC, t) => {
  ESC.forEach(([id, a, b, o = {}], j) => { const el = $(id), cam = el.firstElementChild, sig = ESC[j + 1], so = sig ? sig[3] || {} : {};
    const pegado = sig && Math.abs(sig[1] - b) < .01, dOut = pegado ? (so.d || .4) : 0;
    const vis = t >= a && t < b + dOut; el.style.display = vis ? 'block' : 'none'; if (!vis) return;
    K.entrada(el, t, a, o.ent || 'corte', o.d || .4);
    const pe = 1 + (o.empuje ?? .035) * ease.outCubic(p(t, a, b - a)); const [sx, sy] = K.sacude(t, (o.golpes || []).map(g => [g, 14]));
    let tr = `translate(${sx}px,${sy}px) scale(${pe})`, fil = '', op = 1;
    if (pegado && t >= b) { const e = ease.inCubic(p(t, b, dOut));
      if (so.ent === 'latigo') { tr = `translateX(${-e * 1080}px) ` + tr; fil = `blur(${e * 30}px)`; }
      if (so.ent === 'zoom') { tr = `scale(${1 + e * .6}) ` + tr; fil = `blur(${e * 20}px)`; op = 1 - e; } }
    if (!pegado && (o.sal || 'blur') === 'blur') { const e = ease.inCubic(p(t, b - .16, .16)); if (e > 0) { tr = `translateY(${-e * 50}px) ` + tr; fil = `blur(${e * 22}px)`; op = 1 - e; } }
    cam.style.transform = tr; cam.style.filter = fil; cam.style.opacity = op; });
  // la cara sale con látigo si la escena siguiente entra con látigo
  const cf = $('caraF'); cf.style.transform = ''; cf.style.filter = '';
  ESC.forEach(([, a, , o = {}], j) => { const prev = ESC[j - 1]; if ((o.ent === 'latigo' || o.ent === 'zoom') && !(prev && Math.abs(prev[2] - a) < .01) && t >= a && t < a + (o.d || .4)) {
    const e = ease.inCubic(p(t, a, o.d || .4)); cf.style.transform = o.ent === 'latigo' ? `translateX(${-e * 1080}px)` : `scale(${1 + e * .6})`; cf.style.filter = `blur(${e * 26}px)`; } });
};
