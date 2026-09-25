/* motion.js — primitivas de motion design "premium SaaS" para render(t) fotograma a fotograma.
   Todo es funcion PURA del tiempo t (segundos): nada de setTimeout ni transiciones CSS,
   asi cada fotograma sale igual siempre (se graba con Playwright a 30 fps).            */
const M = (() => {
  const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const lerp = (a, b, k) => a + (b - a) * k;
  const ease = {
    outExpo: x => (x = cl(x)) === 1 ? 1 : 1 - Math.pow(2, -10 * x),
    outCubic: x => 1 - Math.pow(1 - cl(x), 3),
    inOutCubic: x => (x = cl(x)) < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
    inCubic: x => Math.pow(cl(x), 3),
    back: x => { x = cl(x); const c = 1.4; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); },
  };
  // progreso 0..1 de un tramo
  const p = (t, t0, d) => cl((t - t0) / d);

  /* ventana de vida de un elemento: entra (dIn), vive, sale (dOut). Devuelve {vis, kin, kout, u}
     kin: 0->1 al entrar · kout: 0->1 al salir                                              */
  function vida(t, t0, t1, dIn = .45, dOut = .3) {
    return { vis: t >= t0 && t < t1, u: t - t0, kin: ease.outExpo(p(t, t0, dIn)), kout: ease.inCubic(p(t, t1 - dOut, dOut)) };
  }

  /* entrada/salida "premium": desde desenfoque + un poco de escala + un poco de desplazamiento */
  function blurIO(el, t, t0, t1, o = {}) {
    const { dy = 24, s0 = .96, blur = 14, dIn = .5, dOut = .3 } = o;
    const v = vida(t, t0, t1, dIn, dOut);
    if (!v.vis) { el.style.opacity = 0; return v; }
    const k = v.kin * (1 - v.kout);
    el.style.opacity = k;
    el.style.filter = `blur(${(1 - v.kin) * blur + v.kout * blur}px)`;
    el.style.transform = `translateY(${(1 - v.kin) * dy - v.kout * dy * .5}px) scale(${lerp(s0, 1, v.kin) - v.kout * .02})`;
    return v;
  }

  /* texto palabra a palabra: cada palabra aparece desde desenfoque y abajo, en cascada.
     html: palabras separadas por espacio; *palabra* va en color de acento                */
  function palabras(el, html, t, t0, t1, o = {}) {
    const { stagger = .07, dur = .45, blur = 10, dy = 14 } = o;
    if (el.dataset.src !== html) {
      el.dataset.src = html;
      el.innerHTML = html.split(' ').map(w => w.startsWith('*') ? `<span class="w acento">${w.replace(/\*/g, '')}</span>` : `<span class="w">${w}</span>`).join(' ');
    }
    const ws = el.querySelectorAll('.w');
    const out = ease.inCubic(p(t, t1 - .3, .3));
    ws.forEach((w, i) => {
      const k = ease.outExpo(p(t, t0 + i * stagger, dur));
      w.style.display = 'inline-block';
      w.style.opacity = t < t0 || t >= t1 ? 0 : k * (1 - out);
      w.style.filter = `blur(${(1 - k) * blur + out * blur}px)`;
      w.style.transform = `translateY(${(1 - k) * dy}px)`;
    });
  }

  /* barrido con desenfoque de movimiento (whip): el elemento cruza en horizontal */
  function whip(el, t, tMid, dir = 1, dist = 1200, d = .35) {
    const k = p(t, tMid - d / 2, d);
    const x = (ease.inOutCubic(k) - .5) * -dist * dir;
    el.style.transform = `translateX(${x}px)`;
    el.style.filter = `blur(${Math.sin(k * Math.PI) * 18}px)`;
  }

  /* escribe texto letra a letra con cursor parpadeante */
  function teclea(el, txt, t, t0, cps = 14) {
    const n = Math.floor(cl((t - t0) * cps, 0, txt.length));
    const car = Math.floor(t * 2.2) % 2 ? '' : '<span class="caret">|</span>';
    el.innerHTML = txt.slice(0, n) + (t >= t0 - .6 ? car : '');
    return n >= txt.length;
  }

  /* contador numerico */
  const cuenta = (t, t0, d, a, b) => Math.round(lerp(a, b, ease.outCubic(p(t, t0, d))));

  /* cursor: va de A a B y hace "clic" (se encoge) en tClick */
  function cursor(el, t, t0, A, B, tClick) {
    const k = ease.inOutCubic(p(t, t0, .6));
    const c = Math.abs(t - tClick) < .12 ? .82 : 1;
    el.style.opacity = t >= t0 - .1 ? 1 : 0;
    el.style.transform = `translate(${lerp(A[0], B[0], k)}px,${lerp(A[1], B[1], k)}px) scale(${c})`;
    return t >= tClick;
  }

  /* inclinacion 3D suave que se endereza al entrar (pantallas de app) */
  function tilt(el, t, t0, o = {}) {
    const { rx = 18, ry = -22, d = 1.1, flotar = true } = o;
    const k = ease.outExpo(p(t, t0, d));
    const f = flotar ? Math.sin((t - t0) * 1.3) * 1.5 : 0;
    el.style.transform = `perspective(1600px) rotateX(${lerp(rx, 4, k) + f}deg) rotateY(${lerp(ry, -6, k)}deg) translateZ(0)`;
  }

  return { cl, lerp, ease, p, vida, blurIO, palabras, whip, teclea, cuenta, cursor, tilt };
})();
