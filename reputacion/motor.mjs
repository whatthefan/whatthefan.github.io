/* El motor: recibe una reseña, se la pasa a la IA y devuelve el
   veredicto, la apelación para Google y la respuesta pública.

   No tiene nada que ver con la web de PLEA5E: no lo importa nadie de
   src/ ni se sirve desde public/. Vive en su carpeta para poder
   moverlo a su propio repositorio el día que haga falta.

   Lo que devuelve analiza():

     veredicto     'impugnable' o 'no-impugnable'
     fuerza        la mejor de las infracciones: 'alta', 'media', 'baja'
                   o null si no hay ninguna
     infracciones  las que han pasado la comprobación de la cita
     descartadas   las que la IA propuso y no se sostienen (para revisar
                   el criterio, nunca para denunciar)
     apelacion     el texto para Google, o '' si no es impugnable
     respuesta     la respuesta pública, siempre
     resumen       una línea para el dueño */

import { POLITICAS, SISTEMA, ESQUEMA } from './politicas.mjs';

export const MODELO = 'claude-opus-5-5';

const ORDEN_FUERZA = { alta: 3, media: 2, baja: 1 };

/* Lo que lee la IA. Todo lo que no viene se omite en vez de mandarlo
   vacío: una línea "Ciudad: " sin nada detrás invita a inventársela. */
export function montaMensaje(resena) {
  const n = resena.negocio || {};
  const claves = (n.palabras_clave || []).filter(Boolean);
  return [
    n.nombre ? 'Negocio: ' + n.nombre : '',
    n.sector ? 'Sector: ' + n.sector : '',
    n.ciudad ? 'Ciudad: ' + n.ciudad : '',
    claves.length ? 'Palabras clave: ' + claves.join(', ') : '',
    n.contacto ? 'Contacto para la respuesta: ' + n.contacto : '',
    resena.contexto ? '\nContexto del dueño:\n' + resena.contexto : '',
    '\nEstrellas: ' + (resena.estrellas == null ? 'sin dato' : resena.estrellas),
    'Reseña:\n' + resena.texto
  ].filter(Boolean).join('\n');
}

/* Para comparar citas: minúsculas, sin tildes, comillas y espacios
   unificados. La IA a veces cambia una comilla recta por una curva o
   junta dos espacios, y eso no puede tumbar una cita buena. */
export function normaliza(s) {
  return String(s == null ? '' : s)
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[“”«»„]/g, '"').replace(/[‘’‚]/g, "'")
    .replace(/[…]/g, '...')
    .replace(/\s+/g, ' ')
    .trim()
    .toLowerCase();
}

/* La comprobación que protege al negocio. La IA propone; aquí solo
   sobrevive lo que se puede señalar con el dedo: cada cita tiene que
   estar, tal cual, en el texto de donde dice que sale. Una denuncia sin
   fragmento que la respalde es una denuncia que Google rechaza, y una
   denuncia inventada es lo que convierte esto en algo ilegal.

   Si después de filtrar no queda ninguna infracción, la apelación se
   tira: no se entrega nunca un escrito apoyado en citas falsas. */
export function depura(bruto, resena) {
  const fuentes = {
    resena: normaliza(resena.texto),
    dueno: normaliza(resena.contexto)
  };
  const infracciones = [];
  const descartadas = [];
  for (const inf of (bruto && bruto.infracciones) || []) {
    const cita = normaliza(inf.cita);
    const donde = fuentes[inf.fuente];
    let motivo = '';
    if (!POLITICAS[inf.politica]) motivo = 'norma desconocida';
    else if (cita.length < 2) motivo = 'cita vacía';
    else if (!donde || !donde.includes(cita)) motivo = 'la cita no está en el texto';
    if (motivo) descartadas.push({ ...inf, motivo });
    else infracciones.push({ ...inf, norma: POLITICAS[inf.politica].nombre });
  }
  infracciones.sort((a, b) => (ORDEN_FUERZA[b.fuerza] || 0) - (ORDEN_FUERZA[a.fuerza] || 0));
  const impugnable = infracciones.length > 0;
  return {
    veredicto: impugnable ? 'impugnable' : 'no-impugnable',
    fuerza: impugnable ? infracciones[0].fuerza : null,
    infracciones,
    descartadas,
    apelacion: impugnable ? String((bruto && bruto.apelacion) || '').trim() : '',
    respuesta: String((bruto && bruto.respuesta) || '').trim(),
    resumen: String((bruto && bruto.resumen) || '').trim()
  };
}

/* Igual que en src/api/encargo.js: el SDK se carga solo cuando hace
   falta, para que las pruebas sin red ni clave no lo necesiten. */
async function creaCliente(apiKey) {
  const m = await import('@anthropic-ai/sdk');
  const Anthropic = m.default || m.Anthropic;
  return new Anthropic(apiKey ? { apiKey } : {});
}

/* opciones.cliente sirve para las pruebas: se le pasa uno de mentira y
   no se gasta nada. */
export async function analiza(resena, opciones = {}) {
  if (!resena || !String(resena.texto || '').trim()) {
    throw new Error('la reseña no tiene texto');
  }
  const cliente = opciones.cliente || await creaCliente(opciones.apiKey);
  const r = await cliente.beta.messages.create({
    model: MODELO,
    max_tokens: 16000,
    /* Buscar el matiz en una reseña es justo donde pensar compensa;
       medium es el punto entre coste y finura. Si se escapan
       infracciones, se sube a high antes que tocar el prompt. */
    output_config: {
      effort: 'medium',
      format: { type: 'json_schema', schema: ESQUEMA }
    },
    /* Si el filtro de seguridad del modelo rechaza una reseña (las hay
       muy desagradables), la API la reintenta sola con otro modelo en
       la misma llamada. */
    betas: ['server-side-fallback-2026-07-01'],
    fallbacks: 'default',
    system: SISTEMA,
    messages: [{ role: 'user', content: montaMensaje(resena) }]
  });
  if (r.stop_reason === 'refusal') {
    throw new Error('la IA no ha querido analizar esta reseña' +
      (r.stop_details && r.stop_details.category ? ' (' + r.stop_details.category + ')' : ''));
  }
  if (r.stop_reason === 'max_tokens') {
    throw new Error('la respuesta de la IA llegó cortada');
  }
  const txt = (r.content || []).filter((b) => b.type === 'text').map((b) => b.text).join('');
  return depura(JSON.parse(txt), resena);
}
