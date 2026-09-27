/* fx.js — cada SFX lleva su efecto visual. FX = [{t, v, s, db, dur, dir}]
   v: 'whip' (barrido lateral con desenfoque de movimiento), 'flash' (flash de cámara), 'glitch' (RGB + franjas),
      'riser' (tensión: zoom lento + temblor creciente + oscurecer, d = duración), 'impacto' (sacudida + punch),
      'zoomdig' (zoom digital a saltos), null (solo sonido). s/db/dur → mezcla (se leen desde Python). */
(function () {
  const svg = `<svg width="0" height="0" style="position:absolute"><defs>
   <filter id="mb" x="-10%" y="0" width="120%" height="100%"><feGaussianBlur id="mbB" stdDeviation="0 0"/></filter>
   <filter id="gl" x="-5%" y="0" width="110%" height="100%" color-interpolation-filters="sRGB">
    <feTurbulence id="glT" type="fractalNoise" baseFrequency="0.00001 0.035" numOctaves="1" seed="1" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" id="glD" scale="0" xChannelSelector="R" yChannelSelector="G" result="d"/>
    <feColorMatrix in="d" type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="r"/><feOffset in="r" id="glR" dx="0" result="r2"/>
    <feColorMatrix in="d" type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 1 0" result="gb"/><feOffset in="gb" id="glB" dx="0" result="gb2"/>
    <feBlend in="r2" in2="gb2" mode="screen"/></filter></defs></svg>`;
  document.body.insertAdjacentHTML('beforeend', svg +
    '<div id="fxOsc" style="position:absolute;inset:0;z-index:18;pointer-events:none;opacity:0;background:radial-gradient(ellipse 75% 60% at 50% 50%,transparent 30%,#000 100%)"></div>' +
    '<div id="fxFlash" style="position:absolute;inset:0;z-index:19;pointer-events:none;opacity:0;background:#fff"></div>');
})();
function fxRender(t) {
  const { p, ease } = E; let tx = 0, ty = 0, sc = 1, bx = 0, gl = 0, fl = 0, dk = 0;
  for (const f of FX) { const u = t - f.t, dir = f.dir || 1;
    if (f.v === 'whip' && u > -.14 && u < .2) { // sale lo viejo hacia un lado, entra lo nuevo desde el otro
      if (u < 0) { const k = ease.inCubic((u + .14) / .14); tx -= dir * k * 240; bx += k * 70; sc *= 1 + .28 * k; }
      else { const k = 1 - ease.outCubic(u / .2); tx += dir * k * 240; bx += k * 70; sc *= 1 + .28 * k; } }
    if (f.v === 'flash' && u > -.03 && u < .4) { fl = Math.max(fl, u < 0 ? 1 + u / .03 : Math.exp(-u * 13)); if (u > 0) sc *= 1 + .08 * Math.exp(-u * 8); }
    if (f.v === 'glitch' && u > -.08 && u < .26) gl = Math.max(gl, 1 - Math.abs(u - .04) / .22);
    if (f.v === 'riser') { const d = f.d || 1.4; if (u > -d && u < 0) { const k = (u + d) / d, a = 7 * k * k * k; sc *= 1 + .06 * ease.inCubic(k); dk = Math.max(dk, .45 * k); tx += Math.sin(t * 93) * a; ty += Math.cos(t * 71) * a; } }
    if (f.v === 'impacto' && u >= 0 && u < .55) { const e = Math.exp(-u * 8) * (f.a || 30); tx += Math.sin(u * 80) * e; ty += Math.cos(u * 64) * e * .8; sc *= 1 + .06 * Math.exp(-u * 7); gl = Math.max(gl, .6 * Math.exp(-u * 16)); fl = Math.max(fl, .35 * Math.exp(-u * 20)); }
    if (f.v === 'zoomdig' && u >= 0 && u < .5) { const st = Math.min(2, Math.floor(u / .11)); sc *= 1 + .05 * (st + 1) * (1 - ease.inOut(p(t, f.t + .36, .14))); }
  }
  const el = document.getElementById('todo'); el.style.transform = `translate(${tx}px,${ty}px) scale(${sc})`;
  const fs = [];
  if (bx > .5) { document.getElementById('mbB').setAttribute('stdDeviation', `${bx} 0`); fs.push('url(#mb)'); }
  if (gl > .02) { const s = Math.floor(t * 30); document.getElementById('glT').setAttribute('seed', s % 97 + 1);
    document.getElementById('glD').setAttribute('scale', 140 * gl); document.getElementById('glR').setAttribute('dx', 22 * gl * (s % 2 ? 1 : -1)); document.getElementById('glB').setAttribute('dx', -22 * gl * (s % 2 ? 1 : -1)); fs.push('url(#gl)'); }
  el.style.filter = fs.join(' ');
  document.getElementById('fxFlash').style.opacity = fl; document.getElementById('fxOsc').style.opacity = dk;
}
