/* La parte del servidor que no habla con nadie: valida el encargo, monta
   el enlace del generador, entiende lo que contesta la IA y elige los
   colores cuando no hay IA.

   Vive aquí, fuera de la carpeta de cualquier proveedor, porque la usan
   los dos: las funciones de Cloudflare y las de Netlify. Una sola copia:
   dos copias de una tabla de colores acaban siendo dos tablas
   distintas.

   Y va aparte del resto a propósito, para poder probarla sin levantar
   nada ni gastar una llamada a la API. */

export var LIMITES = {
  negocio: 80, ciudad: 60, direccion: 160, tel: 24,
  correo: 120, google: 300, redes: 200, notas: 600, lema: 60,
  pago: 80
};
export var FORMATOS = ['placa', 'stand', 'tarjeta'];

function texto(v, max) {
  if (typeof v !== 'string') return '';
  /* fuera los caracteres de control: no pintan nada y ensucian los
     correos y el panel */
  return v.replace(/[\u0000-\u001F\u007F]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, max);
}

/* Deja el encargo en limpio o dice qué falta. Nunca lanza: un formulario
   mal rellenado no puede tumbar la función. */
export function limpia(crudo) {
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
    /* la referencia que devuelve Stripe al volver del pago. No decide
       nada —quien la manda es el navegador del cliente, o sea que se
       puede inventar—, solo sirve para cuadrarla contra el panel de
       Stripe de un vistazo. */
    pago:      texto(d.pago,      LIMITES.pago),
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
export function enlaceResena(v) {
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
export function enlaceGenerador(base, e, brief) {
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
export function leeBrief(txt) {
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

/* ══════════ colores por oficio, sin IA y sin gastar un euro ══════════

   La IA elige mejor —entiende "queremos algo como el toldo de la
   puerta"— pero cuesta una cuenta, una tarjeta y saldo. Esto no cuesta
   nada y acierta el tono general, que es el 90% del trabajo: una
   cervecería en verde botella y oro, una heladería en rosa y crema, un
   sushi en negro y rojo.

   Se mira lo que ha escrito el cliente: el nombre del negocio y lo que
   ha contado. La primera regla que encaja, gana. Si no encaja ninguna,
   sale el verde de la plantilla de siempre, que nunca queda mal.

   Los colores de la banda son todos OSCUROS a propósito: encima va el
   título en blanco. Los fondos, claros. Eso no se negocia, es lo que
   hace que se lea. */

export var OFICIOS = [
  { que: /cervecer|cerveza|birr|brew|tap ?room|lupul/i,
    banda: '#2E2410', fondo: '#F3EAD6', acento: '#D9A441',
    lema: 'Cervezas · Tapas', porque: 'Marrón cebada y oro de caña, que es lo que pide una cervecería.' },
  { que: /bodeg|vinote|vinos|enote|taberna|tasca/i,
    banda: '#4A1220', fondo: '#F2E7DC', acento: '#C9A227',
    lema: 'Vinos · Tapas', porque: 'Burdeos de vino tinto con el oro de la marca.' },
  { que: /pizz|italian|trattor|pasta/i,
    banda: '#123322', fondo: '#F5EDE0', acento: '#C4342B',
    lema: 'Pizza · Pasta', porque: 'Verde y rojo de bandera italiana, pero apagados para que no chillen.' },
  { que: /sushi|japon|ramen|wok|asiátic|asiatic|poke|thai|chin/i,
    banda: '#14161A', fondo: '#F0EDE6', acento: '#C4342B',
    lema: '', porque: 'Negro tinta y rojo, la pareja de siempre en la cocina asiática.' },
  { que: /mexic|taquer|taco|burrit|tex.?mex/i,
    banda: '#3B1E14', fondo: '#F6EBD5', acento: '#E0A02A',
    lema: 'Tacos · Cocina mexicana', porque: 'Barro y maíz: los colores de una taquería.' },
  { que: /kebab|döner|doner|turc|shawarma/i,
    banda: '#4A1512', fondo: '#F4EADA', acento: '#D9A441',
    lema: '', porque: 'Rojo oscuro y oro, que es como se rotula un kebab.' },
  { que: /hamburgues|burger|smash/i,
    banda: '#2A1A10', fondo: '#F5EBDA', acento: '#D98A1F',
    lema: 'Hamburguesas', porque: 'Marrón de pan tostado y mostaza.' },
  { que: /marisquer|marisco|arroce|paella|pescad|chiringuit|playa|beach/i,
    banda: '#123B52', fondo: '#F1EDE2', acento: '#D9A441',
    lema: '', porque: 'Azul de mar con el oro de la marca.' },
  { que: /asador|parrill|brasa|carn|steak|churrasc/i,
    banda: '#3A1A16', fondo: '#F3EADB', acento: '#C9762A',
    lema: 'Carnes a la brasa', porque: 'Rojo de brasa y naranja de fuego, en tono apagado.' },
  { que: /helader|helad|gelat|horchat/i,
    banda: '#6E2340', fondo: '#FBEFE9', acento: '#E7A0B4',
    lema: '', porque: 'Rosa fresa sobre crema: es el color que la gente espera de una heladería.' },
  { que: /pasteler|panader|obrador|horno|repostr|repost|tarta|croissant/i,
    banda: '#4A3018', fondo: '#F8EFDC', acento: '#D9A441',
    lema: '', porque: 'Marrón de horno y dorado de masa.' },
  { que: /cafeter|café|cafe|tostador|coffee|brunch|desayun/i,
    banda: '#3A2418', fondo: '#F4EADB', acento: '#C08A46',
    lema: 'Café · Desayunos', porque: 'Marrón de café tostado y leche.' },
  { que: /coctel|cóctel|cocktail|gin|pub|discotec|copas|club/i,
    banda: '#241436', fondo: '#F1EDF3', acento: '#C9A227',
    lema: '', porque: 'Morado de noche con oro: se ve bien con poca luz.' },
  { que: /peluquer|barber|barbershop/i,
    banda: '#16181C', fondo: '#F2F0EA', acento: '#C9A227',
    lema: '', porque: 'Negro y oro, el código de toda la vida de una barbería.' },
  { que: /estétic|estetic|belleza|uñas|unas|spa|masaj|depilac/i,
    banda: '#3E2447', fondo: '#F7EFF3', acento: '#C89BB0',
    lema: '', porque: 'Malva y rosa empolvado, que es el tono del sector.' },
  { que: /gimnas|crossfit|fitness|box|entrenami|pádel|padel/i,
    banda: '#1B1F26', fondo: '#EFF1F0', acento: '#7A9A1E',
    lema: '', porque: 'Gris grafito y verde: se lee de lejos y no parece un restaurante.' },
  { que: /clínic|clinic|dental|dentist|fisio|podol|veterinar|médic|medic|farmac|óptic|optic/i,
    banda: '#123B5C', fondo: '#EEF2F4', acento: '#2E9BB5',
    lema: '', porque: 'Azul sanitario: es lo que da confianza en una consulta.' },
  { que: /hotel|hostal|apartament|aloja|turism|casa rural/i,
    banda: '#152A45', fondo: '#F2EEE4', acento: '#C9A227',
    lema: '', porque: 'Azul marino y oro, el tono de recepción de hotel.' },
  { que: /florister|flores|jardín|jardin|vivero|planta/i,
    banda: '#1E3A22', fondo: '#F2F0E4', acento: '#D97A5A',
    lema: '', porque: 'Verde hoja con un coral de flor.' },
  { que: /joyer|relojer|orfebr/i,
    banda: '#16161A', fondo: '#F4F1EA', acento: '#C9A227',
    lema: '', porque: 'Negro y oro: el fondo desaparece y lo que brilla es la marca.' },
  { que: /ferreter|taller|mecánic|mecanic|neumátic|neumatic|chapa|pintura|fontaner|electricist/i,
    banda: '#1E2A38', fondo: '#F0F0EC', acento: '#D97A1F',
    lema: '', porque: 'Azul acero y naranja de señal: el par que se usa en industria.' },
  { que: /inmobiliar|abogad|asesor|gestor|seguro|consultor|notar/i,
    banda: '#182B40', fondo: '#F1F1ED', acento: '#C9A227',
    lema: '', porque: 'Azul serio y oro discreto, sin adornos.' },
  { que: /fruter|ultramarin|carnicer|charcuter|colmad|comestibl|herbolar|dietétic|dietetic/i,
    banda: '#1E3A2A', fondo: '#F3F0E3', acento: '#D9A441',
    lema: '', porque: 'Verde de mercado con oro, que es la combinación de la plantilla.' },
  { que: /tatua|tattoo|piercing/i,
    banda: '#141416', fondo: '#EFEDE8', acento: '#B8342B',
    lema: '', porque: 'Negro y rojo tinta.' },
  { que: /librer|papeler|copister|imprent|encuadern/i,
    banda: '#243A2E', fondo: '#F4F1E6', acento: '#C9A227',
    lema: '', porque: 'Verde de tapa de libro y oro de letra impresa.' },
  { que: /boutiqu|moda|ropa|calzado|zapat|tienda|complement/i,
    banda: '#1A1A1C', fondo: '#F3F1EC', acento: '#C9A227',
    lema: '', porque: 'Negro y oro: en tienda de moda, cuanto más callado el fondo, mejor.' },
  { que: /lavander|tintorer|autoescuela|academ|escuela|guarder/i,
    banda: '#173A55', fondo: '#F0F2F2', acento: '#D9A441',
    lema: '', porque: 'Azul limpio y oro.' },
  { que: /restaurant|cocina|menú|menu|comida|cater|bistr/i,
    banda: '#4A1220', fondo: '#F2E9DC', acento: '#C9A227',
    lema: 'Cocina · Sobremesa', porque: 'Burdeos y oro, el par clásico de carta de restaurante.' },
  { que: /\bbar\b|mesón|meson|cafetín|cantina/i,
    banda: '#192E26', fondo: '#ECE2D3', acento: '#E8C46A',
    lema: 'Bar · Cocina · Sobremesa', porque: 'El verde botella y el oro de la plantilla de siempre.' }
];

var POR_DEFECTO = {
  banda: '#192E26', fondo: '#ECE2D3', acento: '#E8C46A', lema: '',
  porque: 'No he sabido de qué va el negocio por lo que ha escrito, así que va con el verde y el oro de la plantilla. Cámbialo en el generador si no pega.'
};

/* Devuelve un brief con la misma forma que el de la IA, para que el
   resto del camino no tenga que enterarse de cuál de los dos vino. */
export function coloresPorOficio(encargo) {
  var e = encargo || {};
  /* ojo con el nombre: 'texto' ya es la función que limpia cadenas ahí
     arriba, y llamar así a esta variable la tapaba dentro de la función */
  var donde = [e.negocio, e.lema, e.notas, e.redes].filter(Boolean).join(' ');
  var elegido = POR_DEFECTO;
  for (var i = 0; i < OFICIOS.length; i++) {
    if (OFICIOS[i].que.test(donde)) { elegido = OFICIOS[i]; break; }
  }
  return {
    banda: elegido.banda,
    fondo: elegido.fondo,
    acento: elegido.acento,
    /* si el cliente ya ha propuesto un lema, manda el suyo */
    lema: texto(e.lema, LIMITES.lema) || elegido.lema || '',
    titulo: '',
    porque: elegido.porque
  };
}

/* Un identificador corto y legible para nombrar el encargo. No es
   secreto: solo sirve para hablar de él ("el 7K3M2"). */
export function referencia(cuando, negocio) {
  var base = String(negocio || '').toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 3) || 'XXX';
  var t = new Date(cuando || Date.now()).getTime().toString(36).toUpperCase().slice(-5);
  return base + '-' + t;
}
