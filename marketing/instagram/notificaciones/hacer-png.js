// Foto de la publicacion "notificaciones" (1080x1350, exportada al doble: 2160x2700).
// Desde la raiz del repo:  node marketing/instagram/notificaciones/hacer-png.js
const path = require('path');
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
const N = 'marketing/instagram/notificaciones/';
(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });   // sale a 2160x2700, mas nitida
  await pg.goto('file://' + path.resolve(N + 'notificaciones.html')); await pg.waitForTimeout(600);
  await pg.screenshot({ path: N + 'PLEA5E-notificaciones.png' });
  await b.close();
})();
