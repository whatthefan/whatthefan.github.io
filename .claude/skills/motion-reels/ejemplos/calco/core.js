// core.js — motor del calco: three.js con bloom, aberración cromática, grano, viñeta y una capa DOM encima.
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { Line2 } from 'three/addons/lines/Line2.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';
import { LineGeometry } from 'three/addons/lines/LineGeometry.js';
export { THREE, Line2, LineMaterial, LineGeometry };

export const W = 1920, H = 1080;
export const ORO = 0xE9BC46, ORO2 = 0xFFC75A, CHISPA = 0xFFE3A3, BLANCO = 0xECE8E1;
export const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(0x0a0a0b, 1);
renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.NoToneMapping;
document.getElementById('gl').appendChild(renderer.domElement);

const composer = new EffectComposer(renderer);
const rp = new RenderPass(new THREE.Scene(), new THREE.PerspectiveCamera());
const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), .9, .55, .18);
const post = new ShaderPass({
  uniforms: { tDiffuse: { value: null }, uT: { value: 0 }, uCA: { value: .0035 }, uVig: { value: .55 }, uGrano: { value: .05 }, uFlash: { value: 0 }, uFlashC: { value: new THREE.Color(1, .97, .9) } },
  vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }',
  fragmentShader: `uniform sampler2D tDiffuse; uniform float uT, uCA, uVig, uGrano, uFlash; uniform vec3 uFlashC; varying vec2 vUv;
    float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898,78.233)) + uT*37.1) * 43758.5453); }
    void main(){ vec2 d = vUv - .5; float r = dot(d,d);
      vec3 c; c.r = texture2D(tDiffuse, vUv + d*uCA*(1.+r*4.)).r; c.g = texture2D(tDiffuse, vUv).g; c.b = texture2D(tDiffuse, vUv - d*uCA*(1.+r*4.)).b;
      c = pow(max(c, 0.), vec3(1./2.2));                       // a espacio de pantalla para grano y viñeta
      c *= 1. - uVig * smoothstep(.05, .55, r*1.6);
      c += (h(vUv*vec2(1920.,1080.)) - .5) * uGrano;
      c = mix(c, uFlashC, clamp(uFlash,0.,1.));
      gl_FragColor = vec4(pow(max(c, 0.), vec3(2.2)), 1.); }` });
composer.addPass(rp); composer.addPass(bloom); composer.addPass(post);
export function draw(scene, camera, t, o = {}) {
  rp.scene = scene; rp.camera = camera;
  bloom.strength = (o.bloom ?? .9) * .62; bloom.radius = o.radio ?? .45; bloom.threshold = Math.max(.55, o.umbral ?? .6);
  const u = post.uniforms; u.uT.value = t; u.uCA.value = o.ca ?? .0035; u.uVig.value = o.vig ?? .55; u.uGrano.value = o.grano ?? .05; u.uFlash.value = o.flash ?? 0;
  if (o.flashC) u.uFlashC.value.set(o.flashC).convertLinearToSRGB(); else u.uFlashC.value.setRGB(1, .97, .9);
  renderer.setClearColor(o.fondo ?? 0x0a0a0b, 1);
  const dbg = new URLSearchParams(location.search).get('dbg'); if (dbg) { bloom.enabled = !dbg.includes('b'); post.enabled = !dbg.includes('p'); }
  composer.render();
}

/* ---------- tiempo ---------- */
export const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x)), lerp = (a, b, k) => a + (b - a) * k;
export const p = (t, t0, d) => cl((t - t0) / d);
export const E = {
  oE: x => x >= 1 ? 1 : 1 - Math.pow(2, -10 * x), iE: x => x <= 0 ? 0 : Math.pow(2, 10 * x - 10),
  ioE: x => (x = cl(x)) <= 0 ? 0 : x >= 1 ? 1 : x < .5 ? Math.pow(2, 20 * x - 10) / 2 : (2 - Math.pow(2, -20 * x + 10)) / 2,
  oC: x => 1 - Math.pow(1 - cl(x), 3), iC: x => Math.pow(cl(x), 3), io: x => (x = cl(x)) < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
  oB: x => { x = cl(x); const c = 1.7; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); },
};
export const muelle = (t, t0, f = 2, z = .6) => { const u = t - t0; if (u <= 0) return 0; return 1 - Math.exp(-z * 10 * u) * Math.cos(f * 2 * Math.PI * u); };
let sd = 1; export const semilla = s => sd = s; export const rnd = () => (sd = (sd * 16807) % 2147483647) / 2147483647;

