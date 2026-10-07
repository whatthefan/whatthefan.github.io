/* Pruebas sin red ni clave: npm run prueba-reputacion

   Comprueban la parte que no depende de la IA, que es la que decide lo
   que se entrega al cliente. A la IA se la sustituye por un cliente de
   mentira que contesta lo que le digamos. */

import test from 'node:test';
import assert from 'node:assert/strict';
import { depura, normaliza, montaMensaje, analiza } from './motor.mjs';
import { detecta, apelacionPlantilla } from './reglas.mjs';
import { redacta, temas, nombrePila, respuestaPlantilla, agradecimientoPlantilla, mensajeRespuesta } from './redacta.mjs';

const resena = {
  texto: 'Tardaron 40 minutos y el camarero, un imbécil, ni se disculpó.',
  contexto: 'Es un exempleado al que despedimos en marzo.'
};

const inf = (o) => ({ politica: 'contenido-ofensivo', fuente: 'resena',
  cita: 'un imbécil', por_que: 'insulto', fuerza: 'alta', ...o });

test('una cita que está en la reseña sobrevive', () => {
  const v = depura({ infracciones: [inf()], apelacion: 'Solicitamos...', respuesta: 'Gracias', resumen: 'x' }, resena);
  assert.equal(v.veredicto, 'impugnable');
  assert.equal(v.fuerza, 'alta');
  assert.equal(v.infracciones.length, 1);
  assert.equal(v.apelacion, 'Solicitamos...');
});

test('una cita inventada se descarta y se lleva la apelación', () => {
  const v = depura({ infracciones: [inf({ cita: 'es un ladrón' })], apelacion: 'Solicitamos...', respuesta: 'Gracias', resumen: 'x' }, resena);
  assert.equal(v.veredicto, 'no-impugnable');
  assert.equal(v.apelacion, '');
  assert.equal(v.descartadas[0].motivo, 'la cita no está en el texto');
  assert.equal(v.respuesta, 'Gracias');
});

test('tildes, mayúsculas y espacios no tumban una cita buena', () => {
  const v = depura({ infracciones: [inf({ cita: '  UN   imbecil ' })], apelacion: 'a', respuesta: 'b', resumen: 'c' }, resena);
  assert.equal(v.veredicto, 'impugnable');
});

test('la cita del dueño se busca en su contexto, no en la reseña', () => {
  const bien = inf({ politica: 'conflicto-de-intereses', fuente: 'dueno', cita: 'exempleado al que despedimos' });
  const mal = inf({ politica: 'conflicto-de-intereses', fuente: 'resena', cita: 'exempleado al que despedimos' });
  const v = depura({ infracciones: [bien, mal], apelacion: 'a', respuesta: 'b', resumen: 'c' }, resena);
  assert.equal(v.infracciones.length, 1);
  assert.equal(v.descartadas.length, 1);
});

test('sin contexto del dueño, nada puede venir de él', () => {
  const v = depura({ infracciones: [inf({ fuente: 'dueno' })], apelacion: 'a', respuesta: 'b', resumen: 'c' },
    { texto: resena.texto });
  assert.equal(v.veredicto, 'no-impugnable');
});

test('una norma que no existe se descarta', () => {
  const v = depura({ infracciones: [inf({ politica: 'me-cae-mal' })], apelacion: 'a', respuesta: 'b', resumen: 'c' }, resena);
  assert.equal(v.veredicto, 'no-impugnable');
});

test('la fuerza es la de la mejor infracción', () => {
  const v = depura({ infracciones: [inf({ fuerza: 'baja', cita: 'tardaron 40 minutos', politica: 'spam' }), inf({ fuerza: 'media' })],
    apelacion: 'a', respuesta: 'b', resumen: 'c' }, resena);
  assert.equal(v.fuerza, 'media');
  assert.equal(v.infracciones[0].fuerza, 'media');
});

test('normaliza unifica comillas', () => {
  assert.equal(normaliza('“Hola”  ‘tú’'), '"hola" \'tu\'');
});

test('el mensaje no lleva líneas vacías de datos que faltan', () => {
  const m = montaMensaje({ texto: 'mal', negocio: { nombre: 'Bar' } });
  assert.match(m, /Negocio: Bar/);
  assert.doesNotMatch(m, /Ciudad/);
  assert.doesNotMatch(m, /Contexto/);
});

