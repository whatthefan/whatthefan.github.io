/* El detector gratis: reglas fijas, sin IA y sin coste.

   Caza lo evidente: insultos, descripciones físicas, amenazas, teléfonos,
   "trabajé aquí", "no he ido pero"... No entiende el contexto, así que
   cada regla lleva su fuerza: alta cuando no hay duda posible ("la
   gorda de la barra", un teléfono), baja cuando puede ser otra cosa
   ("no hay aparcamiento" puede ser una queja del negocio o de la calle).

   Lo que encuentra se usa de dos maneras:
     · si hay algo de fuerza alta, la reseña ya es denunciable y no hace
       falta gastar una llamada a la IA;
     · si no, se le pasa a la IA como pista para que lo mire con lupa.

   Y si no hay clave de la IA, esto es todo el análisis, con la apelación
   y la respuesta sacadas de plantillas. */

import { POLITICAS } from './politicas.mjs';

/* Una palabra entera, con tildes. \b no vale: en JavaScript no sabe que
   la "é" de "imbécil" es una letra. */
const palabra = (src) => new RegExp('(?<!\\p{L})(?:' + src + ')(?!\\p{L})', 'giu');

const REGLAS = [
  // insultos que no tienen otra lectura
  { politica: 'contenido-ofensivo', fuerza: 'alta', re: palabra(
    'imb[eé]cil(?:es)?|idiotas?|gilipollas|subnormal(?:es)?|cabr[oó]n(?:es|a|as)?|' +
    'hij[oa]s? de puta|capull[oa]s?|retrasad[oa]s?|gentuza|escoria|' +
    'malnacid[oa]s?|cretin[oa]s?') },
  // palabrotas y descalificaciones que a veces van contra el sitio y no contra nadie
  { politica: 'contenido-ofensivo', fuerza: 'media', re: palabra(
    'mierdas?|put[oa]s?|joder|cojones|co[nñ]o|est[uú]pid[oa]s?|pringad[oa]s?|payas[oa]s?|' +
    'tont[oa]s? del culo|ladr[oó]n(?:es|a|as)?|mongol[oa]s?') },
  // descripción física despectiva de una persona: "la gorda de la barra"
  { politica: 'acoso', fuerza: 'alta', re: palabra(
    '(?:la|el|esa|ese|una|un|aquella|aquel) (?:gord[oa]|fe[oa]|enan[oa]|calv[oa]|foca|bizc[oa]|' +
    'cuatro ojos|vieja amargada|amargad[oa])') },
  // amenazas, también las veladas
  { politica: 'acoso', fuerza: 'alta', re: palabra(
    'ya os ver[eé]is|ya te ver[aá]s|os vais a enterar|te vas a enterar|os voy a hundir|' +
    'te voy a hundir|voy a por (?:vosotros|ti|ellos)|s[eé] d[oó]nde vives|te espero fuera|' +
    'hasta que cerr[eé]is|os vais a acordar|te vas a acordar|ojal[aá] (?:cerr[eé]is|os arruin)') },
  // datos personales: teléfono, correo, perfil de redes, matrícula
  { politica: 'informacion-personal', fuerza: 'alta',
    re: /(?<!\d)(?:\+34[\s.-]?)?[6789]\d{2}[\s.-]?\d{3}[\s.-]?\d{3}(?!\d)/g },
  { politica: 'informacion-personal', fuerza: 'alta', re: /[\w.+-]+@[\w-]+\.[\w.]+/g },
  { politica: 'informacion-personal', fuerza: 'media', re: /(?<![\w@])@[A-Za-z0-9_.]{3,30}/g },
  { politica: 'informacion-personal', fuerza: 'alta', re: /(?<![\w])\d{4}[\s-]?[BCDFGHJKLMNPRSTVWXYZ]{3}(?!\w)/g },
  // incitación al odio
  { politica: 'incitacion-al-odio', fuerza: 'alta', re: palabra(
    'sudacas?|panchit[oa]s?|negratas?|maric[oó]n(?:es)?|bolleras?|' +
    'put[oa]s? (?:extranjer|negr|chin|gitan|mor)[oa]s?') },
  // pueden ser otra cosa: "moros y cristianos" son unas fiestas
  { politica: 'incitacion-al-odio', fuerza: 'media', re: palabra('moros?(?! y cristianos)|maricas?') },
  // exempleados y competidores
  { politica: 'conflicto-de-intereses', fuerza: 'alta', re: palabra(
    '(?:trabaj[eé]|he trabajado|trabajaba|estuve trabajando|curr[eé]|curraba) (?:aqu[ií]|ah[ií]|all[ií]|en este|para (?:ellos|este|esta))|' +
    'ex ?emplead[oa]|ex ?trabajador[a]?') },
  { politica: 'conflicto-de-intereses', fuerza: 'media', re: palabra(
    'mejor (?:id|vayan|ve|vete|ir|vayas) a|(?:os|les) recomiendo (?:ir a|que vay[aá]is a) ') },
  // no fue cliente
  { politica: 'experiencia-no-real', fuerza: 'alta', re: palabra(
    'no he (?:ido|estado|entrado|probado)|nunca he (?:ido|estado|entrado)|no fui nunca|' +
    'no he comido nunca') },
  { politica: 'experiencia-no-real', fuerza: 'media', re: palabra(
    'me (?:han|ha) (?:dicho|contado)|seg[uú]n me (?:cuentan|han contado|dicen)|un amigo me dijo') },
  // quejas que no van del negocio
  { politica: 'fuera-de-tema', fuerza: 'baja', re: palabra(
    'aparcar|aparcamiento|obras (?:de|en) la calle|el ayuntamiento|tr[aá]fico|atasco|' +
    'el gobierno|los pol[ií]ticos') },
  // enlaces y publicidad
  { politica: 'spam', fuerza: 'alta', re: /(?:https?:\/\/|www\.)\S+/gi }
];

