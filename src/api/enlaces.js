/* EL PANEL DE LAS DIRECCIONES CORTAS.  Lo usa /taller/enlaces.html .

   Aquí es donde cambias a dónde va una placa que ya está pegada en la
   mesa de un bar. Pide la misma contraseña que el panel de pedidos.

   La sirve el Worker de src/index.js en  /api/enlaces .

   Necesita:
     PANEL_CLAVE   la contraseña del panel
     ENCARGOS      el almacén (KV), el mismo de los pedidos            */

import { enlaceResena } from '../lib/encargo.mjs';
import { NOMBRE_VALIDO, CLAVE_ENLACE, CLAVE_TOTAL, CLAVE_CUENTA, hoyEnMadrid }
  from './enlace.js';

const JSON_CAB = { 'Content-Type': 'application/json; charset=utf-8' };

/* Comparación en tiempo constante, igual que en el panel de pedidos: con
   un === normal se puede ir adivinando la contraseña midiendo lo que
   tarda en contestar. */
function igual(a, b) {
  const x = String(a || ''), y = String(b || '');
  if (x.length !== y.length) return false;
  let d = 0;
  for (let i = 0; i < x.length; i++) d |= x.charCodeAt(i) ^ y.charCodeAt(i);
  return d === 0;
}

function responde(obj, estado) {
  return new Response(JSON.stringify(obj), { status: estado || 200, headers: JSON_CAB });
}

const numero = (v) => parseInt(v || '0', 10) || 0;

/* De lo que escriba él a una dirección de verdad. Vale el código del
   sitio a secas, el enlace de "pedir reseñas" o cualquier dirección
   pegada del navegador: lo mismo que acepta el generador. */
function destinoBueno(v) {
  const s = enlaceResena(String(v || '').trim());
  if (!s) return '';
  let u;
  try { u = new URL(s); } catch (e) { return ''; }
  /* Solo http y https. Cualquier otra cosa pegada ahí (javascript:, data:)
     no tiene ningún motivo legítimo para estar en el destino de una placa. */
  if (u.protocol !== 'http:' && u.protocol !== 'https:') return '';
  return u.toString();
}

export async function onRequest(context) {
  const { request, env } = context;

  const esperada = String(env.PANEL_CLAVE || '').trim();
  if (!esperada) return responde({ error: 'falta PANEL_CLAVE en la configuracion' }, 500);

  const url = new URL(request.url);
  const dada = String(request.headers.get('x-panel-clave') ||
                      url.searchParams.get('clave') || '').trim();
  if (!igual(dada, esperada)) return responde({ error: 'contrasena' }, 401);

  if (!env.ENCARGOS) {
    return responde({
      error: 'El almacén no está conectado. En Cloudflare: el Worker → ' +
             'Settings → Bindings → añadir un KV namespace con el nombre ' +
             'de variable ENCARGOS.'
    }, 500);
  }

  /* ---- crear, cambiar o borrar ---- */
  if (request.method === 'POST') {
    let d;
    try { d = await request.json(); } catch (e) { d = {}; }

    const nombre = String((d && d.nombre) || '').trim().toLowerCase();
    if (!NOMBRE_VALIDO.test(nombre)) {
      return responde({ error: 'El nombre corto solo puede llevar minúsculas, ' +
                               'números y guiones, y entre 2 y 40 letras.' }, 400);
    }

    if (d.accion === 'borrar') {
      /* El destino se va, los contadores se quedan: si alguien borra sin
         querer, al volver a crearlo con el mismo nombre recupera su
         cuenta. Y de todas formas caducan solos. */
      await env.ENCARGOS.delete(CLAVE_ENLACE(nombre));
      return responde({ ok: true });
    }

    const destino = destinoBueno(d.destino);
    if (!destino) {
      return responde({ error: 'Ese destino no vale. Pega el enlace de Google ' +
                               'entero, o el código del sitio.' }, 400);
    }

    const ahora = new Date().toISOString();
    let previo = null;
    try {
      const crudo = await env.ENCARGOS.get(CLAVE_ENLACE(nombre));
      if (crudo) previo = JSON.parse(crudo);
    } catch (e) { previo = null; }

    /* Si no mandan negocio, se queda el que ya tenía. Cambiar solo el
       destino no puede borrarte el nombre con el que lo reconoces. */
    var negocio = String((d && d.negocio) || '').trim().slice(0, 80);
    if (!negocio && previo) negocio = previo.negocio || '';

    await env.ENCARGOS.put(CLAVE_ENLACE(nombre), JSON.stringify({
      destino: destino,
      negocio: negocio,
      creado:  (previo && previo.creado) || ahora,
      cambiado: ahora
    }));
    return responde({ ok: true, nombre: nombre, destino: destino });
  }

  /* ---- la lista ---- */
  try {
    const { keys } = await env.ENCARGOS.list({ prefix: 'r-', limit: 1000 });
    const dia = hoyEnMadrid();
    const lista = [];
    for (const k of keys) {
      const nombre = k.name.slice(2);
      const [crudo, total, hoy] = await Promise.all([
        env.ENCARGOS.get(k.name),
        env.ENCARGOS.get(CLAVE_TOTAL(nombre)),
        env.ENCARGOS.get(CLAVE_CUENTA(nombre, dia))
      ]);
      if (!crudo) continue;
      try {
        const uno = JSON.parse(crudo);
        uno.nombre = nombre;
        uno.total  = numero(total);
        uno.hoy    = numero(hoy);
        lista.push(uno);
      } catch (e) {
        console.error('enlace ilegible: ' + k.name);
      }
    }
    lista.sort((a, b) => String(b.cambiado || '').localeCompare(String(a.cambiado || '')));
    return responde({ lista });
  } catch (err) {
    const detalle = (err && err.message) || 'sin detalle';
    console.error(detalle);
    return responde({ error: detalle }, 500);
  }
}