test('analiza pasa por la comprobación aunque la IA diga otra cosa', async () => {
  const cliente = { beta: { messages: { create: async (p) => {
    assert.equal(p.output_config.format.type, 'json_schema');
    return { stop_reason: 'end_turn', content: [{ type: 'text', text: JSON.stringify({
      infracciones: [inf({ cita: 'esto no lo pone' })], apelacion: 'a', respuesta: 'b', resumen: 'c' }) }] };
  } } } };
  const v = await analiza({ texto: 'Tardaron 40 minutos.' }, { cliente, modo: 'ia' });
  assert.equal(v.veredicto, 'no-impugnable');
  assert.equal(v.apelacion, '');
});

test('una negativa de la IA se dice, no se disfraza', async () => {
  const cliente = { beta: { messages: { create: async () => ({ stop_reason: 'refusal', stop_details: { category: null }, content: [] }) } } };
  await assert.rejects(analiza(resena, { cliente, modo: 'ia' }), /no ha querido/);
});

test('una reseña sin texto no gasta llamada', async () => {
  await assert.rejects(analiza({ texto: '  ' }, { cliente: {} }), /sin texto|no tiene texto/);
});

/* ── El detector gratis y el reparto entre reglas e IA ── */

const nunca = { beta: { messages: { create: async () => { throw new Error('no debía llamar a la IA'); } } } };

test('lo evidente no gasta llamada', async () => {
  const v = await analiza(resena, { cliente: nunca });
  assert.equal(v.origen, 'reglas');
  assert.equal(v.veredicto, 'impugnable');
  assert.match(v.apelacion, /un imbécil/);
  assert.ok(v.respuesta.length > 40);
});

test('en modo gratis nunca se llama a la IA', async () => {
  const v = await analiza({ texto: 'La comida, regular.' }, { cliente: nunca, modo: 'gratis' });
  assert.equal(v.origen, 'reglas');
  assert.equal(v.veredicto, 'no-impugnable');
  assert.equal(v.apelacion, '');
});

test('lo dudoso va a la IA con las pistas de las reglas', async () => {
  let mensaje = '';
  const cliente = { beta: { messages: { create: async (p) => {
    mensaje += p.messages[0].content;
    return { stop_reason: 'end_turn', content: [{ type: 'text', text: JSON.stringify({
      infracciones: [], apelacion: '', respuesta: 'Gracias', resumen: 'nada' }) }] };
  } } } };
  const v = await analiza({ texto: 'Unos moros nos atendieron fatal.' }, { cliente });
  assert.match(mensaje, /incitacion-al-odio: «/);
  assert.equal(v.origen, 'ia');
  /* las reglas lo marcaron (media) y la IA no: se queda la pista, que
     pasa la comprobación porque la cita es literal. La decisión final de
     denunciar es del dueño, que ve la fuerza. */
  assert.equal(v.fuerza, 'media');
});

test('si la IA solo deja infracciones de las reglas, la apelación sale de la plantilla', async () => {
  const cliente = { beta: { messages: { create: async () => ({ stop_reason: 'end_turn', content: [{ type: 'text',
    text: JSON.stringify({ infracciones: [inf({ cita: 'inventada' })], apelacion: 'Escrito con cita falsa', respuesta: 'Gracias', resumen: 'x' }) }] }) } } };
  const v = await analiza({ texto: 'Os recomiendo ir a otro sitio, mejor id a Casa Pepe.' }, { cliente });
  assert.equal(v.veredicto, 'impugnable');
  assert.doesNotMatch(v.apelacion, /cita falsa/);
  assert.match(v.apelacion, /Casa Pepe/);
});

test('el detector caza lo que debe', () => {
  const casos = {
    'La gorda de la barra ni nos miró': 'acoso',
    'Llamad al 612 345 678 y veréis': 'informacion-personal',
    'Ya os veréis': 'acoso',
    'Trabajé aquí y lo sé': 'conflicto-de-intereses',
    'No he ido nunca pero dicen': 'experiencia-no-real',
    'Unos gilipollas': 'contenido-ofensivo'
  };
  for (const [texto, politica] of Object.entries(casos)) {
    assert.ok(detecta({ texto }).some((p) => p.politica === politica), texto);
  }
});

test('el detector no salta con una crítica dura sin insultos', () => {
  assert.deepEqual(detecta({ texto: 'La peor paella de mi vida, carísima. Nos atendió Laura y tardó.' }), []);
  assert.deepEqual(detecta({ texto: 'El cerdo estaba seco y fuimos en coche.' }), []);
});

