// secD.js — 60,3 a 96,5 s: escamas y ojo «OIGO EL TOC» · gráfica y billete «PLEA5E A LA LUNA» · «el último toque llega pronto» · contador «1 TOQUE»
//           · FORMULARIO 5-E · red en papel «acerca, toca, escribe» · apéndice «buscarte en Maps, obsoleto» · hoja de ruta «un toque… y ahí estás»
//           · calendario «sin una sola APP*» · prompt «Mesa 4, por favor, déjanos algo» · «SUBO MI 5»
import { THREE, W, H, E, p, cl, lerp, muelle, linea, trazar, linea1, chispa, camara, panel, frase, pintaKaraoke, semilla, rnd } from './core.js';
import { barraPrompt } from './prompt.js';
import { TRAZOS } from './trazos.js';

const kf = (K, t) => { let i = 0; while (i < K.length - 2 && t >= K[i + 1][0]) i++; const a = K[i], b = K[i + 1], k = E.io(cl((t - a[0]) / (b[0] - a[0] || 1))); return a.slice(1).map((v, j) => lerp(v, b[j + 1], k)); };
const OV = document.getElementById('ov');
const capa = html => { const d = document.createElement('div'); d.className = 'capa'; d.innerHTML = html; OV.appendChild(d); return d; };
const tip = (s, t0, cps, t) => s.slice(0, Math.max(0, Math.min(s.length, Math.floor((t - t0) * cps))));
const PAPEL = '#ECE8DF', TINTA = '#161513', ORO = '#C8912A', ORO2 = '#E3A93A';

