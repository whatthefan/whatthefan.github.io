/* El conector con Google: lo que usa /analiza/ficha/.

   La sirve el Worker de src/index.js en cuatro direcciones:

     /api/negocios        buscar un negocio en Google Maps (público, con tope)
     /api/google/entra    "Conectar con Google": manda al dueño a Google
     /api/google/vuelta   a donde vuelve de Google con el permiso
     /api/ficha           el panel del dueño: sus fichas, su config, sus
                          reseñas pendientes, publicar, desconectar...

   Lo que necesita en Cloudflare (Settings → Variables), y qué pasa si
   falta:

     GOOGLE_MAPS_KEY       la búsqueda de negocios. Sin ella, no se busca.
     GOOGLE_CLIENT_ID      "Conectar con Google". Sin ellas, el botón
     GOOGLE_CLIENT_SECRET  avisa de que aún no está disponible.
     TOKENS_CLAVE          una frase secreta larga: cifra los permisos y
                           firma las sesiones. Imprescindible para conectar.
     ANTHROPIC_API_KEY     respuestas escritas por la IA. Sin ella, con
                           plantillas.
     RESEND_API_KEY, CORREO_DE   los avisos al dueño por correo. */

import * as G from '../lib/google.mjs';
import { cifra, descifra, firma, lee, aleatorio } from '../lib/cripto.mjs';
import { permite } from '../lib/limite.mjs';
import * as V from '../lib/vigia.mjs';

const JSON_CAB = { 'Content-Type': 'application/json; charset=utf-8' };
const SESION = 'plea5e_ficha';
const ESTADO = 'plea5e_estado';
const DIAS_SESION = 30;

const responde = (obj, estado, extra) =>
  new Response(JSON.stringify(obj), { status: estado || 200, headers: { ...JSON_CAB, ...(extra || {}) } });

function galleta(request, nombre) {
  const c = request.headers.get('cookie') || '';
  for (const trozo of c.split(';')) {
    const [k, ...v] = trozo.trim().split('=');
    if (k === nombre) return decodeURIComponent(v.join('='));
  }
  return '';
}
const ponGalleta = (nombre, valor, segundos) =>
  nombre + '=' + encodeURIComponent(valor) + '; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=' + segundos;

/* La dirección de vuelta tiene que ser EXACTAMENTE la que se dio de alta
   en Google Cloud. Se saca de la petición para que funcione igual en
   plea5e.es que en una prueba local. */
const vuelta = (request) => new URL(request.url).origin + '/api/google/vuelta';

export function configurado(env) {
  return {
    maps: Boolean(String(env.GOOGLE_MAPS_KEY || '').trim()),
    google: Boolean(env.GOOGLE_CLIENT_ID && env.GOOGLE_CLIENT_SECRET && String(env.TOKENS_CLAVE || '').length >= 16),
    ia: Boolean(String(env.ANTHROPIC_API_KEY || '').trim()),
    correo: Boolean(env.RESEND_API_KEY && env.CORREO_DE)
  };
}

/* ── /api/negocios ─────────────────────────────────────────────────── */

export async function negocios({ request, env }) {
  const clave = String(env.GOOGLE_MAPS_KEY || '').trim();
  if (!clave) return responde({ error: 'La búsqueda en Google Maps aún no está activada.' }, 503);
  const url = new URL(request.url);
  const q = (url.searchParams.get('q') || '').trim();
  const id = (url.searchParams.get('id') || '').trim();
  if (!q && !id) return responde({ error: 'Escribe el nombre de tu negocio.' }, 400);
  const tope = Number(env.MAPS_TOPE_DIA) || 300;
  if (!(await permite(env, request, 'maps', 40, tope))) {
    return responde({ error: 'Has hecho muchas búsquedas hoy. Vuelve a probar mañana.' }, 429);
  }
  try {
    if (id) return responde({ negocio: await G.fichaNegocio(id, clave) });
    return responde({ negocios: await G.buscaNegocios(q, clave) });
  } catch (err) {
    console.error('maps: ' + err.message);
    return responde({ error: 'Google Maps no ha contestado. Prueba otra vez en un momento.' }, 502);
  }
}

