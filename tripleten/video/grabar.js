// Graba el vídeo de demo (vertical, 1080x1920, 30 fps) a partir de la página real.
//
//   REC_LANG=es node tripleten/video/grabar.js   -> demo.mp4
//   REC_LANG=en node tripleten/video/grabar.js   -> demo-en.mp4
//
// Después pone el sonido con sonido.py (Python 3 + numpy): efectos sincronizados
// con cada toque, mensaje y animación, y una base musical suave. Sin numpy, el
// vídeo sale sin sonido.
//
// Necesita Playwright con Chromium y un ffmpeg con libx264 (variable FFMPEG o
// el del PATH). El reloj de la página es virtual: cada fotograma avanza 1/30 s
// y todas las animaciones (CSS y JS) se sincronizan con él, así que el vídeo
// sale fluido aunque la captura sea lenta.
"use strict";

const fs = require("fs");
const path = require("path");
const http = require("http");
const os = require("os");
const crypto = require("crypto");
const { execFileSync } = require("child_process");

let playwright;
try { playwright = require("playwright"); } catch (e) { playwright = require("/opt/node22/lib/node_modules/playwright"); }

const ROOT = path.resolve(__dirname, "..");
const LANG = process.env.REC_LANG === "en" ? "en" : "es";
const SUFFIX = LANG === "en" ? "-en" : "";
const FRAMES = path.resolve(process.argv[2] || path.join(os.tmpdir(), "croi-frames-" + LANG));
const FFMPEG = process.env.FFMPEG || "ffmpeg";
const FPS = Number(process.env.FPS) || 30;
const VIEW = { width: 432, height: 768 }; // x2.5 = 1080x1920
const MAX_FRAMES = Number(process.env.MAX_FRAMES) || FPS * 150;
const START = new Date("2026-09-30T10:00:00");
// Las fuentes de Google se descargan una vez con curl y se sirven desde caché:
// así el vídeo siempre sale con la tipografía buena aunque la red falle.
const FONT_CACHE = path.join(os.tmpdir(), "croi-fonts");
const UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36";

const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".png": "image/png", ".jpg": "image/jpeg", ".mp4": "video/mp4" };
const server = http.createServer((req, res) => {
  let f = decodeURIComponent(req.url.split("?")[0]);
  if (f.endsWith("/")) f += "index.html";
  const p = path.join(ROOT, f);
  if (!p.startsWith(ROOT) || !fs.existsSync(p)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { "content-type": TYPES[path.extname(p)] || "application/octet-stream" });
  fs.createReadStream(p).pipe(res);
});

// Pausa todas las animaciones y las coloca en el tiempo virtual actual.
function syncAnimations() {
  const now = performance.now();
  for (const a of document.getAnimations()) {
    if (a.__vs === undefined) { a.__vs = now - (a.currentTime || 0); a.pause(); }
    try { a.currentTime = now - a.__vs; } catch (e) {}
  }
  return !!(window.__rec && window.__rec.done);
}

