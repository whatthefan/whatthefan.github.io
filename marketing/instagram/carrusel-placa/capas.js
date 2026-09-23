// Saca la placa de ejemplo por capas con generador-por-capas.html (la copia
// del generador de la web con interruptores: window.OC.<capa> = true la
// esconde). Salen los pasos del carrusel (acumulados) y las piezas sueltas,
// con fondo transparente, para el video.
// Desde la raiz del repo:  node marketing/instagram/carrusel-placa/capas.js
const path = require('path'), fs = require('fs');
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
const C = 'marketing/instagram/carrusel-placa/';
const TODAS = ['fondo', 'banda', 'adornos', 'titulo', 'g', 'nfc', 'qr', 'marco', 'instr', 'cliente', 'lema', 'pie', 'tel'];
const solo = (...v) => Object.fromEntries(TODAS.filter(k => !v.includes(k)).map(k => [k, true]));
const CREMA = '#F4EDE0', BLANCO = '#FFFFFF';
const PASOS = {
  // el carrusel: cada paso anade lo suyo a lo de antes. Primero lo que mas
  // cambia la placa (los colores) y despues el detalle, para que cada foto
  // se note distinta de la anterior
  'paso1-colores': { oc: solo('fondo', 'banda', 'adornos', 'pie'), fondo: CREMA, ve: 'ambos' },
  'paso2-mensaje': { oc: solo('fondo', 'banda', 'adornos', 'pie', 'titulo', 'g'), fondo: CREMA, ve: 'ambos' },
  'paso3-cliente': { oc: solo('fondo', 'banda', 'adornos', 'pie', 'titulo', 'g', 'cliente', 'lema'), fondo: CREMA, ve: 'ambos' },
  'paso4-qr':      { oc: solo('fondo', 'banda', 'adornos', 'pie', 'titulo', 'g', 'cliente', 'lema', 'qr', 'instr'), fondo: CREMA, ve: 'ambos' },
  'paso5-nfc':     { oc: {}, fondo: CREMA, ve: 'ambos' },
  // las piezas sueltas del video
  'pieza-fondo':   { oc: solo('fondo'), fondo: CREMA, ve: 'ambos' },
  'pieza-banda':   { oc: solo('banda', 'adornos', 'pie'), fondo: CREMA, ve: 'ambos' },
  'pieza-titulo':  { oc: solo('titulo', 'g'), fondo: CREMA, ve: 'ambos' },
  'pieza-qr':      { oc: solo('qr', 'marco'), fondo: CREMA, ve: 'ambos' },
  'pieza-nfc':     { oc: solo('nfc'), fondo: CREMA, ve: 'ambos' },
  'pieza-instr':   { oc: solo('instr'), fondo: CREMA, ve: 'ambos' },
  'pieza-cliente': { oc: solo('cliente', 'lema'), fondo: CREMA, ve: 'ambos' },
  'pieza-tel':     { oc: solo('tel'), fondo: CREMA, ve: 'ambos' },
};
(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  pg.on('pageerror', e => console.error('ERROR', e.message));
  await pg.goto('file://' + path.resolve(C + 'generador-por-capas.html'));
  await pg.waitForTimeout(1500);
  await pg.click('#fFormato button[data-v="placa"]');
  await pg.setInputFiles('#fLogo', C + 'logo-ejemplo.png');
  await pg.waitForTimeout(800);
  const pon = async (sel, v) => { await pg.fill(sel, v); await pg.dispatchEvent(sel, 'input'); };
  await pon('#fNegocio', 'Bar La Plaza'); await pon('#fLema', 'Tapas · Cañas · Terraza');
  await pon('#fCorta', 'bar-la-plaza'); await pon('#fGoogle', 'ChIJ-ejemplo');
  const color = (sel, v) => pg.evaluate(([s, v]) => { const e = document.querySelector(s); e.value = v;
    e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); }, [sel, v]);
  await color('#fBanda', '#1F4D3A');
  for (const [nombre, p] of Object.entries(PASOS)) {
    await pg.evaluate(oc => { window.OC = oc; }, p.oc);
    await color('#fFondo', p.fondo);
    await pg.click(`#fQueSeVe button[data-v="${p.ve}"]`);
    await pon('#fNegocio', 'Bar La Plaza');
    await pg.waitForTimeout(900);
    // el generador la saca a 3600 px, que es para imprenta; para redes, 1400 sobra
    const src = await pg.evaluate(() => new Promise(ok => {
      const im = new Image();
      im.onload = () => { const c = document.createElement('canvas'); c.width = c.height = 1400;
        c.getContext('2d').drawImage(im, 0, 0, 1400, 1400); ok(c.toDataURL('image/png')); };
      im.src = document.querySelector('#salida').src;
    }));
    fs.writeFileSync(C + 'capas/' + nombre + '.png', Buffer.from(src.split(',')[1], 'base64'));
    console.log(nombre);
  }
  await b.close();
})();
