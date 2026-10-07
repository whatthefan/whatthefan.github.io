/* Todo lo que se le pide a Google, en un sitio.

   Dos servicios distintos, con permisos distintos:

   · Google Maps (Places API). Para BUSCAR un negocio y ver su nota y sus
     últimas reseñas. Lo puede usar cualquiera, sin conectar nada. Va con
     una clave de PLEA5E: GOOGLE_MAPS_KEY.

   · Google Business Profile. Para LEER TODAS las reseñas de una ficha y
     RESPONDERLAS en Google. Solo con permiso del dueño, que lo da
     entrando con su cuenta de Google ("Conectar con Google"). Va con
     GOOGLE_CLIENT_ID y GOOGLE_CLIENT_SECRET, y Google tiene que haber
     aprobado el acceso a esta API para PLEA5E.

   Cada función recibe `pide` (el fetch) para poder probarlas sin red. */

const ESTRELLAS = { ONE: 1, TWO: 2, THREE: 3, FOUR: 4, FIVE: 5 };

async function json(r, que) {
  const t = await r.text();
  let d = {};
  try { d = t ? JSON.parse(t) : {}; } catch (e) { d = { crudo: t.slice(0, 300) }; }
  if (!r.ok) {
    const msg = (d.error && (d.error.message || d.error_description || d.error)) || d.error_description || ('HTTP ' + r.status);
    const err = new Error(que + ': ' + (typeof msg === 'string' ? msg : JSON.stringify(msg)));
    err.status = r.status;
    throw err;
  }
  return d;
}

/* ── Google Maps: buscar un negocio ────────────────────────────────── */

const CAMPOS_BUSCA = 'places.id,places.displayName,places.formattedAddress,places.rating,' +
  'places.userRatingCount,places.googleMapsUri,places.primaryTypeDisplayName';
const CAMPOS_FICHA = 'id,displayName,formattedAddress,rating,userRatingCount,googleMapsUri,' +
  'primaryTypeDisplayName,websiteUri,nationalPhoneNumber,reviews';

const negocio = (p) => ({
  id: p.id,
  nombre: (p.displayName && p.displayName.text) || '',
  direccion: p.formattedAddress || '',
  tipo: (p.primaryTypeDisplayName && p.primaryTypeDisplayName.text) || '',
  nota: p.rating || null,
  total: p.userRatingCount || 0,
  maps: p.googleMapsUri || '',
  /* el enlace directo a "escribir una reseña": el que llevan las placas */
  escribir: p.id ? 'https://search.google.com/local/writereview?placeid=' + encodeURIComponent(p.id) : ''
});

export async function buscaNegocios(texto, clave, pide = fetch) {
  const r = await pide('https://places.googleapis.com/v1/places:searchText', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Goog-Api-Key': clave, 'X-Goog-FieldMask': CAMPOS_BUSCA },
    body: JSON.stringify({ textQuery: String(texto).slice(0, 120), languageCode: 'es', regionCode: 'ES', pageSize: 6 })
  });
  const d = await json(r, 'Google Maps');
  return (d.places || []).map(negocio);
}

export async function fichaNegocio(id, clave, pide = fetch) {
  if (!/^[\w-]{10,300}$/.test(String(id))) throw new Error('identificador de negocio raro');
  const r = await pide('https://places.googleapis.com/v1/places/' + encodeURIComponent(id) + '?languageCode=es', {
    headers: { 'X-Goog-Api-Key': clave, 'X-Goog-FieldMask': CAMPOS_FICHA }
  });
  const p = await json(r, 'Google Maps');
  return {
    ...negocio(p),
    web: p.websiteUri || '',
    telefono: p.nationalPhoneNumber || '',
    /* Google da como mucho 5, las que considera más relevantes. Para
       verlas todas hace falta conectar la ficha. */
    resenas: (p.reviews || []).map((v) => ({
      autor: (v.authorAttribution && v.authorAttribution.displayName) || '',
      estrellas: v.rating || null,
      texto: (v.originalText && v.originalText.text) || (v.text && v.text.text) || '',
      cuando: v.relativePublishTimeDescription || '',
      denunciar: v.flagContentUri || ''
    }))
  };
}

/* ── Entrar con Google (OAuth) ─────────────────────────────────────── */

export const PERMISOS = 'openid email profile https://www.googleapis.com/auth/business.manage';

export function urlEntrada(env, vuelta, estado) {
  const q = new URLSearchParams({
    client_id: env.GOOGLE_CLIENT_ID,
    redirect_uri: vuelta,
    response_type: 'code',
    scope: PERMISOS,
    /* offline + consent: sin esto Google no da el permiso duradero, y a
       la hora la conexión se cae sola */
    access_type: 'offline',
    prompt: 'consent',
    include_granted_scopes: 'true',
    state: estado
  });
  return 'https://accounts.google.com/o/oauth2/v2/auth?' + q;
}

