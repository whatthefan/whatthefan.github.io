// PDF A4 de la guia y una foto de cada pagina para revisar.
// Desde la raiz del repo:  node marketing/guia-resenas/hacer-pdf.js
const path = require('path'), fs = require('fs');
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
const G = 'marketing/guia-resenas/';
(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1.5 });
  await pg.goto('file://' + path.resolve(G + 'guia.html'));
  await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(500);
  await pg.pdf({ path: G + 'PLEA5E-guia-resenas-google.pdf', format: 'A4', printBackground: true, preferCSSPageSize: true });
  fs.mkdirSync(G + 'paginas', { recursive: true });
  const n = await pg.$$eval('.pag', p => p.length);
  for (let i = 0; i < n; i++) await (await pg.$$(".pag"))[i].screenshot({ path: `${G}paginas/${String(i + 1).padStart(2, '0')}.png` });
  await pg.waitForTimeout(3000);
  await b.close();
})();
