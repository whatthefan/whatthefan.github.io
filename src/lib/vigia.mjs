/* El vigilante: lo que responde solo en Google.

   Cloudflare lo despierta cada dos horas (wrangler.jsonc → triggers) y
   también se puede lanzar a mano desde los paneles. Por cada negocio que
   ha conectado su ficha y la tiene activada:

     1. renueva el permiso de Google (va cifrado en el almacén)
     2. pide las reseñas recientes de la ficha
     3. las que no tienen respuesta y no ha visto antes las analiza
        (reputacion/motor.mjs) y les escribe respuesta con la
        configuración del negocio (tono, firma, contacto...)
     4. publica en Google lo que el dueño ha dejado en automático y deja
        el resto pendiente de un clic en su panel
     5. si hay pendientes o denunciables nuevas, le manda un correo

   Lo que decide qué se publica solo:
     · 4 y 5 estrellas: si auto_positivas (por defecto, sí).
     · 1 a 3: si auto_negativas (por defecto, NO: una respuesta a una
       queja la tiene que ver el dueño). Y nunca en automático si la
       reseña es denunciable o dudosa: primero que decida si la denuncia.

   ── En el almacén ──────────────────────────────────────────────────
     gc-<cuenta>                    el negocio conectado: correo, permiso
                                    cifrado y sus fichas con su config
     gr-<cuenta>-<ficha>-<reseña>   cada reseña que ha pasado por aquí:
                                    publicada, pendiente, ignorada...

   Hay un presupuesto por vuelta (TOPE_VUELTA reseñas) porque Cloudflare
   limita lo que puede hacer cada ejecución. Lo que no da tiempo se coge
   en la siguiente, empezando por los que llevan más rato sin revisar. */

import * as G from './google.mjs';
import { descifra } from './cripto.mjs';
import { analiza as analizaMotor } from '../../reputacion/motor.mjs';

export const TOPE_VUELTA = 12;
/* Al conectar, se miran las reseñas de los últimos 60 días. Las de
   antes, si el dueño quiere, desde el panel. */
export const DIAS_ATRAS = 60;

export const CONFIG_INICIAL = {
  activa: false,
  auto_positivas: true,
  auto_negativas: false,
  tono: 'cercano',
  firma: '',
  contacto: '',
  palabras_clave: [],
  notas: '',
  sector: ''
};

export const claveCuenta = (sub) => 'gc-' + sub;
export const numero = (id) => String(id).split('/').pop();
export const claveResena = (sub, fichaId, resenaId) => 'gr-' + sub + '-' + numero(fichaId) + '-' + resenaId;

/* La configuración tal como llega del panel, recortada y con valores
   sabidos: viene de un navegador y puede llegar cualquier cosa. */
export function limpiaConfig(c, antes) {
  c = c || {};
  const b = { ...CONFIG_INICIAL, ...(antes || {}) };
  const corta = (s, n) => String(s == null ? '' : s).trim().slice(0, n);
  const si = (v, def) => (typeof v === 'boolean' ? v : def);
  const kw = Array.isArray(c.palabras_clave) ? c.palabras_clave : String(c.palabras_clave == null ? b.palabras_clave.join(',') : c.palabras_clave).split(',');
  return {
    activa: si(c.activa, b.activa),
    auto_positivas: si(c.auto_positivas, b.auto_positivas),
    auto_negativas: si(c.auto_negativas, b.auto_negativas),
    tono: c.tono === 'formal' ? 'formal' : (c.tono === 'cercano' ? 'cercano' : b.tono),
    firma: c.firma == null ? b.firma : corta(c.firma, 80),
    contacto: c.contacto == null ? b.contacto : corta(c.contacto, 120),
    palabras_clave: kw.map((k) => corta(k, 60)).filter(Boolean).slice(0, 5),
    notas: c.notas == null ? b.notas : corta(c.notas, 500),
    sector: c.sector == null ? b.sector : corta(c.sector, 60)
  };
}

/* ¿Se publica sola? */
export function decide(resena, analisis, config) {
  if (Number(resena.estrellas) >= 4) return config.auto_positivas ? 'publicar' : 'pendiente';
  if (analisis.veredicto === 'impugnable' || analisis.veredicto === 'revisar') return 'pendiente';
  return config.auto_negativas ? 'publicar' : 'pendiente';
}

