/* Pruebas sin red ni clave: npm run prueba-reputacion

   Comprueban la parte que no depende de la IA, que es la que decide lo
   que se entrega al cliente. A la IA se la sustituye por un cliente de
   mentira que contesta lo que le digamos. */

import test from 'node:test';
import assert from 'node:assert/strict';
import { depura, normaliza, montaMensaje, analiza } from './motor.mjs';

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
  const v = await analiza(resena, { cliente });
  assert.equal(v.veredicto, 'no-impugnable');
});

test('una negativa de la IA se dice, no se disfraza', async () => {
  const cliente = { beta: { messages: { create: async () => ({ stop_reason: 'refusal', stop_details: { category: null }, content: [] }) } } };
  await assert.rejects(analiza(resena, { cliente }), /no ha querido/);
});

test('una reseña sin texto no gasta llamada', async () => {
  await assert.rejects(analiza({ texto: '  ' }, { cliente: {} }), /sin texto|no tiene texto/);
});
