/* Pruebas del conector con Google, sin red: npm run prueba-reputacion

   Google, la IA y el almacén son de mentira. Lo que se prueba es lo que
   hacemos nosotros con lo que contestan. */

import test from 'node:test';
import assert from 'node:assert/strict';
import { cifra, descifra, firma, lee } from './cripto.mjs';
import * as G from './google.mjs';
import * as V from './vigia.mjs';
import { juntaFichas, mensajeGoogle } from '../api/google.js';

const SECRETO = 'una frase secreta bastante larga';

class KV {
  constructor() { this.m = new Map(); }
  async get(k) { return this.m.has(k) ? this.m.get(k) : null; }
  async put(k, v) { this.m.set(k, v); }
  async delete(k) { this.m.delete(k); }
  async list({ prefix = '' } = {}) {
    return { keys: [...this.m.keys()].filter((k) => k.startsWith(prefix)).sort().map((name) => ({ name })) };
  }
}

const FICHA = 'accounts/111/locations/222';

/* Una Google de mentira que apunta lo que le piden. */
function googleFalsa(resenas) {
  const publicadas = [];
  const pide = async (url, op = {}) => {
    const u = String(url);
    const ok = (d) => ({ ok: true, status: 200, text: async () => JSON.stringify(d) });
    if (u.startsWith('https://oauth2.googleapis.com/token')) return ok({ access_token: 'acceso-bueno' });
    if (u.includes('/reviews?')) {
      assert.equal(op.headers.Authorization, 'Bearer acceso-bueno');
      return ok({ reviews: resenas });
    }
    if (u.endsWith('/reply') && op.method === 'PUT') {
      publicadas.push({ url: u, texto: JSON.parse(op.body).comment });
      return ok({ comment: JSON.parse(op.body).comment });
    }
    if (u.startsWith('https://api.resend.com')) { publicadas.push({ correo: JSON.parse(op.body) }); return ok({}); }
    throw new Error('petición inesperada: ' + u);
  };
  return { pide, publicadas };
}

