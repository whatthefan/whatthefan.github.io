// genera.mjs — personajes (Open Peeps, licencia MIT/CC0) con la paleta de PLEA5E, en SVG.
//   node genera.cjs reparto.json carpeta/
// reparto.json: [{ "id":"cliente", "tipo":"busto"|"pie"|"sentado", "cuerpo":"Paper", "pelo":"MediumBangs",
//                  "caras":["Calm","Smile"], "acento":"top"|"paper"|"cup"|null, "gafas":null }]
import { Effigy, R, renderToStaticMarkup, React, createHair, createFace, createAccessory } from './peeps.mjs';
import fs from 'fs';
const e = React.createElement;
// paleta: línea negra, piel y ropa en grises cálidos, un acento oro
const P = { outlineColor: '#141414', skinColor: '#F4F1EA', topColor: '#DAD6CD', pantsColor: '#2B2B2B', shoesColor: '#FFFFFF',
  jacketColor: '#3A3A3A', paperColor: '#1E1F24', cupColor: '#FFFFFF', teeColor: '#DAD6CD', shirtColor: '#DAD6CD' };
const ORO = '#E9BC46';
const [,, entrada, salida] = process.argv;
fs.mkdirSync(salida, { recursive: true });
const cuello = { busto: [615, 639], pie: [745, 0], sentado: [640, 0] };
for (const c of JSON.parse(fs.readFileSync(entrada, 'utf8'))) {
  const opts = { ...P };
  if (c.acento === 'top') opts.topColor = ORO;
  if (c.acento === 'paper') opts.paperColor = ORO;
  if (c.acento === 'cup') opts.cupColor = ORO;
  if (c.acento === 'jacket') opts.jacketColor = ORO;
  for (const cara of c.caras) {
    let svg;
    const head = { type: c.pelo, options: opts }, face = { type: cara, options: opts };
    const acc = c.gafas ? { type: c.gafas, options: opts } : undefined;
    if (c.tipo === 'busto') {
      svg = renderToStaticMarkup(e(Effigy, { body: { type: c.cuerpo, options: opts }, head, face, accessory: acc }));
    } else {
      const C = R[c.tipo === 'pie' ? 'standing' : 'sitting'][c.cuerpo];
      const [nx, ny] = cuello[c.tipo], dx = nx - cuello.busto[0], dy = ny - cuello.busto[1];
      const cab = e('g', { transform: `translate(${dx} ${dy})` },
        e('g', { transform: 'translate(342, 190)' }, createHair(head)),
        e('g', { transform: 'translate(531, 366)' }, createFace(face)),
        acc ? e('g', { transform: 'translate(419, 421)' }, createAccessory(acc)) : null);
      svg = renderToStaticMarkup(e('svg', { xmlns: 'http://www.w3.org/2000/svg', viewBox: '0 -700 1645 3261', width: 1645, height: 3261 }, e(C, opts), cab));
    }
    fs.writeFileSync(`${salida}/${c.id}-${cara}.svg`, svg);
  }
}
console.log('listo');
