/* El analizador gratis de reseñas de la página /analiza/.

   La sirve el Worker de src/index.js en  /api/analiza .

   Es PÚBLICO. Lo denunciable lo buscan solo las reglas
   (reputacion/reglas.mjs), que no gastan nada. La respuesta sí la escribe
   la IA, pensada para esa reseña, pero con tope (src/lib/limite.mjs): 5
   por persona y día y IA_TOPE_DIA para toda la web (200 si no se dice).
   Pasado el tope, sale de plantilla y el usuario ni lo nota.

   El trato con quien la usa: el veredicto y la respuesta, gratis y al
   momento. La apelación para Google, cuando deja su teléfono o correo.
   Ese contacto se guarda en el almacén con la clave  an-<fecha>-<azar>
   y te llega un correo. Es un cliente que acaba de ver en su propia
   ficha el problema que le resuelves.

   Necesita (todo opcional: sin ello el análisis funciona igual):
     ENCARGOS          el almacén (KV) donde se guardan los contactos
     RESEND_API_KEY    para el correo de aviso
     CORREO_AVISO      a dónde te llega
     CORREO_DE         desde qué dirección sale */

import { analiza } from '../../reputacion/motor.mjs';
import { permite } from '../lib/limite.mjs';

const JSON_CAB = { 'Content-Type': 'application/json; charset=utf-8' };

function responde(obj, estado) {
  return new Response(JSON.stringify(obj), { status: estado || 200, headers: JSON_CAB });
}

const corta = (s, n) => String(s == null ? '' : s).trim().slice(0, n);

/* Todo lo que llega se recorta a un tamaño razonable antes de tocarlo:
   es un formulario público y puede llegar cualquier cosa. */
export function limpia(d) {
  d = d || {};
  const n = d.negocio || {};
  const est = Number(d.estrellas);
  return {
    resena: {
      texto: corta(d.texto, 4000),
      estrellas: est >= 1 && est <= 5 ? Math.round(est) : null,
      contexto: corta(d.contexto, 600),
      autor: corta(d.autor, 80),
      negocio: {
        nombre: corta(n.nombre, 80),
        sector: corta(n.sector, 60),
        ciudad: corta(n.ciudad, 60),
        palabras_clave: (Array.isArray(n.palabras_clave) ? n.palabras_clave : String(n.palabras_clave || '').split(','))
          .map((k) => corta(k, 60)).filter(Boolean).slice(0, 4),
        contacto: corta(n.contacto, 120)
      }
    },
    lead: {
      nombre: corta(d.lead && d.lead.nombre, 80),
      contacto: corta(d.lead && d.lead.contacto, 120),
      acepta: Boolean(d.lead && d.lead.acepta)
    },
    /* el campo trampa: las personas no lo ven, los robots lo rellenan */
    trampa: corta(d.web, 200)
  };
}

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

async function avisa(ficha, base, env) {
  const clave = String(env.RESEND_API_KEY || '').trim();
  const para = String(env.CORREO_AVISO || '').trim();
  const desde = String(env.CORREO_DE || '').trim();
  if (!clave || !para || !desde) return false;
  const v = ficha.analisis;
  const negocio = ficha.resena.negocio.nombre || 'sin nombre';
  const html = `
    <div style="font:15px/1.5 -apple-system,Segoe UI,Roboto,Arial,sans-serif;color:#111;max-width:560px">
      <h2 style="margin:0 0 6px">Contacto nuevo del analizador</h2>
      <p style="margin:0 0 14px;color:#555">${esc(negocio)} · ${esc(ficha.lead.nombre)} · <b>${esc(ficha.lead.contacto)}</b></p>
      <p style="margin:0 0 6px"><b>Veredicto:</b> ${esc(v.veredicto)}${v.fuerza ? ' (fuerza ' + esc(v.fuerza) + ')' : ''}</p>
      <blockquote style="margin:0 0 14px;padding:10px 12px;background:#f5f5f5;border-left:3px solid #E9BC46">${esc(ficha.resena.texto)}</blockquote>
      <p style="margin:0 0 18px">${esc(v.resumen)}</p>
      <a href="${esc(base)}/taller/resenas.html" style="background:#E9BC46;color:#100B00;text-decoration:none;padding:12px 20px;border-radius:999px;font-weight:700">Abrir el panel</a>
    </div>`;
  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + clave, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: desde, to: [para],
        subject: 'Reseñas · ' + negocio + ' · ' + v.veredicto + ' · ' + ficha.lead.contacto,
        html
      })
    });
    if (!r.ok) console.error('resend ' + r.status + ' ' + (await r.text()).slice(0, 200));
    return r.ok;
  } catch (err) {
    console.error('aviso: ' + (err && err.message));
    return false;
  }
}

export async function onRequest(context) {
  const { request, env } = context;
  if (request.method !== 'POST') return responde({ error: 'solo POST' }, 405);

  let crudo;
  try { crudo = await request.json(); } catch (e) { return responde({ error: 'envío raro' }, 400); }
  const { resena, lead, trampa } = limpia(crudo);
  if (trampa) return responde({ error: 'envío raro' }, 400);
  if (resena.texto.length < 3) return responde({ error: 'Pega el texto de la reseña.' }, 400);

  const apiKey = String(env.ANTHROPIC_API_KEY || '').trim();
  const conIA = apiKey && (await permite(env, request, 'ia', 5, Number(env.IA_TOPE_DIA) || 200));
  const config = { tono: crudo.tono === 'formal' ? 'formal' : 'cercano', firma: corta(crudo.firma, 80), contacto: resena.negocio.contacto };
  const v = await analiza(resena, conIA
    ? { modo: 'gratis', redactar: 'ia', apiKey, config }
    : { modo: 'gratis', redactar: 'plantilla', config });

  /* Sin contacto, la apelación no sale: es lo que se da a cambio. Se dice
     que la hay, para que sepa que merece la pena dejarlo. */
  const conContacto = lead.contacto.length >= 6 && lead.acepta;
  const publico = {
    tipo: v.tipo, veredicto: v.veredicto, fuerza: v.fuerza, resumen: v.resumen,
    respuesta: v.respuesta,
    infracciones: v.infracciones.map((i) => ({ norma: i.norma, cita: i.cita, fuerza: i.fuerza })),
    apelacion: conContacto ? v.apelacion : '',
    hay_apelacion: Boolean(v.apelacion)
  };
  if (!conContacto) return responde(publico);

  /* Se guarda antes de avisar, como los pedidos: si el correo falla, el
     contacto sigue en el panel. */
  const cuando = Date.now();
  const ficha = { cuando, estado: 'nuevo', lead, resena, analisis: v, origen: 'analizador' };
  let guardado = false;
  try {
    if (!env.ENCARGOS) throw new Error('falta el almacén ENCARGOS');
    const azar = Math.random().toString(36).slice(2, 8);
    await env.ENCARGOS.put('an-' + cuando + '-' + azar, JSON.stringify(ficha));
    guardado = true;
  } catch (err) {
    console.error('guardar contacto: ' + (err && err.message));
  }
  const avisado = await avisa(ficha, new URL(request.url).origin, env);
  return responde({ ...publico, guardado, avisado });
}
