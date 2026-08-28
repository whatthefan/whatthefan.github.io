/* Recibe el encargo del cliente, lo guarda, elige los colores y te manda
   el correo con el enlace del generador ya montado.

   La sirve el Worker de src/index.js en  /api/encargo .

   ── Lo que necesita, y lo que pasa si falta ──────────────────────────

   ENCARGOS            el almacén (KV). Es lo único imprescindible para
                       que el pedido quede guardado. Si falla, el correo
                       sale igual y el pedido no se pierde del todo.
   ANTHROPIC_API_KEY   la IA que elige los colores. OPCIONAL: sin ella
                       los elige la tabla por oficio, gratis.
   RESEND_API_KEY      el correo. Sin ella el encargo se queda en el
                       panel y ya lo ves tú.
   CORREO_AVISO        a dónde te llegan los avisos.
   CORREO_DE           desde qué dirección salen.

   La regla de toda la función: que falle un extra NUNCA puede costar un
   pedido. Por eso se guarda antes de avisar, y por eso cada paso va en
   su propio try. */

import * as L from '../lib/encargo.mjs';

/* El SDK de Anthropic se carga a mano y solo cuando hace falta.

   Pedirlo arriba con un import normal parece más limpio, pero si un día
   no está instalado —o el entorno le falta alguna pieza de Node— la
   función entera revienta ANTES de ejecutarse, y un pedido pagado se
   pierde por culpa de un extra opcional. Ya pasó una vez con el almacén
   de Netlify y costó media hora a ciegas.

   Así, si no carga, se sigue con la tabla de colores y el cliente ni se
   entera. */
async function cargaAnthropic() {
  try {
    const m = await import('@anthropic-ai/sdk');
    return m.default || m.Anthropic;
  } catch (err) {
    console.error('sin SDK de Anthropic: ' + (err && err.message));
    return null;
  }
}

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

/* Le pedimos a Claude el brief. Si algo falla —no hay clave, se cae la
   red, contesta algo que no se entiende— se devuelve null y quien llama
   tira de la tabla por oficio. No hace falta red de seguridad para las
   negativas del modelo: cualquier respuesta que no sea el JSON esperado
   acaba en el mismo sitio, que es la tabla. */
