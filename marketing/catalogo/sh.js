const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(let i=1;i<=5;i++){await p.goto('file://'+process.cwd()+'/cat.html');await p.evaluate(i=>{document.querySelectorAll('.p').forEach(e=>e.classList.remove('on'));document.getElementById('p'+i).classList.add('on')},i);await p.waitForTimeout(400);await p.screenshot({path:`cat-${i}.png`});}
await b.close();})();
