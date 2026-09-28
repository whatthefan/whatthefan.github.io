// fx-de-pagina.js pagina.html → imprime en JSON la lista FX tal como queda al cargar la página
// (la plantilla la rellena con fx(...) en tiempo de ejecución, así que no está escrita en el archivo)
const path = require('path'), fs = require('fs'), http = require('http'), { execSync } = require('child_process');
const { chromium } = require(execSync('npm root -g').toString().trim() + '/playwright');
const pag = path.resolve(process.argv[2]);
const srv = http.createServer((q, r) => fs.readFile(path.join(path.dirname(pag), decodeURIComponent(q.url.split('?')[0])), (e, d) => { if (e) { r.writeHead(404); r.end(); } else r.end(d); }));
srv.listen(0, '127.0.0.1', async () => {
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto(`http://127.0.0.1:${srv.address().port}/${path.basename(pag)}`); await p.waitForFunction(() => window.render);
  console.log(JSON.stringify(await p.evaluate(() => window.FX_MEZCLA || FX))); await b.close(); srv.close();
});