/* ── /api/google/entra y /api/google/vuelta ───────────────────────── */

export async function entra({ request, env }) {
  if (!configurado(env).google) {
    return new Response(null, { status: 302, headers: { Location: '/analiza/ficha/?error=no-disponible' } });
  }
  const url = new URL(request.url);
  /* Si ha elegido su negocio en el buscador, se recuerda para marcar esa
     ficha al volver. */
  const lugar = (url.searchParams.get('lugar') || '').slice(0, 300);
  const estado = aleatorio(18);
  const sello = await firma({ e: estado, lugar }, env.TOKENS_CLAVE, 600);
  return new Response(null, {
    status: 302,
    headers: { Location: G.urlEntrada(env, vuelta(request), estado), 'Set-Cookie': ponGalleta(ESTADO, sello, 600) }
  });
}

export async function vuelve({ request, env }) {
  const url = new URL(request.url);
  const va = (que) => new Response(null, { status: 302, headers: {
    Location: '/analiza/ficha/' + (que ? '?error=' + que : '?conectado=1'),
    'Set-Cookie': ponGalleta(ESTADO, '', 0)
  } });
  if (url.searchParams.get('error')) return va('cancelado');
  /* El estado que se mandó a Google tiene que volver igual: si no, esta
     vuelta no la ha empezado este navegador (o alguien intenta colar un
     permiso ajeno). */
  const guardado = await lee(galleta(request, ESTADO), env.TOKENS_CLAVE);
  if (!guardado || guardado.e !== url.searchParams.get('state')) return va('caducado');

  let tokens, yo;
  try {
    tokens = await G.canjea(url.searchParams.get('code') || '', env, vuelta(request));
    yo = await G.quienSoy(tokens.access_token);
  } catch (err) {
    console.error('vuelta: ' + err.message);
    return va('google');
  }
  if (!String(tokens.scope || '').includes('business.manage')) return va('sin-permiso');

  const k = V.claveCuenta(yo.sub);
  const antes = JSON.parse((await env.ENCARGOS.get(k)) || 'null');
  /* Google solo da el permiso duradero la primera vez (o con prompt=consent,
     que se pide siempre). Si no viene, se conserva el que había. */
  const permiso = tokens.refresh_token ? await cifra(tokens.refresh_token, env.TOKENS_CLAVE) : (antes && antes.permiso);
  if (!permiso) return va('sin-permiso');

  const cuenta = {
    ...(antes || {}),
    sub: yo.sub, email: yo.email || '', nombre: yo.name || '', permiso,
    creada: (antes && antes.creada) || Date.now(), conectada: Date.now(), error: '',
    lugarElegido: guardado.lugar || (antes && antes.lugarElegido) || '',
    fichas: (antes && antes.fichas) || []
  };
  /* Las fichas se piden ya, para que el dueño las vea al volver. Si la
     API aún no está aprobada para PLEA5E, falla aquí: se guarda el error
     y el panel lo explica. */
  try {
    cuenta.fichas = juntaFichas(cuenta.fichas, await G.misFichas(tokens.access_token), cuenta.lugarElegido);
  } catch (err) {
    cuenta.error = mensajeGoogle(err);
  }
  await env.ENCARGOS.put(k, JSON.stringify(cuenta));
  const sesion = await firma({ sub: yo.sub }, env.TOKENS_CLAVE, DIAS_SESION * 86400);
  const r = va('');
  r.headers.append('Set-Cookie', ponGalleta(SESION, sesion, DIAS_SESION * 86400));
  return r;
}

/* Las fichas que devuelve Google, conservando la configuración de las
   que ya estaban. La que eligió en el buscador se activa de entrada. */
