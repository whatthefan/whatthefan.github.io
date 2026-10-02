// exporta.js — saca una textura de texturas.html a PNG (x2 de resolución).
//   node disenos/exporta.js placa placa.png                     (azul, "Bar Nombre")
//   node disenos/exporta.js "placa&color=verde&bar=Bar Manolo" placa-verde.png
//   node disenos/exporta.js "pantalla" pantalla.png 2.6          (tercer argumento: t de la animación)
const path = require('path'), { execSync } = require('child_process');
const { chromium } = require(execSync('npm root -g').toString().trim() + '/playwright');
const [hash, salida, t = '0'] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1800, height: 2600 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'texturas.html') + '#' + encodeURI(hash));
  await p.waitForFunction(() => window.render && document.fonts.ready);
  await p.evaluate(t => render(+t), t);
  await p.waitForTimeout(200);
  const tipo = hash.split('&')[0];
  await (await p.$('#' + tipo)).screenshot({ path: salida, omitBackground: true });
  await b.close();
})();
