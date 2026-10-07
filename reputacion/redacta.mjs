/* El redactor de respuestas: lo que el dueño publica debajo de cada
   reseña, buena o mala.

   Dos maneras, y siempre hay una que funciona:

     redactaIA()          la IA escribe una respuesta de verdad para ESA
                          reseña: nombra lo que cuenta el cliente, usa su
                          nombre, el tono del negocio y su firma. Alrededor
                          de medio céntimo.
     respuestaPlantilla()
     agradecimientoPlantilla()
                          sin IA. No son de bote del todo: miran de qué se
                          queja o qué le gustó (la espera, el precio, la
                          comida, el trato...) y lo nombran.

   redacta() elige: IA si hay, plantilla si no o si la IA falla.

   Lo que se le puede decir de cada negocio (config):
     tono       'cercano' (tutea, por defecto) o 'formal' (de usted)
     firma      cómo se despide: "Manolo, de Bar Manolo"
     contacto   a dónde llevar la conversación en las negativas
     notas      cualquier indicación del dueño ("no ofrezcas invitaciones") */

export const MODELO_RESPUESTA = 'claude-sonnet-5-5';

/* De qué habla la reseña. Sirve a las plantillas para no sonar a
   respuesta de bote, y a la IA no le hace falta. */
const TEMAS = [
  ['espera', /tard|esper|lent[oa]|demora|cola|hora y media|media hora/i],
  ['comida', /fr[ií][oa]s?|crud|salad|quemad|sin sabor|insípid|comida|plato|tapa|paella|croquet|pizza|hamburgues|caf[eé]|postre|carne|pescado/i],
  ['precio', /car[oa]s?\b|carísim|precio|cobr|cuenta|euros|€/i],
  ['trato', /borde|maleducad|antipátic|trato|atenci[oó]n|camarer|dependient|personal|amable|simp[aá]tic/i],
  ['limpieza', /suci|limpi|baño|aseo|olor/i],
  ['ambiente', /ruido|música|ambiente|terraza|local|decoraci|sitio/i],
  ['reserva', /reserv|mesa/i]
];

export function temas(texto) {
  const t = String(texto || '');
  return TEMAS.filter(([, re]) => re.test(t)).map(([k]) => k);
}

const FRASE_QUEJA = {
  espera: 'Sentimos mucho la espera: no es lo que queremos para nadie que viene a vernos',
  comida: 'Lamentamos que la comida no estuviera a la altura de lo que esperabas',
  precio: 'Entendemos lo que dices del precio y nos lo apuntamos',
  trato: 'Sentimos que el trato no fuera el que te merecías',
  limpieza: 'Lo que cuentas de la limpieza no puede pasar y ya lo estamos revisando',
  ambiente: 'Tomamos nota de lo que comentas del local',
  reserva: 'Sentimos el lío con la mesa'
};
const FRASE_ELOGIO = {
  comida: 'nos alegra un montón que disfrutaras de la comida',
  trato: 'se lo diremos al equipo, que le encantará saber que te sentiste bien atendido',
  ambiente: 'qué bien que te gustara el sitio',
  precio: 'nos alegra que te pareciera que merece la pena',
  espera: 'nos alegra que todo saliera rápido',
  limpieza: 'cuidamos mucho esos detalles',
  reserva: 'gracias por reservar con nosotros'
};

/* El nombre de pila del autor, solo si parece un nombre de verdad:
   "Laura G." sí, "Usuario123" o "El Comilón" no. */
export function nombrePila(autor) {
  const p = String(autor || '').trim().split(/\s+/)[0] || '';
  return /^[A-ZÁÉÍÓÚÑ][a-záéíóúñü]{2,14}$/.test(p) ? p : '';
}

function elige(lista, semilla) {
  let h = 0;
  for (const c of String(semilla)) h = (h * 31 + c.charCodeAt(0)) >>> 0;
  return lista[h % lista.length];
}

function datos(resena, config) {
  const n = (resena && resena.negocio) || {};
  const c = config || {};
  const kw = (c.palabras_clave || n.palabras_clave || []).filter(Boolean);
  return {
    nombre: c.nombre || n.nombre || '',
    kw,
    contacto: c.contacto || n.contacto || '',
    firma: c.firma || '',
    formal: c.tono === 'formal',
    pila: nombrePila(resena && resena.autor)
  };
}

const usted = (formal, tu, ud) => (formal ? ud : tu);

export function respuestaPlantilla(resena, config) {
  const d = datos(resena, config);
  const f = d.formal;
  const tema = temas(resena && resena.texto)[0];
  const hola = d.pila ? 'Hola, ' + d.pila + '. ' : 'Hola. ';
  const gracias = usted(f, 'Gracias por contarnos tu experiencia. ', 'Gracias por contarnos su experiencia. ');
  const queja = tema ? FRASE_QUEJA[tema] + '. ' : elige([
    usted(f, 'Sentimos de verdad que tu visita no fuera como esperabas. ', 'Sentimos de verdad que su visita no fuera como esperaba. '),
    usted(f, 'Lamentamos que no te fueras contento. ', 'Lamentamos que no saliera satisfecho. ')
  ], resena && resena.texto);
  const casa = d.nombre && d.kw.length
    ? 'En ' + d.nombre + ' cuidamos mucho ' + d.kw.slice(0, 2).join(' y ') + ', y queremos entender qué pasó para mejorarlo. '
    : 'Queremos entender qué pasó para mejorarlo. ';
  const privado = d.contacto
    ? usted(f, '¿Nos escribes a ' + d.contacto + '? Lo hablamos con calma.', '¿Podría escribirnos a ' + d.contacto + '? Lo hablaremos con calma.')
    : usted(f, 'Escríbenos por privado y lo hablamos con calma.', 'Escríbanos por privado y lo hablaremos con calma.');
  return (hola + gracias + queja + casa + privado + (d.firma ? '\n' + d.firma : '')).trim();
}

