const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
const http=require('http'),fs=require('fs'),path=require('path');const T={'.html':'text/html','.js':'text/javascript','.png':'image/png','.jpg':'image/jpeg'};
const [pag, out, n, fps='30', img='w-placa.png'] = process.argv.slice(2); fs.mkdirSync(out,{recursive:true});
const R='/tmp/claude-0/v3/capa';
const srv=http.createServer((q,r)=>{const f=path.join(R,decodeURIComponent(q.url.split('?')[0]));fs.readFile(f,(e,d)=>{if(e){r.writeHead(404);r.end();return}r.writeHead(200,{'Content-Type':T[path.extname(f)]||'application/octet-stream'});r.end(d)})}).listen(0,async()=>{
 const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
 const p=await b.newPage({viewport:{width:900,height:1100}}); p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto(`http://127.0.0.1:${srv.address().port}/${pag}?img=${img}`); await p.waitForFunction(()=>window.LISTO,null,{timeout:60000});
 for(let i=0;i<+n;i++){ await p.evaluate(t=>render(t),i/(+fps)); await p.screenshot({path:`${out}/${String(i+1).padStart(4,'0')}.png`,omitBackground:true}); }
 await b.close(); srv.close(); });
