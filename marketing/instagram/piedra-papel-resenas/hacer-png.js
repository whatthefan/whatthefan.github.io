// Foto de cada diapositiva del carrusel (1080x1350).
// Desde la raiz del repo:  node marketing/instagram/piedra-papel-resenas/hacer-png.js
const path = require('path'), fs = require('fs');
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
const D = 'marketing/instagram/piedra-papel-resenas/diapositivas/';
(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const f of fs.readdirSync(D).filter(f => f.endsWith('.html')).sort()) {
    await pg.goto('file://' + path.resolve(D + f)); await pg.waitForTimeout(400);
    await pg.screenshot({ path: D + 'PLEA5E-piedra-papel-resenas-' + f.replace('.html', '.png') });
  }
  await b.close();
})();
