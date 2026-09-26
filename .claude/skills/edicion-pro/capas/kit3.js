/* kit3.js — sobre kit2: persona recortada (webp con alfa) más lejos, letras por niveles (detrás / delante de la persona),
   pegatinas que se estampan y garabatos en oro. */
K.persona = (dir, N) => { const c = $('persona'); const f = K.filtro(); f.setAttribute('x', '-30%'); f.setAttribute('y', '-30%'); f.setAttribute('width', '160%'); f.setAttribute('height', '160%');
  K._cara = { c, img: c.querySelector('img'), dir, N, fb: f.firstChild, fid: f.id, ext: 'webp' }; };
K.caraFrame = async t => { const C = K._cara, i = Math.max(1, Math.min(C.N, Math.round(t * 30) + 1));
  if (C.img._i !== i) { C.img.src = `${C.dir}/${pad(i)}.${C.ext || 'jpg'}`; try { await C.img.decode(); } catch (e) {} C.img._i = i; } };
/* reparte los bloques de texto en su capa: B.capa = 'detras' | 'delante' (por defecto) */
K.capas = TX => TX.forEach(B => $(B.capa || 'delante').appendChild(B.el));
/* pegatina que se estampa: cae girada, golpea y se asienta */
K.pegatina = (el, t, t0, t1, rot = -6) => { if (t < t0 || t >= t1) { el.style.opacity = 0; return; }
  const k = muelle(t, t0, 2.6, .5), sal = ease.inCubic(p(t, t1 - .15, .15));
  el.style.opacity = Math.min(1, p(t, t0, .06) * 2) * (1 - sal);
  el.style.transform = `translateY(${-sal * 40}px) scale(${1.9 - .9 * k}) rotate(${rot + (1 - k) * 14}deg)`;
  el.style.filter = sal > 0 ? `blur(${sal * 12}px)` : ''; };
/* garabato en oro que se dibuja y se borra */
K.garabato = (path, t, t0, t1, d = .4) => { traza(path, t, t0, d); path.style.opacity = t >= t0 && t < t1 ? 1 - p(t, t1 - .15, .15) : 0; };
