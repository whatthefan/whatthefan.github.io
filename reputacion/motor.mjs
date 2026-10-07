/* El motor: recibe una reseña y devuelve el veredicto, la apelación para
   Google y la respuesta pública.

   No tiene nada que ver con la web de PLEA5E: no lo importa nadie de
   src/ ni se sirve desde public/. Vive en su carpeta para poder
   moverlo a su propio repositorio el día que haga falta.

   ── Cómo decide, de lo más barato a lo más caro ─────────────────────

   1. Las reglas (reglas.mjs), gratis, miran siempre primero.
   2. Si han encontrado algo evidente (fuerza alta), ya está: la reseña es
      denunciable y la apelación y la respuesta salen de plantillas. No
      se gasta nada.
   3. Si no, y hay clave, entra la IA, con lo que hayan visto las reglas
      como pista. Es la que caza los matices que una lista de palabras
      no ve.
   4. Sin clave, o con { modo: 'gratis' }, se queda en el paso 1.

   Lo que devuelve analiza():

     veredicto     'impugnable', 'no-impugnable' o 'revisar' (solo sin IA:
                   las reglas han visto algo dudoso y tiene que mirarlo una
                   persona antes de denunciar)
     fuerza        la mejor de las infracciones: 'alta', 'media', 'baja'
                   o null si no hay ninguna
     infracciones  las que han pasado la comprobación de la cita
     descartadas   las que no se sostienen (para revisar el criterio,
                   nunca para denunciar)
     apelacion     el texto para Google, o '' si no es impugnable
     respuesta     la respuesta pública, siempre
     resumen       una línea para el dueño
     origen        'reglas' si no ha hecho falta la IA, 'ia' si ha entrado */

import { POLITICAS, SISTEMA, ESQUEMA } from './politicas.mjs';
import { detecta, respuestaPlantilla, apelacionPlantilla } from './reglas.mjs';

/* Sonnet con esfuerzo bajo: unas cuatro veces más barato que Opus y de
   sobra para leer una reseña con lupa. Si se le escapan matices, se
   sube el esfuerzo a 'medium' antes que cambiar de modelo. */
export const MODELO = 'claude-sonnet-5-5';
export const ESFUERZO = 'low';

const ORDEN_FUERZA = { alta: 3, media: 2, baja: 1 };

/* Lo que lee la IA. Todo lo que no viene se omite en vez de mandarlo
   vacío: una línea "Ciudad: " sin nada detrás invita a inventársela. */