const resena = (id, estrellas, texto, extra) => ({
  reviewId: id, name: FICHA + '/reviews/' + id, starRating: ['', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE'][estrellas],
  comment: texto, createTime: new Date().toISOString(), reviewer: { displayName: 'Laura García' }, ...(extra || {})
});

async function montaCuenta(kv, config) {
  const cuenta = {
    sub: '999', email: 'dueno@bar.es', permiso: await cifra('permiso-duradero', SECRETO),
    fichas: [{ id: FICHA, nombre: 'Bar Manolo', desde: 0, config: V.limpiaConfig({ activa: true, ...config }) }]
  };
  await kv.put('gc-999', JSON.stringify(cuenta));
  return cuenta;
}

const env = (kv) => ({ ENCARGOS: kv, TOKENS_CLAVE: SECRETO, GOOGLE_CLIENT_ID: 'id', GOOGLE_CLIENT_SECRET: 'sec',
  RESEND_API_KEY: 're', CORREO_DE: 'avisos@plea5e.es' });

/* ── cifrado y sesiones ── */

test('el permiso se cifra y se descifra, y con otra frase no se abre', async () => {
  const c = await cifra('mi-permiso', SECRETO);
  assert.doesNotMatch(c, /mi-permiso/);
  assert.equal(await descifra(c, SECRETO), 'mi-permiso');
  await assert.rejects(descifra(c, SECRETO + 'x'));
});

test('una sesión tocada o caducada no vale', async () => {
  const s = await firma({ sub: '1' }, SECRETO, 60);
  assert.deepEqual(await lee(s, SECRETO), { sub: '1' });
  assert.equal(await lee(s.slice(0, -2) + 'xx', SECRETO), null);
  assert.equal(await lee(await firma({ sub: '1' }, SECRETO, -1), SECRETO), null);
  assert.equal(await lee('basura', SECRETO), null);
});

test('sin frase secreta no se cifra nada', async () => {
  await assert.rejects(cifra('x', ''), /TOKENS_CLAVE/);
});

/* ── Google ── */

test('las reseñas de Google se leen bien', async () => {
  const { pide } = googleFalsa([resena('a', 2, 'Lento'), resena('b', 5, '', { reviewReply: { comment: 'Gracias' } })]);
  const l = await G.resenas('acceso-bueno', FICHA, pide);
  assert.equal(l[0].estrellas, 2);
  assert.equal(l[0].autor, 'Laura García');
  assert.equal(l[1].respondida, true);
});

test('no se pide nada a Google con un identificador raro', async () => {
  await assert.rejects(G.resenas('x', '../../otra-cosa', async () => { throw new Error('no'); }), /ficha rara/);
  await assert.rejects(G.responde('x', 'accounts/1/locations/2', 'hola', async () => { throw new Error('no'); }), /reseña rara/);
});

test('la URL para entrar pide permiso duradero y de Business Profile', () => {
  const u = new URL(G.urlEntrada({ GOOGLE_CLIENT_ID: 'cid' }, 'https://plea5e.es/api/google/vuelta', 'est'));
  assert.equal(u.searchParams.get('access_type'), 'offline');
  assert.match(u.searchParams.get('scope'), /business\.manage/);
  assert.equal(u.searchParams.get('state'), 'est');
});

/* ── el vigilante ── */

test('las buenas se publican solas; las malas quedan pendientes y avisa', async () => {
  const kv = new KV();
  const cuenta = await montaCuenta(kv, {});
  const g = googleFalsa([resena('p1', 5, 'Las croquetas buenísimas'), resena('n1', 2, 'Tardaron una hora')]);
  const r = await V.revisaCuenta(env(kv), cuenta, { deps: { pide: g.pide } });
  assert.equal(r.publicadas, 1);
  assert.equal(r.pendientes, 1);
  const pub = g.publicadas.filter((x) => x.url);
  assert.equal(pub.length, 1);
  assert.match(pub[0].url, /reviews\/p1\/reply$/);
  assert.match(pub[0].texto, /Laura/);
  const correo = g.publicadas.find((x) => x.correo);
  assert.deepEqual(correo.correo.to, ['dueno@bar.es']);
  assert.equal(JSON.parse(await kv.get(V.claveResena('999', FICHA, 'n1'))).estado, 'pendiente');
});

test('una reseña ya vista o ya respondida no se toca dos veces', async () => {
  const kv = new KV();
  const cuenta = await montaCuenta(kv, {});
  const lista = [resena('p1', 5, 'Genial'), resena('r1', 1, 'Mal', { reviewReply: { comment: 'ya' } })];
  const g1 = googleFalsa(lista);
  await V.revisaCuenta(env(kv), cuenta, { deps: { pide: g1.pide } });
  const g2 = googleFalsa(lista);
  const r = await V.revisaCuenta(env(kv), cuenta, { deps: { pide: g2.pide } });
  assert.equal(r.publicadas, 0);
  assert.equal(g2.publicadas.filter((x) => x.url).length, 0);
});

test('con negativas en automático, las denunciables NO se publican solas', async () => {
  const kv = new KV();
  const cuenta = await montaCuenta(kv, { auto_negativas: true });
  const g = googleFalsa([resena('n1', 2, 'Tardaron una hora'), resena('n2', 1, 'El camarero, un imbécil')]);
  await V.revisaCuenta(env(kv), cuenta, { deps: { pide: g.pide } });
  const pub = g.publicadas.filter((x) => x.url).map((x) => x.url);
  assert.equal(pub.length, 1);
  assert.match(pub[0], /n1\/reply$/);
  assert.equal(JSON.parse(await kv.get(V.claveResena('999', FICHA, 'n2'))).analisis.veredicto, 'impugnable');
});

test('el presupuesto por vuelta se respeta', async () => {
  const kv = new KV();
  const cuenta = await montaCuenta(kv, {});
  const muchas = Array.from({ length: 20 }, (_, i) => resena('x' + i, 5, 'Bien'));
  const g = googleFalsa(muchas);
  const r = await V.revisaCuenta(env(kv), cuenta, { deps: { pide: g.pide }, presupuesto: { n: 3 } });
  assert.equal(r.publicadas, 3);
});

test('las reseñas de antes de conectar no se tocan', async () => {
  const kv = new KV();
  const cuenta = await montaCuenta(kv, {});
  cuenta.fichas[0].desde = Date.now();
  const g = googleFalsa([resena('viejo', 5, 'Bien', { createTime: '2020-01-01T00:00:00Z' })]);
  const r = await V.revisaCuenta(env(kv), cuenta, { deps: { pide: g.pide } });
  assert.equal(r.publicadas, 0);
});

test('si el dueño quitó el permiso, se apunta el error y no revienta', async () => {
  const kv = new KV();
  const cuenta = await montaCuenta(kv, {});
  const pide = async () => ({ ok: false, status: 400, text: async () => '{"error":"invalid_grant"}' });
  const r = await V.revisaCuenta(env(kv), cuenta, { deps: { pide } });
  assert.match(r.errores[0], /Vuelve a conectar/);
  assert.match(JSON.parse(await kv.get('gc-999')).error, /invalid_grant/);
});

test('la vuelta completa solo mira cuentas con algo activo', async () => {
  const kv = new KV();
  await montaCuenta(kv, {});
  await kv.put('gc-apagada', JSON.stringify({ sub: 'apagada', fichas: [{ id: FICHA, config: { activa: false } }] }));
  const g = googleFalsa([resena('p1', 4, 'Muy bien')]);
  const r = await V.vigila(env(kv), { pide: g.pide });
  assert.equal(r.cuentas, 1);
  assert.equal(r.publicadas, 1);
});

/* ── configuración y fichas ── */

test('la configuración que llega del navegador se limpia', () => {
  const c = V.limpiaConfig({ activa: 'sí', tono: 'gritón', firma: 'x'.repeat(500), palabras_clave: 'a, b,,c' });
  assert.equal(c.activa, false);
  assert.equal(c.tono, 'cercano');
  assert.equal(c.firma.length, 80);
  assert.deepEqual(c.palabras_clave, ['a', 'b', 'c']);
  assert.equal(c.auto_negativas, false);
});

test('al reconectar se conserva la configuración, y la ficha elegida se activa', () => {
  const antes = [{ id: 'accounts/1/locations/1', config: V.limpiaConfig({ activa: true, firma: 'Manolo' }), desde: 5 }];
  const nuevas = [{ id: 'accounts/1/locations/1', placeId: 'A' }, { id: 'accounts/1/locations/2', placeId: 'B' }];
  const j = juntaFichas(antes, nuevas, 'B');
  assert.equal(j[0].config.firma, 'Manolo');
  assert.equal(j[0].desde, 5);
  assert.equal(j[1].config.activa, true);
});

test('el error de "API no aprobada" se explica en cristiano', () => {
  const e = new Error('Google Business Profile (cuentas): Quota exceeded for quota metric');
  e.status = 429;
  assert.match(mensajeGoogle(e), /todavía no ha activado/);
});
