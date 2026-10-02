// Captura fotogramas sueltos para revisar:  node fotogramas.js escena.html salida.png 1.0 3.5 ...
const path = require('path');
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
(async () => {
  const [, , html, out, ...ts] = process.argv;
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  pg.on('pageerror', e => console.error('ERROR', e.message));
  await pg.goto('file://' + path.resolve(html)); await pg.waitForTimeout(500);
  for (const t of ts) { await pg.evaluate(t => render(t), +t);
    await pg.screenshot({ path: out.replace('.png', `-${t}.png`), type: 'png' }); }
  await b.close();
})();