export function montaMensaje(resena, pistas = []) {
  const n = resena.negocio || {};
  const claves = (n.palabras_clave || []).filter(Boolean);
  return [
    n.nombre ? 'Negocio: ' + n.nombre : '',
    n.sector ? 'Sector: ' + n.sector : '',
    n.ciudad ? 'Ciudad: ' + n.ciudad : '',
    claves.length ? 'Palabras clave: ' + claves.join(', ') : '',
    n.contacto ? 'Contacto para la respuesta: ' + n.contacto : '',
    resena.contexto ? '\nContexto del dueño:\n' + resena.contexto : '',
    pistas.length
      ? '\nUn filtro automático ha marcado esto como posible infracción. Compruébalo: ' +
        'puede ser un falso positivo, y puede haber más cosas que no ha visto.\n' +
        pistas.map((p) => '- ' + p.politica + ': «' + p.cita + '»').join('\n')
      : '',
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

/* La comprobación que protege al negocio. Se propone lo que sea; aquí
   solo sobrevive lo que se puede señalar con el dedo: cada cita tiene
   que estar, tal cual, en el texto de donde dice que sale. Una denuncia
   sin fragmento que la respalde es una denuncia que Google rechaza, y
   una denuncia inventada es lo que convierte esto en algo ilegal.

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

/* Lo que encuentra la IA más lo que encontraron las reglas y ella no
   recogió. Si los dos marcan lo mismo con la misma norma, se queda el
   de la IA, que explica mejor el porqué. */
function junta(deIA, deReglas) {
  const todas = [...deIA];
  for (const r of deReglas) {
    const cr = normaliza(r.cita);
    const ya = todas.some((i) => i.politica === r.politica &&
      (normaliza(i.cita).includes(cr) || cr.includes(normaliza(i.cita))));
    if (!ya) todas.push(r);
  }
  return todas;
}

function resumenReglas(infracciones) {
  if (!infracciones.length) {
    return 'No se ha encontrado nada que incumpla las normas de Google: toca responderla bien.';
  }
  const normas = [...new Set(infracciones.map((i) => POLITICAS[i.politica].nombre.toLowerCase()))];
  return 'Denunciable por ' + normas.join(' y ') + '.';
}

/* Solo con las reglas. Es lo que sale cuando no hay IA, y también cuando
   las reglas ya han encontrado algo evidente y no merece la pena pagarla. */
function sinIA(resena, pistas) {
  const v = depura({ infracciones: pistas, apelacion: 'x', respuesta: 'x', resumen: 'x' }, resena);
  v.apelacion = apelacionPlantilla(resena, v.infracciones);
  v.respuesta = respuestaPlantilla(resena);
  v.resumen = resumenReglas(v.infracciones);
  /* Una lista de palabras no entiende el contexto. Si lo único que ha
     visto es dudoso, no se da por denunciable: se deja preparado y lo
     decide una persona. Denunciar a ciegas lo que no lo es resta
     credibilidad ante Google. */
  if (v.veredicto === 'impugnable' && v.fuerza !== 'alta') {
    v.veredicto = 'revisar';
    v.resumen = 'Puede ser denunciable: revísalo antes de enviar la apelación. ' + v.resumen;
  }
  v.origen = 'reglas';
  return v;
}

/* Igual que en src/api/encargo.js: el SDK se carga solo cuando hace
   falta, para que las pruebas sin red ni clave no lo necesiten. */
async function creaCliente(apiKey) {
  const m = await import('@anthropic-ai/sdk');
  const Anthropic = m.default || m.Anthropic;
  return new Anthropic(apiKey ? { apiKey } : {});
}

async function conIA(resena, pistas, cliente) {
  const r = await cliente.beta.messages.create({
    model: MODELO,
    max_tokens: 16000,
    output_config: {
      effort: ESFUERZO,
      format: { type: 'json_schema', schema: ESQUEMA }
    },
    /* Si el filtro de seguridad del modelo rechaza una reseña (las hay
       muy desagradables), la API la reintenta sola con otro modelo en
       la misma llamada. */
    betas: ['server-side-fallback-2026-07-01'],
    fallbacks: 'default',
    system: SISTEMA,
    messages: [{ role: 'user', content: montaMensaje(resena, pistas) }]
  });
  if (r.stop_reason === 'refusal') {
    throw new Error('la IA no ha querido analizar esta reseña' +
      (r.stop_details && r.stop_details.category ? ' (' + r.stop_details.category + ')' : ''));
  }
  if (r.stop_reason === 'max_tokens') {
    throw new Error('la respuesta de la IA llegó cortada');
  }
  const txt = (r.content || []).filter((b) => b.type === 'text').map((b) => b.text).join('');
  const bruto = JSON.parse(txt);
  const v = depura({ ...bruto, infracciones: junta(bruto.infracciones || [], pistas) }, resena);
  /* La IA puede no haber escrito apelación porque sus infracciones se
     cayeron en la comprobación y solo quedan las de las reglas. Entonces
     la apelación sale de la plantilla, que solo usa citas comprobadas. */
  const suyas = v.infracciones.filter((i) => i.origen !== 'reglas').length;
  if (v.veredicto === 'impugnable' && (!v.apelacion || !suyas)) {
    v.apelacion = apelacionPlantilla(resena, v.infracciones);
  }
  if (!v.respuesta) v.respuesta = respuestaPlantilla(resena);
  v.origen = 'ia';
  return v;
}

/* opciones:
     apiKey      la clave de Anthropic (si no, la del entorno)
     cliente     uno de mentira para las pruebas
     modo        'gratis'  solo reglas, nunca IA
                 'auto'    (por defecto) IA solo si las reglas no bastan
                 'ia'      IA siempre, aunque las reglas ya lo tengan claro */
export async function analiza(resena, opciones = {}) {
  if (!resena || !String(resena.texto || '').trim()) {
    throw new Error('la reseña no tiene texto');
  }
  const modo = opciones.modo || 'auto';
  const pistas = detecta(resena);
  const evidente = pistas.some((p) => p.fuerza === 'alta');
  const hayIA = Boolean(opciones.cliente || opciones.apiKey || process.env.ANTHROPIC_API_KEY);

  if (modo === 'gratis' || !hayIA || (modo === 'auto' && evidente)) {
    return sinIA(resena, pistas);
  }
  const cliente = opciones.cliente || await creaCliente(opciones.apiKey);
  return conIA(resena, pistas, cliente);
}
