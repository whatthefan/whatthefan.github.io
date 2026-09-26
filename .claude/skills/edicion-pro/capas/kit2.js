/* kit2.js — sobre kit.js: cara en tarjeta (fotogramas reales), transiciones de escena, desenfoque de movimiento,
   sacudidas, chispas, subrayado en oro y palabra grande que golpea. render(t) puede ser async. */
const pad = i => String(i).padStart(4, '0');
/* ---------- cara en tarjeta ---------- */
K.cara = (dir, N) => { const c = $('cara');
  const f = K.filtro(); f.setAttribute('x', '-30%'); f.setAttribute('y', '-30%'); f.setAttribute('width', '160%'); f.setAttribute('height', '160%');
  K._cara = { c, img: c.firstChild, dir, N, fb: f.firstChild, fid: f.id }; };
K.caraFrame = async t => { const C = K._cara, i = Math.max(1, Math.min(C.N, Math.round(t * 30) + 1));
  if (C.img._i !== i) { C.img.src = `${C.dir}/${pad(i)}.jpg`; try { await C.img.decode(); } catch (e) {} C.img._i = i; } };
/* tramos de cara = huecos entre escenas; entrada con muelle, salida «a través» (zoom + desenfoque) */
K.caraPinta = (t, ESC, TOTAL, golpes = []) => {
  const C = K._cara; let tramo = null, ini = 0;
  const cortes = ESC.map(e => [e[1], e[2]]).sort((a, b) => a[0] - b[0]);
  for (const [a, b] of cortes) { if (t < a) { tramo = [ini, a]; break; } ini = Math.max(ini, b); }
  if (!tramo) tramo = [ini, TOTAL + 1];
  if (ESC.some(([, a, b]) => t >= a && t < b)) { C.c.style.display = 'none'; return false; }
  C.c.style.display = 'block';
  const [a, b] = tramo, ent = a > 0.05 ? muelle(t, a, 2.2, .62) : 1, kb = a > 0.05 ? ease.outExpo(p(t, a, .3)) : 1;
  const sal = b < TOTAL ? ease.inCubic(p(t, b - .16, .16)) : 0;
  let s = (.84 + .16 * ent) * (1 + .22 * sal), y = (1 - ent) * 120 - sal * 30;
  golpes.forEach(([tg, amp]) => { s *= golpe(t, tg, amp); });
  const [sx, sy] = K.sacude(t, golpes.map(g => [g[0], g[1] * 260]));
  C.c.style.transform = `translate(${sx}px,${y + sy}px) scale(${s}) rotate(${(1 - ent) * -2.5}deg)`;
  const bl = (1 - kb) * 14 + sal * 22; C.fb.setAttribute('stdDeviation', `${bl * .4} ${bl}`);
  C.c.style.filter = bl > .3 ? `url(#${C.fid})` : ''; C.c.style.opacity = Math.min(kb * 1.4, 1) * (1 - sal * .6);
  C.img.style.transform = `scale(${1 + .06 * p(t, a, Math.min(4, b - a))})`;
  return true;
};
/* ---------- escenas: entrada zoom / látigo, salida desenfoque vertical o látigo ---------- */
K.escenas2 = (ESC, t) => {
  ESC.forEach(([id, a, b]) => { $(id).style.display = t >= a && t < b ? 'block' : 'none'; });
  ESC.forEach(([id, a, b, o = {}], j) => { if (t < a || t >= b) return;
    const el = $(id), cam = el.firstElementChild; if (!el._f) { el._f = K.filtro(); el._f.setAttribute('x', '-10%'); el._f.setAttribute('y', '-30%'); el._f.setAttribute('width', '120%'); el._f.setAttribute('height', '160%'); }
    const prev = ESC[j - 1], sig = ESC[j + 1];
    const latIn = prev && Math.abs(prev[2] - a) < .01, latOut = sig && Math.abs(sig[1] - b) < .01;
    const ki = ease.outExpo(p(t, a, latIn ? .32 : .42)), ko = ease.inCubic(p(t, b - .16, .16));
    let tr = '', blY = 0, blX = 0, op = 1;
    if (latIn) { tr += `translateY(${(1 - ki) * 700}px)`; blY += (1 - ki) * 40; }
    else { tr += `scale(${1 + .16 * (1 - ki)}) rotate(${(1 - ki) * 1.5}deg)`; blX += (1 - ki) * 12; blY += (1 - ki) * 12; op = Math.min(1, ki * 2.2); }
    if (latOut) { tr += ` translateY(${-ko * 700}px)`; blY += ko * 40; }
    else if (o.suave !== false) { tr += ` translateY(${-ko * 40}px)`; blY += ko * 30; op *= 1 - ko; }
    const pe = 1 + (o.empuje ?? .04) * ease.outCubic(p(t, a, b - a));
    const [sx, sy] = K.sacude(t, (o.golpes || []).map(g => [g, 14]));
    cam.style.transform = `${tr} translate(${sx}px,${sy}px) scale(${pe})`;
    el._f.firstChild.setAttribute('stdDeviation', `${blX} ${blY}`);
    cam.style.filter = blX + blY > .3 ? `url(#${el._f.id})` : ''; cam.style.opacity = op;
  });
};
/* sacudida amortiguada: lista [[t0, amplitud px]] → [dx, dy] */
K.sacude = (t, L) => { let x = 0, y = 0; L.forEach(([t0, a]) => { const u = t - t0; if (u < 0 || u > .5) return; const e = Math.exp(-u * 9) * a;
  x += Math.sin(u * 75) * e * .6; y += Math.cos(u * 61) * e; }); return [x, y]; };
