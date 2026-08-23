/* Lo que lee el panel de pedidos. Pide contraseña: sin ella no devuelve
   nada. Netlify la publica en  /.netlify/functions/encargos          */

'use strict';

const { getStore } = require('@netlify/blobs');

/* Comparación en tiempo constante. Con un === normal se puede ir adivinando
   la contraseña midiendo lo que tarda en contestar; es rebuscado, pero
   evitarlo cuesta cuatro líneas. */
function igual(a, b) {
  const x = String(a || ''), y = String(b || '');
  if (x.length !== y.length) return false;
  let d = 0;
  for (let i = 0; i < x.length; i++) d |= x.charCodeAt(i) ^ y.charCodeAt(i);
  return d === 0;
}

exports.handler = async function (event) {
  const cabeceras = { 'Content-Type': 'application/json; charset=utf-8' };
  const esperada = process.env.PANEL_CLAVE;
  if (!esperada) {
    return { statusCode: 500, headers: cabeceras,
             body: '{"error":"falta PANEL_CLAVE en la configuracion"}' };
  }
  const dada = (event.headers['x-panel-clave'] ||
                (event.queryStringParameters || {}).clave || '');
  if (!igual(dada, esperada)) {
    return { statusCode: 401, headers: cabeceras, body: '{"error":"contrasena"}' };
  }

  if (event.httpMethod === 'POST') {
    /* marcar un encargo como hecho o descartado */
    let d; try { d = JSON.parse(event.body || '{}'); } catch (e) { d = {}; }
    if (!d.clave || ['nuevo', 'hecho', 'descartado'].indexOf(d.estado) < 0) {
      return { statusCode: 400, headers: cabeceras, body: '{"error":"envio raro"}' };
    }
    try {
      const store = getStore('encargos');
      const uno = await store.get(d.clave, { type: 'json' });
      if (!uno) return { statusCode: 404, headers: cabeceras, body: '{"error":"no esta"}' };
      uno.estado = d.estado;
      await store.setJSON(d.clave, uno);
      return { statusCode: 200, headers: cabeceras, body: '{"ok":true}' };
    } catch (err) {
      console.error(err && err.message);
      return { statusCode: 500, headers: cabeceras, body: '{"error":"no se ha podido guardar"}' };
    }
  }

  try {
    const store = getStore('encargos');
    const { blobs } = await store.list();
    /* la clave empieza por la fecha en milisegundos, así que ordenar por
       clave al revés deja los nuevos arriba sin tener que leerlos */
    const claves = blobs.map((b) => b.key).sort().reverse().slice(0, 100);
    const lista = [];
    for (const k of claves) {
      const uno = await store.get(k, { type: 'json' });
      if (uno) { uno.clave = k; lista.push(uno); }
    }
    return { statusCode: 200, headers: cabeceras, body: JSON.stringify({ lista }) };
  } catch (err) {
    console.error(err && err.message);
    return { statusCode: 500, headers: cabeceras, body: '{"error":"no se ha podido leer"}' };
  }
};
