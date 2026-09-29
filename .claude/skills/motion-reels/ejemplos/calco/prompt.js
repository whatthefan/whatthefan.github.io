// prompt.js — la barra de prompt del vídeo (texto mono que se escribe, palabra actual en oro, panel de probabilidades, datos debajo)
import { THREE, E, p, cl, panel } from './core.js';
const GOLD = '#F2C14E', GOLDs = 'rgba(242,193,78,';
const mono = (g, s, x, y, c, f) => { g.font = f; g.fillStyle = c; g.fillText(s, x, y); };
/* PAL: [[palabra, t0, [[candidata, prob], ...]], ...]; o: {num, temp, pie, ctx, x0} */
export function barraPrompt(escena, PAL, o = {}) {
  const g = new THREE.Group(); escena.add(g);
  const banda = new THREE.Mesh(new THREE.PlaneGeometry(40, 1.25), new THREE.MeshBasicMaterial({ color: 0x0b0b0c, transparent: true, opacity: .85, depthWrite: false })); banda.position.set(0, 0, -.01); banda.renderOrder = -1; g.add(banda);
  const txt = panel(3200, 170, .95); txt.mesh.position.set(4.6 + (o.x0 ?? -4.3) + 4.3, 0, 0); g.add(txt.mesh);
  const auto = panel(760, 300, 1.45); g.add(auto.mesh); const info = panel(900, 180, .85); g.add(info.mesh); const ctx = panel(700, 120, .55); g.add(ctx.mesh);
  const x0 = o.x0 ?? -4.3, CH = 58; [txt, auto, info, ctx].forEach(q => q.mesh.renderOrder = 2);
  const pinta = t => {
    let vis = ''; PAL.forEach(([w, t0]) => { if (t < t0) return; const n = Math.floor(cl((t - t0) * 22, 0, w.length)); vis += w.slice(0, n) + (n === w.length ? ' ' : ''); });
    const cur = PAL.filter(w => t >= w[1]).pop(), finX = x0 + (vis.length + 2) * .32;
    const vuela = o.vuela ? o.vuela(t) : 0;   // letras que se sueltan (escena «no te olvides»)
    txt.pinta(vis + Math.floor(t * 3) % 2 + Math.floor(vuela * 30), gg => { gg.font = '500 96px M'; let x = 60; gg.fillStyle = 'rgba(236,232,225,.55)'; gg.fillText('›', x, 118); x += CH * 2;
      const ws = vis.split(' '); let ci = 0; ws.forEach((w, i) => { const ult = i === ws.length - 1 || (i === ws.length - 2 && ws[ws.length - 1] === '');
        [...w].forEach((ch, j) => { const dy = vuela ? Math.sin(ci * 1.7) * 50 * vuela : 0, dx = vuela ? Math.cos(ci * 2.3) * 12 * vuela : 0;
          gg.fillStyle = ult ? GOLD : '#F4F0E8'; gg.shadowColor = GOLD; gg.shadowBlur = ult ? 24 : 0; gg.fillText(ch, x + j * CH + dx, 118 + dy); ci++; });
        if (ult && w) { gg.shadowBlur = 0; gg.fillStyle = GOLDs + '.8)'; gg.fillRect(x, 140, w.length * CH, 5); } x += (w.length + 1) * CH; });
      gg.shadowBlur = 0; if (Math.floor(t * 3) % 2) { gg.fillStyle = GOLD; gg.fillRect(x - CH + 4, 40, 6, 96); } });
    auto.mesh.position.set(finX - .6, 1.6, 0); auto.mesh.material.opacity = cl((t - PAL[0][1] + .3) * 4) * (o.fin ? 1 - p(t, o.fin, .3) : 1);
    auto.pinta(cur ? cur[0] : '', gg => { gg.fillStyle = 'rgba(11,11,12,.85)'; gg.fillRect(0, 0, 760, 300); gg.strokeStyle = 'rgba(236,232,225,.25)'; gg.strokeRect(1, 1, 758, 298);
      mono(gg, 'p( siguiente | contexto )', 20, 36, 'rgba(236,232,225,.55)', '400 24px M'); mono(gg, 'muestreada', 590, 36, 'rgba(236,232,225,.45)', '400 22px M');
      (cur ? cur[2] : [['…', 0]]).forEach(([w, pr], i) => { const y = 84 + i * 52; if (!i) { gg.fillStyle = 'rgba(242,193,78,.12)'; gg.fillRect(8, y - 34, 744, 46); }
        mono(gg, (i ? '  ' : '▸ ') + w, 20, y, i ? 'rgba(236,232,225,.6)' : GOLD, '400 28px M'); gg.fillStyle = i ? 'rgba(236,232,225,.35)' : GOLD; gg.fillRect(360, y - 18, 280 * pr, 12); mono(gg, pr.toFixed(2).replace('.', ','), 670, y, i ? 'rgba(236,232,225,.55)' : GOLD, '400 26px M'); }); });
    info.mesh.position.set(x0 + 2.1, -.9, 0); info.pinta(1, gg => { mono(gg, 'PROMPT ' + (o.num || '01'), 0, 40, 'rgba(236,232,225,.8)', '500 30px M'); mono(gg, o.temp || 'T 0,7 · top-p 0,95 · semilla 0x2A', 0, 90, 'rgba(236,232,225,.5)', '400 26px M'); mono(gg, o.pie || 'P(toque) 0,04 · depende del contexto', 0, 140, 'rgba(236,232,225,.5)', '400 26px M'); });
    ctx.mesh.position.set(finX + 1.2, -.9, 0); ctx.mesh.material.opacity = cl((t - PAL[PAL.length - 1][1] + .4) * 3); ctx.pinta(1, gg => { mono(gg, o.ctx || 'CONTEXTO 06 / 8192', 320, 40, 'rgba(236,232,225,.8)', '500 28px M'); mono(gg, '↵ enviar (irreversible)', 310, 90, 'rgba(236,232,225,.45)', '400 24px M'); });
    return finX;
  };
  return { g, pinta };
}
