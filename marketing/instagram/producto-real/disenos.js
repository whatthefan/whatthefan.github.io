// Saca los diseños planos (los de verdad, del generador de la web) que se pegan
// en las fotos: la placa de mesa y el expositor de pie de Bar La Plaza (INVENTADO).
// Desde la raiz del repo:  node marketing/instagram/producto-real/disenos.js
const path = require('path'), fs = require('fs');
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
const C = 'marketing/instagram/carrusel-placa/', D = 'marketing/instagram/producto-real/';
(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  pg.on('pageerror', e => console.error('ERROR', e.message));
  await pg.goto('file://' + path.resolve(C + 'generador-por-capas.html'));
  await pg.waitForTimeout(1500);
  const pon = async (sel, v) => { await pg.fill(sel, v); await pg.dispatchEvent(sel, 'input'); };
  const color = (sel, v) => pg.evaluate(([s, v]) => { const e = document.querySelector(s); e.value = v;
    e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); }, [sel, v]);
  for (const formato of ['placa', 'stand']) {
    await pg.click(`#fFormato button[data-v="${formato}"]`);
    await pg.setInputFiles('#fLogo', C + 'logo-ejemplo.png');
    await pg.waitForTimeout(800);
    await pon('#fNegocio', 'Bar La Plaza'); await pon('#fLema', 'Tapas · Cañas · Terraza');
    await pon('#fCorta', 'bar-la-plaza'); await pon('#fGoogle', 'ChIJ-ejemplo');
    await color('#fBanda', '#1F4D3A'); await color('#fFondo', '#F4EDE0');
    await pg.click('#fQueSeVe button[data-v="ambos"]');
    await pon('#fNegocio', 'Bar La Plaza');
    await pg.waitForTimeout(1200);
    const src = await pg.evaluate(() => new Promise(ok => {
      const im = new Image();
      im.onload = () => { const k = 1600 / Math.max(im.width, im.height), c = document.createElement('canvas');
        c.width = Math.round(im.width * k); c.height = Math.round(im.height * k);
        c.getContext('2d').drawImage(im, 0, 0, c.width, c.height); ok(c.toDataURL('image/png')); };
      im.src = document.querySelector('#salida').src;
    }));
    fs.mkdirSync(D + 'disenos', { recursive: true });
    fs.writeFileSync(D + 'disenos/' + formato + '.png', Buffer.from(src.split(',')[1], 'base64'));
    console.log(formato);
  }
  await b.close();
})();