export function agradecimientoPlantilla(resena, config) {
  const d = datos(resena, config);
  const f = d.formal;
  const tema = temas(resena && resena.texto)[0];
  const hola = d.pila ? '¡Muchas gracias, ' + d.pila + '! ' : '¡Muchísimas gracias por tu reseña! ';
  const elogio = tema ? FRASE_ELOGIO[tema][0].toUpperCase() + FRASE_ELOGIO[tema].slice(1) + '. '
    : usted(f, 'Nos alegra mucho leerte. ', 'Nos alegra mucho leerle. ');
  const kw = d.kw.length ? 'Ponemos mucho cariño en ' + d.kw[0] + ', así que comentarios así nos hacen el día. ' : '';
  const vuelve = usted(f,
    '¡Te esperamos pronto' + (d.nombre ? ' en ' + d.nombre : '') + '!',
    '¡Le esperamos pronto' + (d.nombre ? ' en ' + d.nombre : '') + '!');
  return ((f ? hola.replace('tu reseña', 'su reseña') : hola) + elogio + kw + vuelve + (d.firma ? '\n' + d.firma : '')).trim();
}

/* ── Con IA ───────────────────────────────────────────────────────── */

export const SISTEMA_RESPUESTA = `Escribes la respuesta pública del propietario de un negocio local a una
reseña de Google. Se publica tal cual debajo de la reseña, así que
devuelve SOLO el texto de la respuesta: sin comillas, sin títulos, sin
explicaciones.

Cómo es una buena respuesta:
- Escrita para ESA reseña: nombra lo concreto que cuenta el cliente (el
  plato, la espera, la persona que le atendió bien, el precio...). Nada
  de frases que valdrían para cualquier reseña.
- Si te dan el nombre del autor y parece un nombre real, salúdale por su
  nombre de pila.
- Breve: de 2 a 4 frases. Natural, como lo escribiría el dueño.
- Si encaja de forma natural, menciona una de las palabras clave del
  negocio. Si no encaja, no la fuerces.
- En el idioma de la reseña.
- Tono "cercano": tutea. Tono "formal": de usted.
- Si te dan una firma, termina con ella en una línea aparte.

Si la reseña es buena (4 o 5 estrellas): agradece, celebra lo que le
gustó y anímale a volver.

Si es mala o regular: empatía de verdad, reconoce lo que cuenta sin
admitir culpas concretas ni dar excusas largas, no discutas ni le
contradigas, y lleva la conversación a privado con el contacto que te
den (si no hay, invítale a escribir por privado). Si la reseña incluye
insultos, datos personales o ataques, no los repitas ni los menciones:
responde con educación a la parte de la experiencia.

Nunca: inventes datos del negocio (horarios, promociones, invitaciones,
nombres de empleados), nombres a empleados aunque la reseña lo haga,
menciones denuncias a Google, ni prometas compensaciones que el dueño no
haya autorizado en sus indicaciones.`;

export function mensajeRespuesta(resena, config) {
  const d = datos(resena, config);
  const c = config || {};
  return [
    d.nombre ? 'Negocio: ' + d.nombre : '',
    (resena.negocio && resena.negocio.sector) ? 'Sector: ' + resena.negocio.sector : '',
    d.kw.length ? 'Palabras clave: ' + d.kw.join(', ') : '',
    'Tono: ' + (d.formal ? 'formal' : 'cercano'),
    d.firma ? 'Firma: ' + d.firma : '',
    d.contacto ? 'Contacto para hablar en privado: ' + d.contacto : '',
    c.notas ? 'Indicaciones del dueño: ' + String(c.notas).slice(0, 500) : '',
    '',
    resena.autor ? 'Autor: ' + resena.autor : '',
    'Estrellas: ' + (resena.estrellas == null ? 'sin dato' : resena.estrellas),
    'Reseña:\n' + (String(resena.texto || '').trim() || '(sin texto, solo estrellas)')
  ].filter((x) => x !== '').join('\n');
}

export async function redactaIA(resena, config, cliente) {
  const r = await cliente.beta.messages.create({
    model: MODELO_RESPUESTA,
    max_tokens: 4000,
    output_config: { effort: 'low' },
    betas: ['server-side-fallback-2026-07-01'],
    fallbacks: 'default',
    system: SISTEMA_RESPUESTA,
    messages: [{ role: 'user', content: mensajeRespuesta(resena, config) }]
  });
  if (r.stop_reason === 'refusal') throw new Error('la IA no ha querido responder esta reseña');
  if (r.stop_reason === 'max_tokens') throw new Error('respuesta cortada');
  const txt = (r.content || []).filter((b) => b.type === 'text').map((b) => b.text).join('').trim();
  if (txt.length < 10) throw new Error('respuesta vacía');
  return txt.slice(0, 4000);
}

/* opciones.cliente: el de Anthropic (o uno de mentira en las pruebas).
   Sin cliente, plantilla. Si la IA falla, plantilla también: una reseña
   nunca se queda sin respuesta por un fallo de red. */
export async function redacta(resena, config, opciones = {}) {
  const positiva = Number(resena && resena.estrellas) >= 4;
  const plantilla = () => (positiva ? agradecimientoPlantilla : respuestaPlantilla)(resena, config);
  if (!opciones.cliente) return { texto: plantilla(), origen: 'plantilla' };
  try {
    return { texto: await redactaIA(resena, config, opciones.cliente), origen: 'ia' };
  } catch (err) {
    console.error('redacta: ' + (err && err.message));
    return { texto: plantilla(), origen: 'plantilla' };
  }
}
