/* kit.js — texto, escenas y utilidades comunes para las capas (usa escena.js → E) */
const $ = id => document.getElementById(id);
const { p, ease, muelle, golpe, entra, camara, traza, caras, teclea, flota } = E;
const K = {};
K.filtros = () => { const s = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); s.setAttribute('width', 0); s.setAttribute('height', 0); s.style.position = 'absolute'; s.innerHTML = '<defs id="filtros"></defs>'; document.body.prepend(s); };
let nf = 0;
K.filtro = () => { const f = document.createElementNS('http://www.w3.org/2000/svg', 'filter'); f.id = 'fx' + (nf++);
  f.setAttribute('x', '-20%'); f.setAttribute('y', '-100%'); f.setAttribute('width', '140%'); f.setAttribute('height', '300%');
  f.innerHTML = '<feGaussianBlur stdDeviation="0 0"/>'; $('filtros').appendChild(f); return f; };
/* TX: [{t0,t1,y,c,s:[[palabra,t,clase]],b:[[..]],bs}] */
K.textos = TX => TX.forEach(B => {
  const el = document.createElement('div'); el.className = 'tb ' + (B.c || ''); el.style.top = B.y + 'px';
  const linea = (ws, cls) => '<div class="' + cls + '">' + ws.map(([w, t, x]) => `<span class="w ${x || ''}" data-t="${t}">` + [...w].map(ch => `<span class="l">${ch}</span>`).join('') + '</span>').join(' ') + '</div>';
  el.innerHTML = (B.s && B.s.length ? linea(B.s, 's') : '') + (B.b && B.b.length ? linea(B.b, 'b') : '');
  if (B.bs) el.querySelector('.b').style.fontSize = B.bs + 'px';
  const f = K.filtro(); B.el = el; B.fb = f.firstChild; B.fid = f.id; document.body.appendChild(el);
});
K.texto = (B, t) => {
  const vis = t >= B.t0 - .02 && t < B.t1; B.el.style.display = vis ? 'block' : 'none'; if (!vis) return;
  const k = ease.inCubic(p(t, B.t1 - .16, .16));
  B.fb.setAttribute('stdDeviation', `0 ${k * 26}`); B.el.style.filter = k > 0 ? `url(#${B.fid})` : 'none';
  B.el.style.opacity = 1 - k; B.el.style.transform = `translateY(${-k * 40}px)`;
  B.el.querySelectorAll('.w').forEach(w => { const tw = +w.dataset.t;
    w.querySelectorAll('.l').forEach((l, i) => { const e = ease.outCubic(p(t, tw + i * .018, .24));
      l.style.opacity = e; l.style.filter = `blur(${(1 - e) * 12}px)`; l.style.transform = `translateY(${(1 - e) * 10}px)`; }); });
};
/* escenas: [[id, entra, sale, salidaSuave]] */
K.escenas = (ESC, t) => { let act = null;
  ESC.forEach(([id, a, b]) => { const on = t >= a && t < b; $(id).style.display = on ? 'block' : 'none'; if (on) act = id; });
  ESC.forEach(([id, a, b, suave]) => { if (t >= a && t < b) { const cam = $(id).firstElementChild; camara(cam, t, a, b, { empuje: .035 });
    if (suave) { if (!$(id)._f) $(id)._f = K.filtro(); const k = ease.inCubic(p(t, b - .18, .18)); $(id)._f.firstChild.setAttribute('stdDeviation', `0 ${k * 30}`);
      cam.style.filter = k > 0 ? `url(#${$(id)._f.id})` : ''; cam.style.opacity = 1 - k; } } });
  return act; };
K.destello = (t, t0) => { const u = t - t0; if (u < -.07 || u > .22) return 0; return u < 0 ? ease.outCubic(1 + u / .07) : 1 - ease.outCubic(u / .22); };
K.pop = (el, t, t0, o = {}) => entra(el, t, t0, Object.assign({ y: 30, s: .8, tipo: 'muelle', f: 2.6, z: .55 }, o));
K.tache = (el, t, t0) => { el.style.transform = `scaleX(${ease.outExpo(p(t, t0, .25))})`; el.style.opacity = t >= t0 ? 1 : 0; };
K.pantalla = (img, t, t0, d = .9) => { const PS = ['0', '0.5', '0.7', '0.9', '1.1'], u = p(t, t0, d); img.src = 'pan/pantalla-' + PS[Math.min(4, Math.floor(u * 5))] + '.png'; };
K.anillo = (el, t, t0, x, y) => { const r = p(t, t0, .5), R = 40 + r * 320; Object.assign(el.style, { opacity: t >= t0 && r < 1 ? 1 - r : 0, left: x - R / 2 + 'px', top: y - R / 2 + 'px', width: R + 'px', height: R + 'px' }); };
/* W: palabras con tiempos proporcionales a las letras entre t0 y t1; marca con * las que van en oro, ! en rojo */
K.W = (txt, t0, t1) => { const ws = txt.split(' '), n = ws.reduce((a, w) => a + w.replace(/[*!]/g, '').length + 1, 0); let acc = 0;
  return ws.map(w => { const cls = w.includes('*') ? 'oro' : w.includes('!') ? 'rojo' : ''; const c = w.replace(/[*!]/g, ''); const r = [c, +(t0 + (t1 - t0) * acc / n).toFixed(3), cls]; acc += c.length + 1; return r; }); };
K.estrellas = (el, t, t0, d = .9) => el.querySelectorAll('span').forEach((s, i) => { const u = t0 + i * d / 5; s.classList.toggle('on', t >= u); s.style.transform = `scale(${t >= u ? 1 + .35 * (1 - muelle(t, u, 3, .45)) : 1})`; });