/* ---------- texto a textura (canvas) ----------
   Métricas de fuente fijas (fontBoundingBox) para que todas las palabras compartan línea base.
   escala: unidades de mundo por px de fuente. El plano sale con la línea base en y=0 y el inicio de la tinta en x=0. */
export function texTexto(str, o = {}) {
  const { font = '800 160px A', color = '#ECE8E1', pad = 40, glow = 0, glowC = color, stroke = 0, strokeC = color, ls = 0 } = o;
  const c = document.createElement('canvas'), g = c.getContext('2d'); g.font = font; if (ls) g.letterSpacing = ls + 'px';
  const m = g.measureText(str), asc = m.fontBoundingBoxAscent, des = m.fontBoundingBoxDescent;
  c.width = Math.ceil(m.width + pad * 2); c.height = Math.ceil(asc + des + pad * 2);
  g.font = font; if (ls) g.letterSpacing = ls + 'px'; g.textBaseline = 'alphabetic';
  if (glow) { g.shadowColor = glowC; g.shadowBlur = glow; }
  if (stroke) { g.lineWidth = stroke; g.strokeStyle = strokeC; g.lineJoin = 'round'; g.strokeText(str, pad, pad + asc); }
  else { g.fillStyle = color; g.fillText(str, pad, pad + asc); if (glow) g.fillText(str, pad, pad + asc); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  return { tex: t, w: c.width, h: c.height, asc, des, pad, ink: m.width };
}
/* palabra como plano; e = mundo por px. Origen: inicio de la tinta sobre la línea base */
export function palabra(str, e, o = {}) {
  const r = texTexto(str, o), geo = new THREE.PlaneGeometry(r.w * e, r.h * e);
  geo.translate(r.w * e / 2 - r.pad * e, -(r.h / 2 - r.pad - r.asc) * e, 0);
  const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ map: r.tex, transparent: true, depthWrite: false, toneMapped: false, side: THREE.DoubleSide }));
  m.userData.ink = r.ink * e; m.userData.alto = r.asc * e; return m;
}
/* compat: plano centrado de alto dado */
export function planoTexto(str, alto, o = {}) {
  const r = texTexto(str, o), m = new THREE.Mesh(new THREE.PlaneGeometry(alto * r.w / r.h, alto),
    new THREE.MeshBasicMaterial({ map: r.tex, transparent: true, depthWrite: false, toneMapped: false, side: THREE.DoubleSide }));
  m.userData.ancho = alto * r.w / r.h; return m;
}
/* una línea de palabras (o letras) con sus planos; tam = alto de mayúscula aprox. en mundo */
export function frase(items, tam, o = {}) {
  const font = o.font || '800 200px A', fpx = parseFloat(font.match(/(\d+)px/)[1]), e = tam / (fpx * .72);
  const cv = document.createElement('canvas').getContext('2d'); cv.font = font; if (o.ls) cv.letterSpacing = o.ls + 'px';
  const g = new THREE.Group(); let x = 0; const sp = cv.measureText(' ').width * e;
  items.forEach((it, i) => { const s = typeof it === 'string' ? it : it.s; const m = palabra(s, e, Object.assign({ font, color: '#ffffff', pad: 60 }, o, it.o || {}));
    m.userData.it = typeof it === 'string' ? { s } : it; m.position.x = x; m.userData.x0 = x; g.add(m); x += m.userData.ink + (o.letras ? 0 : sp); });
  g.userData.ancho = o.letras ? x : x - sp;
  if (o.centro) g.children.forEach(m => { m.position.x -= g.userData.ancho / 2; m.userData.x0 = m.position.x; });
  return g;
}
/* karaoke: palabras tenues que se encienden en su t */
export function karaoke(items, tam, o = {}) { return frase(items, tam, o); }
export function pintaKaraoke(g, t, o = {}) {
  const dim = o.dim ?? .13;
  g.children.forEach(m => { const w = m.userData.it, k = E.oC(p(t, w.t ?? 0, .12)), mat = m.material;
    const c = new THREE.Color(w.oro ? (o.oroC ?? 0xF2C14E) : (o.blancoC ?? 0xF1EDE6));
    mat.opacity = (dim + (1 - dim) * k) * (o.op ?? 1); mat.color.copy(new THREE.Color(o.dimC ?? 0x9a948a).lerp(c, k)); });
}
/* ---------- líneas gruesas con brillo ---------- */
const MATS = [];
export function linea(pts, o = {}) {
  if (pts.length < 80) { const q = []; for (let i = 0; i < pts.length - 1; i++) { const n = Math.ceil(80 / (pts.length - 1)); for (let k = 0; k < n; k++) q.push(pts[i].clone().lerp(pts[i + 1], k / n)); } q.push(pts[pts.length - 1].clone()); pts = q; }
  const geo = new LineGeometry(); geo.setPositions(pts.flatMap(v => [v.x, v.y, v.z || 0]));
  const mat = new LineMaterial({ color: o.color ?? ORO, linewidth: o.ancho ?? 2, transparent: true, opacity: o.op ?? 1, depthWrite: false, toneMapped: false, dashed: false });
  mat.resolution.set(W, H); MATS.push(mat);
  const l = new Line2(geo, mat); l.computeLineDistances(); l.userData.n = pts.length; return l;
}
/* muestra solo la fracción k de una línea (trazo que se dibuja) */
export const trazar = (l, k) => { const n = l.userData.n; l.geometry.instanceCount = Math.max(0, Math.floor((n - 1) * cl(k))); };
export const linea1 = (pts, color = 0xffffff, op = .5) => { const g = new THREE.BufferGeometry().setFromPoints(pts); return new THREE.Line(g, new THREE.LineBasicMaterial({ color, transparent: true, opacity: op, depthWrite: false, toneMapped: false })); };
export function rejilla(tam, div, color = 0xffffff, op = .08) {
  const pts = []; const h = tam / 2, s = tam / div;
  for (let i = 0; i <= div; i++) { const q = -h + i * s; pts.push(new THREE.Vector3(q, -h, 0), new THREE.Vector3(q, h, 0), new THREE.Vector3(-h, q, 0), new THREE.Vector3(h, q, 0)); }
  return new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color, transparent: true, opacity: op, depthWrite: false, toneMapped: false }));
}
/* chispa: punto brillante con halo (sprite aditivo) */
let texCh = null;
export function chispa(tam = .3, color = CHISPA) {
  if (!texCh) { const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d'); const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
    gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(.12, 'rgba(255,240,200,.95)'); gr.addColorStop(.35, 'rgba(255,190,80,.35)'); gr.addColorStop(1, 'rgba(255,150,40,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); texCh = new THREE.CanvasTexture(c); }
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: texCh, color, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false })); s.scale.setScalar(tam); return s;
}
export function camara(fov = 35) { return new THREE.PerspectiveCamera(fov, W / H, .01, 500); }

