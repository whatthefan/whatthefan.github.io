/* Lo que comparten /analiza/ y /analiza/ficha/: instalarla como app.

   Por qué no basta con un botón: cada móvil lo hace a su manera, y hay
   un caso en que es imposible, que es justo el más común. Si el enlace
   se abre desde WhatsApp, Instagram o Facebook, se abre en el navegador
   de DENTRO de esa app, y ese navegador no deja instalar nada. Hay que
   decirle a la persona que lo abra en Chrome o Safari.

     · Android con Chrome: el navegador avisa (beforeinstallprompt) y el
       botón instala de un toque.
     · iPhone: Safari no avisa nunca. Se instala desde Compartir →
       "Añadir a pantalla de inicio". Se enseña con dibujo.
     · Dentro de WhatsApp/Instagram/Facebook: "ábrelo en el navegador".
     · Si ya está instalada y abierta como app, el botón ni sale. */

(function () {
  var ua = navigator.userAgent || '';
  var enApp = /FBAN|FBAV|FB_IAB|Instagram|WhatsApp|Line\/|TikTok|Snapchat|; wv\)/i.test(ua);
  var ios = /iPhone|iPad|iPod/i.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var iosSafari = ios && !/CriOS|FxiOS|EdgiOS/i.test(ua);
  var movil = ios || /Android/i.test(ua);
  var instalada = (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) || navigator.standalone === true;
  var pendiente = null;

  var css = document.createElement('style');
  css.textContent =
    '.hoja-fondo{position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:50;display:flex;align-items:flex-end;justify-content:center}' +
    '.hoja{background:#0F1522;color:#EAEDF4;border:1px solid #2A3448;border-radius:18px 18px 0 0;max-width:520px;width:100%;padding:22px 20px 28px;font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}' +
    '.hoja h2{margin:0 0 12px;font-size:20px}.hoja ol{margin:0 0 16px;padding-left:22px}.hoja li{margin-bottom:10px}' +
    '.hoja .ico{display:inline-block;vertical-align:-4px;width:22px;height:22px}' +
    '.hoja .fila{display:flex;gap:8px;flex-wrap:wrap}.hoja code{background:#06080E;padding:2px 6px;border-radius:6px;word-break:break-all}' +
    '.hoja button{font:inherit;font-weight:700;border-radius:999px;padding:11px 18px;border:1px solid #2A3448;background:#141B2B;color:#EAEDF4;cursor:pointer}' +
    '.hoja button.oro{background:#E9BC46;color:#100B00;border-color:#E9BC46}';
  document.head.appendChild(css);

  var COMPARTIR = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="#4DA3FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12M7 8l5-5 5 5"/><path d="M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"/></svg>';
  var MAS = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="#EAEDF4" stroke-width="2"><rect x="4" y="4" width="16" height="16" rx="3"/><path d="M12 8v8M8 12h8"/></svg>';
  var TRES = '<b style="font-size:20px;line-height:1">⋮</b>';

  function hoja(html) {
    var f = document.createElement('div');
    f.className = 'hoja-fondo';
    f.innerHTML = '<div class="hoja" role="dialog" aria-modal="true">' + html +
      '<div class="fila" style="margin-top:6px"><button type="button" data-cierra class="oro">Entendido</button></div></div>';
    f.addEventListener('click', function (e) {
      if (e.target === f || e.target.hasAttribute('data-cierra')) f.remove();
      if (e.target.hasAttribute('data-copia-enlace')) {
        try { navigator.clipboard.writeText(location.href); e.target.textContent = '¡Copiado!'; } catch (x) {}
      }
    });
    document.body.appendChild(f);
  }

  function instala() {
    if (pendiente) {
      pendiente.prompt();
      pendiente.userChoice.then(function (r) { if (r.outcome === 'accepted') ocultaBotones(); });
      pendiente = null;
      return;
    }
    if (enApp) {
      hoja('<h2>Ábrelo en tu navegador</h2>' +
        '<p>Estás viendo esto dentro de otra app (WhatsApp, Instagram…), y desde ahí no se puede instalar.</p>' +
        '<ol><li>Pulsa ' + TRES + ' o el botón de menú de arriba.</li>' +
        '<li>Elige <b>Abrir en el navegador</b> (o «Abrir en Chrome» / «Abrir en Safari»).</li>' +
        '<li>Allí, vuelve a pulsar <b>Instalar</b>.</li></ol>' +
        '<p style="margin:0 0 10px">O copia el enlace y pégalo en Chrome o Safari:</p>' +
        '<div class="fila" style="margin-bottom:10px"><button type="button" data-copia-enlace>Copiar enlace</button></div>');
      return;
    }
    if (ios && !iosSafari) {
      hoja('<h2>Ábrelo en Safari</h2><p>En el iPhone las apps de la web se instalan desde Safari.</p>' +
        '<ol><li>Copia el enlace y ábrelo en <b>Safari</b>.</li><li>Pulsa ' + COMPARTIR + ' <b>Compartir</b>.</li>' +
        '<li>Elige ' + MAS + ' <b>Añadir a pantalla de inicio</b>.</li></ol>' +
        '<div class="fila" style="margin-bottom:10px"><button type="button" data-copia-enlace>Copiar enlace</button></div>');
      return;
    }
    if (ios) {
      hoja('<h2>Instálala en tu iPhone</h2><ol>' +
        '<li>Pulsa ' + COMPARTIR + ' <b>Compartir</b>, abajo en el centro (o arriba en el iPad).</li>' +
        '<li>Baja y elige ' + MAS + ' <b>Añadir a pantalla de inicio</b>.</li>' +
        '<li>Pulsa <b>Añadir</b>. Te sale el icono de PLEA5E con tus apps.</li></ol>');
      return;
    }
    if (movil) {
      hoja('<h2>Instálala en tu móvil</h2><ol>' +
        '<li>Pulsa ' + TRES + ' arriba a la derecha de Chrome.</li>' +
        '<li>Elige <b>Instalar aplicación</b> o <b>Añadir a pantalla de inicio</b>.</li>' +
        '<li>Confirma. Te sale el icono de PLEA5E con tus apps.</li></ol>' +
        '<p style="margin:0 0 10px;color:#8B95AB;font-size:14px">Si usas el navegador de Samsung, el botón está en el menú ☰ → «Añadir página a» → «Pantalla de inicio».</p>');
      return;
    }
    hoja('<h2>Instálala en el ordenador</h2><p>En Chrome o Edge, pulsa el icono de instalar que sale a la derecha de la barra de direcciones, o el menú ⋮ → <b>Instalar PLEA5E Reseñas</b>.</p>' +
      '<p>Para tenerla en el móvil, abre esta misma página en el móvil.</p>');
  }

  function botones() { return document.querySelectorAll('[data-instalar]'); }
  function ocultaBotones() { botones().forEach(function (b) { b.classList.add('oculto'); }); }

  window.addEventListener('beforeinstallprompt', function (e) { e.preventDefault(); pendiente = e; });
  window.addEventListener('appinstalled', ocultaBotones);
  document.addEventListener('DOMContentLoaded', function () {
    if (instalada) return ocultaBotones();
    botones().forEach(function (b) {
      b.classList.remove('oculto');
      b.addEventListener('click', instala);
    });
  });

  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/analiza/sw.js', { scope: '/analiza/' }).catch(function () {});
  }
})();
