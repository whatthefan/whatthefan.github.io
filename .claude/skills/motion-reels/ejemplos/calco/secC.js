// secC.js — 38,2 a 60,5 s: láser · senoide «Teníamos buena racha» · PERO AHORA · agujero negro «EL TOQUE / EMPIEZA»
//           · galaxia «Y TÚ ATIENDES, COBRAS, CORRES» · «siento que todo encaja» (partículas → placa) · barrotes «Cliente, por favor, no te vayas» · SUBO/MI en oro
import { THREE, W, H, E, p, cl, lerp, linea, trazar, linea1, chispa, camara, panel, frase, pintaKaraoke, palabra, semilla, rnd } from './core.js';
import { barraPrompt } from './prompt.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { renderer } from './core.js';

const mono = (g, s, x, y, c = 'rgba(236,232,225,.75)', f = '400 26px M') => { g.font = f; g.fillStyle = c; g.fillText(s, x, y); };
const kf = (K, t) => { let i = 0; while (i < K.length - 2 && t >= K[i + 1][0]) i++; const a = K[i], b = K[i + 1], k = E.io(cl((t - a[0]) / (b[0] - a[0] || 1))); return a.slice(1).map((v, j) => lerp(v, b[j + 1], k)); };
/* texto «extruido»: capas del mismo plano hacia atrás, más oscuras */
function extruir(g, capas = 7, prof = .05, lado = 0x6a4a28) {
  g.children.slice().forEach(m => { for (let i = 1; i <= capas; i++) { const c = m.clone(); c.material = m.material.clone(); c.material.color.set(lado); c.userData = Object.assign({}, m.userData, { capa: i }); c.position.z -= i * prof; c.renderOrder = -i; m.parent.add(c); } m.renderOrder = 1; });
}
/* letras en arco (texto curvo 3D): devuelve grupo con letras colocadas sobre un círculo de radio r, desde el ángulo a0 hacia la derecha */
function arco(str, tam, r, a0, o = {}) {
  const g = new THREE.Group(), f = frase([...str].map(c => ({ s: c })), tam, { font: o.font || '900 220px A', letras: 1 });
  let acc = 0; f.children.slice().forEach(m => { const w = m.userData.ink, a = a0 - (acc + w / 2) / r * (o.dir ?? 1); acc += w + tam * .06;
    const piv = new THREE.Group(); piv.position.set(Math.cos(a) * r, Math.sin(a) * r, 0); piv.rotation.z = a - Math.PI / 2 * (o.dir ?? 1); m.position.set(-w / 2, 0, 0); if ((o.dir ?? 1) < 0) m.rotation.z = Math.PI;
    piv.add(m); piv.userData.m = m; g.add(piv); });
  return g;
}

