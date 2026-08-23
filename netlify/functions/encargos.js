/* Lo que lee el panel de pedidos. Pide contraseña: sin ella no devuelve
   nada. Netlify la publica en  /.netlify/functions/encargos          */

'use strict';

/* La libreria se carga a mano y con red debajo. Si se pide arriba con un
   require normal y no esta instalada, la funcion revienta ANTES de
   ejecutarse: Netlify contesta un 500 pelado y desde el panel solo se ve
   "el servidor ha fallado", que no dice nada. Cargandola asi se puede
   distinguir "falta la libreria" de "el almacen no esta configurado", que
   son dos problemas con dos arreglos distintos. */
function abreAlmacen(nombre) {
  var blobs;
  try {
    blobs = require('@netlify/blobs');
  } catch (err) {
    var e = new Error('Falta la libreria @netlify/blobs en el despliegue. ' +
                      'Netlify no ha instalado las dependencias del package.json.');
    e.causa = 'libreria';
    throw e;
  }
  try {
    return blobs.getStore(nombre);
  } catch (err) {
    var e2 = new Error('El almacen de Netlify (Blobs) no esta disponible: ' +
                       (err && err.message ? err.message : 'sin detalle'));
    e2.causa = 'almacen';
    throw e2;
  }
}

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
  /* Se recortan los espacios de los dos lados. Pegando las variables en
     Netlify es facilisimo que se cuele un espacio o un salto de linea al
     final del valor: tu escribes la contrasena bien, el servidor tiene
     guardada la tuya "con una cola", y no entras nunca. Como una
     contrasena que empieza o acaba en espacio no la quiere nadie, se
     quitan y santas pascuas. */
  const esperada = String(process.env.PANEL_CLAVE || '').trim();
  if (!esperada) {
    return { statusCode: 500, headers: cabeceras,
             body: '{"error":"falta PANEL_CLAVE en la configuracion"}' };
  }
  const dada = String(event.headers['x-panel-clave'] ||
                      (event.queryStringParameters || {}).clave || '').trim();
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
      const store = abreAlmacen('encargos');
      const uno = await store.get(d.clave, { type: 'json' });
      if (!uno) return { statusCode: 404, headers: cabeceras, body: '{"error":"no esta"}' };
      uno.estado = d.estado;
      await store.setJSON(d.clave, uno);
      return { statusCode: 200, headers: cabeceras, body: '{"ok":true}' };
    } catch (err) {
      const detalle = (err && err.message) || 'sin detalle';
      console.error(detalle);
      return { statusCode: 500, headers: cabeceras,
               body: JSON.stringify({ error: detalle }) };
    }
  }

  try {
    const store = abreAlmacen('encargos');
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
    /* El detalle se devuelve tal cual, y a proposito: aqui solo se llega
       DESPUES de acertar la contrasena, asi que lo lee el dueno y nadie
       mas. Sin el detalle, diagnosticar esto es ir a ciegas. */
    const detalle = (err && err.message) || 'sin detalle';
    console.error(detalle);
    return { statusCode: 500, headers: cabeceras,
             body: JSON.stringify({ error: detalle, causa: (err && err.causa) || 'lectura' }) };
  }
};
