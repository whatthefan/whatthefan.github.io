// Graba el video: cada fotograma se pinta con render(t) y se manda a ffmpeg.
// Desde la raiz del repo, despues de montar.py y musica.py:
//   FFMPEG=/ruta/a/ffmpeg node marketing/instagram/carrusel-placa/video/grabar.js
const path = require('path');
const { spawn, execSync } = require('child_process');
const { chromium } = require(execSync('npm root -g').toString().trim() + '/playwright');
const D = 'marketing/instagram/carrusel-placa/video/';
// VEL: el video va 1,5 veces mas rapido que la animacion (lo mismo en musica.py)
const FPS = 30, VEL = 1, DUR = 13 * 5 / 3;  // 13 compases a 144 BPM
(async () => {
  const ff = spawn(process.env.FFMPEG || 'ffmpeg', ['-loglevel', 'error', '-y',
    '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-i', D + 'audio.wav',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', D + 'PLEA5E-placa-destripada.mp4'],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  pg.on('pageerror', e => { console.error('ERROR', e.message); process.exit(1); });
  await pg.goto('file://' + path.resolve(D + 'escena-montada.html'));
  await pg.waitForTimeout(500);
  const n = Math.round(FPS * DUR);
  for (let f = 0; f < n; f++) {
    await pg.evaluate(t => render(t), f / FPS * VEL);
    const img = await pg.screenshot({ type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(img)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 150 === 0) console.log(`${f}/${n}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await b.close();
})();