test('la cita del detector es un trozo literal del texto', () => {
  const texto = 'Todo bien, pero el camarero, un imbécil, ni se disculpó.';
  for (const p of detecta({ texto })) assert.ok(texto.includes(p.cita));
});

test('el contexto del dueño solo sirve para saber quién escribe', () => {
  const p = detecta({ texto: 'Mal servicio.', contexto: 'Es un exempleado, un imbécil.' });
  assert.equal(p.length, 1);
  assert.equal(p[0].fuente, 'dueno');
});

test('sin infracciones no hay apelación de plantilla', () => {
  assert.equal(apelacionPlantilla({ texto: 'x' }, []), '');
});

test('sin IA, lo dudoso queda para revisar y no se da por denunciable', async () => {
  const v = await analiza({ texto: 'Imposible aparcar en toda la calle.' }, { modo: 'gratis' });
  assert.equal(v.veredicto, 'revisar');
});

test('las fiestas de moros y cristianos no son odio', () => {
  assert.deepEqual(detecta({ texto: 'Después del desfile de moros y cristianos.' }), []);
});

test('las de 4 y 5 estrellas se agradecen sin buscar nada ni gastar', async () => {
  const v = await analiza({ texto: 'Todo genial, el camarero un crack', estrellas: 5,
    negocio: { nombre: 'Bar Manolo', palabras_clave: ['tapas caseras'] } }, { cliente: nunca });
  assert.equal(v.tipo, 'positiva');
  assert.equal(v.apelacion, '');
  assert.match(v.respuesta, /gracias/i);
});

/* ── El redactor de respuestas ── */

const neg = { texto: 'Tardamos una hora en comer y las croquetas frías.', estrellas: 2, autor: 'Laura García',
  negocio: { nombre: 'Bar Manolo', palabras_clave: ['tapas caseras'] } };

test('la plantilla nombra lo que cuenta la reseña y saluda por el nombre', () => {
  const t = respuestaPlantilla(neg, { contacto: 'hola@bar.es', firma: 'Manolo' });
  assert.match(t, /Laura/);
  assert.match(t, /espera/);
  assert.match(t, /hola@bar\.es/);
  assert.match(t, /\nManolo$/);
});

test('tono formal: de usted', () => {
  const t = respuestaPlantilla({ ...neg, autor: '' }, { tono: 'formal' });
  assert.match(t, /su experiencia/);
  assert.doesNotMatch(t, /tu experiencia/);
});

test('el agradecimiento celebra lo que le gustó', () => {
  const t = agradecimientoPlantilla({ texto: 'La comida espectacular', estrellas: 5, autor: 'Pepe' }, {});
  assert.match(t, /Pepe/);
  assert.match(t, /comida/);
});

test('solo se saluda por el nombre si parece un nombre', () => {
  assert.equal(nombrePila('Laura G.'), 'Laura');
  assert.equal(nombrePila('usuario123'), '');
  assert.equal(nombrePila('XXL'), '');
});

test('detecta los temas', () => {
  assert.deepEqual(temas('carísimo y el camarero borde'), ['precio', 'trato']);
});

test('la IA recibe la configuración del negocio', () => {
  const m = mensajeRespuesta(neg, { tono: 'formal', firma: 'Manolo', notas: 'no ofrezcas invitaciones' });
  assert.match(m, /Tono: formal/);
  assert.match(m, /Firma: Manolo/);
  assert.match(m, /no ofrezcas invitaciones/);
  assert.match(m, /Autor: Laura García/);
});

test('si la IA falla, plantilla: ninguna reseña se queda sin respuesta', async () => {
  const r = await redacta(neg, {}, { cliente: nunca });
  assert.equal(r.origen, 'plantilla');
  assert.ok(r.texto.length > 30);
});

test('con IA, la respuesta es la suya', async () => {
  const cliente = { beta: { messages: { create: async () => ({ stop_reason: 'end_turn',
    content: [{ type: 'text', text: 'Hola Laura, sentimos la espera de las croquetas.' }] }) } } };
  const v = await analiza(neg, { cliente, modo: 'gratis', redactar: 'ia' });
  assert.equal(v.respuesta_origen, 'ia');
  assert.match(v.respuesta, /croquetas/);
});

test('una reseña de solo estrellas se responde sin buscar nada', async () => {
  const v = await analiza({ texto: '', estrellas: 1 }, { modo: 'gratis' });
  assert.equal(v.veredicto, 'no-impugnable');
  assert.ok(v.respuesta.length > 20);
});
