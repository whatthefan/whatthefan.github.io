/* LA DIRECCIÓN CORTA DE CADA PLACA:  plea5e.es/r/loquesea
   ==========================================================================

   Por qué existe esto, que es lo importante de entender:

   El chip NFC se reprograma acercando el móvil, pero el QR va IMPRESO. Si
   el QR lleva grabada la dirección de Google del bar, esa placa queda
   atada a ese bar para siempre: si cambia de dueño, de nombre o de ficha
   en Google, la placa se tira a la basura.

   Con esto, el QR lleva grabada una dirección nuestra —plea5e.es/r/algo— y
   es AQUÍ donde se decide a dónde va. Cambiar el destino es una línea en
   el panel: la placa que está pegada en la mesa del bar no se toca.

   Y de paso se cuentan los toques, que es lo único que podemos saber.
   OJO CON ESTO: contamos cuánta gente ACERCA EL MÓVIL, no cuánta deja la
   reseña. Google no nos dice quién escribió. No prometas nunca lo segundo.

   Guarda dos cosas en el mismo almacén de los pedidos (así no hay que
   crear nada nuevo en Cloudflare):

     r-<nombre>                el destino, en JSON
     rt-<nombre>               los toques de siempre, un número
     rc-<nombre>-<AAAA-MM-DD>  los toques de ese día, un número

   El total va aparte y no dentro del destino a propósito: si se guardara
   dentro, un toque que entre justo mientras cambias el destino en el
   panel te pisaría el cambio. Cada cosa en su clave y no se tocan.

   Los contadores por día se borran solos al año y pico. Si no, en cinco
   años el almacén son cien mil claves de las que no te acuerdas. El
   total no caduca.                                                      */

/* Las mismas reglas que valida el panel: minúsculas, números y guiones.
   Si esto y el panel no coinciden, se pueden crear enlaces que luego no
   se pueden abrir. */
export const NOMBRE_VALIDO = /^[a-z0-9][a-z0-9-]{1,39}$/;

export const CLAVE_ENLACE  = (n) => 'r-' + n;
export const CLAVE_TOTAL   = (n) => 'rt-' + n;
export const CLAVE_CUENTA  = (n, dia) => 'rc-' + n + '-' + dia;

/* Las claves de arriba NO son pedidos, y el panel de pedidos lista el
   almacén entero. Esta es la lista de prefijos que tiene que saltarse
   para no enseñar enlaces donde deberían salir encargos. */
export const PREFIJOS_ENLACE = ['r-', 'rt-', 'rc-'];

/* el día de hoy en Madrid. En el Worker la hora del sistema es UTC, así
   que en verano un toque de las 00:30 se apuntaría en el día de ayer. */
export function hoyEnMadrid() {
  return new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Europe/Madrid', year: 'numeric', month: '2-digit', day: '2-digit'
  }).format(new Date());
}

/* Un año y pico. Suficiente para enseñar "el mismo mes del año pasado" y
   para que no crezca sin final. */
const VIDA_CUENTA = 60 * 60 * 24 * 400;

const numero = (v) => parseInt(v || '0', 10) || 0;

async function suma(env, nombre) {
  const dia = CLAVE_CUENTA(nombre, hoyEnMadrid());
  const tot = CLAVE_TOTAL(nombre);
  /* Leer, sumar y guardar no es infalible: si entran dos toques en el
     mismo instante, uno se puede perder. Para saber si una placa se usa
     mucho o poco da igual; para facturar no valdría. */
  const [antesDia, antesTot] = await Promise.all([
    env.ENCARGOS.get(dia), env.ENCARGOS.get(tot)
  ]);
  await Promise.all([
    env.ENCARGOS.put(dia, String(numero(antesDia) + 1), { expirationTtl: VIDA_CUENTA }),
    env.ENCARGOS.put(tot, String(numero(antesTot) + 1))
  ]);
}

/* La página de "esta placa todavía no está lista". La ve el cliente de un
   bar, de pie y con el móvil en la mano, así que es corta y no habla de
   enlaces, ni de paneles, ni de nada nuestro: eso no es asunto suyo. Va
   escrita aquí y no en un archivo de public/ porque tiene que contestar
   el propio Worker, sin depender de que exista ningún archivo. */