export async function canjea(codigo, env, vuelta, pide = fetch) {
  const r = await pide('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      code: codigo, client_id: env.GOOGLE_CLIENT_ID, client_secret: env.GOOGLE_CLIENT_SECRET,
      redirect_uri: vuelta, grant_type: 'authorization_code'
    })
  });
  return json(r, 'Google (entrar)');
}

export async function renueva(permiso, env, pide = fetch) {
  const r = await pide('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      refresh_token: permiso, client_id: env.GOOGLE_CLIENT_ID, client_secret: env.GOOGLE_CLIENT_SECRET,
      grant_type: 'refresh_token'
    })
  });
  const d = await json(r, 'Google (renovar permiso)');
  return d.access_token;
}

export async function revoca(permiso, pide = fetch) {
  try {
    await pide('https://oauth2.googleapis.com/revoke', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ token: permiso })
    });
  } catch (e) { /* si falla, el dueño puede quitarlo desde su cuenta de Google */ }
}

export async function quienSoy(acceso, pide = fetch) {
  const r = await pide('https://openidconnect.googleapis.com/v1/userinfo', {
    headers: { Authorization: 'Bearer ' + acceso }
  });
  return json(r, 'Google (quién eres)');
}

/* ── Google Business Profile: las fichas y sus reseñas ─────────────── */

const con = (acceso) => ({ headers: { Authorization: 'Bearer ' + acceso } });

/* Todas las fichas a las que tiene acceso quien ha entrado: las suyas y
   las que administra. */
export async function misFichas(acceso, pide = fetch) {
  const d = await json(await pide('https://mybusinessaccountmanagement.googleapis.com/v1/accounts', con(acceso)),
    'Google Business Profile (cuentas)');
  const fichas = [];
  for (const cuenta of (d.accounts || []).slice(0, 10)) {
    let pagina = '';
    for (let vuelta = 0; vuelta < 5; vuelta++) {
      const q = new URLSearchParams({ readMask: 'name,title,storefrontAddress,metadata', pageSize: '100' });
      if (pagina) q.set('pageToken', pagina);
      const l = await json(await pide('https://mybusinessbusinessinformation.googleapis.com/v1/' +
        cuenta.name + '/locations?' + q, con(acceso)), 'Google Business Profile (fichas)');
      for (const f of l.locations || []) {
        const dir = f.storefrontAddress || {};
        fichas.push({
          id: cuenta.name + '/' + f.name,        // accounts/1/locations/2: lo que pide la API de reseñas
          nombre: f.title || '',
          direccion: [(dir.addressLines || []).join(' '), dir.locality].filter(Boolean).join(', '),
          placeId: (f.metadata && f.metadata.placeId) || '',
          maps: (f.metadata && f.metadata.mapsUri) || '',
          escribir: (f.metadata && f.metadata.newReviewUri) || ''
        });
      }
      pagina = l.nextPageToken || '';
      if (!pagina) break;
    }
  }
  return fichas;
}

export function idValido(id) {
  return /^accounts\/[\w-]+\/locations\/[\w-]+$/.test(String(id));
}

/* Las reseñas más recientes de una ficha, de la más nueva a la más vieja. */
export async function resenas(acceso, fichaId, pide = fetch, cuantas = 50) {
  if (!idValido(fichaId)) throw new Error('ficha rara: ' + fichaId);
  const q = new URLSearchParams({ pageSize: String(cuantas), orderBy: 'updateTime desc' });
  const d = await json(await pide('https://mybusiness.googleapis.com/v4/' + fichaId + '/reviews?' + q, con(acceso)),
    'Google Business Profile (reseñas)');
  return (d.reviews || []).map((v) => ({
    id: v.reviewId,
    nombre: v.name,                                   // accounts/1/locations/2/reviews/3
    autor: (v.reviewer && !v.reviewer.isAnonymous && v.reviewer.displayName) || '',
    estrellas: ESTRELLAS[v.starRating] || null,
    texto: v.comment || '',
    cuando: v.createTime || '',
    respondida: Boolean(v.reviewReply && v.reviewReply.comment),
    respuesta: (v.reviewReply && v.reviewReply.comment) || ''
  }));
}

/* Publica (o cambia) la respuesta del propietario en Google. */
export async function responde(acceso, resenaNombre, texto, pide = fetch) {
  if (!/^accounts\/[\w-]+\/locations\/[\w-]+\/reviews\/[\w-]+$/.test(String(resenaNombre))) {
    throw new Error('reseña rara: ' + resenaNombre);
  }
  const r = await pide('https://mybusiness.googleapis.com/v4/' + resenaNombre + '/reply', {
    method: 'PUT',
    headers: { Authorization: 'Bearer ' + acceso, 'Content-Type': 'application/json' },
    /* Google admite hasta 4096 caracteres */
    body: JSON.stringify({ comment: String(texto).slice(0, 4000) })
  });
  return json(r, 'Google Business Profile (responder)');
}
