// secA.js — 0 a 16,5 s: chispa y ejes · la Estrellita en TikZ · «Veo chispas de 5★» · «en tus ojos» · circuitos «Tu cliente se va contento,»
//           · «no es sorpresa» · gráfica «Y de pronto, silencio» · paisaje 3D «en tu ficha de Google» · «AHORA ES TU CLIENTE / Y TÚ, SU CAMARERO»
import { THREE, W, H, E, p, cl, lerp, muelle, linea, trazar, linea1, rejilla, chispa, camara, panel, puntosSVG, frase, pintaKaraoke, palabra, ORO, semilla, rnd } from './core.js';
import { TRAZOS } from './trazos.js';

const ORO_L = 0xF2C14E, BL = 0xF1EDE6;
const kf = (K, t) => { let i = 0; while (i < K.length - 2 && t >= K[i + 1][0]) i++; const a = K[i], b = K[i + 1], k = E.io(cl((t - a[0]) / (b[0] - a[0] || 1))); return a.slice(1).map((v, j) => lerp(v, b[j + 1], k)); };
const mono = (g, s, x, y, c = 'rgba(236,232,225,.75)', f = '400 26px M') => { g.font = f; g.fillStyle = c; g.fillText(s, x, y); };

export default async function () {
  /* ================= 1 · el mundo del dibujo (0–9,5) ================= */
  const S1 = new THREE.Scene(), C1 = camara(38), M = new THREE.Group(); S1.add(M);
  M.rotation.set(-.16, .1, 0);
  const rej = rejilla(80, 80, 0xffffff, .055); M.add(rej);
  // ejes radiales desde el origen
  const rad = [...Array(8)].map((_, i) => { const a = i * Math.PI / 8, v = new THREE.Vector3(Math.cos(a), Math.sin(a), 0);
    const l = linea([v.clone().multiplyScalar(-14), new THREE.Vector3(), v.clone().multiplyScalar(14)].flatMap((q, j, arr) => j < 2 ? [...Array(40)].map((_, s) => q.clone().lerp(arr[j + 1], s / 40)) : [q]), { color: ORO, ancho: i % 4 ? 1.1 : 1.8, op: i % 4 ? .45 : .9 }); M.add(l); return l; });
  const org = chispa(.9); M.add(org);
  const eti = panel(1400, 1400, 7, { aditivo: true }); M.add(eti.mesh);
  eti.pinta('ejes', g => { g.font = '400 30px M'; g.fillStyle = 'rgba(236,232,225,.55)'; for (let i = -3; i <= 3; i++) { if (!i) continue; g.fillText(String(i), 700 + i * 200 - 8, 740); g.fillText(String(-i), 660, 700 + i * 200 + 10); } g.fillText('(0,0)', 720, 745); });
  // círculo polar con ángulos
  const circ = linea1([...Array(121)].map((_, i) => new THREE.Vector3(Math.cos(i / 120 * Math.PI * 2) * 2.2, Math.sin(i / 120 * Math.PI * 2) * 2.2, 0)), 0xffffff, .35); M.add(circ);
  const ang = panel(1000, 1000, 5.6, { aditivo: true }); M.add(ang.mesh);
  ang.pinta('a', g => { g.font = '400 22px M'; g.fillStyle = 'rgba(236,232,225,.5)'; for (let a = 30; a < 360; a += 30) { const r = 430; g.fillText(a + '°', 500 + Math.cos(a * Math.PI / 180) * r - 18, 500 - Math.sin(a * Math.PI / 180) * r + 8); } g.fillText('z = 1', 520, 470); });
  // --- la Estrellita en TikZ (coordenadas del sello 0..1024 → mundo)
  const s = .0034, OX = -.2, OY = .1, sello = (x, y) => new THREE.Vector3(OX + (x - 512) * s, OY - (y - 540) * s, 0);
  const cuerpo = puntosSVG(TRAZOS.estrella, 260, { x: OX - 512 * s, y: OY + 540 * s, s });
  const cinco = puntosSVG(TRAZOS.cinco, 220, { x: 0, y: 0, s: 1, flipY: false }).map(q => sello(370.4 + q.x * .5668, 754.5 + q.y * .5668));
  const circulo = (cx, cy, r, n = 48) => [...Array(n + 1)].map((_, i) => sello(cx + Math.cos(i / n * 6.283) * r, cy + Math.sin(i / n * 6.283) * r));
  const curva = (a, b, c, n = 30) => [...Array(n + 1)].map((_, i) => { const k = i / n; return sello(lerp(lerp(a[0], b[0], k), lerp(b[0], c[0], k), k), lerp(lerp(a[1], b[1], k), lerp(b[1], c[1], k), k)); });
  const elipse = (cx, cy, rx, ry, n = 40) => [...Array(n + 1)].map((_, i) => sello(cx + Math.cos(i / n * 6.283) * rx, cy + Math.sin(i / n * 6.283) * ry));
  const PIEZAS = [ // [puntos, t0, dur, etiqueta]
    [cuerpo, 2.0, .55, '% cuerpo'], [circulo(468, 262, 44), 2.55, .14], [circulo(556, 262, 44), 2.64, .14], [circulo(476, 270, 16, 20), 2.78, .06], [circulo(548, 270, 16, 20), 2.82, .06],
    [cinco, 2.9, .4, '% el 5'], [curva([318, 420], [220, 470], [150, 520]), 3.3, .14], [circulo(140, 530, 34), 3.42, .1], [curva([706, 420], [800, 330], [868, 222]), 3.55, .14, '% brazo'], [circulo(880, 205, 36), 3.67, .1],
    [curva([335, 790], [322, 880], [318, 955]), 3.8, .1], [elipse(290, 975, 62, 24), 3.88, .08], [curva([689, 790], [702, 880], [706, 955]), 3.95, .1, '% piernas'], [elipse(734, 975, 62, 24), 4.03, .08]];
  const blancas = PIEZAS.map(([pts]) => { const l = linea(pts, { color: 0xF4F1EA, ancho: 1.8, op: .95 }); M.add(l); return l; });
  // versión «circuito»: tres líneas paralelas y nodos
  const off = (pts, d) => pts.map((q, i) => { const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)], t = b.clone().sub(a).normalize(); return q.clone().add(new THREE.Vector3(-t.y, t.x, 0).multiplyScalar(d)); });
  const circuito = PIEZAS.flatMap(([pts]) => [-.045, 0, .045].map((d, j) => { const l = linea(off(pts, d), { color: j === 1 ? 0xFFB347 : ORO, ancho: j === 1 ? 1.6 : 1.1, op: .95 }); M.add(l); return l; }));
  const nodos = new THREE.Group(); M.add(nodos); semilla(5);
  PIEZAS.forEach(([pts]) => { for (let i = 0; i < pts.length; i += Math.max(8, Math.floor(pts.length / 6))) { const n = new THREE.Mesh(new THREE.RingGeometry(.028, .045, 16), new THREE.MeshBasicMaterial({ color: 0xFFD27A, transparent: true, toneMapped: false })); n.position.copy(pts[i]); nodos.add(n); } });
  const pen = chispa(.55); M.add(pen); const chis = [...Array(26)].map(() => { const c = chispa(.18); M.add(c); return c; });
  const viajeros = [...Array(10)].map(() => { const c = chispa(.35); M.add(c); return c; });
  const etiq = panel(2400, 1400, 8.4, { aditivo: true }); etiq.mesh.position.set(-.2, .1, 0); M.add(etiq.mesh);
  // --- código TikZ que se escribe
  const COD = [['% prompt: "Dibuja una estrella en TikZ."', 1], ['\\begin{tikzpicture}', 0], ['\\draw (0,0) star[5 puntas];', 0, '% cuerpo'], ['\\draw (-0.26,0.84) circle (0.13);', 0, '% ojo'], ['\\draw (0.26,0.84) circle (0.13);', 0, '% ojo'],
    ['\\draw (-0.4,0.3) .. controls ..;', 0, '% el 5'], ['\\draw (-0.6,0.4) .. (-1.2,0.1);', 0, '% brazo'], ['\\draw (0.6,0.4) .. (1.2,1.1);', 0, '% brazo'], ['\\draw (-0.5,-0.8) -- (-0.6,-1.4);', 0, '% pierna'], ['\\draw (0.5,-0.8) -- (0.6,-1.4);', 0, '% pierna']];
  const cod = panel(1300, 520, 2.3); cod.mesh.position.set(-5.3, 3.35, 0); M.add(cod.mesh);
  const tabla = panel(900, 170, 1.0); tabla.mesh.position.set(4.3, -2.75, 0); M.add(tabla.mesh);
  const tabla2 = panel(760, 200, 1.1); tabla2.mesh.position.set(-3.2, -2.55, 0); M.add(tabla2.mesh);
  // --- textos
  const T1 = frase([{ s: 'Veo', t: 1.95 }, { s: 'chispas', t: 2.95, oro: 1 }, { s: 'de', t: 3.25 }], .5); T1.position.set(2.6, 3.9, 0); M.add(T1);
  const G5l = frase([{ s: '5', t: 3.45 }, { s: '★', t: 3.8 }], 2.05, { font: '900 300px A', stroke: 5, strokeC: '#ffffff', letras: 1 }); G5l.position.set(3.2, 1.35, .02); M.add(G5l);
  const G5 = frase([{ s: '5', t: 3.45 }, { s: '★', t: 3.8 }], 2.05, { font: '900 300px A', letras: 1 }); G5.position.set(3.2, 1.35, .03); M.add(G5);
  const T2a = frase([{ s: 'en', t: 4.62 }, { s: 'tus', t: 4.8, oro: 1 }], .5); T2a.position.set(1.1, .55, .05); M.add(T2a);
  const T2b = frase([{ s: 'ojos', t: 5.05, oro: 1 }], .5); T2b.position.set(1.1, -.2, .05); M.add(T2b);
  const T3 = [frase([{ s: 'Tu', t: 5.75 }, { s: 'cliente', t: 5.98 }], .52), frase([{ s: 'se', t: 6.45 }, { s: 'va', t: 6.62 }], .52), frase([{ s: 'contento,', t: 7.15, oro: 1 }], .52)];
  T3.forEach((g, i) => { g.position.set(3.3, 1.0 - i * .78, .05); M.add(g); });
  const T4 = [frase([{ s: 'no', t: 8.3 }, { s: 'es', t: 8.45 }], .56), frase([{ s: 'sorpresa', t: 8.7, oro: 1 }], .56)];
  T4.forEach((g, i) => { g.position.set(-7.4, .9 - i * .85, .05); M.add(g); });
  const sorp = panel(900, 60, .28); sorp.mesh.position.set(-5.7, -.35, .05); M.add(sorp.mesh);
  // V en construcción (primer plano, 1,45–2,05)
  const vx = T1.position.x, vy = T1.position.y, vw = T1.children[0].userData.ink;
  const guias = [0, .5, .72].map((h, i) => { const l = linea([new THREE.Vector3(vx - 3, vy + h, .01), new THREE.Vector3(vx + 6, vy + h, .01)], { color: ORO, ancho: 1.2, op: .8 }); M.add(l); return l; });
  const Vtr = linea([new THREE.Vector3(vx + .02, vy + .5, .02), new THREE.Vector3(vx + vw / 2, vy + .01, .02), new THREE.Vector3(vx + vw - .02, vy + .5, .02)].flatMap((q, j, a) => j < 2 ? [...Array(20)].map((_, k) => q.clone().lerp(a[j + 1], k / 20)) : [q]), { color: 0xFFC060, ancho: 7 }); M.add(Vtr);
  const vlab = panel(800, 200, .4, { aditivo: true }); vlab.mesh.position.set(vx + 1.1, vy + .95, .02); M.add(vlab.mesh);
  vlab.pinta(1, g => { mono(g, 'U+0056  LETRA MAYÚSCULA V', 10, 60, 'rgba(236,232,225,.8)', '400 40px M'); mono(g, 'Archivo 800 · avance 0,62', 10, 130, 'rgba(242,184,74,.9)', '400 34px M'); });

  const CAM1 = [[0, 0, 0, 5.2, 0, 0], [1.3, 0, 0, 8.2, 0, 0], [1.42, vx + .25, vy + .3, 2.2, vx + .25, vy + .3], [1.95, vx + .35, vy + .3, 1.7, vx + .35, vy + .28], [2.35, .9, .9, 11.5, .9, .7], [3.1, 1.6, 1.4, 10.4, 1.8, 1.3],
    [3.9, 3.3, 2.0, 7.4, 3.8, 2.0], [4.45, 3.9, 1.8, 6.8, 4.2, 1.6], [4.62, .6, .7, 4.3, .8, .6], [5.45, .75, .5, 4.1, .9, .5], [5.9, 1.9, -.1, 10.6, 1.9, -.1], [7.8, 2.1, -.2, 10.0, 2.1, -.2], [8.25, -2.9, 0, 10.2, -2.9, 0], [9.5, -3.3, 0, 9.6, -3.3, 0]];

  const f1 = t => {
    const [cx, cy, cz, lx, ly] = kf(CAM1, t); C1.position.set(cx + Math.sin(t * .7) * .05, cy + Math.cos(t * .5) * .04, cz); C1.lookAt(lx, ly, 0);
    rej.material.opacity = .055 * cl(t * 4) * (t < 9.1 ? 1 : 1 - p(t, 9.1, .3));
    rad.forEach((l, i) => { trazar(l, E.oC(p(t, .12 + i * .03, .55))); l.material.opacity = (i % 4 ? .45 : .9) * (1 - .75 * p(t, 1.35, .5)) * (t < 9.1 ? 1 : 0); });
    org.visible = t < 2.2; org.scale.setScalar(.25 + .65 * E.oE(p(t, 0, .25)) + .06 * Math.sin(t * 30));
    eti.mesh.material.opacity = cl((t - .3) * 3) * (1 - p(t, 1.35, .4));
    circ.material.opacity = .35 * cl((t - .75) * 3) * (1 - p(t, 2.6, .8)); circ.geometry.setDrawRange(0, Math.floor(121 * E.oC(p(t, .78, .5))));
    ang.mesh.material.opacity = .9 * cl((t - 1.0) * 3) * (1 - p(t, 2.6, .8));
    // V en construcción
    const vv = t > 1.3 && t < 2.3; guias.forEach((l, i) => { l.visible = vv; trazar(l, E.oC(p(t, 1.4 + i * .05, .4))); l.material.opacity = .8 * (1 - p(t, 2.0, .25)); });
    Vtr.visible = vv; trazar(Vtr, E.io(p(t, 1.5, .4))); Vtr.material.opacity = 1 - p(t, 1.97, .15); vlab.mesh.visible = vv; vlab.mesh.material.opacity = cl((t - 1.5) * 4) * (1 - p(t, 1.97, .2));
    // piezas: blanco hasta 5,5; luego circuito; en 8,1 vuelve al blanco fino
    const circOn = cl((t - 5.45) / .4) * (1 - cl((t - 8.0) / .4)), blancoOp = t < 5.5 ? 1 : .35 + .65 * cl((t - 8.0) / .4);
    let penP = null;
    PIEZAS.forEach(([pts, t0, d, et], i) => { const k = cl((t - t0) / d); trazar(blancas[i], k); blancas[i].material.opacity = .95 * blancoOp * (1 - p(t, 9.0, .35));
      if (k > 0 && k < 1) penP = pts[Math.floor(k * (pts.length - 1))];
      for (let j = 0; j < 3; j++) { const l = circuito[i * 3 + j]; trazar(l, E.io(p(t, 5.45 + i * .04 + j * .03, .6))); l.material.opacity = .95 * circOn; } });
    nodos.children.forEach((n, i) => { n.material.opacity = circOn * (.6 + .4 * Math.sin(t * 6 + i)); });
    pen.visible = !!penP && t < 4.2; if (penP) pen.position.copy(penP).setZ(.03); pen.scale.setScalar(.45 + .15 * Math.sin(t * 40));
    // chispas del brazo levantado hacia el 5★ (3,7–4,5)
    const mano = sello(880, 205); chis.forEach((c, i) => { const u = (t - 3.62 - i * .03); c.visible = u > 0 && u < .55; if (!c.visible) return; const a = .9 + (i % 7) * .09 - .3, v = 2.2 + (i % 5) * .5;
      c.position.set(mano.x + Math.cos(a) * v * u, mano.y + Math.sin(a) * v * u - 1.4 * u * u, .04); c.material.opacity = 1 - u / .55; c.scale.setScalar(.14 + .08 * (i % 3)); });
    // chispas que viajan por el circuito
    viajeros.forEach((c, i) => { const [pts] = PIEZAS[(i * 3) % PIEZAS.length]; const k = ((t * .5 + i * .13) % 1); c.visible = circOn > .1; c.position.copy(pts[Math.floor(k * (pts.length - 1))]).setZ(.04); c.material.opacity = circOn; });
    etiq.pinta(Math.floor(t * 10), g => { g.font = '400 30px M'; g.fillStyle = 'rgba(242,170,70,.85)';
      if (t > 2.3 && t < 5.4) g.fillText('% cuerpo', 1650, 1000); if (t > 3.3 && t < 5.4) g.fillText('% el 5', 1300, 820); if (t > 3.6 && t < 5.4) g.fillText('% brazo', 1900, 260);
      if (t > 3.95 && t < 5.4) g.fillText('% piernas', 1500, 1330); if (t > 4.62 && t < 5.5) { g.fillStyle = 'rgba(236,232,225,.7)'; g.fillText('r = 0,13', 1330, 430); } });
    // código
    cod.mesh.material.opacity = cl((t - 1.95) * 4) * (1 - p(t, 5.2, .4)); if (t > 1.9 && t < 5.7) cod.pinta(Math.floor(t * 30), g => {
      let yy = 50; COD.forEach(([s, esCom, com], i) => { const t0 = 2.0 + i * .23, n = Math.floor(cl((t - t0) * 60, 0, s.length)); if (n <= 0) return;
        g.font = '400 34px M'; g.fillStyle = esCom ? 'rgba(236,232,225,.55)' : 'rgba(236,232,225,.82)'; g.fillText(s.slice(0, n), 20, yy);
        if (com && n === s.length) { g.fillStyle = 'rgba(242,170,70,.8)'; g.fillText(com, 830, yy); } if (n < s.length) { g.fillStyle = '#F2B84A'; g.fillRect(20 + g.measureText(s.slice(0, n)).width + 4, yy - 28, 16, 34); } yy += 48; }); });
    tabla.mesh.material.opacity = cl((t - 2.3) * 3) * (1 - p(t, 5.2, .4)); tabla.pinta(t > 2.3 ? 1 : 0, g => { g.strokeStyle = 'rgba(236,232,225,.4)'; g.lineWidth = 2; g.strokeRect(4, 4, 890, 160); g.beginPath(); g.moveTo(4, 60); g.lineTo(894, 60); g.moveTo(200, 4); g.lineTo(200, 164); g.moveTo(560, 60); g.lineTo(560, 164); g.stroke();
      mono(g, 'TÍTULO', 20, 42, 'rgba(236,232,225,.6)', '400 26px M'); mono(g, 'estrella (exp. 1)', 220, 42, 'rgba(236,232,225,.85)', '400 26px M'); mono(g, 'DIBUJO', 20, 110, 'rgba(236,232,225,.6)', '400 26px M'); mono(g, 'la mascota', 220, 110, 'rgba(236,232,225,.85)', '400 26px M'); mono(g, 'CÓDIGO ✓', 590, 110, 'rgba(242,184,74,.9)', '400 26px M'); });
    tabla2.mesh.material.opacity = cl((t - 5.7) * 3) * (1 - p(t, 9.0, .3)); tabla2.pinta(Math.floor(t * 4), g => { const F = [['mesa', 'paso', 'toques', 'P(toque)'], ['4', '0', '0', '0,02'], ['4', '4.000', '0', '0,03'], ['4', '32.000', '1', '0,04']];
      F.forEach((r, i) => r.forEach((c, j) => { if (i && t < 5.9 + i * .35) return; mono(g, c, 20 + j * 180, 40 + i * 44, i ? (i === 3 ? 'rgba(242,184,74,.95)' : 'rgba(236,232,225,.75)') : 'rgba(236,232,225,.5)', '400 26px M'); })); });
    // textos karaoke
    pintaKaraoke(T1, t, { op: 1 - p(t, 5.3, .3) }); T1.visible = t > 1.9;
    G5l.children.forEach((m, i) => { m.material.opacity = .22 * cl((t - 3.2) * 4) * (1 - p(t, 5.3, .3)); m.material.color.set(0xb0aaa0); });
    G5.children.forEach((m, i) => { const w = m.userData.it, k = E.oC(p(t, w.t, .15)); m.material.opacity = k * (1 - p(t, 5.3, .3)); m.material.color.set(0xF0B43C).lerp(new THREE.Color(0xFFE6BE), p(t, 4.3, .6)); m.position.y = (1 - E.oB(p(t, w.t, .3))) * -.4; });
    pintaKaraoke(T2a, t, { op: cl((t - 4.4) * 4) * (1 - p(t, 5.45, .25)) }); pintaKaraoke(T2b, t, { op: cl((t - 4.4) * 4) * (1 - p(t, 5.45, .25)) });
    T3.forEach(g => pintaKaraoke(g, t, { op: cl((t - 5.6) * 4) * (1 - p(t, 8.0, .3)) }));
    T4.forEach(g => pintaKaraoke(g, t, { op: cl((t - 8.1) * 4) * (1 - p(t, 9.35, .15)) }));
    sorp.mesh.material.opacity = 1 - p(t, 9.35, .15); sorp.pinta(Math.floor(t * 40), g => { const s1 = 'sorpresa   −log p = ', n = Math.floor(cl((t - 8.85) * 40, 0, s1.length)); mono(g, s1.slice(0, n), 0, 44, 'rgba(236,232,225,.7)', '400 36px M'); if (n === s1.length) mono(g, (t < 9.2 ? (Math.random() * .2).toFixed(2).replace('.', ',') : '0,00') + ' nats', g.measureText(s1).width, 44, 'rgba(242,184,74,.95)', '400 36px M'); });
    return { escena: S1, cam: C1, post: { bloom: .75, radio: .45, umbral: .6 } };
  };

  /* ================= 2 · gráfica «Y de pronto, silencio» (9,5–11,1) ================= */
  const S2 = new THREE.Scene(), C2 = camara(38), G2 = new THREE.Group(); S2.add(G2); G2.rotation.set(-.05, .12, 0);
  const ejes = linea1([new THREE.Vector3(-5.5, 3, 0), new THREE.Vector3(-5.5, -3, 0), new THREE.Vector3(6, -3, 0)], 0xffffff, .35); G2.add(ejes);
  const lab2 = panel(2400, 1300, 6.9, { aditivo: true }); lab2.mesh.position.set(.3, -.1, 0); G2.add(lab2.mesh);
  lab2.pinta(1, g => { mono(g, 'reseñas/semana     negocio: tu-bar-v2     suavizado: 0', 150, 60, 'rgba(236,232,225,.55)', '400 30px M');
    ['1e2', '1e1', '1e0', '1e-1'].forEach((s, i) => mono(g, s, 40, 150 + i * 330, 'rgba(236,232,225,.45)', '400 26px M')); mono(g, 'SEMANAS →', 2150, 1270, 'rgba(236,232,225,.45)', '400 26px M'); g.save(); g.translate(60, 820); g.rotate(-Math.PI / 2); mono(g, 'RESEÑAS (log)', 0, 0, 'rgba(236,232,225,.45)', '400 24px M'); g.restore(); });
  semilla(9); const curvaP = []; for (let i = 0; i <= 300; i++) { const x = -5.4 + i / 300 * 7.6; let y = 1.9 - Math.pow(i / 300, .6) * .5 + (rnd() - .5) * .22 + (i < 12 ? (12 - i) * .06 : 0); curvaP.push(new THREE.Vector3(x, y, 0)); }
  for (let i = 1; i <= 40; i++) curvaP.push(new THREE.Vector3(2.2 + i * .004, curvaP[300].y - i * .12, 0));
  const curvaL = linea(curvaP, { color: 0xFF9A3A, ancho: 2.4 }); G2.add(curvaL); const pen2 = chispa(.6); G2.add(pen2);
  const TX2 = 'Y de pronto, silencio', L2 = frase([...TX2].map(c => ({ s: c })), .34, { letras: 1, font: '800 200px A' }); G2.add(L2);
  const f2 = t => { const k = E.io(p(t, 9.5, 1.35)), n = curvaP.length, i = Math.floor(k * (n - 1)); trazar(curvaL, k); pen2.position.copy(curvaP[i]).setZ(.02); pen2.visible = k < 1;
    C2.position.set(lerp(-.8, 1.2, E.io(p(t, 9.5, 1.5))), lerp(.6, .5, p(t, 9.5, 1.5)), lerp(11.5, 8.6, E.io(p(t, 9.5, 1.5)))); C2.lookAt(lerp(-1.2, 1.5, E.io(p(t, 9.5, 1.5))), lerp(1.1, .8, p(t, 9.5, 1.5)), 0);
    lab2.mesh.material.opacity = cl((t - 9.5) * 4); ejes.material.opacity = .35 * cl((t - 9.5) * 4);
    // letras sobre la curva, detrás de la chispa
    const cab = curvaP[i], inks = L2.children.map(m => m.userData.ink), tot = inks.reduce((a, b) => a + b, 0); let acum = 0;
    const yCurva = x => { let s0 = 0, n0 = 0; for (const c of curvaP) if (Math.abs(c.x - x) < .25 && c.x < 2.21) { s0 += c.y; n0++; } return n0 ? s0 / n0 : curvaP[300].y; };
    L2.children.forEach((m, j) => { const xL = cab.x - .25 - (tot - acum); acum += inks[j];
      const cae = j >= 13 && k > .93 ? E.iC(p(t, 10.55 + (j - 13) * .03, .5)) : 0; const y0 = yCurva(xL + inks[j] / 2), y1 = yCurva(xL + inks[j] / 2 + .2);
      m.position.set(xL, y0 + .1 - cae * 3, .02); m.rotation.z = Math.atan2(y1 - y0, .2) * .6 + cae * (j % 2 ? 1 : -1);
      m.visible = xL > -5.4; m.material.opacity = cl((xL + 5.4) * 3) * (1 - cae * .7); m.material.color.set(j >= 13 ? 0xF2B84A : 0xF1EDE6); });
    return { escena: S2, cam: C2, post: { bloom: .8, radio: .45, umbral: .6, flash: t > 11.0 ? (t - 11.0) * 4 : 0, flashC: 0x000000 } };
  };

  /* ================= 3 · paisaje 3D de curvas de nivel (11,05–16,5) ================= */
  const S3 = new THREE.Scene(), C3 = camara(42); S3.fog = new THREE.Fog(0x0a0a0b, 8, 38);
  const altura = (x, z) => { const r2 = x * x + z * z; semilla(1); return -3.4 * Math.exp(-r2 / 4.2) - 1.3 * Math.exp(-r2 / 45) + .45 * Math.sin(x * .55 + z * .3) * Math.cos(z * .45 - x * .2) + .22 * Math.sin(x * 1.3 - z * .9) + .12 * Math.sin(z * 2.1 + x); };
  const N = 150, EXT = 32, st = EXT / N, Hh = []; for (let j = 0; j <= N; j++) { Hh[j] = []; for (let i = 0; i <= N; i++) Hh[j][i] = altura(-EXT / 2 + i * st, -EXT / 2 + j * st); }
  const segs = []; for (let L = -4.9; L < 1.1; L += .07) { for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
    const a = Hh[j][i], b = Hh[j][i + 1], c = Hh[j + 1][i + 1], d = Hh[j + 1][i], x = -EXT / 2 + i * st, z = -EXT / 2 + j * st;
    const idx = (a > L) | ((b > L) << 1) | ((c > L) << 2) | ((d > L) << 3); if (idx === 0 || idx === 15) continue;
    const e = [[x + st * (L - a) / (b - a), z], [x + st, z + st * (L - b) / (c - b)], [x + st * (L - d) / (c - d), z + st], [x, z + st * (L - a) / (d - a)]];
    const S = { 1: [3, 0], 2: [0, 1], 3: [3, 1], 4: [1, 2], 5: [3, 2, 0, 1], 6: [0, 2], 7: [3, 2], 8: [2, 3], 9: [0, 2], 10: [0, 3, 1, 2], 11: [1, 2], 12: [1, 3], 13: [0, 1], 14: [0, 3] }[idx];
    for (let q = 0; q < S.length; q += 2) segs.push(e[S[q]][0], L, e[S[q]][1], e[S[q + 1]][0], L, e[S[q + 1]][1]); } }
  const tg = new THREE.BufferGeometry(); tg.setAttribute('position', new THREE.Float32BufferAttribute(segs, 3));
  const terreno = new THREE.LineSegments(tg, new THREE.LineBasicMaterial({ color: 0xDCD8D0, transparent: true, opacity: .5, toneMapped: false, depthWrite: false })); S3.add(terreno);
  // camino naranja que baja al mínimo (ruidoso, en espiral)
  semilla(21); const cam3 = []; for (let i = 0; i <= 260; i++) { const k = i / 260, a = 2.4 + k * 5.2, r = 10.5 * Math.pow(1 - k, 1.3) + .15 + Math.sin(k * 60) * .12 * (1 - k); const x = Math.cos(a) * r + (rnd() - .5) * .18 * (1 - k), z = Math.sin(a) * r + (rnd() - .5) * .18 * (1 - k); cam3.push(new THREE.Vector3(x, altura(x, z) + .05, z)); }
  const camino = linea(cam3, { color: 0xFF7A2A, ancho: 2.6 }); S3.add(camino); const pen3 = chispa(.7); S3.add(pen3);
  const rayo = linea([new THREE.Vector3(-6, 14, 4), new THREE.Vector3(-6, altura(-6, 4), 4)], { color: 0xFFB060, ancho: 2.5 }); S3.add(rayo);
  // «en tu ficha de Google» sobre la ladera
  const T5 = frase([{ s: 'en', t: 11.35 }, { s: 'tu', t: 11.55, oro: 1 }, { s: 'ficha', t: 11.75, oro: 1 }, { s: 'de', t: 12.0, oro: 1 }, { s: 'Google', t: 12.15, oro: 1 }], .55); S3.add(T5);
  const ladera = [...Array(80)].map((_, i) => { const a = 3.3 + i / 80 * 1.3, r = 6.2; const x = Math.cos(a) * r, z = Math.sin(a) * r; return new THREE.Vector3(x, altura(x, z) + .08, z); });
  let acc = 0; T5.children.forEach((m, i) => { m.userData.s0 = acc + i * .25; acc += m.userData.ink; });
  // CLIENTE / CAMARERO
  const tMono = panel(900, 90, .42); S3.add(tMono.mesh); const tMono2 = panel(900, 90, .42); S3.add(tMono2.mesh);
  const CL = frase([...'CLIENTE'].map((c, i) => ({ s: c, t: 13.35 + i * .09 })), 1.35, { font: '900 300px A', letras: 1 }); S3.add(CL);
  const CLo = frase([...'CLIENTE'].map((c, i) => ({ s: c })), 1.35, { font: '900 300px A', letras: 1, stroke: 4, strokeC: '#fff' }); S3.add(CLo);
  const CA = frase([...'CAMARERO'].map((c, i) => ({ s: c, t: 15.55 + i * .07 })), 1.25, { font: '900 300px A', letras: 1 }); S3.add(CA);
  const minimo = panel(800, 120, .45, { aditivo: true }); S3.add(minimo.mesh); minimo.pinta(1, g => { mono(g, 'mínimo agudo', 10, 45, 'rgba(236,232,225,.75)', '400 34px M'); mono(g, '(se olvida fácil)', 10, 95, 'rgba(236,232,225,.45)', '400 34px M'); });
  const pt = panel(600, 70, .3, { aditivo: true }); S3.add(pt.mesh); pt.pinta(1, g => mono(g, 'P(toque) 0,04', 10, 50, 'rgba(255,140,60,.95)', '500 40px M'));
  // coloca los textos en el plano de arriba (vista cenital): tumbados en y≈1,5
  const tumba = (o, x, z, rz = 0) => { o.rotation.set(-Math.PI / 2, 0, rz); o.position.set(x, 1.6, z); };
  tumba(CL, -3.6, -1.2); tumba(CLo, -3.6, -1.2); tumba(tMono.mesh, -3.4, -2.35); tumba(minimo.mesh, 1.6, .5); tumba(pt.mesh, -1.5, 5.4);
  CA.rotation.set(-Math.PI / 2, 0, Math.PI); CA.position.set(3.7, 1.62, 1.7); tMono2.mesh.rotation.set(-Math.PI / 2, 0, Math.PI); tMono2.mesh.position.set(3.4, 1.62, 2.75);
  const CAM3 = [[11.05, -9, 7.5, 12, -3, 0, 2], [12.4, -2.5, 4.5, 8, 0, -1, 0], [12.9, 0, 12.5, 2.2, 0, 0, .3], [15.0, .1, 11.8, 2.0, 0, 0, .3], [16.3, .1, 11.2, 1.6, 0, 0, .3]];
  const f3 = t => {
    const [x, y, z, lx, ly, lz] = kf(CAM3, t); C3.position.set(x, y, z); C3.up.set(0, 1, 0);
    if (t > 12.7) { const roll = E.ioE(p(t, 14.9, 1.1)) * Math.PI + Math.sin(t * .3) * .05; C3.up.set(Math.sin(roll), 0, -Math.cos(roll)); }
    C3.lookAt(lx, ly, lz);
    terreno.material.opacity = .5 * cl((t - 11.0) * 5);
    const kc = E.io(p(t, 12.6, 2.2)); trazar(camino, kc); pen3.visible = kc > 0 && kc < 1; pen3.position.copy(cam3[Math.floor(kc * 259)]);
    rayo.visible = t < 12.0; trazar(rayo, E.oC(p(t, 11.0, .35))); rayo.material.opacity = 1 - p(t, 11.6, .4);
    // palabras siguiendo la ladera
    const v1 = new THREE.Vector3(), v2 = new THREE.Vector3();
    T5.children.forEach((m, i) => { const sP = m.userData.s0 * .9 + (t - 11.2) * .8, idx = Math.min(78, Math.max(0, Math.floor(sP / 8.1 * 79))), q = ladera[idx], q2 = ladera[idx + 1];
      m.position.copy(q); m.quaternion.copy(C3.quaternion); v1.copy(q).project(C3); v2.copy(q2).project(C3); m.rotateZ(Math.atan2((v2.y - v1.y) * H, (v2.x - v1.x) * W)); });
    pintaKaraoke(T5, t, { op: cl((t - 11.2) * 4) * (1 - p(t, 12.6, .3)) }); T5.visible = t < 12.95;
    tMono.mesh.visible = t > 12.8; tMono.pinta(Math.floor(t * 30), g => { const s = 'AHORA ES TU', n = Math.floor(cl((t - 12.85) * 18, 0, s.length)); mono(g, s.slice(0, n) + (n < s.length || Math.floor(t * 3) % 2 ? '█' : ''), 10, 64, 'rgba(236,232,225,.92)', '500 58px M'); });
    CL.children.forEach((m, i) => { const w = m.userData.it, k = E.oC(p(t, w.t, .2)); m.material.opacity = k; m.material.color.set(0xF4F0E8); m.position.y = 0; });
    CLo.children.forEach(m => { m.material.opacity = .28 * cl((t - 13.1) * 4); m.material.color.set(0xd8d2c8); });
    tMono2.mesh.visible = t > 15.3; tMono2.pinta(Math.floor(t * 30), g => { const s = 'Y TÚ, SU', n = Math.floor(cl((t - 15.3) * 18, 0, s.length)); mono(g, s.slice(0, n) + (n < s.length || Math.floor(t * 3) % 2 ? '█' : ''), 10, 64, 'rgba(236,232,225,.92)', '500 58px M'); });
    CA.children.forEach(m => { const k = E.oC(p(t, m.userData.it.t, .2)); m.material.opacity = k; m.material.color.set(0xF4F0E8); });
    minimo.mesh.material.opacity = cl((t - 13.8) * 3) * .9; pt.mesh.material.opacity = cl((t - 13.0) * 3);
    return { escena: S3, cam: C3, post: { bloom: .7, radio: .45, umbral: .6, ca: .004, flash: t < 11.2 ? 1 - (t - 11.05) * 6.7 : 0, flashC: 0x000000 } };
  };

  return [{ t0: 0, t1: 9.5, frame: f1 }, { t0: 9.5, t1: 11.05, frame: f2 }, { t0: 11.05, t1: 16.5, frame: f3 }];
}
