// node grabar.js prueba t1 t2 ...   -> prueba-<t>.png (capa sola)
// node grabar.js todo               -> capa.mov (png con alfa, 30 fps)
const path=require('path'),{spawn}=require('child_process');
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
const FF='/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+path.resolve('capa.html'));await p.waitForFunction(()=>window.LISTO&&document.fonts.ready);await p.waitForTimeout(500);
const modo=process.argv[2];
if(modo==='prueba'){for(const t of process.argv.slice(3)){await p.evaluate(t=>render(+t),t);await p.screenshot({path:`prueba-${t}.png`,omitBackground:true});}}
else{const total=await p.evaluate(()=>P.total);const n=Math.round(total*30);
 const ff=spawn(FF,['-loglevel','error','-y','-f','image2pipe','-framerate','30','-c:v','png','-i','-','-c:v','png','-pix_fmt','rgba','capa.mov'],{stdio:['pipe','inherit','inherit']});
 for(let i=0;i<n;i++){await p.evaluate(t=>render(t),i/30);const buf=await p.screenshot({omitBackground:true,type:'png'});
  if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r)); if(i%150==0)console.log('frame',i,'/',n);}
 ff.stdin.end();await new Promise(r=>ff.on('close',r));}
await b.close();})();
