// Saca los tres modelos del generador de placas (public/taller/generador.html)
// como PNG sin fondo, para enseñarlos limpios en el reel.
// Desde la raiz del repo:  node marketing/instagram/video-como-topstar/modelos.js
const path = require('path'), fs = require('fs');
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
const D = 'marketing/instagram/video-como-topstar/modelos/';
// Negocios de ejemplo (inventados), con colores de marca distintos para que se vea
// que cada placa va con la marca de su local.
const MODELOS = [
  { formato: 'placa',   negocio: 'Bar La Plaza',     lema: 'Tapas · Cañas · Terraza', corta: 'bar-la-plaza',  banda: '#0F1522', fondo: '#FFFFFF' },
  { formato: 'stand',   negocio: 'Barbería Norte',   lema: 'Corte · Barba · Afeitado', corta: 'barberia-norte', banda: '#1F2A24', fondo: '#ECE2D3' },
  { formato: 'tarjeta', negocio: 'Taller Hermanos Ruiz', lema: 'Mecánica · Neumáticos', corta: 'taller-ruiz',  banda: '#7A1F1F', fondo: '#FFFFFF' },
];
(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  pg.on('pageerror', e => console.error('ERROR', e.message));
  await pg.goto('file://' + path.resolve('public/taller/generador.html'));
  await pg.waitForTimeout(1500);
  for (const m of MODELOS) {
    await pg.click(`#fFormato button[data-v="${m.formato}"]`);
    const pon = async (sel, v) => { await pg.fill(sel, v); await pg.dispatchEvent(sel, 'input'); };
    await pon('#fNegocio', m.negocio); await pon('#fLema', m.lema); await pon('#fCorta', m.corta);
    await pon('#fGoogle', 'ChIJ-ejemplo');
    for (const [sel, v] of [['#fBanda', m.banda], ['#fFondo', m.fondo]])
      await pg.evaluate(([s, v]) => { const e = document.querySelector(s); e.value = v;
        e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); }, [sel, v]);
    await pg.waitForTimeout(1200);
    const src = await pg.getAttribute('#salida', 'src');
    fs.writeFileSync(D + m.formato + '.png', Buffer.from(src.split(',')[1], 'base64'));
    console.log(m.formato, src.slice(0, 30));
  }
  await b.close();
})();
