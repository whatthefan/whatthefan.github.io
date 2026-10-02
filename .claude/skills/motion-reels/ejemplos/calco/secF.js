// secF.js — 126,1 a 157: «tal como predijo tu abuela» · [BOCA] A [BOCA] · pantallas anidadas · portátil 3D «¿Qué vio tu cliente?» · escenario «¿ERA TODO POSTUREO?»
//           · estallido y P(toque) que se dispara · ∞ · «Subo mi P(toque) = NaN» · botón «Volver a tocar» y flashback
import { THREE, W, H, E, p, cl, lerp, muelle, linea, trazar, linea1, chispa, camara, panel, frase, pintaKaraoke, semilla, rnd, renderer } from './core.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const kf = (K, t) => { let i = 0; while (i < K.length - 2 && t >= K[i + 1][0]) i++; const a = K[i], b = K[i + 1], k = E.io(cl((t - a[0]) / (b[0] - a[0] || 1))); return a.slice(1).map((v, j) => lerp(v, b[j + 1], k)); };
const OV = document.getElementById('ov');
const capa = html => { const d = document.createElement('div'); d.className = 'capa'; d.innerHTML = html; OV.appendChild(d); return d; };
const mono = (g, s, x, y, c = 'rgba(236,232,225,.75)', f = '400 26px M') => { g.font = f; g.fillStyle = c; g.fillText(s, x, y); };
const tip = (s, t0, cps, t) => s.slice(0, Math.max(0, Math.min(s.length, Math.floor((t - t0) * cps))));
const GOLD = '#F2B640';

