/* Cifrado y firmas, con lo que trae el propio Cloudflare (WebCrypto).

   Para qué hace falta:

   · El permiso que da cada negocio al conectar su ficha (el "refresh
     token" de Google) es una llave: con él se puede responder en su
     nombre. Se guarda CIFRADO en el almacén. Si alguien llegara a leer
     el almacén, no podría usarlo sin TOKENS_CLAVE.

   · La sesión del dueño en /analiza/ficha/ va en una cookie FIRMADA: él
     no puede cambiarla para hacerse pasar por otro negocio.

   Todo sale de una sola variable, TOKENS_CLAVE: una frase larga y
   secreta que se pone una vez en Cloudflare y no se cambia nunca (si se
   cambia, los negocios conectados tienen que volver a conectar). */

const enc = new TextEncoder();
const dec = new TextDecoder();

function b64(bytes) {
  let s = '';
  for (const b of new Uint8Array(bytes)) s += String.fromCharCode(b);
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
function deB64(s) {
  const t = String(s).replace(/-/g, '+').replace(/_/g, '/');
  const bin = atob(t + '='.repeat((4 - (t.length % 4)) % 4));
  return Uint8Array.from(bin, (c) => c.charCodeAt(0));
}

/* Dos llaves distintas sacadas de la misma frase: una para cifrar y otra
   para firmar. Usar la misma para las dos cosas es mala práctica. */
async function llave(secreto, para, usos, algoritmo) {
  if (!secreto || String(secreto).length < 16) {
    throw new Error('falta TOKENS_CLAVE (una frase secreta de al menos 16 letras) en Cloudflare');
  }
  const crudo = await crypto.subtle.digest('SHA-256', enc.encode(para + ':' + secreto));
  return crypto.subtle.importKey('raw', crudo, algoritmo, false, usos);
}

export async function cifra(texto, secreto) {
  const k = await llave(secreto, 'cifrado', ['encrypt'], { name: 'AES-GCM' });
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const c = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, k, enc.encode(texto));
  return b64(iv) + '.' + b64(c);
}

export async function descifra(paquete, secreto) {
  const [iv, c] = String(paquete).split('.');
  const k = await llave(secreto, 'cifrado', ['decrypt'], { name: 'AES-GCM' });
  const p = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: deB64(iv) }, k, deB64(c));
  return dec.decode(p);
}

const HMAC = { name: 'HMAC', hash: 'SHA-256' };

/* Un sello: datos + caducidad + firma. firma(...) lo hace y lee(...) lo
   comprueba; si alguien toca una letra o ya caducó, lee() da null. */
export async function firma(datos, secreto, segundos) {
  const cuerpo = b64(enc.encode(JSON.stringify({ d: datos, h: Date.now() + segundos * 1000 })));
  const k = await llave(secreto, 'firma', ['sign'], HMAC);
  const f = await crypto.subtle.sign('HMAC', k, enc.encode(cuerpo));
  return cuerpo + '.' + b64(f);
}

export async function lee(sello, secreto) {
  try {
    const [cuerpo, f] = String(sello || '').split('.');
    if (!cuerpo || !f) return null;
    const k = await llave(secreto, 'firma', ['verify'], HMAC);
    const bien = await crypto.subtle.verify('HMAC', k, deB64(f), enc.encode(cuerpo));
    if (!bien) return null;
    const o = JSON.parse(dec.decode(deB64(cuerpo)));
    return o.h > Date.now() ? o.d : null;
  } catch (e) {
    return null;
  }
}

export function aleatorio(n = 16) {
  return b64(crypto.getRandomValues(new Uint8Array(n)));
}

/* Una huella corta para no guardar la IP de nadie en el almacén: con
   ella se cuentan los usos por persona sin saber quién es. */
export async function huella(texto) {
  const h = await crypto.subtle.digest('SHA-256', enc.encode(String(texto)));
  return b64(h).slice(0, 16);
}