export default async function () {
  /* ================= 1 · escamas + ojo (60,3–62,45) ================= */
  const S1 = new THREE.Scene(), C1 = camara(38);
  const piel = new THREE.Mesh(new THREE.PlaneGeometry(18, 10.2), new THREE.ShaderMaterial({ uniforms: { t: { value: 0 }, abre: { value: 0 }, luz: { value: 0 } },
    vertexShader: 'varying vec2 v; void main(){ v = (uv - .5) * vec2(18., 10.2); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: `uniform float t, abre, luz; varying vec2 v;
      vec2 h2(vec2 p){ p = vec2(dot(p,vec2(127.1,311.7)), dot(p,vec2(269.5,183.3))); return fract(sin(p)*43758.5453); }
      vec3 worley(vec2 p){ vec2 i = floor(p), f = fract(p); float d1 = 8., d2 = 8.; vec2 id = vec2(0.);
        for(int y=-1;y<=1;y++) for(int x=-1;x<=1;x++){ vec2 g = vec2(x,y), o = h2(i+g); vec2 r = g + o - f; float d = dot(r,r); if(d < d1){ d2 = d1; d1 = d; id = i+g; } else if(d < d2) d2 = d; }
        return vec3(sqrt(d1), sqrt(d2), h2(id).x); }
      void main(){ vec2 p = v; float ax = 2.7, ay = 1.15; float ex = p.x/ax, ey = p.y/(ay*max(.001, 1.-ex*ex));
        float almendra = smoothstep(1.05, .95, abs(ey)) * step(abs(ex), 1.);
        // escamas: más grandes lejos del ojo
        float esc = mix(1.8, 3.6, smoothstep(2.5, 7., length(p*vec2(.8,1.2))));
        vec3 w = worley(p*esc); float borde = smoothstep(0., .14, w.y - w.x); float cup = 1. - w.x*.9;
        float rayas = .72 + .28*sin((p.x*.6+p.y)*260.);
        vec3 col = vec3(.36,.35,.33)*(.15 + .85*borde)*(.35 + .65*cup)*(.55 + .45*w.z)*rayas;
        // párpado: escamas pequeñas dentro de la almendra
        vec3 w2 = worley(p*7.); float b2 = smoothstep(0., .1, w2.y - w2.x); vec3 lid = vec3(.3,.29,.27)*(.2 + .8*b2)*(.5 + .5*(1.-w2.x))*rayas;
        float rim = smoothstep(.8, 1., abs(ey))*almendra; col = mix(col, lid*(1.-rim*.6), almendra);
        // rendija / iris
        float ab = abre*abs(1.-ex*ex); float dentro = step(abs(p.y), ab*ay) * almendra;
        float fib = .6 + .4*sin(atan(p.y, p.x)*90. + length(p)*20.); float rr = length(p/vec2(1.,1.));
        vec3 iris = mix(vec3(1.,.72,.25), vec3(.75,.25,.05), smoothstep(.2, 1.6, rr)) * fib * (1.2 - rr*.35);
        float pup = smoothstep(.16, .12, abs(p.x)/(1. - pow(p.y/1.1, 2.)*.9)); iris = mix(iris, vec3(.02,.01,0.), pup);
        iris += vec3(1.,.6,.2)*exp(-pow((rr-.55)*5., 2.))*.9;
        col = mix(col, iris, dentro);
        float slit = exp(-pow(p.y/(.012 + ab*.3), 2.))*almendra*step(abre, .02)*(.8 + .2*sin(t*20.)) * luz;
        col += vec3(1.,.5,.15)*slit*2.;
        col *= 1. - .55*smoothstep(3., 9., length(p*vec2(.7,1.)));
        gl_FragColor = vec4(col, 1.); }` }));
  S1.add(piel);
  const lz = linea([new THREE.Vector3(-9, -3, 1), new THREE.Vector3(9, 3, 1)], { color: 0xFF8A36, ancho: 3 }); S1.add(lz);
  const oigo = frase([{ s: 'OIGO', t: 61.05 }, { s: 'EL', t: 61.35 }, { s: 'TOQUE', t: 61.55, oro: 1 }], .26, { font: '800 200px A', ls: 8 }); oigo.position.set(-1.25, -.1, .05); S1.add(oigo);
  const aroTxt = new THREE.Group(); S1.add(aroTxt); { const s = 'OIGO EL TOQUE · OIGO EL TOQUE · '; const f = frase([...s].map(c => ({ s: c })), .2, { font: '800 200px A', letras: 1 }); let acc = 0; const R = 2.55;
    f.children.slice().forEach(m => { const a = Math.PI * .5 + acc / R; acc += m.userData.ink + .05; const pv = new THREE.Group(); pv.position.set(Math.cos(a) * R, Math.sin(a) * R * .72, .05); pv.rotation.z = a + Math.PI / 2; m.position.x = -m.userData.ink / 2; pv.add(m); aroTxt.add(pv); }); }
  const toc = frase([...'TOC'].map(c => ({ s: c })), .55, { font: '900 220px A', letras: 1 }); S1.add(toc);
  const aroL = linea([...Array(121)].map((_, i) => new THREE.Vector3(Math.cos(i / 120 * 6.283) * 3.3, Math.sin(i / 120 * 6.283) * 2.35, .04)), { color: 0xFF8A36, ancho: 1.6, op: .8 }); S1.add(aroL);
  const f1 = t => {
    const ab = E.oE(p(t, 61.95, .4)); piel.material.uniforms.t.value = t; piel.material.uniforms.abre.value = ab; piel.material.uniforms.luz.value = cl((t - 60.55) * 3);
    trazar(lz, E.oC(p(t, 60.3, .2))); lz.visible = t < 60.62;
    pintaKaraoke(oigo, t, { op: (1 - ab) * cl((t - 60.9) * 4), dim: .2 }); oigo.children.forEach(m => m.material.color.lerp(new THREE.Color(1, .6, .25), .5));
    aroTxt.visible = ab > .01; aroTxt.children.forEach((pv, i) => { const m = pv.children[0]; m.material.opacity = E.oC(p(t, 62.0 + i * .008, .2)) * .9; m.material.color.set(0xEFE8DC); });
    toc.visible = ab > .01; toc.position.set(-.55, 1.72, .05); toc.children.forEach((m, i) => { m.material.opacity = E.oC(p(t, 62.05 + i * .06, .15)); m.material.color.set(0xF6F0E6); });
    trazar(aroL, E.oC(p(t, 62.0, .35))); aroL.visible = ab > .01;
    const z = lerp(8.2, 7.6, E.io(p(t, 60.3, 1.7))) - .3 * E.oE(p(t, 61.95, .5)); C1.position.set(Math.sin(t) * .1, -.3 + .2 * p(t, 60.3, 2), z); C1.lookAt(0, 0, 0);
    return { escena: S1, cam: C1, post: { bloom: .7, radio: .5, umbral: .75, ca: .005 } };
  };

  /* ================= 2 · gráfica + billete (62,45–64,1) ================= */
  const d2 = capa(`<div id="d2w" style="position:absolute;inset:-40px;background:${PAPEL};transform-origin:50% 50%">
     <svg id="d2g" width="2000" height="1160" style="position:absolute;left:0;top:0"></svg>
     <div id="d2t" style="position:absolute;left:190px;top:330px;font:900 250px/1 A;letter-spacing:-.02em"></div>
     <div id="d2tag" style="position:absolute;left:1488px;top:190px;padding:4px 12px;background:${ORO2};color:#fff;font:500 22px M">P(toque) ↑</div></div>
   <div id="d2n" style="position:absolute;left:260px;top:170px;width:1400px;height:740px;background:#EEEADF;border:3px solid #9b968c;box-shadow:0 40px 90px rgba(0,0,0,.35);display:none;transform-origin:1180px 390px">
     <svg width="1400" height="740" style="position:absolute;inset:0"><rect x="22" y="22" width="1356" height="696" fill="none" stroke="#b9b3a7" stroke-width="2"/><rect x="36" y="36" width="1328" height="668" fill="none" stroke="#c9c3b7" stroke-width="1" stroke-dasharray="3 5"/>
       ${[...Array(60)].map((_, i) => `<path d="M40 ${60 + i * 10} Q 700 ${40 + i * 10 + (i % 2 ? 20 : -20)} 1360 ${60 + i * 10}" stroke="rgba(150,140,125,.12)" fill="none"/>`).join('')}
       <defs><path id="d2arc" d="M960 300 A 250 250 0 0 1 1400 300"/><radialGradient id="luna"><stop offset="0" stop-color="#d9d6cf"/><stop offset=".7" stop-color="#9c978e"/><stop offset="1" stop-color="#555149"/></radialGradient></defs>
       <text font-family="G" font-style="italic" font-size="34" fill="#8a847a" letter-spacing="6"><textPath href="#d2arc">NOTA DE RESERVA LUNAR</textPath></text>
       <circle cx="1180" cy="390" r="190" fill="none" stroke="#a9a397" stroke-width="3"/><circle cx="1180" cy="390" r="160" fill="url(#luna)"/>
       ${[[1120, 340, 30], [1230, 420, 45], [1160, 470, 18], [1240, 330, 14], [1100, 430, 22]].map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="rgba(80,76,70,.35)" stroke="rgba(255,255,255,.25)"/>`).join('')}
       <text x="60" y="110" font-family="G" font-size="56" fill="#6d675c">5★</text><text x="1260" y="110" font-family="G" font-size="56" fill="#6d675c">5★</text></svg>
     <div style="position:absolute;left:90px;top:300px;font:900 190px/1 A;color:#8e897f">PLEA<span style="color:${ORO2}">5</span>E</div>
     <div id="d2luna" style="position:absolute;left:96px;top:520px;font:500 40px M;letter-spacing:.3em;color:#8e897f"></div></div>`);
  { const g = d2.querySelector('#d2g'); let h = ''; for (let i = 0; i < 12; i++) h += `<line x1="0" x2="2000" y1="${120 + i * 80}" y2="${120 + i * 80}" stroke="rgba(0,0,0,.08)"/>`; semilla(6); let d = 'M40 1000', y = 1000; for (let i = 0; i < 180; i++) { y += (rnd() - .52) * 6 - (i > 150 ? (i - 150) * 2.2 : 0); d += ` L${40 + i * 8} ${y}`; }
    h += `<path id="d2curva" d="${d}" fill="none" stroke="#6b665d" stroke-width="3"/><line x1="1490" y1="0" x2="1490" y2="1160" stroke="${ORO2}" stroke-width="3"/>`; for (let i = 0; i < 12; i++) h += `<text x="1510" y="${126 + i * 80}" font-family="M" font-size="16" fill="#8e897f">10^${30 - i * 2}</text>`; g.innerHTML = h; }
  const f2 = t => { const q = d2.querySelector.bind(d2), nota = t > 63.45;
    q('#d2w').style.display = nota ? 'none' : 'block'; q('#d2w').style.transform = `scale(${1.05 + .05 * p(t, 62.45, 1)}) translateX(${-40 * p(t, 62.45, 1)}px)`;
    const s = 'PLEA5E', n = Math.floor(cl((t - 62.55) * 14, 0, 6)); q('#d2t').innerHTML = [...s].map((c, i) => `<span style="color:${i < n ? (c === '5' ? ORO2 : '#8e897f') : 'rgba(142,137,127,.15)'}">${c}</span>`).join('');
    const c = q('#d2curva'); if (!c._L) c._L = c.getTotalLength(); c.style.strokeDasharray = c._L; c.style.strokeDashoffset = c._L * (1 - E.io(p(t, 62.45, .8)));
    q('#d2n').style.display = nota ? 'block' : 'none'; const kz = E.iE(p(t, 63.7, .45)); q('#d2n').style.transform = `scale(${lerp(.92, 1, E.oE(p(t, 63.45, .4))) * (1 + 7 * kz)}) rotate(${-2 + 2 * p(t, 63.45, .6)}deg)`; q('#d2n').style.opacity = 1 - p(t, 64.0, .1);
    q('#d2luna').textContent = tip('A LA LUNA', 63.55, 30, t); q('#d2luna').style.color = ORO2; return null; };

  /* ================= 3 · «el último toque llega pronto» (64,1–66,0) ================= */
  const S3 = new THREE.Scene(), C3 = camara(40); semilla(15);
  const radiales = new THREE.Group(); S3.add(radiales); for (let i = 0; i < 160; i++) { const a = i / 160 * 6.283 + rnd() * .02; radiales.add(linea1([new THREE.Vector3(Math.cos(a) * .4, Math.sin(a) * .4, 0), new THREE.Vector3(Math.cos(a) * 14, Math.sin(a) * 14, 0)], 0xE6E0D6, .13 + rnd() * .08)); }
  const luzO = chispa(1.6); S3.add(luzO); const luzO2 = chispa(4.5, 0xFFB060); luzO2.material.opacity = .35; S3.add(luzO2);
  const O1 = frase([{ s: 'El', t: 64.45 }, { s: 'último', t: 64.7, oro: 1 }, { s: 'toque', t: 65.0 }], .36, { font: 'italic 200px G' }); O1.position.set(-1.9, .35, .1); S3.add(O1);
  const O2 = frase([{ s: 'llega', t: 65.3, oro: 1 }, { s: 'pronto', t: 65.55, oro: 1 }], .3, { font: 'italic 200px G' }); O2.position.set(-.85, -.55, .1); S3.add(O2);
  const f3 = t => { radiales.rotation.z = t * .02; radiales.children.forEach((l, i) => l.scale.setScalar(.6 + .4 * E.oE(p(t, 64.1, .6)))); luzO.scale.setScalar(1.2 + .25 * Math.sin(t * 9)); luzO.position.set(.3, .05, .2);
    [O1, O2].forEach(g => pintaKaraoke(g, t, { dim: .1, oroC: 0xF0A044 })); C3.position.set(0, 0, lerp(5.2, 4.6, p(t, 64.1, 1.9))); C3.lookAt(0, 0, 0);
    return { escena: S3, cam: C3, post: { bloom: 1.1, radio: .6, umbral: .5, flash: t < 64.25 ? 1 - (t - 64.1) * 6.6 : 0, flashC: 0xEFEAE0 } }; };

  /* ================= 4 · contador mecánico «1 TOQUE» (66,0–70,0) ================= */
  const S4 = new THREE.Scene(), C4 = camara(34);
  const texDig = (() => { const c = document.createElement('canvas'); c.width = 256; c.height = 1280; const g = c.getContext('2d'); const gr = g.createLinearGradient(0, 0, 0, 1280);
    g.fillStyle = '#E9E5DC'; g.fillRect(0, 0, 256, 1280); g.font = '500 110px M'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = '#1c1b19';
    for (let d = 0; d < 10; d++) { g.fillText(String(d), 128, 64 + d * 128); g.fillStyle = 'rgba(0,0,0,.08)'; g.fillRect(0, d * 128, 256, 3); g.fillStyle = '#1c1b19'; } const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
  const tambor = (oro) => { const tx = texDig.clone(); tx.needsUpdate = true; const m = new THREE.Mesh(new THREE.CylinderGeometry(.42, .42, .5, 40, 1, true), new THREE.ShaderMaterial({ uniforms: { map: { value: tx }, oro: { value: oro ? 1 : 0 } },
    vertexShader: 'varying vec2 v; varying vec3 n; void main(){ v = uv; n = normalize(normalMatrix*normal); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: 'uniform sampler2D map; uniform float oro; varying vec2 v; varying vec3 n; void main(){ vec3 c = texture2D(map, vec2(1.-v.y, v.x)).rgb*.72; float sh = pow(max(n.z,0.), .8); c *= .2 + .8*sh; if(oro > .5) c = mix(c, vec3(1.,.62,.2)*(.4+.9*sh), (1.-c.r)*.9); gl_FragColor = vec4(c,1.); }' }));
    m.rotation.z = Math.PI / 2; return m; };
  const fila = new THREE.Group(); S4.add(fila); const TAMB = []; const ND = 30;
  for (let i = 0; i < ND; i++) { const tb = tambor(i === ND - 1); const grupo = Math.floor((ND - 1 - i) / 3); tb.position.x = i * .56 + (ND - 1 - grupo) * 0 + (Math.floor(i / 3)) * .22; fila.add(tb); TAMB.push(tb); if (i % 3 === 2 && i < ND - 1) { const coma = panel(60, 120, .4); coma.pinta(1, g => { g.font = '500 90px M'; g.fillStyle = '#E9E5DC'; g.fillText(',', 10, 90); }); coma.mesh.position.set(tb.position.x + .39, -.15, .45); fila.add(coma.mesh); } }
  const marco = new THREE.Mesh(new THREE.PlaneGeometry(40, 1.4), new THREE.MeshBasicMaterial({ color: 0x1a1918 })); marco.position.set(8, 0, -.6); fila.add(marco);
  const tit4 = panel(1600, 260, 1.55); C4.add(tit4.mesh); const nota4 = panel(1600, 80, .3); C4.add(nota4.mesh); S4.add(C4);
  const f4 = t => { const Lx = TAMB[ND - 1].position.x;
    TAMB.forEach((tb, i) => { const giro = t < 67.8 ? (t - 66) * (8 + i % 5) * 6.283 : 0; const dig = i === ND - 1 ? 1 : 0; const fin = E.oB(p(t, 67.8 + (ND - 1 - i) * .01, .5));
      tb.rotation.x = (1 - fin) * giro + fin * (6.283 * (.95 - .1 * dig)); });
    const [x, y, z, lx] = kf([[66.0, Lx - 4.6, .9, 6.2, Lx - 4.6], [67.2, Lx - 6, .5, 14, Lx - 7], [68.4, Lx - 7, .4, 12.5, Lx - 7], [69.2, Lx - 2.4, .4, 5.4, Lx - 2.4], [70.0, Lx - 1.8, .35, 4.6, Lx - 1.8]], t);
    C4.position.set(x, y, z); C4.lookAt(lx, 0, 0);
    tit4.mesh.position.set(-.45, .95, -5); tit4.mesh.scale.setScalar(.45);
    tit4.pinta(Math.floor(t * 12), g => { g.font = '900 170px A'; let x = 20; const W4 = [['1', 66.15, 1, 'uno'], ['TOQUE', 66.45, 0, 'toque'], ['/', 66.8, 1, 'por'], ['mesa', 67.0, 0, 'mesa']];
      W4.forEach(([w, t0, o, lab]) => { g.font = '900 170px A'; g.fillStyle = t > t0 ? (o ? '#E9B43A' : '#F2EEE6') : 'rgba(236,232,225,.15)'; g.fillText(w, x, 170); const ww = g.measureText(w).width;
        g.font = '400 22px M'; g.fillStyle = 'rgba(236,232,225,.45)'; g.fillText(lab, x + 6, 220); x += ww + 40; }); });
    nota4.mesh.position.set(-1.1, -1.25, -5); nota4.mesh.scale.setScalar(.7); nota4.pinta(t > 68 ? 1 : 0, g => { if (t < 68) return; g.font = '400 30px M'; g.fillStyle = 'rgba(236,232,225,.45)'; g.fillText('* Un toque. Redondeado a la baja, por seguridad.', 10, 50); });
    return { escena: S4, cam: C4, post: { bloom: .7, radio: .5, umbral: .8, ca: .004, fondo: t < 66.6 ? 0x5a5754 : 0x0e0d0d, flash: t < 66.15 ? 1 - (t - 66) * 6.6 : 0, flashC: 0xE0DBD2 } }; };

  /* ================= 5 · FORMULARIO 5-E (70,0–74,0) ================= */
  const d5 = capa(`<div id="d5w" style="position:absolute;left:-60px;top:-60px;width:2040px;height:1400px;background:${PAPEL};color:${TINTA};transform-origin:50% 40%">
     <div style="position:absolute;left:200px;top:120px;width:1300px;height:92px;background:${TINTA};color:${PAPEL};display:flex;align-items:center;gap:40px;padding-left:36px">
       <span style="font:900 62px A">FORMULARIO 5-E</span><span style="font:500 20px M;line-height:1.5;letter-spacing:.08em">EVALUACIÓN DE UNA PLACA NFC<br>EDICIÓN RESUMIDA · ESCRIBE CON CLARIDAD</span></div>
     <div id="d5arch" style="position:absolute;left:1260px;top:180px;border:5px solid ${TINTA};border-radius:10px;padding:6px 18px;font:900 44px A;transform:rotate(-6deg);opacity:0">ARCHIVADO</div>
     <div style="position:absolute;left:210px;top:240px;font:500 17px M;letter-spacing:.08em;color:#55524c">EMITIDO POR · DPTO. DE COSAS QUE FUNCIONAN &nbsp;&nbsp;&nbsp; REF. 5E-0042/★ &nbsp;&nbsp;&nbsp; TIEMPO: 1 TOQUE</div>
     <div style="position:absolute;left:150px;top:360px;width:26px;height:26px;border-radius:50%;background:${TINTA}"></div>
     <div style="position:absolute;left:210px;top:350px;font:500 20px M;letter-spacing:.08em">1. HALLAZGOS <span style="color:#8a857b">(describe lo observado)</span></div>
     <div id="d5h" style="position:absolute;left:300px;top:400px;font:400 58px M"></div><div style="position:absolute;left:210px;top:480px;width:1250px;border-bottom:2px solid ${TINTA}"></div>
     <div style="position:absolute;left:210px;top:540px;font:500 20px M;letter-spacing:.08em">2. ESFUERZO DEL CLIENTE</div>
     <div style="position:absolute;left:560px;top:530px;display:flex;gap:60px;font:500 22px M">${['ALTO', 'MEDIO', 'BAJO', 'UN TOQUE'].map((s, i) => `<span><span id="d5c${i}" style="display:inline-block;width:28px;height:28px;border:3px solid ${TINTA};vertical-align:middle;margin-right:12px;text-align:center;font:900 22px/22px A"></span>${s}</span>`).join('')}</div>
     <div style="position:absolute;left:210px;top:640px;font:500 20px M;letter-spacing:.08em">3. CONCLUSIÓN</div><div id="d5c" style="position:absolute;left:300px;top:680px;font:400 58px M"></div><div style="position:absolute;left:210px;top:760px;width:1250px;border-bottom:2px solid ${TINTA}"></div>
     <div style="position:absolute;left:150px;top:830px;width:26px;height:26px;border-radius:50%;background:${TINTA}"></div>
     <div style="position:absolute;left:210px;top:820px;font:500 20px M;letter-spacing:.08em">4. FIRMA DEL EVALUADOR</div>
     <svg style="position:absolute;left:300px;top:840px" width="600" height="180"><path id="d5f" d="M20 120 C 40 40, 70 30, 80 110 C 90 60, 110 40, 125 110 C 135 60, 160 50, 170 105 M 190 100 C 200 70, 230 70, 225 100 C 220 125, 195 120, 200 95 M 245 100 C 260 60, 290 70, 280 110 M 300 90 C 330 60, 360 90, 330 110 C 310 120, 340 130, 380 100 M 20 140 L 460 130" fill="none" stroke="${TINTA}" stroke-width="4" stroke-linecap="round"/></svg>
     <div style="position:absolute;left:310px;top:1030px;font:400 16px M;color:#8a857b">FIRMA AQUÍ</div>
     <div id="d5s" style="position:absolute;left:1080px;top:760px;border:7px solid ${ORO2};color:${ORO2};padding:10px 26px;transform:rotate(-8deg);text-align:center;opacity:0">
       <div style="font:500 16px M;letter-spacing:.2em">EVALUADO · VISTO BUENO</div><div style="font:900 74px/1 A;letter-spacing:-.01em">BASTA UN TOQUE</div><div style="font:500 16px M;letter-spacing:.2em">DPTO. DE COSAS QUE FUNCIONAN</div></div>
     <div style="position:absolute;left:210px;top:1110px;font:400 17px M;color:#55524c">* «Basta un toque» se define en el Formulario 5-C, que aún no se ha redactado. No separar.</div>
     <div style="position:absolute;left:1300px;top:1100px;font:500 20px M">5. P(toque) EST. &nbsp; <b id="d5p" style="font:500 34px M">0,44</b></div></div>`);
  const f5 = t => { const q = s => d5.querySelector(s);
    const [sx, tx, ty, rz] = kf([[70.0, 1.25, -120, -60, -2], [71.5, 1.18, -80, -40, -1], [72.2, 1.5, -260, -380, 2], [73.3, 1.35, -180, -300, 1], [73.5, .95, 0, 0, -1.5], [74.0, .92, 20, 10, -1.5]], t);
    q('#d5w').style.transform = `translate(${tx}px,${ty}px) scale(${sx}) rotate(${rz}deg)`; q('#d5w').style.filter = t > 71.0 && t < 71.35 ? 'blur(6px)' : 'none';
    q('#d5h').textContent = tip('Con un toque bastaba,', 70.1, 18, t) + (t < 71.4 && Math.floor(t * 3) % 2 ? '▍' : '');
    q('#d5c').textContent = tip('pensamos', 72.05, 16, t) + (t > 72 && t < 72.8 && Math.floor(t * 3) % 2 ? '▍' : ''); q('#d5c3').textContent = t > 71.15 ? '✕' : '';
    const f = q('#d5f'); if (!f._L) f._L = f.getTotalLength(); f.style.strokeDasharray = f._L; f.style.strokeDashoffset = f._L * (1 - E.io(p(t, 72.6, .6)));
    const ks = muelle(t, 71.3, 2.2, .5); q('#d5s').style.opacity = t > 71.3 ? 1 : 0; q('#d5s').style.transform = `rotate(-8deg) scale(${t > 71.3 ? 1.6 - .6 * Math.min(ks, 1.1) : 1})`;
    const ka = muelle(t, 73.35, 2.2, .5); q('#d5arch').style.opacity = t > 73.35 ? 1 : 0; q('#d5arch').style.transform = `rotate(-6deg) scale(${t > 73.35 ? 1.6 - .6 * Math.min(ka, 1.1) : 1})`;
    return null; };

  /* ================= 6 · red en papel (74,0–77,5) ================= */
  const CAP = [5, 6, 6, 3], XC = [300, 720, 1140, 1560];
  let red = ''; CAP.forEach((n, l) => { for (let i = 0; i < n; i++) { const y = 540 - (n - 1) * 70 + i * 140; if (l < 3) CAP[l + 1] && [...Array(CAP[l + 1])].forEach((_, j) => { const y2 = 540 - (CAP[l + 1] - 1) * 70 + j * 140; red += `<line class="ar" data-l="${l}" x1="${XC[l]}" y1="${y}" x2="${XC[l + 1]}" y2="${y2}" stroke="rgba(22,21,19,.35)" stroke-width="1.4"/>`; }); } });
  CAP.forEach((n, l) => { for (let i = 0; i < n; i++) { const y = 540 - (n - 1) * 70 + i * 140; red += `<circle class="no" data-l="${l}" cx="${XC[l]}" cy="${y}" r="24" fill="${PAPEL}" stroke="${TINTA}" stroke-width="3"/>`; } });
  const d6 = capa(`<div id="d6w" style="position:absolute;inset:-40px;background:${PAPEL};color:${TINTA};transform-origin:50% 50%"><svg width="2000" height="1160" style="position:absolute;left:40px;top:60px">${red}</svg>
     <div style="position:absolute;left:300px;top:1000px;font:400 18px M;color:#6d675c">ENTRADA · móvil</div><div style="position:absolute;left:1580px;top:900px;font:400 18px M;color:#6d675c">SALIDA · reseña</div>
     ${[['Acerca', 0, 74.1], ['toca', 1, 74.9], ['escribe,', 2, 75.4]].map(([s, l, t0]) => `<div class="pw" data-t="${t0}" style="position:absolute;left:${XC[l] - 20}px;top:70px;font:800 88px A">${s}</div>`).join('')}
     <div id="d6b" style="position:absolute;left:1150px;top:960px;font:800 84px A;transform:scaleX(-1)">otra vez,</div><div id="d6r" style="position:absolute;left:560px;top:975px;font:800 70px A">repite</div></div>`);
  const f6 = t => { const q = s => d6.querySelector(s);
    const [sx, tx] = kf([[74.0, 1.35, 380], [75.0, 1.1, 120], [76.2, 1.0, 0], [77.5, 1.02, -30]], t); q('#d6w').style.transform = `translateX(${tx}px) scale(${sx}) rotate(${-1 + p(t, 74, 3.5)}deg)`;
    d6.querySelectorAll('.pw').forEach(e => { const k = E.oC(p(t, +e.dataset.t, .2)); e.style.opacity = .12 + .88 * k; e.style.textDecoration = k > .5 ? `underline 6px ${ORO2}` : 'none'; e.style.textUnderlineOffset = '14px'; });
    const ola = (t - 74.1) / .55; d6.querySelectorAll('.no').forEach(c => { const l = +c.dataset.l, on = t < 76.0 ? ola > l && ola < l + 1.4 : (3 - (t - 76.0) / .35) < l + .6 && (3 - (t - 76.0) / .35) > l - .8; c.setAttribute('fill', on ? ORO2 : PAPEL); c.setAttribute('stroke', on ? ORO2 : TINTA); });
    d6.querySelectorAll('.ar').forEach(a => { const l = +a.dataset.l, on = ola > l + .5 && ola < l + 1.5 && t < 76; a.setAttribute('stroke', on ? 'rgba(227,169,58,.8)' : 'rgba(22,21,19,.3)'); });
    q('#d6b').style.opacity = cl((t - 76.0) * 4); q('#d6r').style.opacity = cl((t - 76.8) * 4); return null; };

  /* ================= 7 · apéndice: buscarte en Maps, obsoleto (77,5–81,0) ================= */
  const CAJ = [['ABRIR', 'Google Maps', 250, 560], ['BUSCAR', 'tu negocio', 620, 470], ['BAJAR', 'hasta reseñas', 990, 560], ['PULSAR', 'escribir reseña', 1360, 470], ['ELEGIR', 'estrellas', 1360, 700]];
  const d7 = capa(`<div id="d7w" style="position:absolute;inset:-40px;background:${PAPEL};color:${TINTA};transform-origin:30% 40%">
     <div style="position:absolute;left:150px;top:150px;width:1620px;border-bottom:1.5px solid ${TINTA};font:500 20px M;letter-spacing:.14em;padding-bottom:10px">APÉNDICE C — ARQUITECTURAS ANTIGUAS (SOLO COMO REFERENCIA)</div>
     <div id="d7t" style="position:absolute;left:150px;top:230px;font:800 118px A;white-space:nowrap"></div>
     <svg width="2000" height="1200" style="position:absolute;left:0;top:0">${CAJ.map(([a, b, x, y]) => `<rect x="${x}" y="${y}" width="300" height="130" fill="none" stroke="${TINTA}" stroke-width="3"/><text x="${x + 20}" y="${y + 50}" font-family="M" font-size="24" letter-spacing="3">${a}</text><text x="${x + 20}" y="${y + 95}" font-family="M" font-size="20" fill="#6d675c">${b}</text>`).join('')}
       <path d="M550 625 L620 535 M920 535 L990 625 M1290 625 L1360 535 M1510 600 L1510 700" stroke="${TINTA}" stroke-width="2.5" fill="none" marker-end="url(#fl)"/><defs><marker id="fl" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="${TINTA}"/></marker></defs>
       <text x="1100" y="930" font-family="G" font-style="italic" font-size="26" fill="#55524c">Fig. C.1 — El método antiguo (hasta hoy). Cinco pasos, uno detrás de otro.</text>
       <line id="d7x1" x1="220" y1="440" x2="1720" y2="900" stroke="${ORO2}" stroke-width="10" stroke-linecap="round"/><line id="d7x2" x1="1720" y1="420" x2="240" y2="900" stroke="${ORO2}" stroke-width="10" stroke-linecap="round"/></svg>
     <div id="d7o" style="position:absolute;left:1350px;top:210px;font:700 130px C;color:${ORO2}"></div></div>`);
  const f7 = t => { const q = s => d7.querySelector(s);
    const [sx, tx, ty] = kf([[77.5, 1.7, 500, 350], [78.6, 1.55, 380, 300], [79.0, 1.0, 0, 0], [81.0, 1.03, -10, 0]], t); q('#d7w').style.transform = `translate(${tx}px,${ty}px) scale(${sx})`;
    const P = [['Ahora', 77.6], ['buscarte', 78.1], ['es', 78.5]]; q('#d7t').innerHTML = P.map(([w, t0]) => `<span style="opacity:${t > t0 ? 1 : .12}">${w}</span>`).join(' ');
    q('#d7o').textContent = tip('obsoleto', 79.9, 14, t);
    ['#d7x1', '#d7x2'].forEach((id, i) => { const l = q(id); l.style.strokeDasharray = 1700; l.style.strokeDashoffset = 1700 * (1 - E.oC(p(t, 79.95 + i * .2, .3))); }); return null; };

  /* ================= 8 · hoja de ruta + carita «un toque… y ahí estás» (81,0–85,0) ================= */
  const d8 = capa(`<div style="position:absolute;inset:0;background:#0d0c0c"></div>
     <div id="d8w" style="position:absolute;inset:0;perspective:1400px"><div id="d8in" style="position:absolute;inset:0;transform-style:preserve-3d">
       <svg width="1920" height="1080" style="position:absolute;inset:0"><g id="d8cont" fill="none" stroke="rgba(236,232,225,.13)"></g>
         <line x1="760" y1="-100" x2="760" y2="1200" stroke="rgba(236,232,225,.5)" stroke-width="2" stroke-dasharray="10 12"/>
         ${[['DISEÑO', 'propuesta en 48 h', 180], ['ENLACE', 'tu ficha de Google', 520], ['NFC', 'grabado y probado', 860]].map(([a, b, y]) => `<rect x="742" y="${y - 18}" width="36" height="36" transform="rotate(45 760 ${y})" fill="#0d0c0c" stroke="#ECE8E1" stroke-width="2.5"/><text x="820" y="${y}" font-family="M" font-size="30" fill="#ECE8E1">${a}</text><text x="820" y="${y + 34}" font-family="M" font-size="20" fill="rgba(236,232,225,.5)">${b}</text><rect x="620" y="${y - 14}" width="28" height="28" fill="none" stroke="rgba(236,232,225,.6)" stroke-width="2"/>`).join('')}
         <line id="d8rayo" x1="760" y1="1080" x2="760" y2="1080" stroke="#F2B640" stroke-width="5"/></svg>
       <div id="d8g" style="position:absolute;left:600px;top:560px;font:700 300px/1 N;color:#F2B640;text-shadow:0 0 30px rgba(242,182,64,.6);letter-spacing:-.02em"></div>
       <div id="d8cara" style="position:absolute;left:560px;top:140px;width:800px;height:800px;opacity:0">
         <svg width="800" height="800"><circle cx="400" cy="400" r="330" fill="rgba(20,19,18,.9)" stroke="rgba(236,232,225,.55)" stroke-width="6"/><circle cx="400" cy="400" r="300" fill="none" stroke="rgba(236,232,225,.15)" stroke-width="2"/>
           ${[...Array(12)].map((_, i) => `<circle cx="400" cy="400" r="${30 + i * 22}" fill="none" stroke="rgba(236,232,225,.06)"/>`).join('')}
           <circle id="d8o1" cx="300" cy="360" r="34" fill="#FFB347"/><circle id="d8o2" cx="500" cy="360" r="34" fill="#FFB347"/><path d="M250 470 Q400 610 550 470" fill="none" stroke="rgba(236,232,225,.75)" stroke-width="14" stroke-linecap="round"/></svg>
         <div id="d8ahi" style="position:absolute;left:0;right:0;top:90px;text-align:center;font:900 100px A;color:#F4F0E8"></div><div id="d8est" style="position:absolute;left:0;right:0;top:600px;text-align:center;font:900 110px A;color:#F2B640;text-shadow:0 0 30px rgba(242,182,64,.5)"></div>
         <div id="d8y" style="position:absolute;left:760px;top:230px;font:900 64px A;color:#F4F0E8;transform:rotate(90deg);transform-origin:0 0;white-space:nowrap"></div></div></div></div>`);
  { let h = ''; for (let i = 0; i < 16; i++) h += `<ellipse cx="${300 + Math.sin(i) * 20}" cy="${540}" rx="${80 + i * 55}" ry="${60 + i * 48}"/>`; d8.querySelector('#d8cont').innerHTML = h; }
  const f8 = t => { const q = s => d8.querySelector(s);
    const [rx, ry, tz, tx] = kf([[81.0, 18, -12, -200, 0], [82.2, 10, -6, 0, 0], [82.9, 4, 0, 200, 0], [85.0, 8, 10, 0, 0]], t); q('#d8in').style.transform = `translateZ(${tz}px) translateX(${tx}px) rotateX(${rx}deg) rotateY(${ry}deg)`;
    const ry2 = lerp(1080, 180, E.io(p(t, 81.0, 1.6))); q('#d8rayo').setAttribute('y1', ry2);
    const G = t < 81.8 ? 'UN' : t < 82.5 ? 'TOQUE' : ''; q('#d8g').textContent = G; q('#d8g').style.opacity = G ? 1 : 0; q('#d8g').style.left = t < 81.8 ? '640px' : '560px';
    const kc = cl((t - 82.6) * 3); q('#d8cara').style.opacity = kc; q('#d8cara').style.transform = `scale(${.85 + .15 * E.oB(p(t, 82.6, .5))})`;
    q('#d8ahi').textContent = t > 83.1 ? 'Y AHÍ' : ''; q('#d8est').textContent = t > 83.6 ? 'ESTÁS' : ''; q('#d8y').textContent = t > 82.8 ? 'UN TOQUE' : '';
    ['#d8o1', '#d8o2'].forEach(id => q(id).setAttribute('r', 30 + 6 * Math.sin(t * 8))); return null; };

  /* ================= 9 · calendario «sin una sola APP*» (85,0–88,6) ================= */
  const HIT = [['DISEÑO', '✓', 440], ['APROBADO', '✓', 760], ['APP*', '', 1080], ['ENVÍO', '', 1400], ['EN TU MESA', '▲', 1720]];
  const d9 = capa(`<div style="position:absolute;inset:0;background:#0d0c0c"></div><div id="d9w" style="position:absolute;inset:0;transform-origin:50% 60%">
     <svg width="1920" height="1080" style="position:absolute;inset:0">${[...Array(20)].map((_, i) => `<line x1="${i * 100}" y1="0" x2="${i * 100}" y2="1080" stroke="rgba(236,232,225,.05)"/>`).join('')}
       <line x1="200" y1="760" x2="1900" y2="760" stroke="rgba(236,232,225,.35)" stroke-width="2"/>
       ${HIT.map(([a, b, x], i) => `<g class="hit" data-i="${i}"><rect x="${x - 26}" y="734" width="52" height="52" transform="rotate(45 ${x} 760)" fill="${i < 2 ? '#F2B640' : '#0d0c0c'}" stroke="${i === 2 ? 'rgba(236,232,225,.5)' : '#ECE8E1'}" stroke-width="3" ${i === 2 ? 'stroke-dasharray="6 6"' : ''}/><text x="${x - 40}" y="690" font-family="A" font-weight="800" font-size="34" fill="#ECE8E1">${a}</text><text x="${x - 30}" y="840" font-family="M" font-size="20" fill="${i < 2 ? '#F2B640' : 'rgba(236,232,225,.45)'}">${i < 2 ? 'HECHO' : i === 2 ? 'T-0 d' : ''}</text></g>`).join('')}</svg>
     <div style="position:absolute;left:120px;top:90px;font:800 26px A;color:#ECE8E1;font-style:italic">CALENDARIO — TU PLACA, v1.0</div><div style="position:absolute;left:120px;top:128px;font:400 18px M;color:rgba(236,232,225,.45)">REV. C · BASE · FECHAS EN FIRME</div>
     <div id="d9txt" style="position:absolute;left:520px;top:210px;font:900 110px/1.02 A;color:#F4F0E8"></div>
     <div id="d9app" style="position:absolute;left:900px;top:420px;font:900 260px/1 A;color:#F2B640;text-shadow:0 0 40px rgba(242,182,64,.5);opacity:0">APP<sup style="font-size:120px">*</sup></div>
     <div id="d9st" style="position:absolute;left:910px;top:700px;font:500 40px M;color:#F2B640;opacity:0;white-space:nowrap">ESTADO: NO HACE FALTA</div>
     <div id="d9nota" style="position:absolute;left:910px;top:760px;font:400 30px M;color:rgba(236,232,225,.6);opacity:0;white-space:nowrap">* APP: aplicación que tu cliente no tiene que descargar</div></div>`);
  const f9 = t => { const q = s => d9.querySelector(s);
    const P = [['Sin', 85.1, 0, 0], ['una', 85.5, 1, 90], ['sola', 85.9, 2, 180]]; q('#d9txt').innerHTML = P.map(([w, t0, i, dx]) => `<div style="margin-left:${dx}px;opacity:${t > t0 ? 1 : .1};${i === 2 ? 'color:#F2B640' : ''};text-decoration:${t > t0 ? 'underline 5px' : 'none'};text-underline-offset:12px">${w}</div>`).join('');
    const zoom = E.io(p(t, 86.3, .5)) * (1 - E.io(p(t, 87.9, .5))); q('#d9w').style.transform = `scale(${1 + .45 * zoom}) translate(${-120 * zoom}px,${-60 * zoom}px) rotate(${-2 * zoom}deg)`;
    q('#d9app').style.opacity = cl((t - 86.3) * 4); q('#d9st').style.opacity = cl((t - 86.9) * 4); q('#d9nota').style.opacity = cl((t - 87.3) * 4);
    d9.querySelectorAll('.hit').forEach(g => g.style.opacity = cl((t - 85.0 - +g.dataset.i * .15) * 4)); return null; };

  /* ================= 10 · prompt «Mesa 4, por favor, déjanos algo» (88,6–95,4) ================= */
  const S10 = new THREE.Scene(), C10 = camara(40);
  const guias = new THREE.Group(); S10.add(guias); [-.8, .8].forEach(y => guias.add(linea1([new THREE.Vector3(-20, y, -.1), new THREE.Vector3(20, y, -.1)], 0xffffff, .12)));
  const P10 = barraPrompt(S10, [['Mesa', 89.3, [['Mesa', .41], ['Oye', .22], ['Jefe', .09], ['guapo', .02]]], ['4,', 89.6, [['4', .88]]], ['por', 90.4, [['por', .55], ['porfa', .2]]], ['favor,', 90.7, [['favor', .9]]],
    ['déjanos', 92.3, [['déjanos', .38], ['vuelve', .21], ['recomiéndanos', .08]]], ['algo', 93.4, [['algo', .44], ['una', .31], ['propina', .12]]]], { num: '03', temp: 'T 0,9 · top-p 0,98 · 4 comensales', pie: 'P(toque) 0,49 · según la mesa', x0: -4.3, fin: 95.0,
    vuela: t => E.iC(p(t, 91.6, 3.3)) });
  const f10 = t => { const finX = P10.pinta(t); const [x, z] = kf([[88.6, 0, 7.4], [90.2, 0, 6.2], [92.0, 1.5, 6.6], [95.4, 3.0, 8.4]], t);
    C10.position.set(Math.max(x, finX - 4), .5, z); C10.lookAt(Math.max(x, finX - 4), .2, 0); C10.rotateZ(-.03 * p(t, 91.6, 3));
    P10.g.rotation.z = .04 * E.iC(p(t, 91.6, 3.3)); return { escena: S10, cam: C10, post: { bloom: .8, radio: .5, umbral: .7, ca: .004 } }; };

  /* ================= 11 · «SUBO MI» + 5 gigante en contorno (95,4–96,5) ================= */
  const d11 = capa(`<div style="position:absolute;inset:0;background:#0b0b0c"></div><div id="d11n" style="position:absolute;left:0;right:0;top:40px;text-align:center;font:900 1000px/1 A;color:transparent;-webkit-text-stroke:3px rgba(236,232,225,.14)">5</div>
    <div id="d11t" style="position:absolute;left:0;right:0;top:470px;text-align:center;font:500 40px/1.6 M;letter-spacing:.4em;color:#ECE8E1"></div>`);
  const f11 = t => { const q = s => d11.querySelector(s); q('#d11t').innerHTML = (t > 95.45 ? 'SUBO' : '') + '<br>' + (t > 95.85 ? 'MI' : ''); q('#d11n').style.transform = `scale(${1 + .05 * p(t, 95.4, 1.1)})`; return null; };

  return [{ t0: 60.3, t1: 62.45, frame: f1 }, { t0: 62.45, t1: 64.1, frame: f2, dom: d2 }, { t0: 64.1, t1: 66.0, frame: f3 }, { t0: 66.0, t1: 70.0, frame: f4 }, { t0: 70.0, t1: 74.0, frame: f5, dom: d5 },
    { t0: 74.0, t1: 77.5, frame: f6, dom: d6 }, { t0: 77.5, t1: 81.0, frame: f7, dom: d7 }, { t0: 81.0, t1: 85.0, frame: f8, dom: d8 }, { t0: 85.0, t1: 88.6, frame: f9, dom: d9 }, { t0: 88.6, t1: 95.4, frame: f10 }, { t0: 95.4, t1: 96.5, frame: f11, dom: d11 }];
}
