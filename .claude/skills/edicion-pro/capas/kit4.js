/* kit4.js — FORMATO PLEA5E: collage. Sobre kit.js + kit2.js + kit3.js.
   Reglas de ritmo: entrada ≤ 0,45 s, cada elemento se queda quieto ≥ 1 s antes de salir, máx. 3 elementos por escena. */
K.troquel = () => { $('filtros').insertAdjacentHTML('beforeend',
  `<filter id="troquel" x="-25%" y="-25%" width="150%" height="150%"><feMorphology in="SourceAlpha" operator="dilate" radius="9" result="d"/>
     <feFlood flood-color="#fff"/><feComposite in2="d" operator="in" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
   <filter id="troquelP" x="-10%" y="-10%" width="120%" height="120%"><feMorphology in="SourceAlpha" operator="dilate" radius="7" result="d"/>
     <feFlood flood-color="#fff"/><feComposite in2="d" operator="in" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>`); };
/* pegatina que se «pega»: llega grande y girada, se aplasta contra el papel y se asienta. Sale hacia arriba con desenfoque. */
K.pega = (el, t, t0, t1 = 1e9, o = {}) => { const { rot = -4, desde = 1.35, gira = 10 } = o;
  if (t < t0 || t >= t1) { el.style.opacity = 0; return 0; }
  const k = muelle(t, t0, 2.4, .55), sal = ease.inCubic(p(t, t1 - .18, .18));
  el.style.opacity = Math.min(1, p(t, t0, .08) * 1.5) * (1 - sal);
  el._base = `translateY(${-sal * 60}px) scale(${desde - (desde - 1) * k}) rotate(${rot + (1 - k) * gira}deg)`;
  el.style.transform = el._base + (el._extra || ''); return k; };
/* cinta: aparece estirándose */
K.cinta = (el, t, t0, t1 = 1e9) => { const k = ease.outExpo(p(t, t0, .25)); el.style.opacity = t >= t0 && t < t1 ? 1 - p(t, t1 - .15, .15) : 0;
  el.style.transform = `rotate(${el.dataset.r || -8}deg) scaleX(${k})`; };
/* titular con tiempo mínimo en pantalla: si el bloque dura < 1,1 s se alarga hasta el siguiente */
K.minimo = (TX, min = 1.1) => TX.forEach((B, i) => { if (B.t1 - B.t0 < min) { const sig = TX.slice(i + 1).find(x => (x.capa || 'delante') === (B.capa || 'delante')); B.t1 = Math.min(B.t0 + min, sig ? sig.t0 : B.t0 + min); } });
