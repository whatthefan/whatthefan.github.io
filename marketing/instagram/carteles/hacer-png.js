// Foto de cada cartel (a su tamano) y de cada escena.
// Desde la raiz del repo:  node marketing/instagram/carteles/hacer-png.js [nombre ...]
const path = require('path'), fs = require('fs');
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
const C = 'marketing/instagram/carteles/';
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--allow-file-access-from-files'] });
  const quien = process.argv.slice(2);
  for (const f of fs.readdirSync(C).filter(f => f.endsWith('.html') && (!quien.length || quien.includes(f.replace('.html', ''))))) {
    const html = fs.readFileSync(C + f, 'utf8');
    const w = +(/width:(\d+)px;height:(\d+)px/.exec(html) || [0, 1080])[1], h = +(/width:(\d+)px;height:(\d+)px/.exec(html) || [0, 0, 1350])[2];
    const pg = await b.newPage({ viewport: { width: w, height: h } });
    pg.on('pageerror', e => console.error(f, 'ERROR', e.message));
    pg.on('console', m => console.log(f, m.text()));
    await pg.goto('file://' + path.resolve(C + f), { timeout: 600000 });
    await pg.waitForFunction(() => document.fonts.ready.then(() => !window.PINTANDO), null, { timeout: 600000 });
    await pg.waitForTimeout(300);
    await pg.screenshot({ path: C + (f.startsWith('escena') ? 'fotos/' : 'png/') + f.replace('.html', '.png') });
    console.log(f, w, 'x', h);
    await pg.close();
  }
  await b.close();
})();