export function juntaFichas(antes, nuevas, lugarElegido) {
  const porId = new Map((antes || []).map((f) => [f.id, f]));
  return nuevas.map((f) => {
    const vieja = porId.get(f.id);
    const elegida = lugarElegido && f.placeId === lugarElegido;
    return {
      ...f,
      config: vieja ? vieja.config : V.limpiaConfig({ activa: Boolean(elegida) }),
      desde: (vieja && vieja.desde) || Date.now() - V.DIAS_ATRAS * 86400000,
      ultima: vieja ? vieja.ultima : 0,
      error: vieja ? vieja.error : ''
    };
  });
}

/* Lo que dice Google, en cristiano. */
export function mensajeGoogle(err) {
  const m = String((err && err.message) || '');
  if (err && (err.status === 403 || err.status === 429) && /quota|has not been used|disabled|not been enabled|PERMISSION_DENIED/i.test(m)) {
    return 'Google todavía no ha activado la conexión con Business Profile para PLEA5E. En cuanto la apruebe, tus fichas aparecerán aquí solas.';
  }
  if (err && err.status === 401) return 'Google ha cerrado la conexión. Vuelve a conectar.';
  return 'Google ha dado un error: ' + m;
}

/* ── /api/ficha ────────────────────────────────────────────────────── */

async function sesion(request, env) {
  if (String(env.TOKENS_CLAVE || '').length < 16) return null;
  const d = await lee(galleta(request, SESION), env.TOKENS_CLAVE);
  if (!d || !d.sub) return null;
  const t = await env.ENCARGOS.get(V.claveCuenta(d.sub));
  return t ? JSON.parse(t) : null;
}

async function registros(env, sub) {
  const { keys } = await env.ENCARGOS.list({ prefix: 'gr-' + sub + '-', limit: 1000 });
  const lista = [];
  for (const k of keys.slice(-300)) {
    const t = await env.ENCARGOS.get(k.name);
    if (t) { try { lista.push({ ...JSON.parse(t), clave: k.name }); } catch (e) { /* uno roto no tumba la lista */ } }
  }
  return lista.sort((a, b) => Date.parse(b.cuando || 0) - Date.parse(a.cuando || 0) || (b.visto || 0) - (a.visto || 0)).slice(0, 150);
}

/* Lo que ve el navegador de su cuenta: nunca el permiso, ni cifrado. */
const publica = (c) => ({
  email: c.email, nombre: c.nombre, error: c.error || '', ultima: c.ultima || 0,
  fichas: (c.fichas || []).map((f) => ({ id: f.id, nombre: f.nombre, direccion: f.direccion, maps: f.maps,
    escribir: f.escribir || (f.placeId ? 'https://search.google.com/local/writereview?placeid=' + f.placeId : ''),
    config: f.config, ultima: f.ultima || 0, error: f.error || '' }))
});

async function acceso(env, cuenta) {
  return G.renueva(await descifra(cuenta.permiso, env.TOKENS_CLAVE), env);
}