function sinDestino() {
  const html = `<!doctype html>
<html lang="es">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Esta placa todavía no está lista</title>
<style>
  :root{color-scheme:light}
  body{margin:0;min-height:100dvh;display:grid;place-items:center;
       padding:24px;background:#ECE2D3;color:#1C1B19;
       font:400 1rem/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}
  main{max-width:26rem;text-align:center}
  h1{margin:0 0 .6rem;font-size:1.35rem;line-height:1.25}
  p{margin:0 0 1rem;color:#4A453C}
  a{color:#1C1B19;font-weight:700}
  .tel{display:inline-block;margin-top:.4rem;padding:.7rem 1.1rem;
       border-radius:99px;background:#1C1B19;color:#ECE2D3;text-decoration:none}
</style>
<main>
  <h1>Esta placa todavía no está lista</h1>
  <p>Perdona el viaje. El negocio la ha puesto antes de que la
     activáramos por nuestra parte, y lo estamos arreglando.</p>
  <p>Si quieres dejar tu opinión, búscalos en Google y déjasela ahí:
     les hace el mismo bien.</p>
  <p>¿Eres el del negocio? Llámanos y lo dejamos andando hoy mismo.</p>
  <a class="tel" href="tel:+34661403219">661 40 32 19</a>
</main>`;
  return new Response(html, {
    status: 404,
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
      /* Sin esto, el móvil se guardaría el error y seguiría enseñándolo
         durante días aunque el enlace ya esté dado de alta. */
      'Cache-Control': 'no-store, no-cache, must-revalidate'
    }
  });
}

export async function onRequest(context) {
  const { request, env, ctx } = context;
  const url = new URL(request.url);

  /* /r/bar-manolo  y  /r/bar-manolo/  son lo mismo */
  const nombre = decodeURIComponent(url.pathname.slice(3)).replace(/\/+$/, '').toLowerCase();

  /* Si no vale como nombre, o el almacén no está conectado, no inventamos
     nada: que conteste el archivo estático de siempre. Así las carpetas
     que ya había en public/r/ siguen funcionando igual que antes. */
  if (!NOMBRE_VALIDO.test(nombre) || !env.ENCARGOS) return env.ASSETS.fetch(request);

  let guardado = null;
  try {
    const crudo = await env.ENCARGOS.get(CLAVE_ENLACE(nombre));
    if (crudo) guardado = JSON.parse(crudo);
  } catch (err) {
    console.error('enlace ilegible: ' + nombre);
  }

  /* No está en el almacén. Puede ser una de las carpetas antiguas de
     public/r/, así que primero se pregunta por el archivo estático.

     Y si tampoco hay archivo, NO se deja salir el 404 pelado de
     Cloudflare. Antes daba casi igual, porque una placa sin dirección
     corta llevaba Google grabado y funcionaba igual. Ahora el QR de
     TODAS las placas pasa por aquí: si a alguien se le olvida dar de
     alta el enlace antes de imprimir, el cliente del bar acerca el móvil
     y se encuentra una página de error en blanco. Queda como si el
     negocio tuviera la web rota, y el que llama enfadado es el dueño.

     Así que se contesta una página que se entiende, con el teléfono. El
     código sigue siendo 404, que es la verdad, y sin guardar en caché:
     en cuanto se da de alta el enlace, el siguiente toque ya salta. */
  if (!guardado || !guardado.destino) {
    const estatico = await env.ASSETS.fetch(request);
    if (estatico.status !== 404) return estatico;
    return sinDestino();
  }

  /* El toque se apunta DESPUÉS de mandar al cliente a Google. waitUntil
     deja el Worker terminando la tarea con la respuesta ya enviada: el
     cliente no espera ni un milisegundo a que se guarde el número. */
  if (ctx && ctx.waitUntil) ctx.waitUntil(suma(env, nombre).catch(() => {}));

  return new Response(null, {
    status: 302,
    headers: {
      'Location': guardado.destino,
      /* Sin esto, el móvil se guardaría el salto y el día que cambies el
         destino habría clientes yendo al bar de antes durante semanas.
         Es justo lo que venimos a evitar. */
      'Cache-Control': 'no-store, no-cache, must-revalidate',
      'Referrer-Policy': 'no-referrer'
    }
  });
}
