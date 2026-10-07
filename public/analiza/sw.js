/* Lo mínimo para que el móvil deje instalar la app (/analiza/ y
   /analiza/ficha/).

   Cada página se guarda para que abra al instante aunque haya poca
   cobertura, y se vuelve a pedir siempre que hay red: así un cambio en
   la web se ve a la siguiente apertura, sin quedarse con una versión
   vieja. Lo de /api/ no pasa nunca por aquí: necesita el servidor, y
   las sesiones del dueño no se guardan en ningún sitio. */

const CAJA = 'plea5e-analiza-2';

self.addEventListener('install', () => self.skipWaiting());

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys()
    .then((ks) => Promise.all(ks.filter((k) => k !== CAJA).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', (e) => {
  if (e.request.mode !== 'navigate') return;
  /* Sin lo de después del ? : "/analiza/ficha/?conectado=1" es la misma
     página que "/analiza/ficha/". */
  const url = new URL(e.request.url);
  const clave = url.origin + url.pathname;
  e.respondWith(
    fetch(e.request)
      .then((r) => {
        if (r.ok && r.type === 'basic') {
          const copia = r.clone();
          caches.open(CAJA).then((c) => c.put(clave, copia));
        }
        return r;
      })
      .catch(() => caches.match(clave).then((r) => r || caches.match(url.origin + '/analiza/')))
  );
});