async function pideBrief(encargo, env) {
  if (!env.ANTHROPIC_API_KEY) return null;
  const Anthropic = await cargaAnthropic();
  if (!Anthropic) return null;
  try {
    const client = new Anthropic({ apiKey: env.ANTHROPIC_API_KEY });
    const datos = [
      'Negocio: ' + encargo.negocio,
      encargo.lema      ? 'Lema que propone: ' + encargo.lema : '',
      encargo.ciudad    ? 'Ciudad: ' + encargo.ciudad : '',
      encargo.direccion ? 'Dirección: ' + encargo.direccion : '',
      encargo.redes     ? 'Redes o web: ' + encargo.redes : '',
      'Pedido: ' + L.resumenPedido(encargo),
      encargo.notas     ? 'Lo que pide:\n' + encargo.notas : ''
    ].filter(Boolean).join('\n');

    const r = await client.messages.create({
      model: 'claude-opus-5',
      /* Holgado a propósito: es un tope, no un gasto. Ajustado corto, el
         razonamiento del modelo se come el hueco y la respuesta llega
         cortada por la mitad. */
      max_tokens: 8000,
      /* Elegir tres colores no da para mucho pensar; con esto sale más
         barato y más rápido. */
      output_config: { effort: 'low' },
      system: SISTEMA,
      messages: [{ role: 'user', content: datos }]
    });
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

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

async function avisa(encargo, enlace, brief, ref, env) {
  const clave = env.RESEND_API_KEY;
  const para  = env.CORREO_AVISO;
  const desde = env.CORREO_DE;
  if (!clave || !para || !desde) return false;

  const fila = (k, v) => (v ? `<tr><td style="padding:3px 12px 3px 0;color:#666">${k}</td><td style="padding:3px 0"><b>${esc(v)}</b></td></tr>` : '');

  /* El aviso puede llegarte dos veces por el mismo pedido: al irse a
     pagar y al volver. El cartel de arriba dice en cuál de las dos
     estás, para que no parezcan dos pedidos distintos. */
  const CARTEL = {
    'sin-pagar': ['Se ha ido a pagar la fianza', 'Aún no ha vuelto. Si no te llega el cobro, este es al que hay que escribir.', '#8a6d1f', '#fdf6e3'],
    'pagado':    ['Fianza pagada', 'Cuadra la referencia con tu panel de Stripe antes de ponerte.', '#1d6b3f', '#eaf7ef'],
    'llamada':   ['Quiere que le llames antes de pagar', 'No ha pagado nada. Escríbele tú.', '#8a3f1f', '#fdefe8'],
    'enviado':   ['', '', '', '']
  };
  const c = CARTEL[encargo.estado] || CARTEL.enviado;

  const html = `
    <div style="font:15px/1.55 system-ui,sans-serif;color:#111">
      <p style="margin:0 0 4px;font-size:13px;color:#777">Encargo ${esc(ref)}</p>
      <h2 style="margin:0 0 14px;font-size:20px">${esc(encargo.negocio)}</h2>
      ${c[0] ? `<p style="margin:0 0 14px;padding:10px 12px;border-radius:8px;background:${c[3]};color:${c[2]};font-size:14px"><b>${esc(c[0])}</b><br><span style="color:#555">${esc(c[1])}</span></p>` : ''}
      <table style="border-collapse:collapse;font-size:14px">
        ${fila('Ciudad', encargo.ciudad)}
        ${fila('Dirección', encargo.direccion)}
        ${fila('Teléfono', encargo.tel)}
        ${fila('Correo', encargo.correo)}
        ${fila('Redes', encargo.redes)}
        ${fila('Pedido', L.resumenPedido(encargo))}
        ${fila('Google', encargo.google)}
        ${fila('Pago', encargo.pago)}
        ${fila('Fianza', encargo.fianza ? encargo.fianza + ' €' : '')}
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
      /* el asunto lleva en qué punto está: es lo que miras antes de abrir */
      subject: 'Encargo ' + ref + ' · ' + encargo.negocio +
               (L.ESTADO_TXT[encargo.estado] ? ' · ' + L.ESTADO_TXT[encargo.estado] : ''),
      html: html
    })
  });
  if (!r.ok) console.error('resend ' + r.status + ' ' + (await r.text()).slice(0, 200));
  return r.ok;
}

const JSON_CAB = { 'Content-Type': 'application/json; charset=utf-8' };

export async function onRequestPost(context) {
  const { request, env } = context;

  let crudo;
  try { crudo = await request.json(); }
  catch (e) {
    return new Response('{"error":"no entiendo el envío"}', { status: 400, headers: JSON_CAB });
  }

  /* el cepo para robots: un campo escondido que una persona nunca rellena */
  if (crudo && crudo.web) {
    return new Response('{"ok":true}', { status: 200, headers: JSON_CAB });
  }

  const { encargo, faltan } = L.limpia(crudo);
  if (faltan.length) {
    return new Response(JSON.stringify({ error: 'Faltan ' + faltan.join(' y ') + '.' }),
                        { status: 400, headers: JSON_CAB });
  }

  encargo.google = L.enlaceResena(encargo.google);

  /* ── ¿es un pedido nuevo o el mismo de hace un rato? ──
     El mismo pedido puede llegar dos veces: una al irse a pagar y otra
     al volver y mandar el WhatsApp. Si cada envío abriera su ficha,
     el panel se llenaría de duplicados y no habría forma de saber cuál
     es el bueno. Con el identificador que manda el navegador buscamos
     la ficha que ya existe y la ACTUALIZAMOS.

     Si el almacén falla o no viene identificador, se sigue como toda la
     vida: ficha nueva. Un duplicado molesta; perder un pedido, no. */
  let anterior = null, clave = null;
  if (encargo.pedidoId && env.ENCARGOS) {
    try {
      clave = await env.ENCARGOS.get('id-' + encargo.pedidoId);
      if (clave) {
        const crudoAnt = await env.ENCARGOS.get(clave);
        if (crudoAnt) anterior = JSON.parse(crudoAnt);
      }
    } catch (err) {
      console.error('buscar el anterior: ' + (err && err.message));
      anterior = null; clave = null;
    }
  }

  const cuando = anterior ? anterior.cuando : Date.now();
  const ref    = anterior ? anterior.ref    : L.referencia(cuando, encargo.negocio);

  /* Los colores solo se piden UNA vez por pedido: en el segundo envío ya
     los tenemos, y volver a preguntarle a la IA es pagar dos veces por
     la misma respuesta. */
  const brief = (anterior && anterior.brief)
              || (await pideBrief(encargo, env))
              || L.coloresPorOficio(encargo);
  const base = new URL(request.url).origin;
  const enlace = L.enlaceGenerador(base, encargo, brief);

  /* Se guarda ANTES de avisar: si el correo falla, el encargo sigue en el
     panel. Al revés se perdería. */
  let guardado = false;
  try {
    if (!env.ENCARGOS) throw new Error('falta el almacén ENCARGOS');
    const k = clave || (String(cuando) + '-' + ref);
    await env.ENCARGOS.put(k, JSON.stringify({
      ref, cuando, encargo, brief, enlace,
      /* el estado del taller (nuevo/hecho/descartado) no se pisa al
         actualizar: si ya lo habías marcado como hecho, sigue hecho */
      estado: (anterior && anterior.estado) || 'nuevo',
      /* y el del cliente, que es el que cambia entre envío y envío */
      paso: encargo.estado,
      tocado: Date.now()
    }));
    /* el índice que permite encontrarla la próxima vez */
    if (encargo.pedidoId) await env.ENCARGOS.put('id-' + encargo.pedidoId, k);
    guardado = true;
  } catch (err) {
    console.error('guardar: ' + (err && err.message));
  }

  const avisado = await avisa(encargo, enlace, brief, ref, env);

  return new Response(JSON.stringify({ ok: true, ref, avisado, guardado, nuevo: !anterior }),
                      { status: 200, headers: JSON_CAB });
}

/* Cualquier otro método: fuera. El formulario solo manda POST. */
export async function onRequest(context) {
  if (context.request.method === 'POST') return onRequestPost(context);
  return new Response('{"error":"solo POST"}', { status: 405, headers: JSON_CAB });
}
