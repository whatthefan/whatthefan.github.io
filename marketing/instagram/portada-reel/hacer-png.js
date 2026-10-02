// Foto de la portada del reel (1080x1920).
// Desde la raiz del repo:  node marketing/instagram/portada-reel/hacer-png.js
const path = require('path');
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
const D = 'marketing/instagram/portada-reel/';
(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await pg.goto('file://' + path.resolve(D + 'portada.html'));
  await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(500);
  await pg.screenshot({ path: D + 'PLEA5E-portada-reel.png' });
  await b.close();
})();
