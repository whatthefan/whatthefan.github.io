/* escena.js — motor de escenas con INTEGRIDAD: cada escena tiene entrada, acción y salida, todo función de t.
   (Se graba fotograma a fotograma con grabar.js, así que nada de setTimeout ni transiciones CSS.)

   Anatomía de una escena (ver SKILL.md, «Anatomía de una escena»):
     entrada 0,3-0,6 s  → los elementos llegan por jerarquía (soporte → objeto → personaje → detalle), 60-90 ms entre ellos
     acción             → UN suceso claro clavado a la palabra (clic, escaneo, cambio de color, burbuja) con
                          anticipación (se encoge 0,08 s) y remate (muelle que se asienta)
     mantenimiento      → cámara que empuja 2-4 % y deriva lenta: nunca congelado
     salida 0,16-0,2 s  → la escena entera sube con desenfoque vertical, o corte seco en el corte de plano   */
const E = (() => {
  const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const p = (t, t0, d) => cl((t - t0) / d);
  const lerp = (a, b, k) => a + (b - a) * k;
  const ease = {
    outExpo: x => x >= 1 ? 1 : 1 - Math.pow(2, -10 * x),
    outCubic: x => 1 - Math.pow(1 - x, 3),
    inCubic: x => x * x * x,
    inOut: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
  };
  /* muelle amortiguado 0→1 (rebasa un poco y se asienta). f: oscilaciones/s, z: amortiguación */
  function muelle(t, t0, f = 2.4, z = .5) {
    const u = t - t0; if (u <= 0) return 0;
    const w = 2 * Math.PI * f, a = z * w, wd = w * Math.sqrt(1 - z * z);
    return 1 - Math.exp(-a * u) * (Math.cos(wd * u) + a / wd * Math.sin(wd * u));
  }
  /* anticipación: se encoge un poco justo antes de la acción y rebota después */
  const golpe = (t, t0, amp = .06) => t < t0 - .08 ? 1 : t < t0 ? 1 - amp * p(t, t0 - .08, .08) : 1 - amp + amp * muelle(t, t0, 3, .45);

  /* entrada genérica: desde {x,y,s,r,blur} con muelle o expo */
  function entra(el, t, t0, o = {}) {
    const { x = 0, y = 40, s = .92, r = 0, blur = 14, tipo = 'expo', d = .5, f = 2.2, z = .55 } = o;
    const k = tipo === 'muelle' ? muelle(t, t0, f, z) : ease.outExpo(p(t, t0, d));
    const kv = ease.outExpo(p(t, t0, .35));
    el.style.opacity = t < t0 ? 0 : kv;
    el.style.filter = blur ? `blur(${(1 - kv) * blur}px)` : '';
    el._base = `translate(${(1 - k) * x}px,${(1 - k) * y}px) scale(${lerp(s, 1, k)}) rotate(${(1 - k) * r}deg)`;
    el.style.transform = el._base + (el._extra || '');
    return k;
  }
  /* cámara de escena: empuje lento + deriva */
  function camara(el, t, t0, t1, o = {}) {
    const { empuje = .035, dx = 0, dy = 0 } = o;
    const k = p(t, t0, t1 - t0);
    el.style.transform = `scale(${1 + empuje * ease.outCubic(k)}) translate(${dx * k}px,${dy * k}px)`;
  }
  /* salida de escena entera: desenfoque vertical (filtro SVG) + sube + se va */
  function salida(el, fb, t, t1, d = .18) {
    const k = ease.inCubic(p(t, t1 - d, d));
    fb.setAttribute('stdDeviation', `0 ${k * 30}`);
    el.style.filter = k > 0 ? `url(#${fb.parentNode.id})` : '';
    el.style.opacity = 1 - k;
    return k;
  }
  /* dibuja un trazo SVG (línea, subrayado, tachado) */
  function traza(path, t, t0, d = .35) {
    if (!path._L) { path._L = path.getTotalLength(); path.style.strokeDasharray = path._L; }
    path.style.strokeDashoffset = path._L * (1 - ease.inOut(p(t, t0, d)));
  }
  /* cursor: recorrido [[t,x,y],…] con inOut entre puntos; clics = [t,…] (se hunde 0,1 s) */
  function cursor(el, t, ruta, clics = []) {
    let x = ruta[0][1], y = ruta[0][2];
    for (let i = 0; i < ruta.length - 1; i++) {
      const [ta, xa, ya] = ruta[i], [tb, xb, yb] = ruta[i + 1];
      if (t >= ta) { const k = ease.inOut(p(t, ta, tb - ta)); x = lerp(xa, xb, k); y = lerp(ya, yb, k); }
    }
    const c = clics.some(tc => t >= tc && t < tc + .1) ? .86 : 1;
    el.style.opacity = t >= ruta[0][0] ? ease.outExpo(p(t, ruta[0][0], .2)) : 0;
    el.style.transform = `translate(${x}px,${y}px) scale(${c})`;
  }
  /* escribe texto letra a letra */
  const teclea = (txt, t, t0, cps = 26) => txt.slice(0, Math.floor(cl((t - t0) * cps, 0, txt.length)));
  /* cambia una imagen por otra (caras del personaje) sin parpadeo: muestra la que toca */
  function caras(imgs, t, cambios) { let i = 0; cambios.forEach((tc, j) => { if (t >= tc) i = j; }); imgs.forEach((im, j) => im.style.opacity = j === i ? 1 : 0); return i; }
  /* flotar suave */
  const flota = (t, fase = 0, amp = 5) => ` translateY(${Math.sin(t * 1.3 + fase) * amp}px)`;
  return { cl, p, lerp, ease, muelle, golpe, entra, camara, salida, traza, cursor, teclea, caras, flota };
})();
