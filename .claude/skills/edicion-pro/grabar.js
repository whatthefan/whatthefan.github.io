// grabar.js — graba una página HTML con render(t) fotograma a fotograma, con fondo transparente.
//   node grabar.js capa.html prueba 0.5 1.2 3        -> prueba-<capa>-<t>.png (para revisar)
//   node grabar.js capa.html detras  salida.mov       -> vídeo PNG con alfa a 30 fps
// La página lee la capa de location.hash (#detras / #delante) y define window.TOTAL y render(t).
// Usa el ffmpeg de imageio-ffmpeg si no hay otro (variable FFMPEG).
const path = require('path'), { spawn, execSync } = require('child_process');
const { chromium } = require(execSync('npm root -g').toString().trim() + '/playwright');
const FF = process.env.FFMPEG || '/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2';
const [pagina, capa, ...resto] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.log('ERR', e.message));
  const modo = capa === 'prueba' ? (resto.shift(), 'prueba') : 'video';
  const nombreCapa = modo === 'prueba' ? process.argv[4] : capa;
  await p.goto('file://' + path.resolve(pagina) + '#' + nombreCapa);
  await p.waitForFunction(() => window.render && document.fonts.ready);
  await p.waitForTimeout(400);
  if (modo === 'prueba') {
    for (const t of resto) {
      await p.evaluate(t => render(+t), t);
      await p.screenshot({ path: `prueba-${nombreCapa}-${t}.png`, omitBackground: true });
    }
  } else {
    const n = Math.round((await p.evaluate(() => window.TOTAL)) * 30);
    const ff = spawn(FF, ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'png', '-i', '-',
      '-c:v', 'png', '-pix_fmt', 'rgba', resto[0]], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = 0; i < n; i++) {
      await p.evaluate(t => render(t), i / 30);
      const buf = await p.screenshot({ omitBackground: true, type: 'png' });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 150 === 0) console.log(capa, i, '/', n);
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
  }
  await b.close();
})();