export async function ficha({ request, env }) {
  if (!env.ENCARGOS) return responde({ error: 'El almacén no está conectado.' }, 500);
  const cfg = configurado(env);
  const cuenta = await sesion(request, env);
  if (request.method === 'GET') {
    if (!cuenta) return responde({ conectado: false, configurado: cfg });
    return responde({ conectado: true, configurado: cfg, cuenta: publica(cuenta), resenas: await registros(env, cuenta.sub) });
  }
  if (request.method !== 'POST') return responde({ error: 'método' }, 405);
  if (!cuenta) return responde({ error: 'Tu sesión ha caducado. Vuelve a conectar con Google.' }, 401);

  let d;
  try { d = await request.json(); } catch (e) { d = {}; }
  const k = V.claveCuenta(cuenta.sub);
  const guarda = () => env.ENCARGOS.put(k, JSON.stringify(cuenta));
  const suFicha = (id) => (cuenta.fichas || []).find((f) => f.id === id);
  /* Solo se tocan reseñas de SU cuenta: la clave lleva su identificador. */
  const suResena = (clave) => typeof clave === 'string' && clave.startsWith('gr-' + cuenta.sub + '-');

  try {
    switch (d.accion) {
      case 'config': {
        const f = suFicha(d.ficha);
        if (!f) return responde({ error: 'Esa ficha no es tuya.' }, 404);
        const estabaApagada = !(f.config && f.config.activa);
        f.config = V.limpiaConfig(d.config, f.config);
        /* Al activarla, se revisa ya: el dueño ve resultados al momento
           en vez de esperar a la siguiente vuelta del vigilante. */
        let revision = null;
        await guarda();
        if (estabaApagada && f.config.activa) {
          revision = await V.revisaCuenta(env, cuenta, { soloFicha: f.id, presupuesto: { n: 8 } });
        }
        return responde({ ok: true, revision, cuenta: publica(cuenta) });
      }
      case 'revisa': {
        if (!suFicha(d.ficha)) return responde({ error: 'Esa ficha no es tuya.' }, 404);
        const revision = await V.revisaCuenta(env, cuenta, { soloFicha: d.ficha, presupuesto: { n: 8 } });
        return responde({ ok: true, revision, resenas: await registros(env, cuenta.sub) });
      }
      case 'publica': {
        if (!suResena(d.clave)) return responde({ error: 'Esa reseña no es tuya.' }, 404);
        const r = JSON.parse((await env.ENCARGOS.get(d.clave)) || 'null');
        if (!r) return responde({ error: 'No está.' }, 404);
        const texto = String(d.texto || r.respuesta || '').trim().slice(0, 4000);
        if (texto.length < 2) return responde({ error: 'La respuesta está vacía.' }, 400);
        await G.responde(await acceso(env, cuenta), r.nombre, texto);
        Object.assign(r, { respuesta: texto, estado: 'publicada', publicada: Date.now(), error: '' });
        await env.ENCARGOS.put(d.clave, JSON.stringify(r));
        return responde({ ok: true, resena: { ...r, clave: d.clave } });
      }
      case 'ignora': {
        if (!suResena(d.clave)) return responde({ error: 'Esa reseña no es tuya.' }, 404);
        const r = JSON.parse((await env.ENCARGOS.get(d.clave)) || 'null');
        if (!r) return responde({ error: 'No está.' }, 404);
        r.estado = 'ignorada';
        await env.ENCARGOS.put(d.clave, JSON.stringify(r));
        return responde({ ok: true });
      }
      case 'recarga': {
        try {
          cuenta.fichas = juntaFichas(cuenta.fichas, await G.misFichas(await acceso(env, cuenta)), cuenta.lugarElegido);
          cuenta.error = '';
        } catch (err) {
          cuenta.error = mensajeGoogle(err);
        }
        await guarda();
        return responde({ ok: true, cuenta: publica(cuenta) });
      }
      case 'salir':
        return responde({ ok: true }, 200, { 'Set-Cookie': ponGalleta(SESION, '', 0) });
      case 'desconecta': {
        /* Se borra todo y se le devuelve el permiso a Google. */
        try { await G.revoca(await descifra(cuenta.permiso, env.TOKENS_CLAVE)); } catch (e) { /* sigue */ }
        const { keys } = await env.ENCARGOS.list({ prefix: 'gr-' + cuenta.sub + '-', limit: 1000 });
        for (const x of keys) await env.ENCARGOS.delete(x.name);
        await env.ENCARGOS.delete(k);
        return responde({ ok: true }, 200, { 'Set-Cookie': ponGalleta(SESION, '', 0) });
      }
      default:
        return responde({ error: 'acción desconocida' }, 400);
    }
  } catch (err) {
    console.error('ficha: ' + err.message);
    return responde({ error: mensajeGoogle(err) }, 502);
  }
}