const ORDEN = { alta: 3, media: 2, baja: 1 };

/* La cita que se enseña: el trozo de frase donde está la palabra, de
   coma a coma. Sale tal cual del texto, así que siempre pasa la
   comprobación del motor. */
function trozo(texto, desde, hasta) {
  const corte = /[.,;:!?¡¿\n()]/;
  let a = desde, b = hasta;
  while (a > 0 && !corte.test(texto[a - 1]) && desde - a < 80) a--;
  while (b < texto.length && !corte.test(texto[b]) && b - hasta < 80) b++;
  return texto.slice(a, b).trim();
}

export function detecta(resena) {
  const encontradas = busca(String((resena && resena.texto) || ''), 'resena', REGLAS);
  /* Lo que cuenta el dueño ("es un exempleado") también cuenta, pero
     solo para saber quién escribe: un insulto en el contexto del dueño
     no hace denunciable la reseña. */
  const contexto = String((resena && resena.contexto) || '');
  if (contexto) {
    encontradas.push(...busca(contexto, 'dueno',
      REGLAS.filter((r) => r.politica === 'conflicto-de-intereses')));
  }
  return encontradas;
}

function busca(texto, fuente, reglas) {
  const encontradas = [];
  for (const regla of reglas) {
    regla.re.lastIndex = 0;
    for (const m of texto.matchAll(regla.re)) {
      const cita = trozo(texto, m.index, m.index + m[0].length);
      const repetida = encontradas.find((e) => e.politica === regla.politica && e.cita === cita);
      if (repetida) {
        if (ORDEN[regla.fuerza] > ORDEN[repetida.fuerza]) repetida.fuerza = regla.fuerza;
        continue;
      }
      encontradas.push({
        politica: regla.politica, fuente, cita, fuerza: regla.fuerza,
        por_que: 'contiene «' + m[0] + '»', origen: 'reglas'
      });
    }
  }
  return encontradas;
}

/* ── Plantillas para cuando no hay IA ─────────────────────────────── */

/* Para que dos respuestas seguidas no salgan idénticas: Google y los
   clientes notan enseguida una respuesta de bote. Sale siempre la misma
   para la misma reseña, eso sí, para que repetir el análisis no la
   cambie. */
function elige(lista, semilla) {
  let h = 0;
  for (const c of String(semilla)) h = (h * 31 + c.charCodeAt(0)) >>> 0;
  return lista[h % lista.length];
}

export function respuestaPlantilla(resena) {
  const n = (resena && resena.negocio) || {};
  const nombre = n.nombre || 'nuestro negocio';
  const kw = (n.palabras_clave || []).filter(Boolean);
  const claves = kw.length >= 2 ? kw[0] + ' y ' + kw[1] : (kw[0] || 'el trato a nuestros clientes');
  const contacto = n.contacto
    ? 'Escríbenos a ' + n.contacto + ' y lo hablamos con calma.'
    : 'Escríbenos por privado y lo hablamos con calma.';
  return elige([
    'Hola, gracias por contarnos tu experiencia. Sentimos de verdad que tu visita no fuera como esperabas. ' +
      'En ' + nombre + ' cuidamos cada detalle, desde ' + claves + ', y queremos entender qué pasó para mejorarlo. ' +
      contacto,
    'Gracias por tomarte el tiempo de escribirnos, y lamentamos que no te fueras contento. ' +
      'Nos importa mucho que quien viene a ' + nombre + ' por ' + claves + ' salga con ganas de volver. ' +
      contacto + ' Nos encantaría poder darte otra oportunidad.',
    'Hola, sentimos mucho que tu experiencia no estuviera a la altura. Leemos cada opinión con atención ' +
      'porque es lo que nos ayuda a seguir mejorando en ' + claves + '. ' + contacto
  ], resena && resena.texto);
}

export function apelacionPlantilla(resena, infracciones) {
  if (!infracciones.length) return '';
  const nombre = (resena.negocio && resena.negocio.nombre) || 'nuestro establecimiento';
  const normas = [...new Set(infracciones.map((i) => POLITICAS[i.politica].nombre))];
  const lista = normas.length > 1
    ? normas.slice(0, -1).join(', ') + ' y ' + normas[normas.length - 1]
    : normas[0];
  const pruebas = infracciones.map((i) => i.fuente === 'dueno'
    ? 'Además, nos consta que el autor no es un cliente sino parte interesada («' + i.cita +
      '»), lo que constituye un ' + POLITICAS[i.politica].nombre.toLowerCase() + '.'
    : 'La reseña incluye el fragmento «' + i.cita + '», que constituye un caso de ' +
      POLITICAS[i.politica].nombre.toLowerCase() + '.'
  ).join(' ');
  return [
    'En representación de ' + nombre + ', solicitamos la revisión y retirada de la reseña indicada por ' +
      'incumplir la Política de contenido prohibido y restringido de Google Maps, en concreto en lo relativo a ' +
      lista + '.',
    pruebas + ' Dicho contenido no se ajusta a los criterios que la plataforma exige a las contribuciones ' +
      'de los usuarios.',
    'Por lo expuesto, solicitamos que se aplique la citada política y se retire la reseña. Quedamos a ' +
      'disposición del equipo de Google para aportar cualquier información adicional que se precise.'
  ].join('\n\n');
}
