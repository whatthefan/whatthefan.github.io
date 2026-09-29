// secE.js — 96,5 a 126,1 s: placas que llenan la sala · «YA NO QUEDA EXCUSA» · mecha · tesis de ortogonalidad «blues» · torre de bloques
//           · «NFC, QR, SÚPER-DIRECTO» · «SALTÁNDOTE CADA PASO DE MÁS» · «EN CADA MESA DEL BAR» · «el «luego te la dejo» se tuerce» · SUBO MI P(TOQUE)
import { THREE, W, H, E, p, cl, lerp, muelle, linea, trazar, linea1, chispa, camara, panel, frase, pintaKaraoke, semilla, rnd, renderer } from './core.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const kf = (K, t) => { let i = 0; while (i < K.length - 2 && t >= K[i + 1][0]) i++; const a = K[i], b = K[i + 1], k = E.io(cl((t - a[0]) / (b[0] - a[0] || 1))); return a.slice(1).map((v, j) => lerp(v, b[j + 1], k)); };
const OV = document.getElementById('ov');
const capa = html => { const d = document.createElement('div'); d.className = 'capa'; d.innerHTML = html; OV.appendChild(d); return d; };
const mono = (g, s, x, y, c = 'rgba(236,232,225,.75)', f = '400 26px M') => { g.font = f; g.fillStyle = c; g.fillText(s, x, y); };
const tip = (s, t0, cps, t) => s.slice(0, Math.max(0, Math.min(s.length, Math.floor((t - t0) * cps))));
const GOLD = '#F2B640';
/* contorno de placa: rectángulo redondeado + icono NFC (tres arcos) */
function contornoPlaca(w = 2.2, h = 2.5, r = .38, n = 160) { const pts = [], L = 2 * (w + h - 4 * r) + 2 * Math.PI * r; const seg = [];
  const add = (x, y) => pts.push(new THREE.Vector3(x, y, 0)); const hw = w / 2, hh = h / 2;
  for (let i = 0; i <= n; i++) { const s = i / n * L; let q = s; const lados = [[w - 2 * r, (u) => add(-hw + r + u, hh)], [Math.PI * r / 2, u => { const a = Math.PI / 2 - u / r; add(hw - r + Math.cos(a) * r, hh - r + Math.sin(a) * r); }], [h - 2 * r, u => add(hw, hh - r - u)], [Math.PI * r / 2, u => { const a = -u / r; add(hw - r + Math.cos(a) * r, -hh + r + Math.sin(a) * r); }],
      [w - 2 * r, u => add(hw - r - u, -hh)], [Math.PI * r / 2, u => { const a = -Math.PI / 2 - u / r; add(-hw + r + Math.cos(a) * r, -hh + r + Math.sin(a) * r); }], [h - 2 * r, u => add(-hw, -hh + r + u)], [Math.PI * r / 2, u => { const a = Math.PI - u / r; add(-hw + r + Math.cos(a) * r, hh - r + Math.sin(a) * r); }]];
    for (const [len, f] of lados) { if (q <= len) { f(q); break; } q -= len; } }
  return pts; }

