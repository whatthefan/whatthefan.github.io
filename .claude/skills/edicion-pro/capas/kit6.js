/* kit6.js — estilo JoeEditor (usa escena.js → E). Todo es función de t (se graba fotograma a fotograma). */
const $ = id => document.getElementById(id);
const { p, ease, muelle, golpe, entra, traza } = E;
const K6 = {};
const pad4 = i => String(i).padStart(4, '0');
/* ---- cara con texto detrás: fondo real (jpg) + persona (webp con alfa) del MISMO fotograma ---- */
K6.cara = (dirFondo, dirPersona, N) => { K6._c = { fondo: $('caraFondo'), blur: $('caraBlur'), pers: $('caraPersona'), dirFondo, dirPersona, N }; };
K6.caraFrame = async (t, pos = '50% 40%') => { const C = K6._c, i = Math.max(1, Math.min(C.N, Math.round(t * 30) + 1));
  
  if (C.fondo._i !== i) { C.fondo.src = C.blur.src = `${C.dirFondo}/${pad4(i)}.jpg`; C.pers.src = `${C.dirPersona}/${pad4(i)}.webp`;
    await Promise.all([C.fondo.decode().catch(() => {}), C.pers.decode().catch(() => {})]); C.fondo._i = i; } };
/* ---- clip de vídeo como secuencia de imágenes: src(i) ---- */
K6.clip = async (img, t, t0, dir, i0, vel = 1, ext = 'jpg') => { const i = i0 + Math.floor((t - t0) * 30 * vel); if (img._i !== i) { img.src = `${dir}/${pad4(i)}.${ext}`; await img.decode().catch(() => {}); img._i = i; } };
/* ---- textos ---- */
K6.nodos = [];
K6.sub = (palabras, t0, t1, y, o = {}) => { // palabras [[texto, t]] ; aparecen una a una con un «pop»
  const el = document.createElement('div'); el.className = 'sub'; el.style.top = y + 'px'; if (o.size) el.style.fontSize = o.size + 'px';
  el.innerHTML = palabras.map(([w, t]) => `<span class="w" data-t="${t}">${w}</span>`).join(' '); $(o.capa || 'delante').appendChild(el);
  K6.nodos.push({ el, t0, t1, tipo: 'sub' }); return el; };
K6.grande = (clase, txt, t0, t1, y, o = {}) => { const el = document.createElement('div'); el.className = clase; el.style.top = y + 'px';
  if (o.size) el.style.fontSize = o.size + 'px'; if (o.color) el.style.color = o.color; if (o.x) el.style.transform = `translateX(${o.x}px)`; el.innerHTML = txt;
  $(o.capa || 'delante').appendChild(el); K6.nodos.push({ el, t0, t1, tipo: clase.split(' ')[0], rot: o.rot || 0, x: o.x || 0 }); return el; };
K6.pintaTextos = t => K6.nodos.forEach(n => { const { el, t0, t1 } = n; const vis = t >= t0 - .01 && t < t1; el.style.display = vis ? 'block' : 'none'; if (!vis) return;
  const sal = ease.inCubic(p(t, t1 - .14, .14));
  if (n.tipo === 'sub') { el.querySelectorAll('.w').forEach(w => { const tw = +w.dataset.t, k = t < tw ? 0 : muelle(t, tw, 3.2, .55), e = ease.outCubic(p(t, tw, .12));
      w.style.opacity = e; w.style.transform = `translateY(${(1 - Math.min(k, 1.1)) * 14}px) scale(${.7 + .3 * k})`; });
    el.style.opacity = 1 - sal; el.style.filter = sal ? `blur(${sal * 14}px)` : ''; return; }
  if (n.tipo === 'script') { // se «escribe»: barrido de izquierda a derecha + ligero giro
    const k = ease.outCubic(p(t, t0, .45)); el.style.clipPath = `inset(-30% ${(1 - k) * 100}% -30% -10%)`;
    el.style.transform = `translateX(${n.x}px) rotate(${n.rot}deg) scale(${1.08 - .08 * ease.outCubic(p(t, t0, .6))})`; el.style.opacity = 1 - sal; el.style.filter = sal ? `blur(${sal * 16}px)` : ''; return; }
  // cond / num: entra desde desenfocado y grande
  const k = muelle(t, t0, 2.2, .7), e = ease.outExpo(p(t, t0, .35));
  el.style.opacity = e * (1 - sal); el.style.filter = `blur(${(1 - e) * 18 + sal * 16}px)`;
  el.style.transform = `translateX(${n.x}px) scale(${1.25 - .25 * Math.min(k, 1.05)}) rotate(${n.rot}deg)`; });
/* ---- fuga de luz (film burn) ---- */
K6.fugaInit = () => { const f = $('fuga'); [['#ff7a18', 70], ['#ffcf6b', 55], ['#ff3d1f', 45], ['#fff3d6', 35]].forEach(([c, s]) => { const i = document.createElement('i'); i.style.background = `radial-gradient(circle,${c},transparent 65%)`; i.style.width = i.style.height = s + '%'; f.appendChild(i); }); };
K6.fuga = (t, lista) => { let op = 0, u0 = 0, sem = 0; lista.forEach(([t0, dur = .5], j) => { const u = (t - t0) / dur; if (u > -.25 && u < 1) { const v = u < .3 ? (u + .25) / .55 : 1 - (u - .3) / .7; if (v > op) { op = v; u0 = u; sem = j; } } });
  const f = $('fuga'); f.style.opacity = Math.max(0, Math.min(1, op * 1.1));
  [...f.children].forEach((i, k) => { const a = sem * 1.7 + k * 2.1; i.style.left = (10 + 50 * (.5 + .5 * Math.sin(a + u0 * 2.2))) + '%'; i.style.top = (5 + 60 * (.5 + .5 * Math.cos(a * 1.3 + u0 * 1.6))) + '%'; }); };
K6.flash = (t, lista) => { let op = 0; lista.forEach(t0 => { const u = t - t0; if (u > -.05 && u < .18) op = Math.max(op, u < 0 ? 1 + u / .05 : 1 - u / .18); }); $('flash').style.opacity = op; };
/* ---- escenas: [id, a, b, {ent: 'corte'|'latigo'|'zoom'|'pip'}] ---- */
K6.escenas = (ESC, t) => ESC.forEach(([id, a, b, o = {}]) => { const el = $(id), on = t >= a && t < b; el.style.display = on ? 'block' : 'none'; if (!on) return;
  const k = p(t, a, o.d || .3), e = ease.outExpo(k); let tr = '', fil = '';
  if (o.ent === 'latigo' && k < 1) { tr = `translateX(${(1 - e) * 900}px)`; fil = `blur(${(1 - e) * 30}px)`; }
  if (o.ent === 'zoom' && k < 1) { tr = `scale(${1.35 - .35 * e})`; fil = `blur(${(1 - e) * 16}px)`; }
  if (o.ent === 'abajo' && k < 1) { tr = `translateY(${(1 - e) * 700}px)`; fil = `blur(${(1 - e) * 24}px)`; }
  const pe = 1 + (o.empuje ?? .04) * p(t, a, b - a); el.style.transform = `${tr} scale(${pe})`; el.style.filter = fil; });
K6.sacude = (t, L) => { let x = 0, y = 0; L.forEach(([t0, a]) => { const u = t - t0; if (u < 0 || u > .45) return; const e = Math.exp(-u * 10) * a; x += Math.sin(u * 80) * e * .6; y += Math.cos(u * 63) * e; }); return `translate(${x}px,${y}px)`; };
