const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(async () => await chromium.launch());
  const pg = await b.newPage({ viewport: { width: 432, height: 768 }, deviceScaleFactor: 2.5 });
  await pg.goto('http://localhost:8765/index.html', { waitUntil: 'networkidle' });
  await pg.evaluate(() => { document.querySelectorAll('[class*=galleta],[id*=galleta],[class*=cookie],[id*=cookie]').forEach(e => e.remove()); document.querySelectorAll('*').forEach(e=>{ if(getComputedStyle(e).position==='fixed') e.style.display='none'; }); });
  for (let y = 0; y < 30000; y += 500) { await pg.evaluate(y => scrollTo(0, y), y); await pg.waitForTimeout(60); }
  await pg.evaluate(() => scrollTo(0, 0)); await pg.waitForTimeout(800);
  const H = await pg.evaluate(() => document.documentElement.scrollHeight);
  const secs = await pg.evaluate(() => [...document.querySelectorAll('section,footer,header,[id]')].filter(e=>e.id).map(e => [e.id, e.getBoundingClientRect().top + scrollY]).slice(0,60));
  console.log(H, JSON.stringify(secs));
  await pg.screenshot({ path: '/tmp/claude-0/placas20/web/pagina.png', fullPage: true });
  await b.close();
})();
