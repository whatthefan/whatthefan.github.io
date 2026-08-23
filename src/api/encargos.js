/* Lo que lee y actualiza el panel de pedidos. Pide contraseña: sin ella
   no devuelve nada.

   La sirve el Worker de src/index.js en  /api/encargos .

   Necesita:
     PANEL_CLAVE   la contraseña del panel
     ENCARGOS      el almacén (KV) donde están los pedidos */

const JSON_CAB = { 'Content-Type': 'application/json; charset=utf-8' };

/* Comparación en tiempo constante. Con un === normal se puede ir
   adivinando la contraseña midiendo lo que tarda en contestar; es
   rebuscado, pero evitarlo cuesta cuatro líneas. */
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

  /* Se recortan los espacios de los dos lados. Pegando las variables en
     el panel del proveedor es facilísimo que se cuele un espacio o un
     salto de línea al final: escribes la contraseña bien, la guardada
     tiene "una cola", y no entras nunca sin saber por qué. */
  const esperada = String(env.PANEL_CLAVE || '').trim();
  if (!esperada) {
    return responde({ error: 'falta PANEL_CLAVE en la configuracion' }, 500);
  }

  const url = new URL(request.url);
  const dada = String(request.headers.get('x-panel-clave') ||
                      url.searchParams.get('clave') || '').trim();
  if (!igual(dada, esperada)) {
    return responde({ error: 'contrasena' }, 401);
  }

  if (!env.ENCARGOS) {
    return responde({
      error: 'El almacén de pedidos no está conectado. En Cloudflare: ' +
             'el Worker → Settings → Bindings → añadir un KV namespace ' +
             'con el nombre de variable ENCARGOS.'
    }, 500);
  }

  /* ---- marcar un encargo como hecho o descartado ---- */
  if (request.method === 'POST') {
    let d;
    try { d = await request.json(); } catch (e) { d = {}; }
    if (!d || !d.clave || ['nuevo', 'hecho', 'descartado'].indexOf(d.estado) < 0) {
      return responde({ error: 'envio raro' }, 400);
    }
    try {
      const crudo = await env.ENCARGOS.get(d.clave);
      if (!crudo) return responde({ error: 'no esta' }, 404);
      const uno = JSON.parse(crudo);
      uno.estado = d.estado;
      await env.ENCARGOS.put(d.clave, JSON.stringify(uno));
      return responde({ ok: true });
    } catch (err) {
      const detalle = (err && err.message) || 'sin detalle';
      console.error(detalle);
      return responde({ error: detalle }, 500);
    }
  }

  /* ---- la lista ---- */
  try {
    /* La clave empieza por la fecha en milisegundos, así que ordenar por
       clave al revés deja los nuevos arriba sin tener que abrirlos. */
    const { keys } = await env.ENCARGOS.list({ limit: 1000 });
    const claves = keys.map((k) => k.name).sort().reverse().slice(0, 100);
    const lista = [];
    for (const k of claves) {
      const crudo = await env.ENCARGOS.get(k);
      if (!crudo) continue;
      try {
        const uno = JSON.parse(crudo);
        uno.clave = k;
        lista.push(uno);
      } catch (e) {
        /* un pedido con el JSON roto no puede tumbar el panel entero */
        console.error('pedido ilegible: ' + k);
      }
    }
    return responde({ lista });
  } catch (err) {
    /* El detalle se devuelve tal cual, y a propósito: aquí solo se llega
       DESPUÉS de acertar la contraseña, así que lo lee el dueño y nadie
       más. Sin el detalle, diagnosticar esto es ir a ciegas. */
    const detalle = (err && err.message) || 'sin detalle';
    console.error(detalle);
    return responde({ error: detalle }, 500);
  }
}
