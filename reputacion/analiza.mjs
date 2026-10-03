/* Para probar el motor desde la terminal con reseñas de verdad.

     npm run reputacion                 pasa todas las de ejemplos.json
     npm run reputacion -- fisico       solo la que tenga ese id
     npm run reputacion -- "texto..."   una reseña suelta, con el negocio
                                        de ejemplos.json

   Necesita ANTHROPIC_API_KEY en el entorno, y cada reseña es una
   llamada que se paga (unos céntimos). Al final dice cuántas han
   acertado el veredicto que se esperaba: es la forma de saber si un
   cambio en politicas.mjs mejora o empeora el criterio. */

import fs from 'node:fs';
import { analiza } from './motor.mjs';

const datos = JSON.parse(fs.readFileSync(new URL('./ejemplos.json', import.meta.url), 'utf8'));
const arg = process.argv.slice(2).join(' ').trim();

let lista = datos.resenas;
if (arg) {
  const porId = lista.filter((r) => r.id === arg);
  lista = porId.length ? porId : [{ id: 'suelta', texto: arg }];
}

let aciertos = 0, conEspera = 0;
for (const r of lista) {
  const resena = { ...r, negocio: datos.negocio };
  console.log('\n══ ' + r.id + ' ' + '═'.repeat(Math.max(0, 60 - r.id.length)));
  console.log(r.texto);
  try {
    const v = await analiza(resena);
    console.log('\n→ ' + v.veredicto.toUpperCase() + (v.fuerza ? ' (fuerza ' + v.fuerza + ')' : ''));
    console.log('  ' + v.resumen);
    for (const i of v.infracciones) {
      console.log('  · ' + i.norma + ': «' + i.cita + '» (' + i.fuerza + ')');
    }
    for (const d of v.descartadas) {
      console.log('  ✗ descartada, ' + d.motivo + ': «' + d.cita + '»');
    }
    if (v.apelacion) console.log('\n[Apelación]\n' + v.apelacion);
    console.log('\n[Respuesta]\n' + v.respuesta);
    if (r.espera) {
      conEspera++;
      if (v.veredicto === r.espera) aciertos++;
      else console.log('\n!! se esperaba ' + r.espera);
    }
  } catch (err) {
    console.log('\n!! ' + (err && err.message));
  }
}
if (conEspera) console.log('\nAciertos: ' + aciertos + ' de ' + conEspera);
