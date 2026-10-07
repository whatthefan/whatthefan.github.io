/* Topes de uso para lo que es público y cuesta dinero (la búsqueda de
   Google Maps y las respuestas con IA del analizador gratis).

   Dos topes a la vez: por persona y día (por la huella de su IP, nunca
   la IP misma) y para toda la web y día. El de la web es el que de
   verdad protege la factura: aunque alguien cambie de IP mil veces, el
   día no pasa de ahí.

   Se cuentan en el almacén con claves  lim-...  que caducan solas a los
   dos días. El almacén de Cloudflare tarda unos segundos en ponerse de
   acuerdo entre servidores, así que el tope puede pasarse por poco en
   una ráfaga. Para lo que se protege aquí, sobra. */

import { huella } from './cripto.mjs';

const hoy = () => new Date().toISOString().slice(0, 10);

async function suma(kv, k) {
  const n = Number(await kv.get(k)) || 0;
  await kv.put(k, String(n + 1), { expirationTtl: 172800 });
  return n + 1;
}

/* true si se puede; false si ya se ha llegado a algún tope. Sin almacén
   no se deja pasar: mejor un "vuelve mañana" que una factura. */
export async function permite(env, request, que, porPersona, porDia) {
  if (!env.ENCARGOS) return false;
  const ip = request.headers.get('cf-connecting-ip') || request.headers.get('x-forwarded-for') || 'sin-ip';
  const quien = await huella(ip + '|' + que);
  const kPersona = 'lim-' + que + '-' + hoy() + '-' + quien;
  const kDia = 'lim-' + que + '-' + hoy();
  const [p, d] = await Promise.all([env.ENCARGOS.get(kPersona), env.ENCARGOS.get(kDia)]);
  if ((Number(p) || 0) >= porPersona || (Number(d) || 0) >= porDia) return false;
  await Promise.all([suma(env.ENCARGOS, kPersona), suma(env.ENCARGOS, kDia)]);
  return true;
}