export default async function () {
  /* ================= 1 · «tal como predijo tu abuela» (126,1–128,3) ================= */
  const S1 = new THREE.Scene(), C1 = camara(40);
  const hor = linea([new THREE.Vector3(-12, 0, 0), new THREE.Vector3(12, 0, 0)], { color: 0xFF8A36, ancho: 2 }); S1.add(hor);
  const arcos = [0, 1, 2, 3].map(i => { const R = 1.6 + i * .7; const l = linea([...Array(80)].map((_, k) => { const a = Math.PI * .5 + k / 79 * Math.PI; return new THREE.Vector3(1.2 + Math.cos(a) * R * .6, Math.sin(a) * R, 0); }), { color: 0xE8E3DA, ancho: 1.2, op: .45 }); S1.add(l); return l; });
  const ANOT = ['casi', 'exactamente', 'como', 'lo avisó', 'lo dijo', 'lo sabía', 'de toda la vida'];
  const lab1 = panel(W, H, 2 * 8 * Math.tan(20 * Math.PI / 180), { aditivo: true }); lab1.mesh.position.z = 0; S1.add(lab1.mesh);
  const T1 = frase([{ s: 'TAL', t: 126.4 }, { s: 'COMO', t: 126.7 }, { s: 'PREDIJO', t: 127.1, oro: 1 }], .26, { font: '800 200px A' }); T1.position.set(-1.6, .12, .02); S1.add(T1);
  const abu = frase([{ s: 'tu abuela', t: 127.6, oro: 1 }], .42, { font: '700 220px C' }); abu.position.set(T1.position.x + T1.userData.ancho + .3, .1, .02); S1.add(abu);
  const ch1 = chispa(.7); S1.add(ch1);
  const f1 = t => { trazar(hor, E.io(p(t, 126.1, .6))); arcos.forEach((l, i) => trazar(l, E.io(p(t, 126.5 + i * .12, .6)))); pintaKaraoke(T1, t, { dim: 0, oroC: 0xFF9A3A }); pintaKaraoke(abu, t, { dim: 0, oroC: 0xFF9A3A });
    const cx = lerp(-3.5, 3.5, E.io(p(t, 126.2, 1.8))); ch1.position.set(cx, 0, .05);
    lab1.pinta(Math.floor(t * 10), g => { ANOT.forEach((s, i) => { if (t < 126.9 + i * .1) return; const y = 80 + i * 130 + (i > 4 ? 300 : 0); g.strokeStyle = 'rgba(236,232,225,.3)'; g.beginPath(); g.moveTo(1180, y); g.lineTo(1260, y); g.stroke(); mono(g, s, 1270, y + 8, 'rgba(236,232,225,.6)', '400 22px M'); }); });
    C1.position.set(lerp(-1.5, .5, p(t, 126.1, 2.2)), 0, 7.2); C1.lookAt(C1.position.x, 0, 0); return { escena: S1, cam: C1, post: { bloom: .9, radio: .5, umbral: .6 } }; };

  /* ================= 2 · [BOCA] A [BOCA] + pantallas anidadas (128,3–132,6) ================= */
  semilla(77); let cod = ''; for (let i = 0; i < 2200; i++) { const w = 20 + Math.floor(rnd() * 90); cod += `<i style="display:inline-block;width:${w}px;height:14px;margin:6px 8px;background:rgba(236,232,225,${.04 + rnd() * .12})"></i>`; }
  const pantalla = (n) => `<div class="nido" style="position:absolute;left:50%;top:50%;width:1920px;height:1080px;margin:-540px 0 0 -960px;background:#0e0d0d;overflow:hidden;border:${n ? 6 : 0}px solid rgba(236,232,225,.6)">
      <div style="position:absolute;inset:0;line-height:0">${cod}</div><div style="position:absolute;left:1600px;top:40px;font:500 40px M;color:#F2EEE6">P(toque)<br><span style="color:${GOLD}">0,99</span></div>
      <div class="lin1" style="position:absolute;left:150px;top:300px;font:900 120px A;color:#F2EEE6;white-space:nowrap"></div><div class="lin2" style="position:absolute;left:150px;top:450px;font:900 120px A;color:${GOLD};white-space:nowrap"></div></div>`;
  const d2 = capa(`<div style="position:absolute;inset:0;background:#0b0b0c"></div><div id="f2z" style="position:absolute;inset:0;transform-origin:50% 50%">${pantalla(0)}</div>`);
  { const z = d2.querySelector('#f2z'); let cur = z.querySelector('.nido'); for (let i = 1; i < 4; i++) { cur.insertAdjacentHTML('beforeend', `<div style="position:absolute;left:560px;top:380px;width:800px;height:450px;overflow:hidden"><div style="transform:scale(.4167);transform-origin:0 0;width:1920px;height:1080px;position:absolute">${pantalla(1)}</div></div>`); cur = cur.querySelectorAll('.nido')[1] || cur.querySelector('.nido'); } }
  const mask = w => `<span style="display:inline-block;background:#E9E5DC;color:#1a1918;font:500 30px M;padding:22px 30px;vertical-align:middle;min-width:${w}px;text-align:center;margin:0 8px">[BOCA]</span>`;
  const f2 = t => { const nidos = d2.querySelectorAll('.nido');
    nidos.forEach((n, i) => { const l1 = n.querySelector('.lin1'), l2 = n.querySelector('.lin2');
      if (t < 130.8) { const r1 = t > 128.5, r2 = t > 129.3, r3 = t > 129.9; l1.innerHTML = `DE LOS DÍAS DEL ${r2 ? 'BOCA' : mask(240)}`; l2.innerHTML = `${r3 ? '<span style="color:#F2EEE6">A</span> BOCA' : mask(120) + mask(240)}`; if (!r1) l1.innerHTML = mask(300) + mask(260); }
      else { l1.innerHTML = 'A UN TOQUE,'; l2.innerHTML = t > 131.5 ? 'MESA A MESA' : mask(300) + mask(200); } });
    const kz = t < 130.8 ? 0 : E.io(p(t, 130.8, 1.8)); d2.querySelector('#f2z').style.transform = `scale(${Math.pow(2.4, 3 * (1 - kz)) / Math.pow(2.4, 3)}) rotate(${-4 * Math.sin(kz * 3)}deg)`;
    if (t < 130.8) d2.querySelector('#f2z').style.transform = `scale(${1 + .04 * p(t, 128.3, 2.5)})`;
    return null; };
  // corrige la escala del nido: al principio se ve la pantalla más interior a pantalla completa
  const f2b = t => { const r = f2(t); const z = d2.querySelector('#f2z'); z.style.transformOrigin = '960px 605px'; const kz = t < 130.8 ? 0 : E.io(p(t, 130.8, 1.8)); z.style.transform = t < 130.8 ? `scale(${1 + .04 * p(t, 128.3, 2.5)})` : `scale(${lerp(2.4, .92, kz)}) rotate(${-3 * kz}deg)`; return r; };

  /* ================= 3 · portátil 3D (132,6–138,0) ================= */
  const S3 = new THREE.Scene(), C3 = camara(35); S3.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), .04).texture;
  const suelo = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.MeshStandardMaterial({ color: 0x1c1b1a, roughness: .7, envMapIntensity: .1 })); suelo.rotation.x = -Math.PI / 2; suelo.receiveShadow = true; S3.add(suelo);
  renderer.shadowMap.enabled = true;
  const foco = new THREE.SpotLight(0xfff1e0, 16, 20, .5, .6, 1.2); foco.position.set(0, 6, 1.5); foco.castShadow = true; foco.shadow.mapSize.set(1024, 1024); S3.add(foco, foco.target);
  const carcasa = new THREE.MeshStandardMaterial({ color: 0x2b2a29, metalness: .6, roughness: .45, envMapIntensity: .3 });
  const base = new THREE.Mesh(new THREE.BoxGeometry(3.2, .12, 2.2), carcasa); base.position.y = .06; base.castShadow = true; S3.add(base);
  const tecl = panel(900, 560, 1.8); tecl.mesh.rotation.x = -Math.PI / 2; tecl.mesh.position.set(0, .125, .1); S3.add(tecl.mesh);
  tecl.pinta(1, g => { g.fillStyle = '#1a1918'; g.fillRect(0, 0, 900, 560); for (let r = 0; r < 5; r++) for (let c = 0; c < 13; c++) { g.fillStyle = '#d8d3ca'; g.fillRect(40 + c * 64, 30 + r * 64, 54, 54); } g.fillStyle = '#2a2927'; g.fillRect(300, 380, 300, 160); });
  const tapa = new THREE.Group(); tapa.position.set(0, .12, -1.08); S3.add(tapa);
  const tapaM = new THREE.Mesh(new THREE.BoxGeometry(3.2, 2.1, .08), carcasa); tapaM.position.y = 1.05; tapaM.castShadow = true; tapa.add(tapaM);
  const pant = panel(1600, 1040, 1.96); pant.mesh.position.set(0, 1.05, .045); tapa.add(pant.mesh);
  const peg = panel(1600, 1040, 1.96); peg.mesh.position.set(0, 1.05, -.045); peg.mesh.rotation.y = Math.PI; tapa.add(peg.mesh);
  peg.mesh.material.color.set(0x8f8b84); peg.pinta(1, g => { g.fillStyle = '#E9B43A'; g.fillRect(180, 200, 520, 130); g.font = '900 80px A'; g.fillStyle = '#140f06'; g.fillText('PLEA5E', 230, 295);
    g.fillStyle = '#EDEAE3'; g.beginPath(); g.arc(1200, 300, 130, 0, 7); g.fill(); g.fillStyle = '#1b1a18'; g.beginPath(); g.arc(1150, 270, 16, 0, 7); g.arc(1250, 270, 16, 0, 7); g.fill(); g.lineWidth = 14; g.beginPath(); g.arc(1200, 320, 70, .3, Math.PI - .3); g.strokeStyle = '#1b1a18'; g.stroke();
    g.fillStyle = '#131211'; g.fillRect(300, 480, 380, 380); g.strokeStyle = '#EDEAE3'; g.lineWidth = 6; g.beginPath(); for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, r = i % 2 ? 60 : 140; g.lineTo(490 + Math.cos(a) * r, 670 + Math.sin(a) * r); } g.closePath(); g.stroke();
    g.fillStyle = '#EDEAE3'; g.beginPath(); g.ellipse(1080, 700, 220, 110, -.1, 0, 7); g.fill(); g.fillStyle = '#1b1a18'; g.font = '700 38px A'; g.fillText('DÉJANOS', 990, 690); g.fillText('ALGO', 1030, 735); });
  const T3a = frase([{ s: '¿Qué', t: 133.4 }, { s: 'vio', t: 133.7, oro: 1 }, { s: 'tu', t: 133.95 }, { s: 'cliente?', t: 134.1 }], .16, { font: 'italic 200px G' });
  const T3b = frase([{ s: 'Nunca', t: 134.6, oro: 1 }, { s: 'lo', t: 134.9 }, { s: 'sabrás', t: 135.1, oro: 1 }], .16, { font: 'italic 200px G' });
  const hud3 = new THREE.Group(); hud3.add(T3a, T3b); T3b.position.y = -.28; C3.add(hud3); hud3.position.set(-2.45, 1.2, -5); S3.add(C3);
  const f3 = t => { const ab = t < 134.2 ? 0 : t < 136.6 ? E.oE(p(t, 134.2, .8)) : 1 - E.io(p(t, 136.6, .9)); tapa.rotation.x = lerp(-1.62, -.28, ab) * -1 * -1;
    tapa.rotation.x = lerp(1.55, .28, ab) * -1 + 0; tapa.rotation.x = -lerp(-1.52, .25, ab);
    const glow = t > 134.2 ? cl(ab * 1.2) : 0; pant.pinta(Math.floor(glow * 20), g => { g.fillStyle = `rgb(${Math.round(30 + 170 * glow)},${Math.round(28 + 150 * glow)},${Math.round(24 + 125 * glow)})`; g.fillRect(0, 0, 1600, 1040);
      g.fillStyle = `rgba(90,40,10,${glow})`; g.fillRect(300, 380, 1000, 280); g.strokeStyle = `rgba(240,150,60,${glow})`; g.lineWidth = 6; g.strokeRect(300, 380, 1000, 280); g.font = '500 80px M'; g.fillStyle = `rgba(255,170,90,${glow})`; g.fillText('REDACTADO', 560, 550); });
    foco.intensity = 16 * (1 - .7 * p(t, 136.6, 1.2)); S3.background = null;
    const [x, y, z] = kf([[132.6, 2.4, 1.6, -5.2], [133.6, 1.4, 1.5, -4.6], [134.3, .9, 2.4, 4.8], [135.6, -.6, 2.2, 4.4], [136.6, 0, 1.5, 5.4], [138.0, 0, .9, 6.4]], t); C3.position.set(x, y, z); C3.lookAt(0, .9, 0);
    [T3a, T3b].forEach(g => pintaKaraoke(g, t, { dim: 0, oroC: 0xFF8A3A, op: cl((t - 133.3) * 4) })); hud3.position.set(-2.55, 1.35, -5);
    return { escena: S3, cam: C3, post: { bloom: .8, radio: .6, umbral: .72, ca: .004, fondo: 0x070707 } }; };

  /* ================= 4 · escenario «¿ERA TODO POSTUREO?» (138,0–140,25) ================= */
  const S4 = new THREE.Scene(), C4 = camara(38);
  const telon = (x, w) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, 5.5, 60, 1), new THREE.ShaderMaterial({ vertexShader: 'varying vec2 v; void main(){ v = uv; gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: 'varying vec2 v; void main(){ float f = .5 + .5*sin(v.x*70.); vec3 c = vec3(.42,.05,.04)*(.25 + .75*f)*(.35 + .65*v.y*.8); gl_FragColor = vec4(c,1.); }' })); m.position.set(x, 2.75, -1); return m; };
  S4.add(telon(-3.1, 1.6), telon(3.1, 1.6)); const fondoE = new THREE.Mesh(new THREE.PlaneGeometry(5, 5.5), new THREE.MeshBasicMaterial({ color: 0x050404 })); fondoE.position.set(0, 2.75, -1.2); S4.add(fondoE);
  const marcoE = new THREE.Mesh(new THREE.PlaneGeometry(9, 1.2), new THREE.MeshBasicMaterial({ color: 0x121010 })); marcoE.position.set(0, 5.7, -.9); S4.add(marcoE);
  const cono = new THREE.Mesh(new THREE.ConeGeometry(.75, 3.6, 48, 1, true), new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide,
    vertexShader: 'varying vec2 v; varying vec3 n; void main(){ v = uv; n = normalize(normalMatrix*normal); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: 'varying vec2 v; varying vec3 n; void main(){ float e = pow(1.-abs(n.z), 1.5); float a = (.15 + .5*(1.-v.y))*(.25 + .75*(1.-e)); gl_FragColor = vec4(vec3(1.,.95,.86)*a*.3, 1.); }' })); cono.position.set(0, 2.0, 0); S4.add(cono);
  const charco = new THREE.Mesh(new THREE.CircleGeometry(.8, 48), new THREE.MeshBasicMaterial({ color: 0xB9B3A8, transparent: true, opacity: .7 })); charco.rotation.x = -Math.PI / 2; charco.scale.set(1, .35, 1); charco.position.set(0, .21, 0); S4.add(charco);
  const suelo4 = new THREE.Mesh(new THREE.PlaneGeometry(12, 4), new THREE.MeshBasicMaterial({ color: 0x0b0a0a })); suelo4.rotation.x = -Math.PI / 2; suelo4.position.y = .2; S4.add(suelo4);
  const T4 = frase([{ s: '¿ERA', t: 138.3, oro: 1 }, { s: 'TODO', t: 138.6, oro: 1 }, { s: 'POSTUREO?', t: 139.1 }], .22, { font: '500 200px G', ls: 16, centro: 1 }); T4.position.set(0, 5.62, -.85); S4.add(T4);
  const f4 = t => { pintaKaraoke(T4, t, { dim: .35, oroC: 0xFF7A3A }); C4.position.set(0, 2.9, lerp(9.6, 8.6, p(t, 138, 2.2))); C4.lookAt(0, 2.8, 0);
    const k = p(t, 140.0, .25); return { escena: S4, cam: C4, post: { bloom: .9, radio: .6, umbral: .6, ca: .003, flash: E.iC(k), flashC: 0xF3EEE4 } }; };

  /* ================= 5 · estallido + P(toque) que se dispara (140,25–147,0) ================= */
  const S5 = new THREE.Scene(), C5 = camara(40);
  const rafaga = new THREE.Mesh(new THREE.PlaneGeometry(22, 12.4), new THREE.ShaderMaterial({ uniforms: { t: { value: 0 }, k: { value: 1 } }, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false,
    vertexShader: 'varying vec2 v; void main(){ v = (uv-.5)*vec2(22.,12.4); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: `uniform float t, k; varying vec2 v; float h(float x){ return fract(sin(x*127.1)*43758.5); }
      void main(){ float r = length(v), a = atan(v.y, v.x); float id = floor(a*140.); float s = h(id); float streak = step(.55, s) * smoothstep(0., .6, fract(r*.12*(1.+s) - t*(1.5+s*2.)))*(1.-smoothstep(.0,.25, abs(fract(a*140.)-.5)*2.-.3));
        vec3 c = mix(vec3(1.,.55,.18), vec3(1.,.93,.8), exp(-r*.25)) * (streak*1.1 + exp(-r*r*.9)*1.3 + exp(-r*.45)*.25) * k; gl_FragColor = vec4(c,1.); }` })); S5.add(rafaga);
  const d5 = capa(`<div id="f5n" style="position:absolute;inset:0;font:500 150px M;color:#F2EEE6;text-shadow:0 0 30px rgba(255,255,255,.35)"></div>`);
  const f5 = t => { rafaga.material.uniforms.t.value = t; rafaga.material.uniforms.k.value = t < 142.4 ? 1 : 0; C5.position.set(0, 0, 8); C5.lookAt(0, 0, 0);
    const N = d5.querySelector('#f5n'); const etiq = `<div style="font:500 30px M;letter-spacing:.3em;color:#FF8A3A;margin-bottom:10px">P(TOQUE)</div>`;
    const barra = (k, tx) => `<div style="position:absolute;left:0;right:0;top:${140}px;height:4px;background:linear-gradient(90deg,#FF8A3A ${k * 100}%,rgba(255,138,58,.2) ${k * 100}%);box-shadow:0 0 20px rgba(255,138,58,.7)"></div><div style="position:absolute;left:${k * 100}%;top:110px;font:400 18px M;color:rgba(236,232,225,.6)">${tx}</div>`;
    let h = ''; if (t < 142.5) h = `<div style="position:absolute;left:170px;top:420px">${etiq}1,00${barra(.62, '')}</div>`;
    else if (t < 145.0) { const V = [[142.5, '1,01'], [142.8, '1,10'], [143.1, '1,50'], [143.4, '2,00'], [143.7, '3,14'], [144.1, '10,00'], [144.5, '1.000,00']]; let v = V[0]; V.forEach(x => { if (t >= x[0]) v = x; });
      const big = v[1].length > 5; h = `<div style="position:absolute;left:${big ? 60 : 100}px;top:${big ? 300 : 360}px;width:1800px;font-size:${big ? 230 : 170}px">${etiq}${v[1]}${barra(.3 + .6 * p(t, 142.5, 2.5), v[1] === '3,14' ? 'π (irracional)' : v[1] === '10,00' ? 'un orden de magnitud' : '')}</div>`; }
    else { const n = Math.floor(lerp(3, 1200, E.iC(p(t, 145.0, 1.9)))); let s = '<span style="color:#FF8A3A">1</span>'; for (let i = 0; i < n; i++) s += (i % 3 === 0 ? ' ' : '') + '0'; const fs = n < 30 ? 90 : n < 120 ? 60 : n < 400 ? 34 : 18;
      const ex = n < 12 ? '1e9' : n < 40 ? '1e30' : n < 200 ? '1e100' : '1e1000'; h = `<div style="position:absolute;left:100px;top:120px;width:1720px;font-size:${fs}px;line-height:1.35;word-break:break-all">${etiq.replace('P(TOQUE)', 'P(TOQUE) =')}${s}</div><div style="position:absolute;right:110px;bottom:120px;font:500 44px M;color:#FF8A3A">${ex}</div>`; }
    N.innerHTML = h; return t < 142.5 ? { escena: S5, cam: C5, post: { bloom: 1.2, radio: .7, umbral: .4, flash: t < 140.4 ? 1 - (t - 140.25) * 6.6 : 0, flashC: 0xF3EEE4 } } : null; };

  /* ================= 6 · ∞ (147,0–149,4) ================= */
  const S6 = new THREE.Scene(), C6 = camara(40); const lem = [...Array(300)].map((_, i) => { const a = i / 299 * Math.PI * 2 + Math.PI / 2, s = 2.4 / (1 + Math.sin(a) ** 2); return new THREE.Vector3(Math.cos(a) * s, Math.sin(a) * Math.cos(a) * s, 0); });
  const inf = linea(lem, { color: 0xFF8A36, ancho: 3.2 }); S6.add(inf); const ch6 = chispa(.8); S6.add(ch6); const pi6 = frase([{ s: '3,14' }], .9, { font: '500 200px M', centro: 1 }); pi6.position.y = -.4; S6.add(pi6);
  const inf2 = frase([{ s: '∞' }], 1.3, { font: '500 300px A', centro: 1 }); inf2.position.y = -.6; S6.add(inf2);
  const f6 = t => { const k = E.io(p(t, 147.0, .9)); trazar(inf, k); ch6.position.copy(lem[Math.floor(k * 299)]); ch6.visible = k < 1 && t < 147.9; inf.visible = t < 147.95;
    pi6.visible = t >= 147.95 && t < 148.5; pi6.children.forEach(m => m.material.color.set(0xF2EEE6)); inf2.visible = t >= 148.5; inf2.children.forEach(m => m.material.color.set(0xFF8A36));
    C6.position.set(0, 0, 7); C6.lookAt(0, 0, 0); return { escena: S6, cam: C6, post: { bloom: 1.1, radio: .5, umbral: .5 } }; };

  /* ================= 7 · «Subo mi P(toque) = …» (149,4–153,2) ================= */
  const d7 = capa(`<div style="position:absolute;inset:0;background:#0b0b0c"></div><div id="f7a" style="position:absolute;left:110px;top:250px;font:500 110px I;color:#F2EEE6"></div>
    <div id="f7b" style="position:absolute;left:110px;top:430px;font:400 230px G;color:#FF8A36;text-shadow:0 0 40px rgba(255,138,54,.45);white-space:nowrap"></div><div id="f7n" style="position:absolute;left:112px;top:760px;font:400 22px M;color:rgba(236,232,225,.45)"></div>
    <div style="position:absolute;left:100px;right:100px;top:650px;border-top:1px solid rgba(236,232,225,.15)"></div><div style="position:absolute;right:120px;top:520px;font:400 26px M;color:rgba(236,232,225,.4)">(1)</div>`);
  const f7 = t => { const q = s => d7.querySelector(s); q('#f7a').innerHTML = `Subo${t > 149.8 ? ' mi' : ''}`;
    const R = t < 150.4 ? '' : t < 151.0 ? '∞' : t < 151.6 ? '<span style="display:inline-block;transform:rotate(90deg)">∞</span>' : t < 152.2 ? '<span style="display:inline-flex;flex-direction:column;vertical-align:middle;font-size:.6em;line-height:1;text-align:center"><span style="border-bottom:5px solid #F2EEE6">0</span><span>0</span></span>' : 'NaN';
    q('#f7b').innerHTML = t > 149.9 ? `<i>P</i>(toque) <span style="color:#F2EEE6">=</span> <span style="color:${R === 'NaN' ? '#cfc9bf' : '#F2EEE6'}">${R}</span>` : '';
    q('#f7n').textContent = t > 152.3 ? '* estimación ya no definida' : ''; return null; };

  /* ================= 8 · botón «Volver a tocar» (153,2–155,3) ================= */
  const d8 = capa(`<div style="position:absolute;inset:0;background:#0b0b0c"></div><div id="f8p" style="position:absolute;left:955px;top:470px;width:10px;height:10px;border-radius:50%;background:#FFB45A;box-shadow:0 0 30px 10px rgba(255,150,60,.6)"></div>
    <div id="f8b" style="position:absolute;left:810px;top:540px;width:300px;height:64px;border:2px solid rgba(236,232,225,.55);border-radius:8px;display:flex;align-items:center;justify-content:center;gap:12px;font:500 26px M;color:#F2EEE6;background:#141312;opacity:0">↻ Volver a tocar</div>
    <div id="f8s" style="position:absolute;left:0;right:0;top:622px;text-align:center;font:400 18px M;color:rgba(236,232,225,.45);opacity:0">plea5e.es · placas NFC y QR · pago único</div>
    <svg id="f8c" width="34" height="48" viewBox="0 0 34 48" style="position:absolute;left:1300px;top:760px"><path d="M3 2 L3 38 L12 30 L18 44 L24 41 L18 28 L30 28 Z" fill="#fff" stroke="#000" stroke-width="2"/></svg>
    <div id="f8f" style="position:absolute;inset:0;background:#F3EEE4;opacity:0"></div>`);
  const f8 = t => { const q = s => d8.querySelector(s); q('#f8b').style.opacity = cl((t - 153.6) * 3); q('#f8s').style.opacity = cl((t - 153.9) * 3);
    const k = E.io(p(t, 154.1, .7)); q('#f8c').style.left = lerp(1300, 1000, k) + 'px'; q('#f8c').style.top = lerp(760, 575, k) + 'px';
    const cl_ = t > 154.9; q('#f8b').style.transform = `scale(${cl_ && t < 155.05 ? .94 : 1})`; q('#f8f').style.opacity = cl((t - 155.05) * 6); return null; };

  return [{ t0: 126.1, t1: 128.3, frame: f1 }, { t0: 128.3, t1: 132.6, frame: f2b, dom: d2 }, { t0: 132.6, t1: 138.0, frame: f3 }, { t0: 138.0, t1: 140.25, frame: f4 },
    { t0: 140.25, t1: 147.0, frame: f5, dom: d5 }, { t0: 147.0, t1: 149.4, frame: f6 }, { t0: 149.4, t1: 153.2, frame: f7, dom: d7 }, { t0: 153.2, t1: 155.3, frame: f8, dom: d8 }];
}
