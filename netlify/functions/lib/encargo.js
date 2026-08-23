/* La parte del servidor que no habla con nadie: valida el encargo, monta
   el enlace del generador y entiende lo que contesta la IA.
   Va aparte a propósito, para poder probarla sin levantar Netlify ni
   gastar una llamada a la API. */

'use strict';

var LIMITES = {
  negocio: 80, ciudad: 60, direccion: 160, tel: 24,
  correo: 120, google: 300, redes: 200, notas: 600, lema: 60
};
var FORMATOS = ['placa', 'stand', 'tarjeta'];

function texto(v, max) {
  if (typeof v !== 'string') return '';
  /* fuera los caracteres de control: no pintan nada y ensucian los
     correos y el panel */
  return v.replace(/[\u0000-\u001F\u007F]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, max);
}

/* Deja el encargo en limpio o dice qué falta. Nunca lanza: un formulario
   mal rellenado no puede tumbar la función. */
function limpia(crudo) {
  var d = crudo && typeof crudo === 'object' ? crudo : {};
  var e = {
    negocio:   texto(d.negocio,   LIMITES.negocio),
    lema:      texto(d.lema,      LIMITES.lema),
    ciudad:    texto(d.ciudad,    LIMITES.ciudad),
    direccion: texto(d.direccion, LIMITES.direccion),
    tel:       texto(d.tel,       LIMITES.tel),
    correo:    texto(d.correo,    LIMITES.correo),
    google:    texto(d.google,    LIMITES.google),
    redes:     texto(d.redes,     LIMITES.redes),
    notas:     texto(d.notas,     LIMITES.notas),
    formato:   FORMATOS.indexOf(d.formato) > -1 ? d.formato : 'placa',
    cantidad:  Math.max(1, Math.min(500, parseInt(d.cantidad, 10) || 1))
  };

  var faltan = [];
  if (!e.negocio) faltan.push('el nombre del negocio');
  if (!e.tel && !e.correo) faltan.push('un teléfono o un correo');
  /* el correo solo se mira si lo han puesto: es opcional si hay teléfono */
  if (e.correo && !/^[^@\s]+@[^@\s.]+\.[^@\s]{2,}$/.test(e.correo)) {
    faltan.push('un correo bien escrito');
  }
  return { encargo: e, faltan: faltan };
}

/* Del enlace de Google nos quedamos con lo que sirve para el QR. Vale el
   código a secas, el enlace de "pedir reseñas" o cualquier dirección. */
function enlaceResena(v) {
  var s = texto(v, LIMITES.google);
  if (!s) return '';
  if (/^https?:\/\//i.test(s)) return s;
  if (/^[A-Za-z0-9_-]{15,}$/.test(s)) {
    return 'https://search.google.com/local/writereview?placeid=' + s;
  }
  return s;
}

/* El enlace que abre el generador con todo puesto. Los datos van detrás
   de la almohadilla: así no salen del navegador de quien lo abre. */
function enlaceGenerador(base, e, brief) {
  var b = brief || {};
  var pares = [
    ['n', e.negocio],
    ['l', b.lema || e.lema],
    ['g', e.google],
    ['f', e.formato],
    ['b', b.banda],
    ['d', b.fondo],
    ['a', b.acento],
    ['t', b.titulo]
  ];
  var trozos = pares
    .filter(function (p) { return p[1]; })
    .map(function (p) { return p[0] + '=' + encodeURIComponent(p[1]); });
  return String(base).replace(/\/+$/, '') + '/taller/generador.html#' + trozos.join('&');
}

/* Lo que contesta la IA viene como texto. Puede traer la valla de código
   de markdown alrededor, o venir a medias si se corta. Nada de eso puede
   tumbar el encargo: si no se entiende, se sigue sin brief y ya lo
   decides tú a mano en el generador. */
function leeBrief(txt) {
  if (typeof txt !== 'string' || !txt.trim()) return null;
  var s = txt.trim().replace(/^```(?:json)?\s*/i, '').replace(/```\s*$/, '').trim();
  var i = s.indexOf('{'), j = s.lastIndexOf('}');
  if (i < 0 || j <= i) return null;
  var d;
  try { d = JSON.parse(s.slice(i, j + 1)); } catch (err) { return null; }
  if (!d || typeof d !== 'object') return null;

  var hex = function (v) {
    if (typeof v !== 'string') return '';
    var h = v.trim();
    if (!/^#?[0-9A-Fa-f]{6}$/.test(h)) return '';
    return (h.charAt(0) === '#' ? h : '#' + h).toUpperCase();
  };
  var brief = {
    banda:  hex(d.banda),
    fondo:  hex(d.fondo),
    acento: hex(d.acento),
    lema:   texto(d.lema, LIMITES.lema),
    titulo: texto(d.titulo, 90),
    porque: texto(d.porque, 300)
  };
  /* si no ha acertado ni un color, el brief no aporta nada */
  if (!brief.banda && !brief.fondo && !brief.acento && !brief.lema) return null;
  return brief;
}

/* Un identificador corto y legible para nombrar el encargo. No es
   secreto: solo sirve para hablar de él ("el 7K3M2"). */
function referencia(cuando, negocio) {
  var base = String(negocio || '').toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 3) || 'XXX';
  var t = new Date(cuando || Date.now()).getTime().toString(36).toUpperCase().slice(-5);
  return base + '-' + t;
}

module.exports = { limpia: limpia, enlaceResena: enlaceResena,
                   enlaceGenerador: enlaceGenerador, leeBrief: leeBrief,
                   referencia: referencia, LIMITES: LIMITES, FORMATOS: FORMATOS };
