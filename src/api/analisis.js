/* Lo que usa el panel de reseñas (/taller/resenas.html). Pide la misma
   contraseña que el de pedidos: sin ella no devuelve nada.

   La sirve el Worker de src/index.js en  /api/analisis .

     GET                                    la lista de fichas  an-...
     POST { accion: 'estado', clave, estado }   nuevo / contactado / cliente / descartado
     POST { accion: 'borra', clave }
     POST { accion: 'analiza', ...reseña, ia, guardar }
          analiza una reseña desde el panel. Con ia: true usa la IA
          donde las reglas no bastan (cuesta alrededor de un céntimo);
          con guardar: true la deja en la lista.

   Necesita:
     PANEL_CLAVE         la contraseña del panel
     ENCARGOS            el almacén (KV), el mismo de los pedidos
     ANTHROPIC_API_KEY   solo para analizar con IA */

import { analiza } from '../../reputacion/motor.mjs';
import { limpia } from './analiza.js';

const JSON_CAB = { 'Content-Type': 'application/json; charset=utf-8' };
const ESTADOS = ['nuevo', 'contactado', 'cliente', 'descartado'];

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

export async function onRequest(context) {
  const { request, env } = context;

  const esperada = String(env.PANEL_CLAVE || '').trim();
  if (!esperada) return responde({ error: 'falta PANEL_CLAVE en la configuracion' }, 500);
  const dada = String(request.headers.get('x-panel-clave') || '').trim();
  if (!igual(dada, esperada)) return responde({ error: 'contrasena' }, 401);
  if (!env.ENCARGOS) return responde({ error: 'El almacén ENCARGOS no está conectado.' }, 500);

  try {
    if (request.method === 'GET') {
      /* La clave lleva la fecha: al revés, los nuevos arriba. */
      const { keys } = await env.ENCARGOS.list({ prefix: 'an-', limit: 1000 });
      const claves = keys.map((k) => k.name).sort().reverse().slice(0, 200);
      const lista = [];
      for (const k of claves) {
        const crudo = await env.ENCARGOS.get(k);
        if (!crudo) continue;
        try { lista.push({ ...JSON.parse(crudo), clave: k }); }
        catch (e) { console.error('ficha ilegible: ' + k); }
      }
      return responde({ lista, ia: Boolean(String(env.ANTHROPIC_API_KEY || '').trim()) });
    }

    if (request.method !== 'POST') return responde({ error: 'método' }, 405);
    let d;
    try { d = await request.json(); } catch (e) { d = {}; }

    /* Solo se tocan fichas de reseñas: con una clave cualquiera se
       podría borrar un pedido desde aquí. */
    const esFicha = (k) => typeof k === 'string' && k.startsWith('an-');

    if (d.accion === 'estado') {
      if (!esFicha(d.clave) || ESTADOS.indexOf(d.estado) < 0) return responde({ error: 'envío raro' }, 400);
      const crudo = await env.ENCARGOS.get(d.clave);
      if (!crudo) return responde({ error: 'no está' }, 404);
      const uno = JSON.parse(crudo);
      uno.estado = d.estado;
      uno.tocado = Date.now();
      await env.ENCARGOS.put(d.clave, JSON.stringify(uno));
      return responde({ ok: true });
    }

    if (d.accion === 'borra') {
      if (!esFicha(d.clave)) return responde({ error: 'envío raro' }, 400);
      await env.ENCARGOS.delete(d.clave);
      return responde({ ok: true });
    }

    if (d.accion === 'analiza') {
      const { resena, lead } = limpia(d);
      if (resena.texto.length < 3) return responde({ error: 'falta el texto de la reseña' }, 400);
      const apiKey = String(env.ANTHROPIC_API_KEY || '').trim();
      if (d.ia && !apiKey) return responde({ error: 'Para usar la IA falta ANTHROPIC_API_KEY en Cloudflare.' }, 400);
      const v = await analiza(resena, d.ia ? { apiKey, modo: 'auto' } : { modo: 'gratis' });
      let clave = '';
      if (d.guardar) {
        const cuando = Date.now();
        clave = 'an-' + cuando + '-' + Math.random().toString(36).slice(2, 8);
        await env.ENCARGOS.put(clave, JSON.stringify({
          cuando, estado: 'cliente', lead, resena, analisis: v, origen: 'panel'
        }));
      }
      return responde({ analisis: v, clave });
    }

    return responde({ error: 'acción desconocida' }, 400);
  } catch (err) {
    /* Como en el de pedidos: aquí solo se llega con la contraseña, así
       que el detalle lo lee el dueño y nadie más. */
    const detalle = (err && err.message) || 'sin detalle';
    console.error(detalle);
    return responde({ error: detalle }, 500);
  }
}
