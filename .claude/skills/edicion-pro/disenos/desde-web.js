// desde-web.js — saca los diseños ORIGINALES de PLEA5E usando el generador de la web (public/taller/generador.html).
// Usar SIEMPRE esto para enseñar placas en los vídeos (no recreaciones).
//   node desde-web.js salida/ '[{"f":"placa","negocio":"Bar Manolo","lema":"Bar · Tapas","banda":"#192E26","n":"placa-verde"}]'
// f: placa | stand | tarjeta · banda/fondo/acento: colores (opcionales) · n: nombre del PNG
const path = require('path'), fs = require('fs'), { execSync } = require('child_process');
const { chromium } = require(execSync('npm root -g').toString().trim() + '/playwright');
const REPO = process.env.REPO || path.resolve(__dirname, '../../../..');
const GEN = path.join(REPO, 'public/taller/generador.html');
const [salida, lista] = process.argv.slice(2);
(async () => {
  fs.mkdirSync(salida, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  p.on('pageerror', e => console.log('ERR', e.message));
  for (const d of JSON.parse(lista)) {
    await p.goto('file://' + GEN);
    await p.waitForTimeout(600);
    await p.click(`button[data-v="${d.f || 'placa'}"]`);
    const pon = async (sel, v) => { if (v === undefined) return; await p.$eval(sel, (el, v) => { el.value = v; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); }, v); };
    await pon('#fNegocio', d.negocio); await pon('#fLema', d.lema);
    await pon('#fBanda', d.banda); await pon('#fFondo', d.fondo); await pon('#fAcento', d.acento);
    await p.waitForTimeout(1200);
    const src = await p.$eval('#salida', el => el.src);
    fs.writeFileSync(path.join(salida, (d.n || d.f) + '.png'), Buffer.from(src.split(',')[1], 'base64'));
    console.log('ok', d.n || d.f);
  }
  await b.close();
})();