(async () => {
  await new Promise((r) => server.listen(0, r));
  const url = "http://localhost:" + server.address().port + "/?lang=" + LANG;
  fs.rmSync(FRAMES, { recursive: true, force: true });
  fs.mkdirSync(FRAMES, { recursive: true });

  const browser = await playwright.chromium.launch();
  const ctx = await browser.newContext({ viewport: VIEW, deviceScaleFactor: 2.5, isMobile: true, hasTouch: true, ignoreHTTPSErrors: true, acceptDownloads: true, locale: LANG === "en" ? "en-US" : "es-ES" });
  await ctx.addInitScript(() => { try { localStorage.setItem("croi_ab", '"A"'); } catch (e) {} });
  fs.mkdirSync(FONT_CACHE, { recursive: true });
  await ctx.route(/^https:\/\/fonts\.(googleapis|gstatic)\.com\//, async (route) => {
    const u = route.request().url();
    const f = path.join(FONT_CACHE, crypto.createHash("md5").update(u).digest("hex"));
    if (!fs.existsSync(f)) execFileSync("curl", ["-sSfL", "--retry", "3", "-A", UA, "-o", f, u]);
    await route.fulfill({ path: f, contentType: u.includes("googleapis") ? "text/css" : "font/woff2", headers: { "access-control-allow-origin": "*" } });
  });
  const page = await ctx.newPage();
  page.on("pageerror", (e) => console.error("pageerror:", e.message));
  await page.clock.install({ time: START });
  await page.clock.pauseAt(new Date(START.getTime() + 100));
  await page.goto(url);
  await page.evaluate(() => document.fonts.ready.then(() => true));
  await page.addScriptTag({ path: path.join(__dirname, "director.js") });
  await page.clock.runFor(1500);
  await page.evaluate(() => { window.__startDirector(); });

  const dt = 1000 / FPS;
  let i = 0, done = false, tail = 0;
  while (i < MAX_FRAMES) {
    await page.clock.runFor(dt);
    done = await page.evaluate(syncAnimations);
    await page.screenshot({ path: path.join(FRAMES, "f" + String(i).padStart(5, "0") + ".jpg"), type: "jpeg", quality: 92 });
    i++;
    if (i % 150 === 0) console.log("fotograma", i, "(" + (i / FPS).toFixed(1) + " s)");
    if (done && ++tail > 2) break;
  }
  const chapters = await page.evaluate(() => window.__rec.chapters);
  const sfx = await page.evaluate(() => window.__rec.sfx);
  await browser.close();
  server.close();
  console.log("fotogramas:", i, "duración:", (i / FPS).toFixed(1), "s");
  console.log("capítulos:", JSON.stringify(chapters));
  fs.writeFileSync(path.join(__dirname, "capitulos" + SUFFIX + ".json"), JSON.stringify(chapters, null, 2) + "\n");
  const sfxFile = path.join(__dirname, "efectos" + SUFFIX + ".json");
  fs.writeFileSync(sfxFile, JSON.stringify({ duration: i / FPS, offset: 1 / FPS, events: sfx }) + "\n");
  console.log("efectos de sonido:", sfx.length);

  if (process.env.SKIP_VIDEO) { console.log("sin vídeo (SKIP_VIDEO)"); return; }
  const out = path.join(ROOT, "demo" + SUFFIX + ".mp4");
  const wav = path.join(FRAMES, "sonido.wav");
  let audio = false;
  try {
    execFileSync(process.env.PYTHON || "python3", [path.join(__dirname, "sonido.py"), sfxFile, wav], { stdio: "inherit" });
    audio = fs.existsSync(wav);
  } catch (e) { console.error("sin sonido:", e.message); }
  execFileSync(FFMPEG, ["-y", "-v", "error", "-framerate", String(FPS), "-i", path.join(FRAMES, "f%05d.jpg")]
    .concat(audio ? ["-i", wav] : [])
    .concat(["-c:v", "libx264", "-preset", "slow", "-crf", "24", "-pix_fmt", "yuv420p"])
    .concat(audio ? ["-c:a", "aac", "-b:a", "160k", "-shortest"] : [])
    .concat(["-movflags", "+faststart", out]), { stdio: "inherit" });
  const poster = chapters.find((c) => c.name === "numeros");
  const posterFrame = Math.round(((poster ? poster.t : 20) + 7.1) * FPS);
  execFileSync(FFMPEG, ["-y", "-v", "error", "-i", path.join(FRAMES, "f" + String(posterFrame).padStart(5, "0") + ".jpg"),
    "-vf", "scale=720:-2", "-q:v", "4", path.join(ROOT, "demo-poster" + SUFFIX + ".jpg")], { stdio: "inherit" });
  console.log("listo:", out, audio ? "(con sonido)" : "(sin sonido)");
})().catch((e) => { console.error(e); server.close(); process.exit(1); });