/* desenfoque de movimiento: pos(t) → [x,y]; aplica translate + blur direccional según velocidad */
K.mueve = (el, t, pos, extra = '') => { if (!el._f) { el._f = K.filtro(); el._f.setAttribute('x', '-60%'); el._f.setAttribute('y', '-60%'); el._f.setAttribute('width', '220%'); el._f.setAttribute('height', '220%'); }
  const [x, y] = pos(t), [x0, y0] = pos(t - 1 / 30), vx = Math.abs(x - x0), vy = Math.abs(y - y0);
  el.style.transform = `translate(${x}px,${y}px)` + extra;
  el._f.firstChild.setAttribute('stdDeviation', `${Math.min(vx * .35, 30)} ${Math.min(vy * .35, 30)}`);
  el.style.filter = vx + vy > 3 ? `url(#${el._f.id})` : ''; };
/* chispas: estallido radial con gravedad */
K.chispas = (cont, t, t0, o = {}) => { const { x = 540, y = 960, n = 14, v = 520, clase = 'chispa', d = .7, g = 900, sem = 1 } = o;
  const key = '_ch' + t0; if (!cont[key]) { cont[key] = [...Array(n)].map((_, i) => { const e = document.createElement('div'); e.className = clase;
      const r = Math.sin(i * 12.9898 * sem + t0 * 78.233) * 43758.5453; const f = r - Math.floor(r);
      e._a = (i / n) * Math.PI * 2 + f * .5; e._v = v * (.55 + .6 * f); e._s = .6 + .8 * ((f * 7) % 1); cont.appendChild(e); return e; }); }
  cont[key].forEach(e => { const u = t - t0; if (u < 0 || u > d) { e.style.opacity = 0; return; }
    const px = x + Math.cos(e._a) * e._v * u, py = y + Math.sin(e._a) * e._v * u + g * u * u / 2;
    e.style.opacity = 1 - u / d; e.style.left = px + 'px'; e.style.top = py + 'px'; e.style.transform = `scale(${e._s * (1 - u / d * .6)})`; }); };
/* ---------- texto v2: palabra grande que golpea + subrayado a mano en las de oro ---------- */
K.textos2 = TX => { K.textos(TX); TX.forEach(B => B.el.querySelectorAll('.b .w.oro').forEach(w => w.insertAdjacentHTML('beforeend', '<i class="subraya"></i>'))); };
K.texto2 = (B, t) => { K.texto(B, t); if (B.el.style.display === 'none') return;
  B.el.querySelectorAll('.b .w').forEach(w => { const tw = +w.dataset.t, k = t < tw ? 0 : muelle(t, tw, 2.6, .5);
    w.style.transform = `scale(${1.22 - .22 * k})`;
    const s = w.querySelector('.subraya'); if (s) { const u = ease.outExpo(p(t, tw + .22, .35)); s.style.transform = `scaleX(${u}) rotate(-1.2deg)`; s.style.opacity = u > 0 ? 1 : 0; } }); };
