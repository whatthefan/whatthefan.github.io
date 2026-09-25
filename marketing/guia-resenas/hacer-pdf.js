// PDF A4 y una foto de cada pagina para revisar.
// Desde la raiz del repo:  node marketing/guia-resenas/hacer-pdf.js [guia|kit]
const path = require('path'), fs = require('fs');
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
const G = 'marketing/guia-resenas/';
const CUAL = { guia: ['guia.html', 'PLEA5E-guia-resenas-google.pdf', 'paginas'], kit: ['kit-venta.html', 'PLEA5E-kit-de-venta.pdf', 'paginas-kit'] };
(async () => {
  const b = await chromium.launch();
  for (const k of (process.argv[2] ? [process.argv[2]] : Object.keys(CUAL))) {
    const [src, pdf, dir] = CUAL[k];
    const pg = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1.5 });
    await pg.goto('file://' + path.resolve(G + src));
    await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(500);
    await pg.pdf({ path: G + pdf, format: 'A4', printBackground: true, preferCSSPageSize: true });
    fs.rmSync(G + dir, { recursive: true, force: true }); fs.mkdirSync(G + dir, { recursive: true });
    const hojas = await pg.$$('.pag');
    for (let i = 0; i < hojas.length; i++) await hojas[i].screenshot({ path: `${G}${dir}/${String(i + 1).padStart(2, '0')}.png` });
    console.log(pdf, hojas.length, 'paginas');
    await pg.close();
  }
  await b.close();
})();