export default async function () {
  /* ================= 1 · láser + senoide (38,2–41,4) ================= */
  const S1 = new THREE.Scene(), C1 = camara(40);
  const rej = new THREE.Group(); S1.add(rej); for (let i = -30; i <= 30; i++) { rej.add(linea1([new THREE.Vector3(i * .5, -9, 0), new THREE.Vector3(i * .5, 9, 0)], 0xffffff, i % 5 ? .12 : .22)); if (Math.abs(i) <= 18) rej.add(linea1([new THREE.Vector3(-15, i * .5, 0), new THREE.Vector3(15, i * .5, 0)], 0xffffff, i % 5 ? .12 : .22)); }
  const onda = n => [...Array(n + 1)].map((_, i) => { const x = -9 + i / n * 18; return new THREE.Vector3(x, 0, .02); });
  const senoPts = onda(600), seno = linea(senoPts, { color: 0xFF9A3A, ancho: 3.2 }); S1.add(seno); const penS = chispa(.8); S1.add(penS);
  const racha = frase([...'Teníamos buena racha'].map(c => ({ s: c })), .42, { letras: 1, font: '500 200px A', stroke: 3, strokeC: '#fff' }); S1.add(racha);
  const rachaF = frase([...'Teníamos buena racha'].map(c => ({ s: c })), .42, { letras: 1, font: '500 200px A' }); S1.add(rachaF);
  const hudS = panel(W, 140, 1.2); S1.add(hudS.mesh);
  // PERO AHORA (3D extruido, la O es un aro con chispa)
  const pero = frase([{ s: 'PERO', t: 41.35 }], .5, { font: '900 220px A' }); pero.position.set(-1.9, 1.15, .2); S1.add(pero);
  const ahora = frase([...'AHORA'].map((c, i) => ({ s: c, t: 41.55 + i * .03 })), 1.25, { font: '900 300px A', letras: 1 }); ahora.position.set(-2.6, -.35, .2); S1.add(ahora); extruir(ahora, 8, .045, 0x7a4d22);
  const chAh = chispa(1.4); S1.add(chAh);
  const f1 = t => {
    const kL = E.oC(p(t, 38.2, .35)); // láser que cruza
    const amp = E.io(p(t, 38.6, .8)) * .55;
    senoPts.forEach((q, i) => { q.y = Math.sin(q.x * 1.6 - t * 2.2) * amp; }); seno.material.opacity = 1 - p(t, 41.3, .2); penS.material.opacity = 1 - p(t, 41.3, .2);
    seno.geometry.setPositions(senoPts.flatMap(v => [v.x, v.y, v.z])); seno.geometry.instanceCount = Math.floor(600 * kL);
    penS.position.set(-9 + 18 * kL, Math.sin((-9 + 18 * kL) * 1.6 - t * 2.2) * amp, .05); penS.visible = kL < 1;
    rej.children.forEach(l => l.material.opacity = (l.userData.o ??= l.material.opacity) * cl((t - 38.5) * 3));
    // letras sobre la onda
    const cab = -5.5 + (t - 38.7) * 3.6; let acc = 0; const inks = racha.children.map(m => m.userData.ink);
    [racha, rachaF].forEach((g, gi) => { acc = 0; g.children.forEach((m, j) => { const x = -6.4 + acc; acc += inks[j] + .02; const y = Math.sin(x * 1.6 - t * 2.2) * amp + .75, y2 = Math.sin((x + .1) * 1.6 - t * 2.2) * amp + .75;
      m.position.set(x, y, .05); m.rotation.z = Math.atan2(y2 - y, .1); const on = x < cab; m.material.opacity = gi ? (on ? E.oC(cl((cab - x) * 2)) : 0) : .3 * cl((t - 38.6) * 3); m.material.color.set(gi ? 0xFF9A3A : 0xFFB27A); }); g.visible = t < 41.5; });
    hudS.mesh.position.set(0, 3.2, 0); hudS.pinta(Math.floor(t * 8), g => { mono(g, 'CH1  0,2 V/div   DC', 40, 40, 'rgba(236,232,225,.6)', '400 24px M'); mono(g, 'CH2  P(toque)  ' + (.04 + (t - 38) * .01).toFixed(2).replace('.', ','), 40, 76, 'rgba(242,170,70,.8)', '400 24px M'); mono(g, '(mudo)', 40, 112, 'rgba(236,232,225,.35)', '400 24px M');
      mono(g, 'M 113,4 ms/div', 1650, 40, 'rgba(236,232,225,.6)', '400 24px M'); mono(g, 'racha 0,62 · estable', 1600, 76, 'rgba(236,232,225,.45)', '400 24px M'); });
    // PERO AHORA
    const kA = t > 41.3; pero.visible = kA; ahora.visible = kA; pintaKaraoke(pero, t, { dim: 0 });
    ahora.children.forEach(m => { const u = m.userData, k = E.oC(p(t, u.it.t, .2)); m.material.opacity = k; if (!u.capa) m.material.color.set(0xF5C79A); m.position.y = (1 - E.oB(p(t, u.it.t, .3))) * -.3; });
    const O = ahora.children[3]; chAh.visible = kA; chAh.position.set(ahora.position.x + O.position.x + O.userData.ink / 2, ahora.position.y + .6, .5); chAh.scale.setScalar(1.2 + .3 * Math.sin(t * 20) + 8 * E.iE(p(t, 41.8, .3)));
    // cámara: fija sobre la onda; en «AHORA» se inclina y se mete en la O
    const kz = E.iE(p(t, 41.75, .3)), k3 = t > 41.3 ? 1 : 0; C1.position.set(lerp(1.4 * k3, chAh.position.x, kz), lerp(-1.0 * k3, chAh.position.y, kz), lerp(9 - k3, .6, kz)); C1.lookAt(lerp(0, chAh.position.x, kz), lerp(.1 * k3, chAh.position.y, kz), 0);
    return { escena: S1, cam: C1, post: { bloom: 1.0, radio: .5, umbral: .55, ca: .004, flash: E.iC(p(t, 41.85, .12)), flashC: 0xFFE8C8 } };
  };

  /* ================= 2 · agujero negro + galaxia (41,95–52,3) ================= */
  const S2 = new THREE.Scene(), C2 = camara(45);
  const pozo = (x, z, f) => -(1.2 + f) * 3 / (1 + (x * x + z * z) / (1.4 + f * .5));
  const malla = new THREE.Group(); S2.add(malla); const LIN = [];
  for (let i = -22; i <= 22; i++) { const a = [], b = []; for (let k = -44; k <= 44; k++) { a.push(new THREE.Vector3(i * .6, 0, k * .3)); b.push(new THREE.Vector3(k * .3, 0, i * .6)); } [a, b].forEach(pts => { const l = linea1(pts, 0xE9E4DA, .5); l.userData.pts = pts; malla.add(l); LIN.push(l); }); }
  const agujero = new THREE.Mesh(new THREE.SphereGeometry(.62, 48, 32), new THREE.MeshBasicMaterial({ color: 0x000000 })); S2.add(agujero);
  const disco = new THREE.Mesh(new THREE.PlaneGeometry(6, 6), new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, uniforms: { t: { value: 0 }, k: { value: 1 } },
    vertexShader: 'varying vec2 v; void main(){ v = uv*2.-1.; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: `uniform float t, k; varying vec2 v; float h(vec2 p){ return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5); }
      float n(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3.-2.*f); return mix(mix(h(i),h(i+vec2(1,0)),f.x), mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x), f.y); }
      void main(){ float r = length(v)*3., a = atan(v.y, v.x); float anillo = exp(-pow((r-.72)*16., 2.)); float halo = exp(-pow((r-.8)*3.2, 2.))*.55;
        float fil = n(vec2(a*8. + t*3. - r*9., r*14.)); float sp = (halo + anillo*1.6) * (.45 + .9*fil);
        vec3 c = mix(vec3(1.,.42,.1), vec3(1.,.86,.62), anillo) * sp * k; c += vec3(1.,.5,.15)*exp(-r*1.4)*.12*k; gl_FragColor = vec4(c * step(.62, r), 1.); }` }));
  disco.renderOrder = 3; disco.material.depthTest = false; S2.add(disco);
  // galaxia de partículas (brazos en espiral)
  semilla(44); const NP = 9000, gp = new Float32Array(NP * 3), gc = new Float32Array(NP * 3), gd = [];
  for (let i = 0; i < NP; i++) { const br = i % 3, r = .7 + Math.pow(rnd(), .7) * 7, a = br * 2.094 + r * .9 + (rnd() - .5) * .5; gd.push([r, a, (rnd() - .5) * .08]); const w = Math.max(0, 1 - r / 7); gc[i * 3] = 1; gc[i * 3 + 1] = .55 + .4 * w; gc[i * 3 + 2] = .25 + .5 * w * w; }
  const gG = new THREE.BufferGeometry(); gG.setAttribute('position', new THREE.BufferAttribute(gp, 3)); gG.setAttribute('color', new THREE.BufferAttribute(gc, 3));
  const galaxia = new THREE.Points(gG, new THREE.PointsMaterial({ size: .045, vertexColors: true, transparent: true, opacity: .9, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false })); S2.add(galaxia);
  // estelas (trazos en espiral) para el «swirl»
  const estelas = new THREE.Group(); S2.add(estelas); for (let i = 0; i < 140; i++) { const r0 = 1 + rnd() * 6.5, a0 = rnd() * 6.283, pts = []; for (let k = 0; k < 24; k++) { const r = r0 - k * .06, a = a0 + k * .09; pts.push(new THREE.Vector3(Math.cos(a) * r, pozo(Math.cos(a) * r, Math.sin(a) * r, 0) * .15 + .02, Math.sin(a) * r)); }
    const l = linea1(pts, rnd() > .6 ? 0xFFB070 : 0xE8E0D2, .35); l.userData.v = .2 + rnd() * .4; estelas.add(l); }
  // EL TOQUE / EMPIEZA en arco
  const arr = arco('EL TOQUE', .62, 1.9, Math.PI * .86); const abj = arco('EMPIEZA', .62, 1.9, Math.PI * 1.22, { dir: -1 }); S2.add(arr, abj);
  [arr, abj].forEach((g, gi) => g.children.forEach((pv, i) => { pv.userData.t0 = (gi ? 44.0 : 42.45) + i * (gi ? .1 : .09); }));
  // gran arco de texto que barre alrededor de la galaxia
  const barrido = [['Y TÚ', 45.55], ['ATIENDES,', 46.1], ['COBRAS,', 47.0], ['CORRES', 47.9]];
  const anillo = new THREE.Group(); S2.add(anillo); let accA = 0; const RA = 3.3;
  barrido.forEach(([w, t0], wi) => { const f = frase([...w].map(c => ({ s: c })), .62, { font: '900 240px A', letras: 1 }); f.children.slice().forEach((m, j) => { const ang = accA / RA; accA += m.userData.ink + .08;
      const pv = new THREE.Group(); pv.position.set(Math.sin(ang) * RA, 0, Math.cos(ang) * RA); pv.rotation.y = ang; m.position.set(0, 0, 0); pv.add(m); pv.userData = { m, t0: t0 + j * .045 }; anillo.add(pv); }); accA += .55; });
  extruir(anillo, 0);
  anillo.children.forEach(pv => { const m = pv.userData.m; for (let i = 1; i <= 6; i++) { const c = m.clone(); c.material = m.material.clone(); c.material.color.set(0x6b5134); c.position.z -= i * .04; c.userData = { capa: i }; pv.add(c); } });
  // «siento que todo encaja»: texto de puntos → placa de puntos
  const puntosTexto = (str, font, ancho, alto, paso) => { const c = document.createElement('canvas'); c.width = ancho; c.height = alto; const g = c.getContext('2d'); g.font = font; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = '#fff'; g.fillText(str, ancho / 2, alto / 2);
    const d = g.getImageData(0, 0, ancho, alto).data, out = []; for (let y = 0; y < alto; y += paso) for (let x = 0; x < ancho; x += paso) if (d[(y * ancho + x) * 4 + 3] > 128) out.push([x - ancho / 2, alto / 2 - y]); return out; };
  const P1 = puntosTexto('siento que todo', '900 150px A', 1500, 220, 3).map(([x, y]) => [x * .0052, y * .0052 + .5]);
  const P2 = puntosTexto('encaja', '900 150px A', 1000, 220, 3).map(([x, y]) => [x * .0052, y * .0052 - .5]);
  const TXT = [...P1, ...P2]; semilla(51);
  // placa de destino: contorno redondeado + icono NFC + QR, en puntos
  const DEST = []; const rr = (x, y) => DEST.push([x, y]);
  for (let i = 0; i < 700; i++) { const k = i / 700 * 4, s = k % 1, lado = Math.floor(k), w = 1.6, h = 1.8; if (lado === 0) rr(-w + 2 * w * s, h); else if (lado === 1) rr(w, h - 2 * h * s); else if (lado === 2) rr(w - 2 * w * s, -h); else rr(-w, -h + 2 * h * s); }
  for (let i = 0; i < 420; i++) { const a = i / 420 * 6.283; rr(-.7 + Math.cos(a) * .5, -.1 + Math.sin(a) * .5); }
  for (let y = 0; y < 9; y++) for (let x = 0; x < 9; x++) if (((x * 7 + y * 13) % 5) < 3 || (x < 3 && y < 3) || (x > 5 && y < 3) || (x < 3 && y > 5)) for (let q = 0; q < 3; q++) rr(.35 + x * .11 + rnd() * .08, .35 - y * .11 - rnd() * .08);
  for (let i = 0; i < 260; i++) rr(-1.2 + i / 260 * 2.4, 1.3);
  const NT = TXT.length, tp = new Float32Array(NT * 3), tG = new THREE.BufferGeometry(); tG.setAttribute('position', new THREE.BufferAttribute(tp, 3));
  const tPts = new THREE.Points(tG, new THREE.PointsMaterial({ size: .03, color: 0xFFD9A0, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, toneMapped: false })); S2.add(tPts);
  const rnds = TXT.map(() => [rnd(), rnd(), rnd()]);
  const CAM2 = [[41.95, 0, 2.2, 3.6, 0, -2.2, 0], [44.9, 0, 1.9, 3.2, 0, -2.3, 0], [45.2, 0, 5.2, 7.4, 0, -.8, 0], [47.2, 1.8, 4.2, 7.0, 0, -.6, 0], [48.6, -1.6, 3.6, 7.2, 0, -.5, 0], [49.3, 0, 3.6, 6.2, 0, 0, 0], [52.3, 0, 3.6, 5.6, 0, 0, 0]];
  const f2 = t => {
    const fz = t < 45 ? 0 : 1; // tras 45 s: la galaxia
    LIN.forEach(l => { const pts = l.userData.pts; pts.forEach(q => q.y = pozo(q.x, q.z, fz * .8) * (t < 45 ? 1 : .45)); l.geometry.setFromPoints(pts); l.material.opacity = .5 * cl((t - 41.95) * 3); });
    agujero.position.set(0, pozo(0, 0, 0) * .75, 0); agujero.visible = t < 45.1; disco.visible = t < 45.1; disco.material.uniforms.t.value = t; disco.material.uniforms.k.value = 1 + .5 * Math.sin(t * 4);
    disco.position.copy(agujero.position); disco.quaternion.copy(C2.quaternion);
    [arr, abj].forEach(g => { g.visible = t < 45.1; g.position.copy(agujero.position).add(new THREE.Vector3(0, 0, .3)); g.quaternion.copy(C2.quaternion);
      g.children.forEach(pv => { const k = E.oC(p(t, pv.userData.t0, .2)); pv.userData.m.material.opacity = k; pv.userData.m.material.color.set(0xF6D5B0); pv.scale.setScalar(.6 + .4 * E.oB(p(t, pv.userData.t0, .3))); }); });
    // galaxia
    const kg = cl((t - 45.2) * 1.5); galaxia.visible = t > 45.1; estelas.visible = t > 45.1;
    gd.forEach(([r, a, h], i) => { const aa = a - (t - 45) * (.5 + .6 / (r + .6)); gp[i * 3] = Math.cos(aa) * r; gp[i * 3 + 1] = pozo(Math.cos(aa) * r, Math.sin(aa) * r, 0) * .15 + h; gp[i * 3 + 2] = Math.sin(aa) * r; });
    gG.attributes.position.needsUpdate = true; galaxia.material.opacity = .9 * kg * (1 - .6 * p(t, 49.0, 1));
    estelas.children.forEach(l => { l.rotation.y = -t * l.userData.v; l.material.opacity = .35 * kg; });
    anillo.visible = t > 45.3 && t < 49.1; anillo.position.set(0, .5, 0); anillo.rotation.set(0, -lerp(-.35, accA / RA - .9, E.io(p(t, 45.4, 3.7))), 0);
    anillo.children.forEach(pv => { const k = E.oC(p(t, pv.userData.t0, .15)); pv.children.forEach(m => { m.material.opacity = k * (m.userData.capa ? .9 : 1); if (!m.userData.capa) m.material.color.set(0xE8C9A6); }); });
    // texto de puntos → placa
    const kx = E.io(p(t, 50.9, 1.1)); tPts.visible = t > 49.0; tPts.material.opacity = cl((t - 49.0) * 3);
    TXT.forEach(([x, y], i) => { const [a, b, c] = rnds[i], d = DEST[i % DEST.length], tur = Math.sin(kx * Math.PI) * 1.4, ap = cl((t - 49.1 - (x + 3.6) * .12) * 4);
      tp[i * 3] = lerp(x, d[0] * 1.1, kx) + (a - .5) * tur + (1 - ap) * (a - .5) * .4; tp[i * 3 + 1] = lerp(y, d[1] * 1.1 + .1, kx) + (b - .5) * tur; tp[i * 3 + 2] = .5 + (c - .5) * tur * 2; });
    tG.attributes.position.needsUpdate = true; tPts.material.size = .022 + .01 * Math.sin(kx * 3.14);
    const [x, y, z, lx, ly, lz] = kf(CAM2, t); C2.position.set(x, y, z); C2.lookAt(lx, ly, lz);
    return { escena: S2, cam: C2, post: { bloom: 1.1, radio: .6, umbral: .5, ca: .005, flash: t < 42.15 ? 1 - (t - 41.95) * 5 : (t > 44.95 && t < 45.3 ? 1 - Math.abs(t - 45.1) * 6 : 0), flashC: t < 42.2 ? 0xFFE8C8 : 0x000000 } };
  };

  /* ================= 3 · barrotes + prompt (52,3–59,0) ================= */
  const S3 = new THREE.Scene(), C3 = camara(40); const pm = new THREE.PMREMGenerator(renderer); S3.environment = pm.fromScene(new RoomEnvironment(), .04).texture;
  const pared = new THREE.Mesh(new THREE.PlaneGeometry(40, 20), new THREE.ShaderMaterial({ vertexShader: 'varying vec2 v; void main(){ v = uv; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }', fragmentShader: 'varying vec2 v; void main(){ float d = length((v-.5)*vec2(2.,1.)); gl_FragColor = vec4(vec3(.16,.155,.15)*(1.-d*.9),1.); }' }));
  pared.position.z = -3; S3.add(pared);
  const barMat = new THREE.MeshStandardMaterial({ color: 0x9a9690, metalness: 1, roughness: .22, envMapIntensity: 1.2 });
  const barras = []; for (let i = -14; i <= 14; i++) { const b = new THREE.Mesh(new THREE.CylinderGeometry(.045, .045, 14, 24), barMat); b.position.set(i * .78, 0, 1.6); S3.add(b); barras.push(b); }
  S3.add(new THREE.AmbientLight(0xffffff, .2)); const luz = new THREE.PointLight(0xffe6c8, 30, 30); luz.position.set(0, 3, 4); S3.add(luz);
  const P3 = barraPrompt(S3, [['Cliente,', 52.9, [['Cliente', .60], ['Señor', .20], ['Oye', .07], ['cariño', .04]]], ['por', 55.3, [['por', .52], ['porfa', .19]]], ['favor,', 55.6, [['favor', .88]]], ['no', 56.3, [['no', .49], ['vuelve', .12]]],
    ['te', 56.6, [['te', .7]]], ['vayas', 57.1, [['vayas', .66], ['olvides', .14], ['enfades', .03]]]], { num: '02', temp: 'T 1,3 · top-p 1,00 · persona: ???', pie: 'P(toque) 0,20 · según el humor', x0: -4.3, fin: 58.9 });
  P3.g.position.set(0, -.3, 0);
  const buen = panel(1400, 90, .4); S3.add(buen.mesh);
  const arcoN = linea([...Array(80)].map((_, i) => { const a = Math.PI * 1.15 + i / 79 * Math.PI * .7; return new THREE.Vector3(Math.cos(a) * 4.6, Math.sin(a) * 1.6 + .9, .2); }), { color: 0xFF8A3A, ancho: 3 }); S3.add(arcoN);
  const f3 = t => {
    const finX = P3.pinta(t);
    const [x, y, z] = kf([[52.3, -3.0, 0, 5.2], [54.8, -1.6, .1, 4.4], [56.5, finX - 3.4, 0, 5.4], [58.0, 1.8, .6, 8.2], [59.0, 1.2, .8, 9.5]], t); C3.position.set(x, y, z); C3.lookAt(x + .4, y - .1, 0);
    buen.mesh.position.set(-.2, -1.75, .1); buen.pinta(Math.floor(t * 30), g => { const s = 'Has sido un buen cliente.', n = Math.floor(cl((t - 57.9) * 30, 0, s.length)); mono(g, s.slice(0, n), 10, 60, 'rgba(236,232,225,.85)', '400 44px M'); });
    trazar(arcoN, E.oC(p(t, 57.7, .6))); arcoN.visible = t > 57.6;
    return { escena: S3, cam: C3, post: { bloom: .8, radio: .5, umbral: .7, ca: .004, fondo: 0x121110, flash: t < 52.45 ? 1 - (t - 52.3) * 6.6 : 0, flashC: 0x000000 } };
  };

  /* ================= 4 · SUBO / MI sobre oro (59,0–60,3) ================= */
  const d4 = document.createElement('div'); d4.className = 'capa'; document.getElementById('ov').appendChild(d4);
  d4.innerHTML = `<div style="position:absolute;inset:0;background:#E9B43A"></div><div id="c_t" style="position:absolute;left:60px;top:60px;font:900 560px/1 A;letter-spacing:-.05em;color:#140f06;white-space:nowrap"></div><div style="position:absolute;left:70px;top:40px;font:400 20px M;color:rgba(20,15,6,.5)">P(toque) ↑</div>`;
  const f4 = t => { const el = d4.querySelector('#c_t'); el.textContent = t < 59.6 ? 'SUBO' : 'MI'; const k = E.oE(p(t, t < 59.6 ? 59.0 : 59.6, .4)); el.style.transform = `translateY(${(1 - k) * 200}px)`; el.style.filter = `blur(${(1 - k) * 12}px)`; el.style.top = t < 59.6 ? '120px' : '260px'; return null; };

  return [{ t0: 38.2, t1: 41.95, frame: f1 }, { t0: 41.95, t1: 52.3, frame: f2 }, { t0: 52.3, t1: 59.0, frame: f3 }, { t0: 59.0, t1: 60.3, frame: f4, dom: d4 }];
}
