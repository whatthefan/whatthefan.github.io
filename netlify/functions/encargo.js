/* Recibe el encargo del cliente, lo guarda, le pide a Claude el brief de
   diseño y te manda a ti el correo con el enlace del generador ya montado.
   Netlify la publica sola en  /.netlify/functions/encargo

   Variables de entorno (Netlify > Project configuration > Environment):
     ANTHROPIC_API_KEY   la clave de la API de Claude (OPCIONAL)
     RESEND_API_KEY      la clave de Resend, para el correo
     CORREO_AVISO        a dónde te llegan los avisos
     CORREO_DE           desde qué dirección salen (dominio verificado)
     PANEL_CLAVE         la contraseña del panel de pedidos

   Si falta ANTHROPIC_API_KEY no pasa nada: los colores los elige la
   tabla por oficio de lib/encargo.js, que es gratis y acierta el tono.
   Si falta RESEND_API_KEY tampoco se pierde nada, el encargo se queda en
   el panel. Que falle un extra no puede costar un pedido. */

'use strict';

const { getStore } = require('@netlify/blobs');
const Anthropic = require('@anthropic-ai/sdk');
const L = require('./lib/encargo.js');

const SISTEMA = `Eres el ayudante de diseño de PLEA5E, que fabrica placas
con chip NFC y código QR para que los clientes de un negocio le dejen
reseña en Google.

Todas las placas salen de UNA plantilla fija, que no se cambia: banda de
color arriba con el borde de abajo curvado, texto blanco en mayúsculas,
fondo claro, la G de Google, el icono de acercar el móvil, el QR y abajo
el nombre del negocio. Tú NO diseñas la placa: solo eliges los colores y
el texto que van dentro de esa plantilla.

Te dan los datos que ha escrito un cliente. Devuelve SOLO un objeto JSON,
sin explicaciones alrededor y sin vallas de código, con estas claves:

  banda   color de la banda de arriba, en #RRGGBB. Tiene que ser OSCURO
          (para que el texto blanco se lea encima) y pegar con el tipo de
          negocio. Si no tienes ni idea, pon "#192E26".
  fondo   color del cuerpo, en #RRGGBB. Claro. Por defecto "#ECE2D3".
  acento  color de las rayas y las estrellas, en #RRGGBB. Por defecto
          "#E8C46A", el oro de la marca.
  lema    una línea corta debajo del nombre, de 3 a 5 palabras, sacada de
          lo que ha contado el cliente (por ejemplo "Bar · Cocina ·
          Sobremesa"). Si no hay material, cadena vacía.
  titulo  el texto de la banda. Deja "¡Nos encantaría tu reseña en
          Google!" salvo que el cliente pida otra cosa.
  porque  una frase para el dueño de PLEA5E explicando por qué has
          elegido esos colores.

Reglas: no te inventes datos del negocio que no te hayan dado. No pongas
el logo ni describas dibujos. Si el cliente pide colores concretos,
mándanlos ellos.`;

/* le pedimos a Claude el brief. Si algo falla, se sigue sin brief. */
async function pideBrief(encargo) {
  if (!process.env.ANTHROPIC_API_KEY) return null;
  try {
    const client = new Anthropic();
    const datos = [
      'Negocio: ' + encargo.negocio,
      encargo.lema      ? 'Lema que propone: ' + encargo.lema : '',
      encargo.ciudad    ? 'Ciudad: ' + encargo.ciudad : '',
      encargo.direccion ? 'Dirección: ' + encargo.direccion : '',
      encargo.redes     ? 'Redes o web: ' + encargo.redes : '',
      'Formato: ' + encargo.formato + ' × ' + encargo.cantidad,
      encargo.notas     ? 'Lo que pide:\n' + encargo.notas : ''
    ].filter(Boolean).join('\n');

    const r = await client.messages.create({
      model: 'claude-opus-5',
      max_tokens: 1200,
      /* trabajo corto y acotado: no hace falta gastar en pensar mucho */
      output_config: { effort: 'low' },
      system: SISTEMA,
      messages: [{ role: 'user', content: datos }]
    });
    /* el contenido es una lista de bloques; nos quedamos con el texto */
    const txt = (r.content || [])
      .filter((b) => b.type === 'text')
      .map((b) => b.text)
      .join('\n');
    return L.leeBrief(txt);
  } catch (err) {
    console.error('brief: ' + (err && err.message));
    return null;
  }
}

