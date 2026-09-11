/* La puerta de entrada de todo. Cloudflare ejecuta esto en cada petición
   que llega a plea5e.es.

   Hace tres cosas y nada más:

     · /api/...       lo atiende el código de al lado
     · /r/loquesea    es el salto de una placa: mira en el almacén a dónde
                      tiene que ir hoy ese QR y manda allí al cliente
     · todo lo demás  —la web, el generador, las fotos, el panel—  se lo
       pide al almacén de archivos estáticos (public/), que es el propio
       Cloudflare y va a toda velocidad desde el servidor más cercano al
       cliente.

   Por qué así: Cloudflare tenía dos productos, Pages para webs y Workers
   para código. Ahora empuja todo a Workers, y en Workers la web es un
   añadido del código y no al revés. Este archivo es la costura entre las
   dos cosas. */

import { onRequest as encargo }  from './api/encargo.js';
import { onRequest as encargos } from './api/encargos.js';
import { onRequest as enlace }   from './api/enlace.js';
import { onRequest as enlaces }  from './api/enlaces.js';

/* Una tabla, no una cadena de ifs: añadir una función nueva es añadir una
   línea, y no hay forma de que dos rutas se pisen sin que se vea. */
const RUTAS = {
  '/api/encargo':  encargo,
  '/api/encargos': encargos,
  '/api/enlaces':  enlaces
};

export default {
  async fetch(request, env, ctx) {
    const ruta = new URL(request.url).pathname;
    const atiende = RUTAS[ruta];
    if (atiende) {
      try {
        return await atiende({ request, env, ctx });
      } catch (err) {
        /* Una función que se cae no puede tumbar la web entera ni dejar
           al cliente mirando una pantalla en blanco del navegador. */
        console.error('en ' + ruta + ': ' + (err && err.stack || err));
        return new Response(
          JSON.stringify({ error: (err && err.message) || 'fallo inesperado' }),
          { status: 500, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
      }
    }
    /* Las direcciones cortas de las placas. No pueden ir en la tabla de
       arriba porque cada una es distinta: /r/bar-manolo, /r/piccola...
       Si el nombre no está guardado, enlace.js devuelve el archivo
       estático de siempre, así que las carpetas que ya existían en
       public/r/ siguen funcionando sin tocarlas. */
    if (ruta.startsWith('/r/')) {
      try {
        return await enlace({ request, env, ctx });
      } catch (err) {
        /* Un fallo aquí es un cliente delante de una placa con el móvil en
           la mano. Que vaya al archivo estático antes que a un error. */
        console.error('en ' + ruta + ': ' + (err && err.stack || err));
        return env.ASSETS.fetch(request);
      }
    }

    /* Cualquier otra dirección: un archivo de public/. Si no existe,
       Cloudflare devuelve su 404; no hay que hacer nada. */
    return env.ASSETS.fetch(request);
  }
};