async function leeJSON(kv, k) {
  const t = await kv.get(k);
  if (!t) return null;
  try { return JSON.parse(t); } catch (e) { return null; }
}

/* Una ficha: lo nuevo, analizado, respondido o apartado. Devuelve lo que
   ha hecho para el resumen y el correo. */
export async function revisaFicha({ env, cuenta, ficha, acceso, presupuesto, deps }) {
  const pide = deps.pide || fetch;
  const analiza = deps.analiza || analizaMotor;
  const hecho = { publicadas: 0, pendientes: [], errores: [] };
  const config = limpiaConfig(ficha.config);
  const desde = Number(ficha.desde || 0);
  const lista = await G.resenas(acceso, ficha.id, pide);

  for (const r of lista) {
    if (presupuesto.n <= 0) break;
    if (r.respondida) continue;
    if (desde && r.cuando && Date.parse(r.cuando) < desde) continue;
    const k = claveResena(cuenta.sub, ficha.id, r.id);
    if (await env.ENCARGOS.get(k)) continue;
    presupuesto.n--;

    let analisis;
    try {
      analisis = await analiza({
        texto: r.texto, estrellas: r.estrellas, autor: r.autor,
        negocio: { nombre: ficha.nombre, sector: config.sector, palabras_clave: config.palabras_clave, contacto: config.contacto }
      }, { apiKey: String(env.ANTHROPIC_API_KEY || '').trim() || undefined, modo: 'auto', config: { ...config, nombre: ficha.nombre } });
    } catch (err) {
      hecho.errores.push('analizar: ' + err.message);
      continue;
    }
    const registro = {
      cuenta: cuenta.sub, ficha: ficha.id, fichaNombre: ficha.nombre, nombre: r.nombre,
      autor: r.autor, estrellas: r.estrellas, texto: r.texto, cuando: r.cuando,
      respuesta: analisis.respuesta,
      analisis: {
        tipo: analisis.tipo, veredicto: analisis.veredicto, fuerza: analisis.fuerza, resumen: analisis.resumen,
        apelacion: analisis.apelacion,
        infracciones: (analisis.infracciones || []).map((i) => ({ norma: i.norma, cita: i.cita, fuerza: i.fuerza }))
      },
      estado: 'pendiente', visto: Date.now()
    };
    if (decide(r, analisis, config) === 'publicar') {
      try {
        await G.responde(acceso, r.nombre, analisis.respuesta, pide);
        registro.estado = 'publicada';
        registro.publicada = Date.now();
        hecho.publicadas++;
      } catch (err) {
        registro.estado = 'pendiente';
        registro.error = err.message;
        hecho.errores.push('publicar: ' + err.message);
      }
    }
    if (registro.estado === 'pendiente') hecho.pendientes.push(registro);
    await env.ENCARGOS.put(k, JSON.stringify(registro));
  }
  return hecho;
}

function esc(s) {
  return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

/* El correo al dueño cuando hay algo que necesita su clic. */
export async function avisaDueno(env, cuenta, pendientes, pide = fetch) {
  const clave = String(env.RESEND_API_KEY || '').trim();
  const desde = String(env.CORREO_DE || '').trim();
  if (!clave || !desde || !cuenta.email || !pendientes.length) return false;
  const denunciables = pendientes.filter((p) => p.analisis.veredicto === 'impugnable').length;
  const filas = pendientes.slice(0, 10).map((p) => `
    <tr><td style="padding:10px 0;border-bottom:1px solid #eee">
      <b>${'★'.repeat(p.estrellas || 0)}</b> ${esc(p.autor || 'Anónimo')} · ${esc(p.fichaNombre)}<br>
      <span style="color:#555">${esc(String(p.texto || '(solo estrellas)').slice(0, 220))}</span>
      ${p.analisis.veredicto === 'impugnable' ? '<br><b style="color:#2a8a57">Se puede denunciar</b>' : ''}
    </td></tr>`).join('');
  const base = String(env.WEB_BASE || 'https://plea5e.es').replace(/\/$/, '');
  const html = `
    <div style="font:15px/1.5 -apple-system,Segoe UI,Roboto,Arial,sans-serif;color:#111;max-width:560px">
      <h2 style="margin:0 0 8px">Tienes ${pendientes.length} ${pendientes.length === 1 ? 'reseña' : 'reseñas'} esperando tu respuesta</h2>
      <p style="margin:0 0 14px;color:#555">Ya están contestadas: solo tienes que revisarlas y darle a publicar.${denunciables ? ' <b>' + denunciables + ' se ' + (denunciables === 1 ? 'puede' : 'pueden') + ' denunciar</b> y tienes la denuncia preparada.' : ''}</p>
      <table style="width:100%;border-collapse:collapse">${filas}</table>
      <p style="margin:20px 0 0"><a href="${base}/analiza/ficha/" style="background:#E9BC46;color:#100B00;text-decoration:none;padding:12px 20px;border-radius:999px;font-weight:700">Revisar y publicar</a></p>
    </div>`;
  try {
    const r = await pide('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + clave, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from: desde, to: [cuenta.email],
        subject: pendientes.length + ' ' + (pendientes.length === 1 ? 'reseña nueva' : 'reseñas nuevas') + ' en Google' + (denunciables ? ' · ' + denunciables + ' denunciable' + (denunciables > 1 ? 's' : '') : ''),
        html })
    });
    return r.ok;
  } catch (e) { return false; }
}

