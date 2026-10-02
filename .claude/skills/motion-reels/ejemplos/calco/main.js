// main.js — registro de escenas. Cada sección exporta [{t0, t1, frame(t) -> {escena, cam, post} | null, dom}]
import { draw, THREE, W, H } from './core.js';
await document.fonts.ready; await Promise.all(['800 20px A', '900 20px A', '700 20px N', '20px M', '500 20px M', 'italic 20px G', '20px G', '500 20px I', '700 20px C', '600 20px A', '700 20px A', '500 20px A'].map(f => document.fonts.load(f)));
const SEC = ['secA', 'secB', 'secC', 'secD', 'secE', 'secF'];   // se añaden secciones según se construyen
const ESC = [];
for (const s of SEC) { const m = await import('./' + s + '.js'); ESC.push(...(await m.default())); }
window.TOTAL = +(new URLSearchParams(location.search).get('total') || 157);
const GD = document.getElementById('granoDom'), VD = document.getElementById('vinDom'), GDc = GD.getContext('2d');
const GRN = [...Array(6)].map(() => { const d = GDc.createImageData(960, 540); for (let i = 0; i < d.data.length; i += 4) { const v = Math.random() * 255; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; } return d; });
const vacia = new THREE.Scene(), camV = new THREE.PerspectiveCamera();
const FB = [[155.3, 134.8], [155.5, 3.9], [155.7, 43.9], [155.9, 28.9], [156.1, 62.3]];
window.render = async t0 => { let t = t0;
  if (t0 >= 155.3 && t0 < 156.3) { const f = FB.filter(x => t0 >= x[0]).pop(); t = f[1] + (t0 - f[0]); }
  if (t0 >= 156.3) t = 999;
  let r = null, dom = false;
  for (const e of ESC) { const on = t >= e.t0 && t < e.t1; if (e.dom) e.dom.style.display = on ? 'block' : 'none'; if (on) { if (e.dom) dom = true; const x = await e.frame(t); if (x) r = x; } }
  GD.style.display = VD.style.display = dom ? 'block' : 'none'; if (dom) GDc.putImageData(GRN[Math.floor(t * 30) % 6], 0, 0);
  if (r) draw(r.escena, r.cam, t, r.post || {}); else draw(vacia, camV, t, { fondo: 0x0a0a0b });
};
await window.render(0); window.LISTO = true;