export default async function () {
  const pm = new THREE.PMREMGenerator(renderer), env = pm.fromScene(new RoomEnvironment(), .04).texture;
  /* ================= 1 · placas que llenan la sala (96,5–101,3) ================= */
  const S1 = new THREE.Scene(), C1 = camara(38); S1.environment = env; S1.fog = new THREE.Fog(0x0a0a0b, 8, 26);
  const cp = contornoPlaca(), cpIn = contornoPlaca(1.64, 1.94, .24);
  const neon = linea([...cp, ...cpIn.slice(0, 120)], { color: 0xFF8A36, ancho: 3.4 }); S1.add(neon); const penN = chispa(.8); S1.add(penN);
  const metal = new THREE.MeshStandardMaterial({ color: 0x8e8a84, metalness: 1, roughness: .25, envMapIntensity: .7 });
  const tuboPlaca = () => { const g = new THREE.Group(); g.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(cp, true), 220, .07, 12, true), metal)); g.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(cpIn, true), 200, .06, 12, true), metal));
    [0, 1, 2].forEach(i => { const a = [...Array(20)].map((_, k) => { const an = -.7 + k / 19 * 1.4; return new THREE.Vector3(-.25 + Math.cos(an) * (.25 + i * .22), Math.sin(an) * (.25 + i * .22), 0); }); g.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(a), 40, .04, 8), metal)); }); return g; };
  const heroe = tuboPlaca(); S1.add(heroe);
  // patrón 2D de contornos (muchas placas planas) y luego campo 3D
  const patron = new THREE.Group(); S1.add(patron); semilla(4);
  for (let i = -8; i <= 8; i++) for (let j = -5; j <= 5; j++) { const l = linea1(cp.concat([cp[0]]), 0xE8E3DA, .7); l.position.set(i * 2.6 + (j % 2) * 1.3, j * 2.9, 0); l.rotation.z = (rnd() > .5 ? Math.PI / 2 : 0); l.scale.setScalar(.95); l.userData.t0 = 98.1 + (Math.abs(i) + Math.abs(j)) * .05; patron.add(l); }
  const campo = new THREE.Group(); S1.add(campo);
  const proto = tuboPlaca(); const geos = proto.children.map(m => m.geometry);
  const NI = 260; const insts = geos.map(g => { const im = new THREE.InstancedMesh(g, metal, NI); campo.add(im); return im; }); const M4 = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler();
  for (let k = 0; k < NI; k++) { const x = (k % 20 - 10) * 2.7 + (rnd() - .5) * .8, z = -Math.floor(k / 20) * 2.9 + 4 + (rnd() - .5) * .8; e.set(-Math.PI / 2 + (rnd() - .5) * .25, 0, rnd() * 6.283); q.setFromEuler(e); M4.compose(new THREE.Vector3(x, (rnd()) * .25, z), q, new THREE.Vector3(1, 1, 1)); insts.forEach(im => im.setMatrixAt(k, M4)); }
  S1.add(new THREE.AmbientLight(0xffffff, .3)); const lz1 = new THREE.PointLight(0xFF9A40, 6, 20); lz1.position.set(2, 3, 2); S1.add(lz1);
  const cabeza = panel(1500, 90, .36); S1.add(cabeza.mesh);
  const nota = panel(760, 300, 1.5); S1.add(nota.mesh);
  const tall = frase([...'YA NO QUEDA EXCUSA'].map((c, i) => ({ s: c, t: 100.05 + i * .045 })), .95, { font: '700 300px N', letras: 1, centro: 1 }); S1.add(tall);
  const f1 = t => {
    const kn = E.io(p(t, 96.5, .9)); trazar(neon, kn); const npts = cp.length + 120; penN.position.copy([...cp, ...cpIn][Math.floor(kn * (npts - 1))] || cp[0]); penN.visible = kn < 1;
    const k3 = E.oE(p(t, 97.25, .5)); heroe.visible = t > 97.2 && t < 98.4; heroe.scale.setScalar(.8 + .2 * k3); heroe.rotation.set(Math.sin(t) * .15, Math.sin(t * .7) * .3, .05); neon.material.opacity = 1 - k3;
    patron.visible = t > 98.0 && t < 99.4; patron.children.forEach(l => { l.material.opacity = .7 * cl((t - l.userData.t0) * 4); });
    campo.visible = t > 99.2;
    // cámara: frontal para el neón y el patrón; baja y rasante para el campo 3D
    if (t < 99.2) { const z = t < 98.0 ? 6.2 : lerp(8, 14, E.io(p(t, 98.0, 1.2))); C1.position.set(0, 0, z); C1.lookAt(0, 0, 0); }
    else { const u = t - 99.2; C1.position.set(-1 + u * .5, 1.3 - u * .05, 6 - u * 1.4); C1.lookAt(1 + u * .4, .2, -4 - u); }
    cabeza.mesh.position.copy(C1.position).add(new THREE.Vector3(-2.2, 1.55, -4.5).applyQuaternion(C1.quaternion)); cabeza.mesh.quaternion.copy(C1.quaternion);
    cabeza.pinta(Math.floor(t * 10), g => { const P = [['mientras', 96.6], ['las', 96.9], ['placas', 97.1, 1], ['llenan', 97.6], ['la', 97.85], ['sala', 98.0]]; let x = 10; g.font = '500 60px I';
      P.forEach(([w, t0, o]) => { g.fillStyle = t > t0 ? (o ? GOLD : '#E8E3DA') : 'rgba(232,227,218,.2)'; g.fillText(w, x, 64); x += g.measureText(w + ' ').width; }); });
    cabeza.mesh.visible = t < 99.3;
    nota.mesh.visible = t > 98.6 && t < 100.1; nota.mesh.position.copy(C1.position).add(new THREE.Vector3(1.7, .6, -4.5).applyQuaternion(C1.quaternion)); nota.mesh.quaternion.copy(C1.quaternion);
    nota.pinta(Math.floor(t * 20), g => { g.fillStyle = 'rgba(18,17,16,.92)'; g.fillRect(0, 0, 760, 300); g.strokeStyle = 'rgba(236,232,225,.25)'; g.strokeRect(1, 1, 758, 298); mono(g, '✉ RESPUESTA AUTOMÁTICA', 24, 40, 'rgba(236,232,225,.45)', '400 20px M');
      mono(g, tip('El jefe está de vacaciones.', 98.7, 22, t), 24, 100, '#F2EEE6', '500 32px M'); mono(g, 'La placa sigue funcionando sola:', 24, 160, 'rgba(236,232,225,.6)', '400 22px M'); mono(g, 'acercar el móvil y listo.', 24, 196, 'rgba(236,232,225,.6)', '400 22px M'); });
    tall.visible = t > 99.95; tall.position.copy(C1.position).add(new THREE.Vector3(0, -.45, -5.2).applyQuaternion(C1.quaternion)); tall.quaternion.copy(C1.quaternion);
    tall.children.forEach((m, i) => { const w = m.userData.it, k = E.oC(p(t, w.t, .12)); m.material.opacity = .25 + .75 * k; m.material.color.set(k > .5 && t < w.t + .25 ? 0xFF9A3A : 0xCFC9BF); });
    return { escena: S1, cam: C1, post: { bloom: .6, radio: .45, umbral: .88, ca: .004 } };
  };

  /* ================= 2 · la mecha (101,3–105,8) ================= */
  const S2 = new THREE.Scene(), C2 = camara(40);
  const curvaM = new THREE.CatmullRomCurve3([...Array(12)].map((_, i) => new THREE.Vector3(-14 + i * 2.8, Math.sin(i * .9) * .6 - 1 + i * .25, Math.cos(i * .7) * .8)));
  const mecha = new THREE.Mesh(new THREE.TubeGeometry(curvaM, 500, .13, 20), new THREE.ShaderMaterial({ uniforms: { quema: { value: 0 } },
    vertexShader: 'varying vec2 v; varying vec3 n; void main(){ v = uv; n = normalize(normalMatrix*normal); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: `uniform float quema; varying vec2 v; varying vec3 n; void main(){ float tr = step(.5, fract(v.x*420. + v.y*2.)) * .6 + .4*step(.5, fract(v.x*420. - v.y*2.)); float sh = .25 + .75*max(n.z, 0.)*max(0., n.y*.5+.6);
      vec3 c = vec3(.78,.76,.72)*(.35+.65*tr)*sh; float d = v.x - quema; c = mix(c, vec3(.06,.05,.04), step(d, 0.)); c += vec3(1.,.45,.12)*exp(-pow(d*120., 2.))*2.; gl_FragColor = vec4(c,1.); }` }));
  S2.add(mecha); const chM = chispa(1.1); S2.add(chM); const chisM = [...Array(40)].map(() => { const c = chispa(.15); S2.add(c); return c; });
  const FR = [['Ya', 101.5], ['es', 101.7], ['tarde,', 101.9], ['encendimos', 102.5], ['la', 103.1], ['mecha', 103.3, 1]];
  const txtM = new THREE.Group(); S2.add(txtM); FR.forEach(([w, t0, o]) => { const f = frase([{ s: w, t: t0, oro: o }], o ? .8 : .42, { font: '800 200px A' }); f.userData.t0 = t0; f.userData.o = o; txtM.add(f); });
  const f2 = t => { const kq = lerp(.05, .78, E.io(p(t, 101.3, 4.5))); mecha.material.uniforms.quema.value = kq; const pos = curvaM.getPointAt(kq), tg = curvaM.getTangentAt(kq);
    chM.position.copy(pos).add(new THREE.Vector3(0, 0, .15)); chM.scale.setScalar(.9 + .3 * Math.sin(t * 40));
    chisM.forEach((c, i) => { const u = ((t * 1.8 + i * .07) % .6); c.position.copy(pos).add(new THREE.Vector3(Math.cos(i * 2.3) * u * 1.3, Math.sin(i * 1.7) * u * 1.3 + u * .5, Math.sin(i) * u)); c.material.opacity = 1 - u / .6; });
    const Lc = curvaM.getLength(), ws = txtM.children.map(f => f.userData.ancho); let fin = .35;
    for (let i = ws.length - 1; i >= 0; i--) { const f = txtM.children[i], u = cl(kq - (fin + ws[i]) / Lc, .002, .998); fin += ws[i] + .18; const qq = curvaM.getPointAt(u), tq = curvaM.getTangentAt(u);
      f.position.copy(qq).add(new THREE.Vector3(0, .2, .1)); f.rotation.z = Math.atan2(tq.y, tq.x); pintaKaraoke(f, t, { dim: .15, oroC: 0xFF9A3A }); f.visible = t > f.userData.t0 - .4; }
    C2.position.set(pos.x - 3.0, pos.y + .5, 6.6 - p(t, 103, 2.8) * 1.6); C2.lookAt(pos.x + .6, pos.y + .1, 0);
    return { escena: S2, cam: C2, post: { bloom: 1.1, radio: .6, umbral: .5, ca: .005, fondo: 0x0d0907 } }; };

  /* ================= 3 · tesis de ortogonalidad (105,8–111,1) ================= */
  const S3 = new THREE.Scene(), C3 = camara(38); semilla(19);
  const ejes = linea([new THREE.Vector3(-4.5, 3, 0), new THREE.Vector3(-4.5, -2, 0), new THREE.Vector3(4.8, -2, 0)], { color: 0xE8E3DA, ancho: 1.4, op: .6 }); S3.add(ejes);
  const puntos = new THREE.Group(); S3.add(puntos); const ETQ = ['el que vuelve', 'el que recomienda', 'el que se olvida', '«ahora te la dejo»', 'la mesa 4', 'tu mejor cliente', 'el que pide la cuenta', 'el de los lunes'];
  for (let i = 0; i < 70; i++) { const m = new THREE.Mesh(new THREE.RingGeometry(.035, .055, 16), new THREE.MeshBasicMaterial({ color: 0xE8E3DA, transparent: true, toneMapped: false })); m.position.set(-4.2 + rnd() * 8.8, -1.8 + rnd() * 4.6, 0); m.userData.t0 = 106.8 + rnd() * 1.6; puntos.add(m); }
  const lab3 = panel(W, H, 7.2, { aditivo: true }); lab3.mesh.position.set(0, .4, 0); S3.add(lab3.mesh); const cur3 = linea([...Array(80)].map((_, i) => new THREE.Vector3(-3.6 + i / 79 * 7.8, -.4 + Math.sin(i / 79 * Math.PI) * .6, .01)), { color: 0xE8E3DA, ancho: 1.6, op: .7 }); S3.add(cur3);
  const tesis = frase([{ s: 'Tesis', t: 106.0 }, { s: 'de', t: 106.35 }, { s: 'la', t: 106.5 }, { s: 'ortogonalidad', t: 106.7 }], .34, { font: '500 200px I' }); S3.add(tesis);
  const blues = frase([...'blues'].map((c, i) => ({ s: c, t: 108.1 + i * .08 })), .7, { font: 'italic 260px G', letras: 1 }); blues.position.set(-.9, .1, .05); S3.add(blues);
  const chT = chispa(.9); S3.add(chT);
  const f3 = t => { const kx = E.io(p(t, 105.8, .9)); chT.position.set(lerp(-6, 4.8, kx), t < 106.8 ? -.2 : -2, .05); chT.visible = t < 107.2 || t > 109.8;
    if (t > 109.8) chT.position.set(lerp(-4.5, 4.8, p(t, 109.8, 1.2)), -2, .05);
    trazar(ejes, E.io(p(t, 106.8, .5))); puntos.children.forEach(m => { const k = E.oB(p(t, m.userData.t0, .3)); m.scale.setScalar(Math.max(.001, k)); });
    trazar(cur3, E.io(p(t, 107.9, .6)));
    lab3.pinta(Math.floor(t * 8), g => { if (t < 106.8) return; mono(g, 'DEJA RESEÑA ↑', 330, 95, 'rgba(236,232,225,.55)', '400 20px M'); mono(g, 'CLIENTE CONTENTO →', 1440, 925, 'rgba(236,232,225,.55)', '400 20px M');
      puntos.children.slice(0, 8).forEach((m, i) => { if (t < m.userData.t0 + .2) return; const x = (m.position.x + 4.5) / 9.6 * 1540 + 380, y = 540 - (m.position.y - .4) * 150; mono(g, '○ ' + ETQ[i], x - 10, y + 6, 'rgba(236,232,225,.6)', '400 18px M'); });
      mono(g, 'r = 0,00', 1550, 520, 'rgba(236,232,225,.55)', '400 20px M'); mono(g, 'cualquier nivel de contento, cualquier nivel de reseña', 1150, 60, 'rgba(236,232,225,.4)', 'italic 22px G'); });
    tesis.position.set(t < 106.8 ? -2.3 : -2.6, t < 106.8 ? -.7 : -2.8, .05); pintaKaraoke(tesis, t, { dim: .2 });
    blues.children.forEach(m => { const k = E.oC(p(t, m.userData.it.t, .2)); m.material.opacity = k; m.material.color.set(0xF3E6D2).lerp(new THREE.Color(0xF0A044), 1 - p(t, m.userData.it.t + .3, .5)); });
    C3.position.set(lerp(-2.6, 0, E.io(p(t, 106.5, 1))), lerp(-1, .3, E.io(p(t, 106.5, 1))), lerp(4.2, 8.2, E.io(p(t, 106.5, 1.2))) - .5 * p(t, 108, 3)); C3.lookAt(C3.position.x * .6, .2, 0);
    return { escena: S3, cam: C3, post: { bloom: 1.0, radio: .55, umbral: .55, ca: .004, fondo: 0x0d0b09 } }; };

  /* ================= 4 · torre de bloques de metacrilato (111,1–115,3) ================= */
  const S4 = new THREE.Scene(), C4 = camara(40); S4.fog = new THREE.Fog(0x0a0a0b, 6, 22);
  const bloque = (i) => { const g = new THREE.Group(); const edg = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(4.2, .9, 2.4)), new THREE.LineBasicMaterial({ color: 0xE6E1D8, transparent: true, opacity: .55, toneMapped: false })); g.add(edg);
    const vid = new THREE.Mesh(new THREE.BoxGeometry(4.2, .9, 2.4), new THREE.MeshBasicMaterial({ color: 0x9fb0c0, transparent: true, opacity: .05, depthWrite: false })); g.add(vid);
    const pn = panel(1400, 300, .86, { aditivo: true }); pn.mesh.position.z = 1.21; pn.pinta(1, gg => { gg.strokeStyle = 'rgba(236,232,225,.55)'; gg.lineWidth = 3; gg.strokeRect(20, 20, 1360, 260); mono(gg, 'PLACA DE MESA', 50, 70, 'rgba(236,232,225,.6)', '400 30px M');
      [['METACRILATO 4 mm', 110], ['CHIP NFC', 175], ['QR', 240]].forEach(([s, y]) => { gg.strokeRect(420, y - 40, 600, 52); mono(gg, s, 460, y - 4, 'rgba(236,232,225,.7)', '400 28px M'); }); mono(gg, 'L.' + String(i).padStart(3, '0'), 1220, 70, 'rgba(236,232,225,.45)', '400 26px M'); });
    g.add(pn.mesh); return g; };
  const torre = new THREE.Group(); S4.add(torre); for (let i = 0; i < 16; i++) { const b = bloque(i + 1); b.position.y = -i * 1.5; b.rotation.y = (i % 2 ? .06 : -.06); torre.add(b); }
  const eje = linea1([new THREE.Vector3(0, 3, 1.3), new THREE.Vector3(0, -26, 1.3)], 0xE6E1D8, .35); S4.add(eje);
  const SLAM = [['«SOLO', 111.2, 1, -0], ['METACRILATO', 111.75, 0, -1.5], ['DE ARRIBA', 112.6, 0, -3], ['ABAJO»', 113.1, 1, -4.5], ['HASTA QUE', 113.8, 0, -6], ['LO', 114.35, 1, -7.5], ['TOCAS', 114.8, 1, -9]];
  const slams = SLAM.map(([s, t0, o, y]) => { const f = frase([...s].map((c, i) => ({ s: c, t: t0 + i * .025 })), .62, { font: '900 240px A', letras: 1, centro: 1 }); f.position.set(0, y + .1, 1.6); f.userData = { t0, o }; S4.add(f); return f; });
  const hud4 = panel(700, 140, .6); S4.add(hud4.mesh);
  const f4 = t => { const y = lerp(0, -9, E.io(p(t, 111.1, 4.1))), rz = Math.sin(t * .8) * .08;
    C4.position.set(2.2 * Math.cos(t * .5), y + 1.4, 6.2); C4.lookAt(0, y - .2, 1.0); C4.rotateZ(rz);
    slams.forEach(f => { const { t0, o } = f.userData; f.visible = t > t0 - .05; f.children.forEach(m => { const k = E.oB(p(t, m.userData.it.t, .25)); m.material.opacity = cl(k); m.scale.setScalar(.6 + .4 * cl(k) + .3 * (1 - cl(k))); m.material.color.set(o ? 0xFF9A3A : 0xF1ECE4); });
      f.lookAt(C4.position.x, f.position.y, C4.position.z); });
    hud4.mesh.position.copy(C4.position).add(new THREE.Vector3(-3.2, 1.6, -4.6).applyQuaternion(C4.quaternion)); hud4.mesh.quaternion.copy(C4.quaternion);
    hud4.pinta(Math.floor(t * 4), g => { mono(g, 'PROFUNDIDAD', 10, 30, 'rgba(236,232,225,.5)', '400 22px M'); mono(g, 'L.' + String(5 + Math.floor((t - 111.1) * 2.3)).padStart(3, '0') + ' / ∞', 10, 80, '#F2EEE6', '500 40px M'); mono(g, 'P(toque) ' + (.3 + (t - 111) * .02).toFixed(2).replace('.', ','), 10, 120, 'rgba(242,182,64,.8)', '400 22px M'); });
    return { escena: S4, cam: C4, post: { bloom: .9, radio: .5, umbral: .6, ca: .005 } }; };

  /* ================= 5 · tipografía: SÚPER-DIRECTO / SALTÁNDOTE / EN CADA MESA (115,3–121,0) ================= */
  const d5 = capa(`<div style="position:absolute;inset:0;background:#0d0c0c"></div><div style="position:absolute;inset:40px;border:1.5px solid rgba(236,232,225,.25)"></div>
    <div id="e5d" style="position:absolute;left:40px;top:40px;right:40px;bottom:40px;overflow:hidden"></div>
    <div id="e5c" style="position:absolute;right:80px;bottom:80px;border:1.5px solid rgba(236,232,225,.35);padding:10px 18px;font:500 34px M;color:#F2EEE6;background:#0d0c0c"></div>
    <div id="e5f" style="position:absolute;left:0;top:0;right:0;bottom:0;display:none"></div>`);
  const f5 = t => { const q = s => d5.querySelector(s), D = q('#e5d');
    if (t < 117.3) { q('#e5f').style.display = 'none'; D.style.display = 'block'; const n = Math.floor(lerp(1, 16, p(t, 115.8, .9))); const L1 = 'NFC, QR, ', L2 = 'SÚPER-DIRECTO ';
      let h = ''; for (let r = 0; r < 16; r++) { const lit = r === 3; const s = (r % 2 ? L2 : L1).repeat(8); const off = (t * (r % 2 ? -120 : 90) + r * 55) % 600;
        h += `<div style="position:absolute;left:${-600 + off}px;top:${60 + r * 58}px;font:${lit ? 800 : 700} 64px/1 A;white-space:nowrap;color:${r < n ? (lit ? '#F2EEE6' : 'rgba(236,232,225,.28)') : 'transparent'}">${lit ? `<span style="color:#F2EEE6">NFC, QR,</span> <span style="color:${GOLD}">SÚPER-DIRECTO</span> ` + s : s}</div>`; }
      if (t < 115.8) h = `<div style="position:absolute;left:80px;top:480px;font:500 70px/1.2 A;letter-spacing:.05em;color:#F2EEE6"><span style="color:${GOLD}">N</span>FC, QR,<br><span style="color:rgba(236,232,225,.6)">SÚPER-DIRECTO</span></div>`;
      D.innerHTML = h; q('#e5c').style.display = 'block'; q('#e5c').innerHTML = `<div style="font:400 16px M;color:rgba(236,232,225,.5)">RÉPLICAS</div>${Math.round(lerp(20, 18288, E.iC(p(t, 115.3, 2)))).toLocaleString('es-ES')}`; }
    else { D.style.display = 'none'; q('#e5c').style.display = 'none'; const F = q('#e5f'); F.style.display = 'block';
      if (t < 119.3) { const k = p(t, 117.3, 2.0); F.innerHTML = `<div style="position:absolute;left:${-60 - 700 * E.io(k)}px;top:${lerp(160, -80, E.io(k))}px;font:700 330px/.9 N;white-space:nowrap;letter-spacing:-.01em">
          <div><span style="color:${GOLD}">SALTÁNDOTE</span></div><div style="color:#F2EEE6">CADA <span style="color:transparent;-webkit-text-stroke:3px rgba(236,232,225,.4)">PASO</span></div><div><span style="color:${t > 118.5 ? GOLD : 'transparent'};-webkit-text-stroke:3px ${GOLD}">DE MÁS</span></div></div>`; }
      else { const k = p(t, 119.3, 1.7); let cel = ''; for (let i = 0; i < 24; i++) { const x = (i % 8) * 240, y = Math.floor(i / 8) * 360; cel += `<div style="position:absolute;left:${x}px;top:${y}px;width:236px;height:356px;border:2px solid rgba(255,140,60,.25);background:radial-gradient(circle at 50% 40%,rgba(233,120,40,${.25 + .2 * Math.sin(i + t * 3)}),transparent 70%)"><div style="font:400 16px M;color:rgba(255,200,150,.5);padding:8px">MESA ${String(i + 1).padStart(2, '0')}</div></div>`; }
        F.innerHTML = `<div style="position:absolute;inset:0;background:#1a0c07">${cel}</div><div style="position:absolute;left:0;right:0;top:${160 - 40 * k}px;text-align:center;font:900 250px/.95 A;color:rgba(236,232,225,.9);-webkit-text-stroke:2px #fff;text-shadow:0 0 30px rgba(0,0,0,.6);transform:scale(${1 + .05 * k})">EN CADA<br>MESA<br><span style="opacity:${cl((t - 120.2) * 3)}">DEL BAR</span></div>
          <div style="position:absolute;right:120px;bottom:120px;border:1.5px solid rgba(236,232,225,.4);padding:10px 18px;font:500 34px M;color:#F2EEE6;background:rgba(10,10,10,.8)"><div style="font:400 16px M;color:rgba(236,232,225,.5)">MESAS CON PLACA</div>${Math.min(24, Math.floor(p(t, 119.3, 1.4) * 24) + 1)} / 24</div>`; } }
    return null; };

  /* ================= 6 · «el «luego te la dejo» se tuerce» (121,0–124,4) ================= */
  const d6 = capa(`<div style="position:absolute;inset:0;background:#0d0c0c"></div><div id="e6w" style="position:absolute;inset:0;transform-origin:40% 50%">
     <svg width="1920" height="1080" style="position:absolute;inset:0"><line x1="-100" y1="760" x2="2000" y2="560" stroke="rgba(236,232,225,.3)" stroke-width="2"/><line x1="-100" y1="900" x2="2000" y2="700" stroke="rgba(242,182,64,.25)" stroke-width="2"/></svg>
     <div id="e6a" style="position:absolute;left:170px;top:190px;font:900 200px/1 A;color:#F2EEE6;white-space:nowrap">«LUEGO</div>
     <div id="e6b" style="position:absolute;left:210px;top:400px;font:900 120px/1 A;color:#F2EEE6;white-space:nowrap">TE LA DEJO»</div>
     <div id="e6c" style="position:absolute;left:230px;top:560px;font:900 220px/1 A;color:${GOLD};white-space:nowrap">SE TUERCE</div>
     <svg id="e6cara" width="440" height="440" viewBox="0 0 440 440" style="position:absolute;left:1260px;top:240px"><circle cx="220" cy="220" r="200" fill="#EDEAE3"/><circle cx="160" cy="180" r="18" fill="#1b1a18"/><circle cx="280" cy="180" r="18" fill="#1b1a18"/><path id="e6boca" d="M130 260 Q220 330 310 260" fill="none" stroke="#1b1a18" stroke-width="20" stroke-linecap="round"/></svg>
     <div style="position:absolute;left:120px;bottom:110px;border:1.5px solid rgba(236,232,225,.35);padding:10px 18px;font:500 34px M;color:#F2EEE6"><div style="font:400 16px M;color:rgba(236,232,225,.5)">P(olvido)</div><span id="e6p"></span></div></div>`);
  const f6 = t => { const q = s => d6.querySelector(s); const k = E.io(p(t, 122.0, 2.2));
    q('#e6w').style.transform = `rotate(${-8 * k}deg) translateY(${40 * k}px)`; q('#e6a').style.opacity = cl((t - 121.1) * 4); q('#e6b').style.opacity = cl((t - 121.5) * 4); q('#e6c').style.opacity = cl((t - 122.0) * 4);
    q('#e6c').style.transform = `rotate(${-10 * k}deg) skewX(${-15 * k}deg)`; q('#e6c').style.letterSpacing = (k * .05) + 'em';
    q('#e6cara').style.transform = `rotate(${-200 * k}deg) translateX(${-40 * k}px)`; const sm = lerp(330, 200, k); q('#e6boca').setAttribute('d', `M130 ${260 + 20 * k} Q220 ${sm} 310 ${260 + 20 * k}`);
    q('#e6p').textContent = lerp(.12, .58, E.io(p(t, 121.0, 3.3))).toFixed(2).replace('.', ','); return null; };

  /* ================= 7 · SUBO / MI (oro) · P(TOQUE) en papel (124,4–126,1) ================= */
  const d7 = capa(`<div id="e7f" style="position:absolute;inset:0"></div><div id="e7t" style="position:absolute;left:0;right:0;text-align:center;white-space:nowrap"></div>`);
  const f7 = t => { const q = s => d7.querySelector(s);
    if (t < 125.55) { q('#e7f').style.background = '#E9B43A'; const w = t < 125.0 ? 'SUBO' : 'MI'; q('#e7t').style.cssText = `position:absolute;left:0;right:0;top:${w === 'MI' ? 60 : 180}px;text-align:center;font:900 ${w === 'MI' ? 900 : 560}px/1 A;color:#140f06;letter-spacing:-.04em;text-shadow:${[...Array(8)].map((_, i) => `${i * 3}px ${i * 3}px 0 rgba(90,55,10,${.5 - i * .05})`).join(',')}`; q('#e7t').textContent = w; }
    else { q('#e7f').style.background = '#ECE8DF'; q('#e7t').style.cssText = `position:absolute;left:0;right:0;top:390px;text-align:center;font:900 230px/1 A;color:#161513;filter:blur(${(1 - p(t, 125.55, .3)) * 10}px)`; q('#e7t').innerHTML = `P<span style="color:#c9c3b8">(</span><span style="color:${t > 125.8 ? '#161513' : '#c9c3b8'}">TOQUE</span><span style="color:#c9c3b8">)</span>`; }
    return null; };

  return [{ t0: 96.5, t1: 101.3, frame: f1 }, { t0: 101.3, t1: 105.8, frame: f2 }, { t0: 105.8, t1: 111.1, frame: f3 }, { t0: 111.1, t1: 115.3, frame: f4 }, { t0: 115.3, t1: 121.0, frame: f5, dom: d5 }, { t0: 121.0, t1: 124.4, frame: f6, dom: d6 }, { t0: 124.4, t1: 126.1, frame: f7, dom: d7 }];
}