async function avisa(encargo, enlace, brief, ref) {
  const clave = process.env.RESEND_API_KEY;
  const para  = process.env.CORREO_AVISO;
  const desde = process.env.CORREO_DE;
  if (!clave || !para || !desde) return false;

  const fila = (k, v) => (v ? `<tr><td style="padding:3px 12px 3px 0;color:#666">${k}</td><td style="padding:3px 0"><b>${esc(v)}</b></td></tr>` : '');
  const html = `
    <div style="font:15px/1.55 system-ui,sans-serif;color:#111">
      <p style="margin:0 0 4px;font-size:13px;color:#777">Encargo ${esc(ref)}</p>
      <h2 style="margin:0 0 14px;font-size:20px">${esc(encargo.negocio)}</h2>
      <table style="border-collapse:collapse;font-size:14px">
        ${fila('Ciudad', encargo.ciudad)}
        ${fila('Dirección', encargo.direccion)}
        ${fila('Teléfono', encargo.tel)}
        ${fila('Correo', encargo.correo)}
        ${fila('Redes', encargo.redes)}
        ${fila('Pedido', encargo.formato + ' × ' + encargo.cantidad)}
        ${fila('Google', encargo.google)}
        ${fila('Pago', encargo.pago)}
      </table>
      ${encargo.notas ? `<p style="margin:14px 0 0"><b>Lo que pide:</b><br>${esc(encargo.notas)}</p>` : ''}
      ${brief && brief.porque ? `<p style="margin:14px 0 0;padding:10px 12px;background:#faf6ec;border-left:3px solid #E8C46A"><b>Propuesta de color:</b> ${esc(brief.porque)}</p>` : ''}
      <p style="margin:22px 0 0">
        <a href="${esc(enlace)}" style="background:#E9BC46;color:#100B00;text-decoration:none;padding:12px 20px;border-radius:999px;font-weight:700">Abrir el diseño</a>
      </p>
      <p style="margin:16px 0 0;font-size:12px;color:#888">
        Se abre el generador con todo puesto. El logo, si lo ha mandado, va adjunto o te lo pasa por WhatsApp.
      </p>
    </div>`;

  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + clave, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: desde, to: [para],
      subject: 'Encargo ' + ref + ' · ' + encargo.negocio,
      html: html
    })
  });
  if (!r.ok) console.error('resend ' + r.status + ' ' + (await r.text()).slice(0, 200));
  return r.ok;
}

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

exports.handler = async function (event) {
  const cabeceras = { 'Content-Type': 'application/json; charset=utf-8' };
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers: cabeceras, body: '{"error":"solo POST"}' };
  }

  let crudo;
  try { crudo = JSON.parse(event.body || '{}'); }
  catch (e) { return { statusCode: 400, headers: cabeceras, body: '{"error":"no entiendo el envío"}' }; }

  /* el cepo para robots: un campo escondido que una persona nunca rellena */
  if (crudo.web) return { statusCode: 200, headers: cabeceras, body: '{"ok":true}' };

  const { encargo, faltan } = L.limpia(crudo);
  if (faltan.length) {
    return { statusCode: 400, headers: cabeceras,
             body: JSON.stringify({ error: 'Faltan ' + faltan.join(' y ') + '.' }) };
  }

  const cuando = Date.now();
  const ref = L.referencia(cuando, encargo.negocio);
  encargo.google = L.enlaceResena(encargo.google);

  /* Primero la IA, si hay clave. Si no la hay —o falla, o contesta algo
     que no se entiende— entra la tabla de colores por oficio, que no
     cuesta nada y acierta el tono. Así el encargo NUNCA llega sin una
     propuesta de color: en el peor caso llega con el verde de siempre. */
  const brief = (await pideBrief(encargo)) || L.coloresPorOficio(encargo);
  const base = process.env.URL || ('https://' + (event.headers.host || 'plea5e.es'));
  const enlace = L.enlaceGenerador(base, encargo, brief);

  /* Se guarda ANTES de avisar: si el correo falla, el encargo sigue en el
     panel. Al revés se perdería. */
  try {
    const store = getStore('encargos');
    await store.setJSON(String(cuando) + '-' + ref, {
      ref, cuando, encargo, brief, enlace, estado: 'nuevo'
    });
  } catch (err) {
    console.error('guardar: ' + (err && err.message));
  }

  const avisado = await avisa(encargo, enlace, brief, ref);

  return { statusCode: 200, headers: cabeceras,
           body: JSON.stringify({ ok: true, ref: ref, avisado: avisado }) };
};