/* ---------- capa DOM ---------- */
export const OV = document.getElementById('ov');
export function capa(html = '', css = '') { const d = document.createElement('div'); d.className = 'capa'; d.style.cssText = css; d.innerHTML = html; OV.appendChild(d); return d; }
export const tipo = (el, s, t0, cps, t, cursor = '▍') => { const n = Math.max(0, Math.min(s.length, Math.floor((t - t0) * cps))); el.textContent = s.slice(0, n) + (cursor && t >= t0 - .2 && (n < s.length || Math.floor(t * 2.5) % 2) ? cursor : ''); return n; };

/* ---------- panel: un canvas 2D dentro del mundo 3D (código, tablas, etiquetas que cambian) ---------- */
export function panel(wpx, hpx, altoMundo, o = {}) {
  const c = document.createElement('canvas'); c.width = wpx; c.height = hpx; const g = c.getContext('2d');
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  const m = new THREE.Mesh(new THREE.PlaneGeometry(altoMundo * wpx / hpx, altoMundo), new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, toneMapped: false, side: THREE.DoubleSide, blending: o.aditivo ? THREE.AdditiveBlending : THREE.NormalBlending }));
  let clave = null;
  return { mesh: m, g, c, pinta(k, fn) { if (k === clave) return; clave = k; g.clearRect(0, 0, wpx, hpx); fn(g); tex.needsUpdate = true; } };
}
/* puntos de un trazado SVG (d) muestreados; transform opcional (x,y,escala) */
export function puntosSVG(d, n = 200, tr = { x: 0, y: 0, s: 1, flipY: true }) {
  const p = document.createElementNS('http://www.w3.org/2000/svg', 'path'); p.setAttribute('d', d);
  const sv = document.createElementNS('http://www.w3.org/2000/svg', 'svg'); sv.appendChild(p); document.body.appendChild(sv);
  const L = p.getTotalLength(), out = [];
  for (let i = 0; i <= n; i++) { const q = p.getPointAtLength(L * i / n); out.push(new THREE.Vector3(tr.x + q.x * tr.s, tr.y + (tr.flipY === false ? q.y : -q.y) * tr.s, 0)); }
  sv.remove(); return out;
}
