/* Lo mínimo para que el móvil deje instalar el analizador como una app.

   Guarda la página para que abra al instante aunque haya poca cobertura,
   y la vuelve a pedir siempre que hay red: así un cambio en la web se ve
   a la siguiente apertura, sin quedarse con una versión vieja. El
   análisis (/api/...) no pasa nunca por aquí: necesita el servidor. */

const CAJA = 'plea5e-analiza-1';
const PAGINA = '/analiza/';

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CAJA).then((c) => c.add(PAGINA)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys()
    .then((ks) => Promise.all(ks.filter((k) => k !== CAJA).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', (e) => {
  if (e.request.mode !== 'navigate') return;
  e.respondWith(
    fetch(e.request)
      .then((r) => {
        const copia = r.clone();
        caches.open(CAJA).then((c) => c.put(PAGINA, copia));
        return r;
      })
      .catch(() => caches.match(PAGINA))
  );
});