/* Una cuenta entera. soloFicha: para el botón "revisar ahora". */
export async function revisaCuenta(env, cuenta, opciones = {}) {
  const deps = opciones.deps || {};
  const pide = deps.pide || fetch;
  const presupuesto = opciones.presupuesto || { n: TOPE_VUELTA };
  const resumen = { publicadas: 0, pendientes: 0, errores: [] };
  const activas = (cuenta.fichas || []).filter((f) => (opciones.soloFicha ? f.id === opciones.soloFicha : f.config && f.config.activa));
  if (!activas.length) return resumen;

  let acceso;
  try {
    acceso = await G.renueva(await descifra(cuenta.permiso, env.TOKENS_CLAVE), env, pide);
  } catch (err) {
    /* Lo normal: el dueño quitó el permiso desde su cuenta de Google. */
    cuenta.error = 'No se puede entrar en la ficha: ' + err.message + '. Vuelve a conectar con Google.';
    await env.ENCARGOS.put(claveCuenta(cuenta.sub), JSON.stringify(cuenta));
    resumen.errores.push(cuenta.error);
    return resumen;
  }
  const nuevas = [];
  for (const ficha of activas) {
    if (presupuesto.n <= 0) break;
    try {
      const h = await revisaFicha({ env, cuenta, ficha, acceso, presupuesto, deps });
      resumen.publicadas += h.publicadas;
      resumen.pendientes += h.pendientes.length;
      resumen.errores.push(...h.errores);
      nuevas.push(...h.pendientes);
      ficha.ultima = Date.now();
      ficha.error = h.errores[0] || '';
    } catch (err) {
      ficha.error = err.message;
      resumen.errores.push(ficha.nombre + ': ' + err.message);
    }
  }
  cuenta.ultima = Date.now();
  cuenta.error = '';
  await env.ENCARGOS.put(claveCuenta(cuenta.sub), JSON.stringify(cuenta));
  if (nuevas.length) await avisaDueno(env, cuenta, nuevas, pide);
  return resumen;
}

/* La vuelta completa: todas las cuentas con algo activo, empezando por
   las que llevan más tiempo sin revisar. */
export async function vigila(env, deps = {}) {
  if (!env.ENCARGOS || !env.GOOGLE_CLIENT_ID || !env.TOKENS_CLAVE) return { saltado: 'falta configuración' };
  const { keys } = await env.ENCARGOS.list({ prefix: 'gc-', limit: 1000 });
  const cuentas = [];
  for (const k of keys) {
    const c = await leeJSON(env.ENCARGOS, k.name);
    if (c && (c.fichas || []).some((f) => f.config && f.config.activa)) cuentas.push(c);
  }
  cuentas.sort((a, b) => (a.ultima || 0) - (b.ultima || 0));
  const presupuesto = { n: TOPE_VUELTA };
  const total = { cuentas: 0, publicadas: 0, pendientes: 0, errores: [] };
  for (const c of cuentas) {
    if (presupuesto.n <= 0) break;
    const r = await revisaCuenta(env, c, { presupuesto, deps });
    total.cuentas++;
    total.publicadas += r.publicadas;
    total.pendientes += r.pendientes;
    total.errores.push(...r.errores);
  }
  return total;
}
