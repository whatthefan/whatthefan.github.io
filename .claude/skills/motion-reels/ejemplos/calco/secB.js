// secB.js — 16,5 a 38,2 s: anillos + prompt «Google, por favor, no me olvides» · flash · SUBO / MI / P(TOQUE) · «porque el futuro hace TOOC»
//           · biblioteca 3D «atrapado en Google Maps con cuarenta pestañas» · carita + monstruo «mira detrás de su «luego te la dejo», con tus ojos de dueño»
import { THREE, W, H, E, p, cl, lerp, muelle, linea, trazar, linea1, chispa, camara, panel, frase, pintaKaraoke, ORO, semilla, rnd } from './core.js';

const mono = (g, s, x, y, c = 'rgba(236,232,225,.75)', f = '400 26px M') => { g.font = f; g.fillStyle = c; g.fillText(s, x, y); };
const kf = (K, t) => { let i = 0; while (i < K.length - 2 && t >= K[i + 1][0]) i++; const a = K[i], b = K[i + 1], k = E.io(cl((t - a[0]) / (b[0] - a[0] || 1))); return a.slice(1).map((v, j) => lerp(v, b[j + 1], k)); };
const GOLD = '#F2C14E', GOLDs = 'rgba(242,193,78,';

export default async function () {
  /* ================= 1 · anillos + prompt (16,5–22,15) ================= */
  const S1 = new THREE.Scene(), C1 = camara(40);
  const anillos = new THREE.Group(); S1.add(anillos); semilla(3);
  for (let i = 0; i < 46; i++) { const r = .35 + i * .19, pts = []; const f1 = rnd() * 6, f2 = rnd() * 6;
    for (let k = 0; k <= 180; k++) { const a = k / 180 * Math.PI * 2, w = 1 + .05 * Math.sin(a * 3 + f1) + .03 * Math.sin(a * 7 + f2) + .015 * Math.sin(a * 13 + i); pts.push(new THREE.Vector3(Math.cos(a) * r * w, Math.sin(a) * r * w, 0)); }
    const l = linea1(pts, 0xE8E2D8, .75 - i * .01); l.userData.r = r; anillos.add(l); }
  const brillo = new THREE.Mesh(new THREE.PlaneGeometry(9, 9), new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, uniforms: { k: { value: 1 } },
    vertexShader: 'varying vec2 v; void main(){ v = uv; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: 'uniform float k; varying vec2 v; void main(){ float d = length(v-.5)*2.; vec3 c = vec3(1.,.55,.18)*exp(-d*d*6.)*.9*k + vec3(1.,.8,.5)*exp(-d*d*60.)*.6*k; gl_FragColor = vec4(c,1.); }' }));
  brillo.position.z = -.1; S1.add(brillo);
  const rayos = new THREE.Group(); S1.add(rayos); for (let i = 0; i < 90; i++) { const a = i / 90 * Math.PI * 2 + rnd() * .03; const l = linea1([new THREE.Vector3(Math.cos(a) * 1.5, Math.sin(a) * 1.5, 0), new THREE.Vector3(Math.cos(a) * 14, Math.sin(a) * 14, 0)], 0xEDE6DA, .0); rayos.add(l); }
  // banda del prompt
  const banda = new THREE.Mesh(new THREE.PlaneGeometry(40, 1.25), new THREE.MeshBasicMaterial({ color: 0x0b0b0c, transparent: true, opacity: .82, depthWrite: false })); banda.position.set(0, -.55, .3); banda.renderOrder = -1; S1.add(banda);
  const bl = linea1([new THREE.Vector3(-20, .08, .31), new THREE.Vector3(20, .08, .31)], 0xffffff, .12); bl.position.y = -.55; S1.add(bl); const bl2 = bl.clone(); bl2.position.y = -1.7; S1.add(bl2);
  const PAL = [['Google,', 17.0, [['Google', .61], ['Maps', .12], ['TripAdvisor', .04], ['mamá', .02]]], ['por', 18.0, [['por', .48], ['porfa', .21], ['venga', .07], ['oye', .02]]], ['favor,', 18.35, [['favor', .83], ['fa', .04]]],
    ['no', 19.25, [['no', .44], ['déjame', .11], ['ayúdame', .06]]], ['me', 19.6, [['me', .71], ['te', .08]]], ['olvides', 20.25, [['olvides', .63], ['dejes', .09], ['bloquees', .03], ['ignores', .02]]]];
  const txt = panel(3200, 170, .95); txt.mesh.position.set(4.6, -.55, .35); S1.add(txt.mesh);
  const auto = panel(760, 300, 1.45); S1.add(auto.mesh);
  const info = panel(900, 180, .85); S1.add(info.mesh); const ctx = panel(700, 120, .55); S1.add(ctx.mesh);
  const CH = 58; // ancho de carácter (px) de la mono a 96px
  const f1 = t => {
    const pal = PAL.filter(w => t >= w[1]); let s = '› '; PAL.forEach(w => { if (t >= w[1]) s += w[0] + ' '; });
    // letras escritas: la palabra actual se escribe a 22 cps
    let full = '', vis = ''; PAL.forEach(([w, t0]) => { if (t < t0) return; const n = Math.floor(cl((t - t0) * 22, 0, w.length)); vis += w.slice(0, n) + (n === w.length ? ' ' : ''); });
    const cur = pal[pal.length - 1];
    const desp = 0, finX = -4.3 + (vis.length + 2) * .32;
    txt.pinta(vis + Math.floor(t * 3) % 2, g => { g.font = '400 96px M'; let x = 60 - desp; g.fillStyle = 'rgba(236,232,225,.55)'; g.fillText('›', x, 118); x += CH * 2;
      const ws = vis.split(' '); ws.forEach((w, i) => { const ult = i === ws.length - 1 || (i === ws.length - 2 && ws[ws.length - 1] === ''); g.fillStyle = ult ? GOLD : 'rgba(236,232,225,.92)'; if (ult) { g.shadowColor = GOLD; g.shadowBlur = 24; } else g.shadowBlur = 0;
        g.fillText(w, x, 118); if (ult && w) { g.fillStyle = GOLDs + '.8)'; g.fillRect(x, 140, w.length * CH, 5); } x += (w.length + 1) * CH; });
      g.shadowBlur = 0; if (Math.floor(t * 3) % 2) { g.fillStyle = GOLD; g.fillRect(x - CH + 4, 40, 6, 96); } });
    // panel de probabilidades
    auto.mesh.position.set(finX - .6, 1.05, .36); auto.mesh.material.opacity = cl((t - 16.8) * 4) * (1 - p(t, 21.0, .3));
    auto.pinta(cur ? cur[0] : '', g => { g.fillStyle = 'rgba(11,11,12,.85)'; g.fillRect(0, 0, 760, 300); g.strokeStyle = 'rgba(236,232,225,.25)'; g.strokeRect(1, 1, 758, 298);
      mono(g, 'p( siguiente | contexto )', 20, 36, 'rgba(236,232,225,.55)', '400 24px M'); mono(g, 'muestreada', 590, 36, 'rgba(236,232,225,.45)', '400 22px M');
      (cur ? cur[2] : [['…', 0]]).forEach(([w, pr], i) => { const y = 84 + i * 52; if (!i) { g.fillStyle = 'rgba(242,193,78,.12)'; g.fillRect(8, y - 34, 744, 46); }
        mono(g, (i ? '  ' : '▸ ') + w, 20, y, i ? 'rgba(236,232,225,.6)' : GOLD, '400 28px M'); g.fillStyle = i ? 'rgba(236,232,225,.35)' : GOLD; g.fillRect(360, y - 18, 280 * pr, 12); mono(g, pr.toFixed(2).replace('.', ','), 670, y, i ? 'rgba(236,232,225,.55)' : GOLD, '400 26px M'); }); });
    info.mesh.position.set(-2.4, -1.45, .36); info.pinta(1, g => { mono(g, 'PROMPT 01', 0, 40, 'rgba(236,232,225,.8)', '500 30px M'); mono(g, 'T 0,7 · top-p 0,95 · semilla 0x2A', 0, 90, 'rgba(236,232,225,.5)', '400 26px M'); mono(g, 'P(toque) 0,04 · depende del contexto', 0, 140, 'rgba(236,232,225,.5)', '400 26px M'); g.fillStyle = GOLD; g.fillRect(222, 18, 40, 28); });
    ctx.mesh.position.set(finX + 1.2, -1.45, .36); ctx.mesh.material.opacity = cl((t - 19.8) * 3); ctx.pinta(1, g => { mono(g, 'CONTEXTO 06 / 8192', 700 - 380, 40, 'rgba(236,232,225,.8)', '500 28px M'); mono(g, '↵ enviar (irreversible)', 700 - 390, 90, 'rgba(236,232,225,.45)', '400 24px M'); });
    // anillos respiran; ráfaga final
    anillos.children.forEach((l, i) => { const s = 1 + .012 * Math.sin(t * 2 - i * .4); l.scale.setScalar(s * (1 + 1.2 * E.iE(p(t, 21.2, .9)))); });
    brillo.material.uniforms.k.value = .45 + .08 * Math.sin(t * 3) + 1.6 * E.iC(p(t, 21.0, 1.1));
    rayos.children.forEach((l, i) => { l.material.opacity = .45 * E.oC(p(t, 21.0 + (i % 7) * .02, .3)); l.scale.setScalar(1 + (t - 21) * 2); });
    const cxT = Math.max(-1.2, finX - 3.2); const [cx0, cy, cz] = kf([[16.5, 0, -.2, 7.6], [18.5, 0, -.25, 7.0], [20.4, 0, -.3, 6.4], [21.0, 0, -.4, 6.6], [22.2, 0, -.4, 3.6]], t); const cx = lerp(cxT, 0, p(t, 21.0, .8));
    C1.position.set(cx, cy + .9, cz); C1.lookAt(cx, cy, 0); C1.rotateZ(-.05);
    return { escena: S1, cam: C1, post: { bloom: 1.0, radio: .5, umbral: .6, ca: .004 + .01 * p(t, 21.0, 1), flash: E.iC(p(t, 21.75, .4)) } };
  };

  /* ================= 2 · SUBO / MI / P(TOQUE) (22,15–24,35): capa DOM tipográfica ================= */
  const d2 = document.createElement('div'); d2.className = 'capa'; document.getElementById('ov').appendChild(d2);
  d2.innerHTML = `<div id="b_fondo" style="position:absolute;inset:0;background:#d9d4cb"></div>
    <div id="b_subo" style="position:absolute;left:0;right:0;top:120px;text-align:center;font:900 560px/1 A;letter-spacing:-.04em;color:#F4F0E8"></div>
    <div id="b_mi" style="position:absolute;left:0;right:0;top:250px;text-align:center;font:900 560px/1 A;letter-spacing:-.04em;color:#F4F0E8"></div>
    <div id="b_pt" style="position:absolute;left:0;right:0;top:390px;text-align:center;font:900 250px/1 A;letter-spacing:-.02em;color:#F4F0E8"></div>
    <div id="b_hud" style="position:absolute;left:60px;top:50px;font:400 20px M;color:rgba(20,20,20,.45)">HOJA 02 · P(toque)</div>`;
  const $ = id => d2.querySelector('#' + id);
  const f2 = t => {
    const gris = t < 22.85; $('b_fondo').style.background = gris ? '#cfcac0' : '#0a0a0b'; $('b_fondo').style.opacity = 1;
    $('b_subo').style.display = t < 22.85 ? 'block' : 'none'; $('b_subo').textContent = 'SUBO'; $('b_subo').style.transform = `scale(${1.08 - .08 * E.oE(p(t, 22.15, .5))})`; $('b_subo').style.color = '#F6F2EA';
    $('b_subo').style.textShadow = '0 0 1px rgba(0,0,0,.2)';
    $('b_mi').style.display = t >= 22.85 && t < 23.45 ? 'block' : 'none'; $('b_mi').textContent = 'MI';
    const k = p(t, 22.85, .6); $('b_mi').style.textShadow = [...Array(6)].map((_, i) => `${0}px ${(i + 1) * 14 * (1 - k)}px 0 rgba(236,232,225,${.25 - i * .035})`).join(',');
    $('b_pt').style.display = t >= 23.45 ? 'block' : 'none'; const kp = p(t, 23.45, .35); $('b_pt').innerHTML = `P<span style="color:${kp < 1 ? '#6d6862' : '#F4F0E8'}">(</span><span style="color:rgba(${Math.round(lerp(109, 244, kp))},${Math.round(lerp(104, 240, kp))},${Math.round(lerp(98, 232, kp))},1)">TOQUE</span><span style="color:${kp < 1 ? '#6d6862' : '#F4F0E8'}">)</span>`;
    $('b_pt').style.transform = `scale(${1 + .04 * p(t, 23.45, 1)})`; $('b_hud').style.color = gris ? 'rgba(20,20,20,.45)' : 'rgba(236,232,225,.35)';
    return null; };

  /* ================= 3 · «porque el futuro hace TOOC» (24,35–25,9) ================= */
  const S3 = new THREE.Scene(), C3 = camara(40); semilla(8);
  const ramas = []; const crece = (o, a, len, d, t0) => { if (d > 6) return; const e = o.clone().add(new THREE.Vector3(Math.cos(a) * len, Math.sin(a) * len, 0)); const l = linea([o, e], { color: d < 2 ? 0xFFC872 : ORO, ancho: 2.2 - d * .2, op: .95 }); l.userData.t0 = t0; l.userData.d = .12 + d * .02; S3.add(l); ramas.push(l);
    const n = d < 2 ? 3 : 2; for (let i = 0; i < n; i++) crece(e, a + (i - (n - 1) / 2) * (1.9 - d * .1) + (rnd() - .5) * .5, len * (.72 + rnd() * .2), d + 1, t0 + .1 + d * .015); };
  crece(new THREE.Vector3(2.2, -.2, 0), 0, 1.3, 0, 24.4); crece(new THREE.Vector3(2.2, -.2, 0), 2.1, 1.3, 0, 24.45); crece(new THREE.Vector3(2.2, -.2, 0), -2.1, 1.3, 0, 24.5);
  const puntas = ramas.map(() => { const c = chispa(.25); S3.add(c); return c; });
  const circ3 = linea1([...Array(121)].map((_, i) => new THREE.Vector3(2.2 + Math.cos(i / 120 * 6.283) * 3.4, -.2 + Math.sin(i / 120 * 6.283) * 3.4, -.05)), 0xffffff, .12); S3.add(circ3);
  const L3 = [frase([{ s: 'PORQUE', t: 24.4 }, { s: 'EL', t: 24.6 }], .32, { font: '800 200px A' }), frase([{ s: 'FUTURO', t: 24.8, oro: 1 }], .62, { font: '900 200px A' }), frase([{ s: 'HACE', t: 25.15 }], .62, { font: '900 200px A' })];
  L3.forEach((g, i) => { g.position.set(-6.4, 2.6 - [0, .9, 1.75][i], 0); S3.add(g); });
  const TO = frase([{ s: 'T', t: 25.4 }, { s: 'O', t: 25.45 }, { s: 'O', t: 25.5 }, { s: 'C', t: 25.55 }], 1.5, { font: '900 300px A', letras: 1 }); TO.position.set(-1.3, -1.6, .1); S3.add(TO);
  const aros = [0, 1].map(i => { const a = linea([...Array(97)].map((_, k) => new THREE.Vector3(Math.cos(k / 96 * 6.283) * 1.25, Math.sin(k / 96 * 6.283) * 1.25, 0)), { color: 0xEFEAE0, ancho: 6, op: .9 }); a.position.set(TO.children[1 + i].position.x + TO.position.x + .55, -1.6 + .75, .05); S3.add(a); return a; });
  const cont3 = panel(500, 120, .6); cont3.mesh.position.set(5.6, 3.0, 0); S3.add(cont3.mesh);
  const f3 = t => {
    ramas.forEach((l, i) => { const k = p(t, l.userData.t0, l.userData.d); trazar(l, k); const c = puntas[i]; c.visible = k > 0 && k < 1; if (c.visible) { const a = l.geometry.attributes.instanceStart; } });
    ramas.forEach((l, i) => { const k = p(t, l.userData.t0, l.userData.d); puntas[i].visible = k > 0 && k < 1; if (puntas[i].visible) { const pos = l.geometry.attributes.instanceEnd.array, n = Math.max(0, l.geometry.instanceCount - 1); puntas[i].position.set(pos[n * 3], pos[n * 3 + 1], .02); } });
    L3.forEach(g => pintaKaraoke(g, t, { dim: .12 }));
    TO.children.forEach((m, i) => { const k = E.oC(p(t, m.userData.it.t, .15)); m.material.opacity = (i === 1 || i === 2) ? k * .95 : k; m.material.color.set(i === 1 || i === 2 ? 0xF2C14E : 0xF4F0E8); });
    aros.forEach((a, i) => { trazar(a, E.oC(p(t, 25.45 + i * .05, .35))); a.scale.setScalar(1 + .08 * Math.sin(t * 5 + i)); });
    cont3.pinta(Math.floor(t * 10), g => { mono(g, 'RAMAS', 330, 36, 'rgba(236,232,225,.5)', '400 22px M'); const n = Math.min(64, Math.pow(2, Math.floor((t - 24.3) * 5) + 1)); mono(g, String(n).padStart(4, '0'), 300, 100, GOLD, '500 56px M'); });
    C3.position.set(lerp(.4, .9, p(t, 24.3, 1.6)), 0, lerp(10, 8.6, E.io(p(t, 24.3, 1.6)))); C3.lookAt(.2, .1, 0);
    return { escena: S3, cam: C3, post: { bloom: 1.0, radio: .5, umbral: .6 } };
  };

  /* ================= 4 · biblioteca 3D de alambre (25,9–30,2) ================= */
  const S4 = new THREE.Scene(), C4 = camara(58); S4.fog = new THREE.Fog(0x0a0a0b, 6, 34); semilla(12);
  const segsB = [], caja = (x, y, z, w, h, d) => { const X = [x, x + w], Y = [y, y + h], Z = [z, z + d];
    [[0, 0, 0, 1, 0, 0], [0, 1, 0, 1, 1, 0], [0, 0, 1, 1, 0, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 1, 0], [1, 0, 0, 1, 1, 0], [0, 0, 1, 0, 1, 1], [1, 0, 1, 1, 1, 1], [0, 0, 0, 0, 0, 1], [1, 0, 0, 1, 0, 1], [0, 1, 0, 0, 1, 1], [1, 1, 0, 1, 1, 1]]
      .forEach(([a, b, c, d2_, e, f]) => segsB.push(X[a], Y[b], Z[c], X[d2_], Y[e], Z[f])); };
  // sala: estanterías a ambos lados (z = profundidad), libros de anchos al azar
  const estante = (x0, dir, z0, z1) => { for (let z = z0; z < z1; z += 2.2) { caja(x0, 0, z, .9 * dir, 4.6, 2.1); for (let bal = 0; bal < 5; bal++) { const y = .15 + bal * .9; segsB.push(x0, y, z, x0 + .9 * dir, y, z, x0, y, z + 2.1, x0 + .9 * dir, y, z + 2.1, x0 + .9 * dir, y, z, x0 + .9 * dir, y, z + 2.1);
    let zz = z + .05; while (zz < z + 2.0) { const w = .06 + rnd() * .12, h = .45 + rnd() * .3; if (rnd() > .08) caja(x0 + .88 * dir, y, zz, -.6 * dir * (.6 + rnd() * .4), h, w); zz += w + .01; } } } };
  estante(-3.2, 1, -14, 6); estante(3.2, -1, -14, 6);
  // techo y suelo (rejilla), pared del fondo con puerta
  for (let x = -3.2; x <= 3.21; x += .8) segsB.push(x, 0, -14, x, 0, 6, x, 5, -14, x, 5, 6); for (let z = -14; z <= 6; z += .8) segsB.push(-3.2, 0, z, 3.2, 0, z, -3.2, 5, z, 3.2, 5, z);
  caja(1.2, 0, -14, 1.1, 2.3, .05); for (let i = 0; i < 4; i++) caja(-2.6 + i * 1.6, 4.95, -8 + i * 3, .9, .05, 1.8);
  // túnel octogonal de entrada (z 6..30)
  for (let z = 6; z < 30; z += 1.1) { for (let k = 0; k < 8; k++) { const a = k / 8 * 6.283 + .39, b = (k + 1) / 8 * 6.283 + .39, r = 3.6; segsB.push(Math.cos(a) * r, 2.4 + Math.sin(a) * r, z, Math.cos(b) * r, 2.4 + Math.sin(b) * r, z, Math.cos(a) * r, 2.4 + Math.sin(a) * r, z, Math.cos(a) * r, 2.4 + Math.sin(a) * r, z + 1.1);
    for (let q = 1; q < 5; q++) { const c = (a * (5 - q) + b * q) / 5; segsB.push(Math.cos(c) * r, 2.4 + Math.sin(c) * r, z, Math.cos(c) * r * .86, 2.4 + Math.sin(c) * r * .86, z); } } }
  const bg = new THREE.BufferGeometry(); bg.setAttribute('position', new THREE.Float32BufferAttribute(segsB, 3));
  S4.add(new THREE.LineSegments(bg, new THREE.LineBasicMaterial({ color: 0xBDB8AF, transparent: true, opacity: .32, toneMapped: false, depthWrite: false })));
  // cartel negro con texto
  const cartel = panel(1400, 560, 2.3); cartel.mesh.position.set(0, 3.0, -8.98); S4.add(cartel.mesh);
  const cartelFondo = new THREE.Mesh(new THREE.PlaneGeometry(5.9, 2.4), new THREE.MeshBasicMaterial({ color: 0x050505 })); cartelFondo.position.set(0, 3.0, -9.02); S4.add(cartelFondo);
  const papeles = [...Array(18)].map(() => { const m = new THREE.Mesh(new THREE.PlaneGeometry(.18, .24), new THREE.MeshBasicMaterial({ color: 0xB9B4AA, side: THREE.DoubleSide, toneMapped: false })); m.userData = { x: (rnd() - .5) * 5, y: 1 + rnd() * 3.5, z: -8.7 + rnd() * 3.5, r: rnd() * 6, v: .3 + rnd() * .6 }; S4.add(m); return m; });
  // «pestañas» que crecen del suelo (hebras doradas)
  const hebras = new THREE.Group(); S4.add(hebras);
  for (let i = 0; i < 260; i++) { const x = (rnd() - .5) * 6, z = -8.5 + rnd() * 6.5, h = .5 + rnd() * 1.6, cu = (rnd() - .5) * .8, pts = [];
    for (let k = 0; k <= 12; k++) { const u = k / 12; pts.push(new THREE.Vector3(x + cu * u * u + Math.sin(u * 5 + i) * .05, u * h, z + cu * .5 * u * u)); }
    const l = linea1(pts, rnd() > .5 ? 0xF7E27A : 0xC9B24A, .8); l.userData.t0 = 28.9 + rnd() * .8; hebras.add(l); }
  const CAM4 = [[25.9, 0, 2.4, 29, 0, 2.4, 0, 0], [26.5, 0, 2.4, 9, 0, 2.6, -9, 0], [27.3, -.4, 2.5, .2, .1, 2.95, -9, .05], [28.4, .4, 2.4, -2.2, 0, 3.0, -9, -.04], [29.3, .2, 2.5, -4.6, 0, 3.0, -9, .1], [30.2, -.2, 2.6, -5.8, 0, 3.05, -9, -.08]];
  const f4 = t => {
    const [x, y, z, lx, ly, lz, roll] = kf(CAM4, t); C4.position.set(x + (t > 28.9 ? Math.sin(t * 43) * .04 : 0), y + (t > 28.9 ? Math.cos(t * 37) * .04 : 0), z); C4.lookAt(lx, ly, lz); C4.rotateZ(roll + Math.sin(t * 1.3) * .03);
    const fase = t < 28.1 ? 0 : t < 28.9 ? 1 : 2;
    cartel.pinta(fase + '' + Math.floor(t * 12), g => { g.textBaseline = 'alphabetic';
      if (fase === 0) { const A = [['ATRAPADO', 26.55, 0], ['EN', 26.95, 0], ['GOOGLE', 27.2, 1], ['MAPS,', 27.6, 1]]; let x = 70, y = 220;
        A.forEach(([w, t0, o], i) => { g.font = '900 150px A'; const on = t >= t0; g.fillStyle = on ? (o ? GOLD : '#F4F0E8') : 'rgba(244,240,232,.12)'; if (i === 2) { x = 70; y = 420; } g.fillText(w, x, y); x += g.measureText(w + ' ').width; }); }
      else if (fase === 1) { g.font = '900 170px A'; g.fillStyle = '#F4F0E8'; g.fillText('CON', 90, 330); g.fillStyle = t > 28.45 ? GOLD : 'rgba(244,240,232,.12)'; g.fillText('CUARENTA', 90 + g.measureText('CON ').width, 330); }
      else { g.font = '900 120px A'; g.fillStyle = '#F4F0E8'; g.fillText('CON CUARENTA', 150, 190); g.font = '900 230px A'; g.fillStyle = '#F7D85A'; g.shadowColor = '#F7D85A'; g.shadowBlur = 18; g.fillText('PESTAÑAS', 90, 440); } });
    cartel.mesh.rotation.z = fase === 2 ? -.06 : 0; cartel.mesh.position.x = fase === 1 ? -.6 : 0;
    papeles.forEach((m, i) => { const u = m.userData, tt = t * u.v; m.position.set(u.x + Math.sin(tt + i) * .4, u.y - ((t * .35 * u.v) % 3.5), u.z); m.rotation.set(tt * 1.3, tt, u.r + tt * .7); });
    hebras.children.forEach(l => { const k = E.oC(p(t, l.userData.t0, .9)); l.scale.set(1, Math.max(.001, k), 1); l.material.opacity = .85 * k; });
    return { escena: S4, cam: C4, post: { bloom: .6, radio: .5, umbral: .7, ca: .005, flash: t < 26.05 ? 1 - (t - 25.9) * 6.6 : 0, flashC: 0x000000 } };
  };

  /* ================= 5 · carita + monstruo (30,2–38,2) ================= */
  const S5 = new THREE.Scene(), C5 = camara(38);
  // material «huella dactilar»: rayas finas según la posición, con luz lateral
  const rayado = (col = new THREE.Color(.62, .6, .57)) => new THREE.ShaderMaterial({ uniforms: { col: { value: col }, t: { value: 0 } },
    vertexShader: 'varying vec3 vP, vN; void main(){ vec4 w = modelMatrix*vec4(position,1.); vP = w.xyz; vN = normalize(mat3(modelMatrix)*normal); gl_Position = projectionMatrix*viewMatrix*w; }',
    fragmentShader: `uniform vec3 col; varying vec3 vP, vN; void main(){ vec3 L = normalize(vec3(-.5,.7,.6)); float d = max(dot(vN,L),0.); float rim = pow(1.-abs(vN.z),2.);
      float s = sin(dot(vP, normalize(vec3(.3,1.,.2)))*140. + sin(vP.x*9.)*3.); float lin = smoothstep(.1,.6,s);
      vec3 c = col*(.04 + .96*d)*(.12+.88*lin) + vec3(1.,.5,.18)*rim*.35*d; gl_FragColor = vec4(c,1.); }` });
  const mons = new THREE.Group(); S5.add(mons); semilla(31);
  const bolas = []; for (let i = 0; i < 40; i++) { const r = .22 + rnd() * .55, a = rnd() * 6.283, b = (rnd() - .5) * 2.0, R = .5 + rnd() * 1.1; const m = new THREE.Mesh(new THREE.SphereGeometry(r, 48, 32), rayado()); m.position.set(Math.cos(a) * R, b * .8, Math.sin(a) * R * .7); m.userData.f = rnd() * 6; mons.add(m); bolas.push(m); }
  const tentaculos = []; for (let i = 0; i < 9; i++) { const pts = []; const a = rnd() * 6.283, e = (rnd() - .5) * 1.5; let q = new THREE.Vector3(Math.cos(a) * 1.4, e, Math.sin(a) * 1.0);
    for (let k = 0; k < 6; k++) { pts.push(q.clone()); q.add(new THREE.Vector3(Math.cos(a + k * .4) * .9, (rnd() - .3) * .8, Math.sin(a + k * .3) * .6)); }
    const m = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 80, .1 - i * .006, 12, false), rayado()); mons.add(m); tentaculos.push(m); }
  // ojos
  const ojoTex = (() => { const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d'); g.fillStyle = '#1a0a02'; g.fillRect(0, 0, 256, 256);
    const gr = g.createRadialGradient(128, 128, 10, 128, 128, 118); gr.addColorStop(0, '#FFE9A0'); gr.addColorStop(.25, '#FFB02E'); gr.addColorStop(.7, '#C8561A'); gr.addColorStop(1, '#2a0f04'); g.fillStyle = gr; g.beginPath(); g.arc(128, 128, 118, 0, 7); g.fill();
    for (let i = 0; i < 90; i++) { const a = i / 90 * 6.283; g.strokeStyle = `rgba(90,30,5,${.3 + Math.random() * .4})`; g.beginPath(); g.moveTo(128 + Math.cos(a) * 30, 128 + Math.sin(a) * 30); g.lineTo(128 + Math.cos(a) * 115, 128 + Math.sin(a) * 115); g.stroke(); }
    g.fillStyle = '#050201'; g.beginPath(); g.ellipse(128, 128, 16, 44, 0, 0, 7); g.fill(); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
  const ojos = bolas.slice(0, 9).map((b, i) => { const r = b.geometry.parameters.radius, o = new THREE.Mesh(new THREE.CircleGeometry(r * .55, 48), new THREE.MeshBasicMaterial({ map: ojoTex, toneMapped: false, transparent: true }));
    o.userData = { b, r, t0: 33.3 + i * .22 }; mons.add(o); return o; });
  // carita (disco blanco con rayado fino)
  const caraC = document.createElement('canvas'); caraC.width = caraC.height = 1024; { const g = caraC.getContext('2d'); g.fillStyle = '#EDEAE3'; g.beginPath(); g.arc(512, 512, 500, 0, 7); g.fill();
    for (let y = 0; y < 1024; y += 6) { g.strokeStyle = 'rgba(0,0,0,.035)'; g.beginPath(); g.moveTo(0, y); g.lineTo(1024, y + 30); g.stroke(); }
    g.fillStyle = '#1b1a18'; g.beginPath(); g.arc(380, 400, 40, 0, 7); g.fill(); g.beginPath(); g.arc(644, 400, 40, 0, 7); g.fill(); g.lineWidth = 34; g.lineCap = 'round'; g.strokeStyle = '#1b1a18'; g.beginPath(); g.arc(512, 520, 230, .25, Math.PI - .25); g.stroke(); }
  const caraT = new THREE.CanvasTexture(caraC); caraT.colorSpace = THREE.SRGBColorSpace;
  const carita = new THREE.Group(); const caraF = new THREE.Mesh(new THREE.CircleGeometry(1, 96), new THREE.MeshBasicMaterial({ map: caraT, color: 0xd9d5cd, toneMapped: false }));
  const canto = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, .09, 96, 1, true), new THREE.MeshBasicMaterial({ color: 0x8a867f, side: THREE.DoubleSide })); canto.rotation.x = Math.PI / 2; canto.position.z = -.045; carita.add(caraF, canto); S5.add(carita);
  const rendija = new THREE.Mesh(new THREE.PlaneGeometry(.5, 3), new THREE.MeshBasicMaterial({ color: 0x0a0a0b })); S5.add(rendija);
  const txtCara = panel(1400, 140, .42); S5.add(txtCara.mesh);
  const LIES = [frase([{ s: 'SU', t: 30.9 }, { s: '«LUEGO', t: 31.15 }], .55, { font: '900 200px A' }), frase([{ s: 'TE LA DEJO»,', t: 31.6, oro: 1 }], .6, { font: '900 200px A' })];
  LIES.forEach((g, i) => { g.position.set(-2.9 + i * .5, -1.0 - i * .85, 1.6); g.rotation.set(-.15, .25, .12); S5.add(g); });
  const OJOS = [['CON', 33.3], ['TUS', 33.75], ['OJOS', 34.3], ['DE DUEÑO', 35.1, 1]].map(([s, t0, o], i) => { const g = frase([{ s, t: t0, oro: o }], i === 3 ? .42 : .3, { font: (i >= 2 ? '800' : '700') + ' 200px A' }); g.position.set(-3.5, 2.5 - i * .75 - (i === 3 ? .1 : 0), 1.0); S5.add(g); return g; });
  const hud = panel(W, H, 2 * 9 * Math.tan(19 * Math.PI / 180), { aditivo: false }); S5.add(hud.mesh);
  const ETQ = ['PRISA 0,91', 'MÓVIL SIN BATERÍA', 'PARKING', 'NIÑOS', 'LLUVIA', 'OLVIDO', 'COLA', 'CANSANCIO', '«YA SI ESO»'];
  const f5 = t => {
    const kIn = E.oE(p(t, 30.2, 1.2));
    // cámara: primero la carita en primer plano, luego se aparta y queda arriba a la derecha
    const cz = kf([[30.2, 0, 0, 3.4], [30.9, .3, 0, 4.2], [31.6, 1.2, .4, 9.2], [33.3, 1.0, .2, 9.6], [38.2, 1.1, .3, 8.8]], t);
    C5.position.set(cz[0], cz[1], cz[2]); C5.lookAt(cz[0] - .4, cz[1] - .1, 0);
    const kc = E.io(p(t, 30.85, .9)); carita.position.set(lerp(0, 4.4, kc), lerp(0, 2.2, kc), lerp(.8, 1.2, kc)); carita.scale.setScalar(lerp(.82, .62, kc)); carita.rotation.z = Math.sin(t * .8) * .06;
    rendija.position.set(carita.position.x + lerp(-.9, .6, p(t, 30.2, .7)), carita.position.y, carita.position.z + .06); rendija.scale.set(carita.scale.x * (t < 30.9 ? 1 : 0) * .5, carita.scale.x * .7, 1);
    txtCara.mesh.position.set(carita.position.x, carita.position.y + .55 * carita.scale.x, carita.position.z + .07); txtCara.mesh.scale.setScalar(carita.scale.x / .82 * .5);
    txtCara.pinta(Math.floor(t * 20), g => { const P = [['mira', 30.25], ['detrás', 30.45, 1], ['del', 30.7]]; let x = 250; g.font = '500 110px I'; P.forEach(([w, t0, o]) => { g.fillStyle = t > t0 ? (o ? '#E7A93A' : '#3b3833') : 'rgba(59,56,51,.25)'; g.fillText(w, x, 110); x += g.measureText(w + ' ').width; }); });
    mons.rotation.set(Math.sin(t * .3) * .1, t * .12, 0); mons.position.set(lerp(2.2, 1.4, kIn), -.2, lerp(-3.5, 0, E.io(p(t, 30.8, .9)))); mons.scale.setScalar(1.25);
    bolas.forEach((b, i) => b.scale.setScalar(1 + .04 * Math.sin(t * 2 + b.userData.f)));
    mons.updateMatrixWorld(); const camL = mons.worldToLocal(C5.position.clone());
    ojos.forEach(o => { const { b, r } = o.userData, d = camL.clone().sub(b.position).normalize(); o.position.copy(b.position).addScaledVector(d, r * b.scale.x * 1.01); o.lookAt(C5.position);
      const k = E.oB(p(t, o.userData.t0, .35)); o.scale.set(Math.max(.001, k), Math.max(.001, k * (.3 + .7 * Math.abs(Math.sin(t * .7 + r * 9)) ** .1)), 1); });
    LIES.forEach(g => pintaKaraoke(g, t, { op: cl((t - 30.8) * 4) * (1 - p(t, 33.0, .3)), dim: .15 }));
    OJOS.forEach(g => pintaKaraoke(g, t, { op: cl((t - 33.1) * 4) }));
    hud.mesh.position.copy(C5.position).add(new THREE.Vector3(0, 0, -9).applyQuaternion(C5.quaternion)); hud.mesh.quaternion.copy(C5.quaternion);
    hud.pinta(Math.floor(t * 15), g => { if (t < 32.9) return; const v = new THREE.Vector3();
      ojos.forEach((o, i) => { if (t < o.userData.t0) return; v.setFromMatrixPosition(o.matrixWorld).project(C5); const x = (v.x + 1) / 2 * W, y = (1 - v.y) / 2 * H, r = 46;
        g.strokeStyle = 'rgba(242,120,50,.9)'; g.lineWidth = 2; g.strokeRect(x - r, y - r, r * 2, r * 2); g.fillStyle = 'rgba(242,110,40,.95)'; g.fillRect(x + r - 4, y - r - 26, 150, 24); g.font = '500 16px M'; g.fillStyle = '#140a04'; g.fillText(ETQ[i], x + r + 2, y - r - 9);
        if (i < 4 && t > 33.3 + i * .5) { g.strokeStyle = 'rgba(236,232,225,.35)'; g.beginPath(); g.moveTo(560, 250 + i * 145); g.lineTo(x - r, y); g.stroke(); } });
      g.strokeStyle = 'rgba(236,232,225,.3)'; g.strokeRect(60, 930, 220, 90); g.font = '400 18px M'; g.fillStyle = 'rgba(236,232,225,.5)'; g.fillText('P(olvido)', 76, 958); g.font = '500 40px M'; g.fillStyle = '#F4F0E8'; g.fillText(t < 36 ? '0,16' : '0,17', 76, 1005); });
    return { escena: S5, cam: C5, post: { bloom: .8, radio: .5, umbral: .8, ca: .004, fondo: 0x0c0b0b } };
  };

  return [{ t0: 16.5, t1: 22.15, frame: f1 }, { t0: 22.15, t1: 24.35, frame: f2, dom: d2 }, { t0: 24.35, t1: 25.9, frame: f3 }, { t0: 25.9, t1: 30.2, frame: f4 }, { t0: 30.2, t1: 38.2, frame: f5 }];
}
