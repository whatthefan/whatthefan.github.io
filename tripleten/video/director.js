// Guion del vídeo de demo. Se inyecta en la página durante la grabación
// (grabar.js) y se ejecuta con el reloj virtual de Playwright: cada espera y
// cada animación avanza fotograma a fotograma, así que el vídeo sale igual
// en cada grabación.
(function () {
  "use strict";

  var rec = (window.__rec = { chapters: [], sfx: [], done: false, t0: 0 });
  // Mismo guion en los dos idiomas: la página decide con ?lang=.
  var EN = document.documentElement.lang === "en";
  var T = function (es, en) { return EN ? en : es; };
  // Cada efecto de sonido queda apuntado con su instante; sonido.py los
  // sintetiza y los mezcla con el vídeo.
  function sound(name, extra) {
    if (!rec.t0) return;
    var e = { n: name, t: Math.round(performance.now() - rec.t0) / 1000 };
    if (extra) for (var k in extra) e[k] = extra[k];
    rec.sfx.push(e);
  }
  window.__sfx = function (name) { sound(name); };
  var $ = function (s) { return document.querySelector(s); };
  var sleep = function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); };
  var ease = function (t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
  function tween(dur, fn) {
    return new Promise(function (res) {
      var t0 = performance.now();
      (function f() {
        var p = Math.min(1, (performance.now() - t0) / dur);
        fn(ease(p));
        if (p < 1) requestAnimationFrame(f); else res();
      })();
    });
  }

  // El scroll suave del navegador va en tiempo real; lo sustituimos por uno
  // que avanza con el reloj virtual.
  var nativeScrollTo = window.scrollTo.bind(window);
  function scrollY(top, dur) {
    var max = document.documentElement.scrollHeight - innerHeight;
    top = Math.max(0, Math.min(max, top));
    var y0 = window.pageYOffset;
    return tween(dur || 800, function (e) { nativeScrollTo(0, y0 + (top - y0) * e); });
  }
  window.scrollTo = function (a, b) {
    if (a && typeof a === "object") { if (a.behavior === "smooth") { scrollY(a.top, 700); return; } return nativeScrollTo(0, a.top); }
    return nativeScrollTo(a, b);
  };
  function scrollToEl(sel, offset, dur) {
    var el = typeof sel === "string" ? $(sel) : sel;
    return scrollY(el.getBoundingClientRect().top + window.pageYOffset - (offset === undefined ? 150 : offset), dur);
  }

  // ---------- Capa de vídeo ----------
  var css = document.createElement("style");
  css.textContent = [
    "html{scroll-behavior:auto!important}",
    "#vCap{position:fixed;z-index:200;left:14px;right:14px;top:74px;padding:14px 16px;border-radius:18px;background:rgba(6,12,9,.92);border:1px solid rgba(57,255,136,.55);box-shadow:0 18px 50px rgba(0,0,0,.6),0 0 30px rgba(57,255,136,.18);opacity:0;transform:translateY(-14px) scale(.98);transition:opacity .35s ease,transform .45s cubic-bezier(.2,.9,.25,1.2)}",
    "#vCap.on{opacity:1;transform:none}",
    "#vCap small{display:inline-block;padding:3px 9px;border-radius:999px;background:#39ff88;color:#03140a;font:700 12px/1.3 'JetBrains Mono',monospace;letter-spacing:.06em}",
    "#vCap b{display:block;margin-top:7px;color:#f1f5f2;font:700 23px/1.2 'Space Grotesk',sans-serif;letter-spacing:-.01em}",
    "#vCap span{display:block;margin-top:4px;color:#aeb8b2;font:500 15px/1.35 Inter,sans-serif}",
    "#vFinger{position:fixed;z-index:210;left:0;top:0;width:46px;height:46px;margin:-23px 0 0 -23px;border-radius:50%;background:rgba(255,255,255,.28);border:3px solid #fff;box-shadow:0 6px 18px rgba(0,0,0,.45),0 0 0 6px rgba(57,255,136,.25);opacity:0;transition:opacity .3s,transform .15s ease}",
    "#vFinger.on{opacity:1}#vFinger.down{transform:scale(.78);background:rgba(57,255,136,.6)}",
    ".vRipple{position:fixed;z-index:205;width:46px;height:46px;margin:-23px 0 0 -23px;border-radius:50%;border:3px solid #39ff88;pointer-events:none;animation:vRip .6s ease-out forwards}",
    "@keyframes vRip{from{transform:scale(.6);opacity:1}to{transform:scale(2.4);opacity:0}}",
    "#vBar{position:fixed;z-index:220;left:0;bottom:0;height:4px;width:0;background:linear-gradient(90deg,#00e5a0,#39ff88);box-shadow:0 0 12px #39ff88}",
    ".vScreen{position:fixed;inset:0;z-index:230;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:40px 30px;background:radial-gradient(120% 70% at 50% 0%,rgba(57,255,136,.28),transparent 60%),#04060a;opacity:0;transition:opacity .6s ease;pointer-events:none}",
    ".vScreen.on{opacity:1}",
    ".vScreen .nv{width:150px;height:150px;animation:vBob 2.4s ease-in-out infinite;filter:drop-shadow(0 0 30px rgba(57,255,136,.5))}",
    "@keyframes vBob{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}",
    ".vScreen h1{margin:26px 0 0;font:700 44px/1.02 'Space Grotesk',sans-serif;letter-spacing:-.035em;color:#f1f5f2}",
    ".vScreen h1 em{font-style:normal;color:#39ff88;text-shadow:0 0 30px rgba(57,255,136,.5)}",
    ".vScreen p{margin:18px 0 0;color:#aeb8b2;font:500 19px/1.4 Inter,sans-serif}",
    ".vScreen .tag{margin-top:26px;padding:8px 16px;border-radius:999px;border:1px solid rgba(57,255,136,.5);color:#39ff88;font:600 14px Inter,sans-serif;letter-spacing:.08em;text-transform:uppercase}",
    ".vScreen .cta{margin-top:30px;padding:20px 30px;white-space:nowrap;border-radius:18px;background:#fff;color:#03140a;font:700 26px 'Space Grotesk',sans-serif;box-shadow:0 0 0 7px rgba(57,255,136,.18),0 0 50px rgba(57,255,136,.5)}",
    ".vScreen ul{list-style:none;margin:28px 0 0;padding:0;display:grid;gap:12px;text-align:left}",
    ".vScreen li{display:flex;gap:12px;align-items:center;color:#e3ebe6;font:500 18px Inter,sans-serif;opacity:0;transform:translateY(10px);transition:all .5s ease}",
    ".vScreen li.on{opacity:1;transform:none}",
    ".vScreen li i{flex-shrink:0;width:26px;height:26px;border-radius:50%;background:#39ff88;color:#03140a;display:grid;place-items:center;font:700 15px Inter,sans-serif;font-style:normal}",
    EN ? ".vScreen h1{font-size:40px}.vScreen .cta{font-size:22px;padding:18px 24px}" : "",
    ".vScreen .foot{position:absolute;bottom:34px;left:0;right:0;color:#5d6761;font:500 13px Inter,sans-serif}"
  ].join("\n");
  document.head.appendChild(css);

  var cap = document.createElement("div"); cap.id = "vCap"; cap.innerHTML = "<small></small><b></b><span></span>"; document.body.appendChild(cap);
  var finger = document.createElement("div"); finger.id = "vFinger"; document.body.appendChild(finger);
  var bar = document.createElement("div"); bar.id = "vBar"; document.body.appendChild(bar);
  var novaSvg = document.querySelector("#nova svg").outerHTML.replace("<svg ", '<svg class="nv" ');
  var fx = innerWidth / 2, fy = innerHeight * 0.7;
  finger.style.transform = "";
  function fx0() { return fx / innerWidth; }
  function placeFinger() { finger.style.left = fx + "px"; finger.style.top = fy + "px"; }
  placeFinger();

  var TOTAL = 104000;
  function chapter(name) { rec.chapters.push({ name: name, t: Math.round((performance.now() - rec.t0) / 100) / 10 }); }
  async function caption(step, title, text) {
    if (cap.classList.contains("on")) { cap.classList.remove("on"); await sleep(260); }
    sound("whoosh");
    cap.querySelector("small").textContent = step;
    cap.querySelector("b").textContent = title;
    cap.querySelector("span").textContent = text || "";
    cap.querySelector("span").style.display = text ? "" : "none";
    cap.classList.add("on");
  }
  function hideCaption() { cap.classList.remove("on"); }
  async function point(target, dx, dy, dur) {
    var el = typeof target === "string" ? $(target) : target;
    var r = el.getBoundingClientRect();
    var tx = r.left + r.width / 2 + (dx || 0), ty = r.top + r.height / 2 + (dy || 0);
    finger.classList.add("on");
    var x0 = fx, y0 = fy;
    await tween(dur || 650, function (e) { fx = x0 + (tx - x0) * e; fy = y0 + (ty - y0) * e; placeFinger(); });
  }
  async function tap(target, dx, dy) {
    var el = typeof target === "string" ? $(target) : target;
    await point(el, dx, dy);
    finger.classList.add("down");
    sound(el.tagName === "INPUT" ? "tapsoft" : "tap", { x: Math.round(fx0() * 100) / 100 });
    var rp = document.createElement("div"); rp.className = "vRipple"; rp.style.left = fx + "px"; rp.style.top = fy + "px"; document.body.appendChild(rp);
    setTimeout(function () { rp.remove(); }, 700);
    await sleep(140);
    if (el.tagName === "INPUT") el.focus(); else el.click();
    finger.classList.remove("down");
    await sleep(160);
  }
  async function type(sel, text, gap) {
    var el = $(sel);
    await tap(el);
    for (var i = 0; i < text.length; i++) {
      el.value = el.value + text.charAt(i);
      window.__sfxKey();
      try { el.setSelectionRange(el.value.length, el.value.length); } catch (e) {}
      el.dispatchEvent(new Event("input", { bubbles: true }));
      await sleep(gap || 120);
    }
    el.blur();
  }
  async function screen(html, ms) {
    var s = document.createElement("div"); s.className = "vScreen"; s.innerHTML = html; document.body.appendChild(s);
    await sleep(30); s.classList.add("on");
    var lis = s.querySelectorAll("li");
    for (var i = 0; i < lis.length; i++) { await sleep(i ? 420 : 700); lis[i].classList.add("on"); sound("li", { i: i }); }
    await sleep(ms);
    return s;
  }
  window.__sfxKey = function () { sound("key"); };
  async function closeScreen(s) { s.classList.remove("on"); await sleep(650); s.remove(); }

  (function progress() {
    bar.style.width = Math.min(100, ((performance.now() - rec.t0) / TOTAL) * 100) + "%";
    if (!rec.done) requestAnimationFrame(progress);
  })();

  window.__startDirector = async function () {
    rec.t0 = performance.now();

    // ---------- Intro ----------
    chapter("intro");
    sound("intro");
    var intro = await screen(novaSvg + T('<h1>¿En cuántos meses se <em>paga sola</em> tu carrera en Tech?</h1><p>Te lo enseño paso a paso.<br>Sin registro. Desde tu móvil.</p>', '<h1>How many months until your tech career <em>pays for itself</em>?</h1><p>I\'ll show you step by step.<br>No sign-up. Right from your phone.</p>') + '<div class="tag">Career ROI Lab · TripleTen</div>', 3600);
    sound("swoosh");
    await closeScreen(intro);

    // ---------- 1. Perfil ----------
    chapter("perfil");
    await scrollToEl("#perfil", 140, 900);
    await caption(T("PASO 1 DE 5", "STEP 1 OF 5"), T("Cuéntame de dónde vienes", "Tell me where you're coming from"), T("Tu nombre, tu sector y lo que te hace ilusión", "Your name, your field and what excites you"));
    await sleep(400);
    await type("#name", "Laura", 130);
    await sleep(500);
    await tap('#jobs .chip[data-id="hosteleria"]');
    await sleep(1500);
    await scrollToEl("#interests", 200, 700);
    await tap('#interests .chip[data-id="break"]');
    await sleep(700);
    await tap('#interests .chip[data-id="automate"]');
    await sleep(900);
    await caption(T("PASO 1 DE 5", "STEP 1 OF 5"), T("Tu programa ideal, y por qué", "Your ideal program, and why"), T("Encaje calculado con tu perfil", "Fit calculated from your profile"));
    await scrollToEl("#matchCard", 170, 1000);
    await point("#matchPct", 0, 0, 700);
    await sleep(2200);
    await point("#matchReasons", -60, 0, 600);
    await sleep(1400);
    await tap("#useMatch");
    await sleep(1100);

    // ---------- 2. Números ----------
    chapter("numeros");
    await caption(T("PASO 2 DE 5", "STEP 2 OF 5"), T("Pon tu sueldo actual", "Enter your current salary"), T("Precio y salario del programa ya vienen rellenos", "The program's price and salary are already filled in"));
    await scrollToEl("#current", 260, 700);
    await type("#current", "24000", 150);
    await sleep(500);
    await caption(T("PASO 2 DE 5", "STEP 2 OF 5"), T("Y pulsa el botón gigante", "And hit the big button"), "");
    await scrollToEl("#calcBtn", 380, 600);
    await tap("#calcBtn");
    finger.classList.remove("on");
    await sleep(900);
    await scrollToEl("#resultCol", 232, 600);
    await caption(T("PASO 2 DE 5", "STEP 2 OF 5"), T("Meses exactos para recuperar tu inversión", "Exact months to earn back your investment"), T("Con tu nombre, tu fecha y tu subida al mes", "With your name, your date and your monthly raise"));
    await sleep(3600);
    await scrollToEl("#chartCard", 190, 900);
    await caption(T("PASO 2 DE 5", "STEP 2 OF 5"), T("Tu dinero, mes a mes", "Your money, month by month"), T("Desliza el dedo: ves cuándo empiezas a ganar", "Drag your finger: see when you start coming out ahead"));
    var hit = $("#hit"), r = hit.getBoundingClientRect(), cy = r.top + r.height * 0.55;
    await point(hit, -r.width / 2 + 10, r.height * 0.05, 500);
    finger.classList.add("down");
    sound("scrub", { d: 2.2 });
    await tween(2200, function (e) {
      fx = r.left + 10 + (r.width - 20) * e; fy = cy; placeFinger();
      hit.dispatchEvent(new PointerEvent("pointermove", { clientX: fx, clientY: fy, bubbles: true }));
    });
    finger.classList.remove("down");
    hit.dispatchEvent(new PointerEvent("pointerleave", { bubbles: true }));
    await sleep(300);
    finger.classList.remove("on");
    await caption(T("TU VIAJE", "YOUR JOURNEY"), T("Fecha a fecha, hasta tu nueva vida", "Date by date, to your new life"), T("Nova te acompaña por cada hito", "Nova walks you through every milestone"));
    await scrollToEl("#viaje", 70, 900);
    await scrollY(window.pageYOffset + 520, 2600);
    await sleep(600);

    // ---------- 3. Semana ----------
    chapter("semana");
    await caption(T("PASO 3 DE 5", "STEP 3 OF 5"), T("Encaja 20 h en tu semana", "Fit 20 h into your week"), T("Toca tus huecos libres, sin dejar tu trabajo", "Tap your free slots, without quitting your job"));
    await scrollToEl("#week", 250, 900);
    await tap('#presets .chip[data-i="0"]');
    await sleep(900);
    await tap('.slot[data-k="5t"]');
    await sleep(500);
    await tap('.slot[data-k="6t"]');
    await sleep(1500);
    await caption(T("PASO 3 DE 5", "STEP 3 OF 5"), T("Y llévalo a tu calendario", "And send it to your calendar"), T("Tus sesiones de estudio, cada semana", "Your study sessions, every week"));
    await scrollToEl("#icsWeek", 420, 700);
    await tap("#icsWeek");
    await sleep(1200);

    // ---------- 4. Recompensa ----------
    chapter("recompensa");
    await caption(T("PASO 4 DE 5", "STEP 4 OF 5"), T("¿Qué harás con la diferencia?", "What will you do with the difference?"), T("Cada sueño, en meses de subida", "Every dream, in months of your raise"));
    await scrollToEl("#dreams", 250, 900);
    await tap('.dream[data-id="viaje"]');
    await sleep(900);
    await tap('.dream[data-id="portatil"]');
    await sleep(900);
    await scrollToEl("#dreamTotal", 420, 700);
    finger.classList.remove("on");
    await sleep(1400);

    // ---------- 5. Tarjeta ----------
    chapter("tarjeta");
    await caption(T("PASO 5 DE 5", "STEP 5 OF 5"), T("Tu tarjeta, lista para compartir", "Your card, ready to share"), T("Hecha con tus datos, para post o story", "Made with your numbers, for a post or a story"));
    await scrollToEl("#cardPreview", 222, 900);
    await sleep(2000);
    await scrollToEl(".seg", 380, 600);
    await caption(T("PASO 5 DE 5", "STEP 5 OF 5"), T("Post o story, tú eliges", "Post or story, your choice"), T("1080 px, lista para subir", "1080 px, ready to post"));
    await tap('.seg button[data-fmt="story"]');
    await sleep(300);
    finger.classList.remove("on");
    await scrollToEl("#cardPreview", 222, 700);
    await sleep(1600);
    await scrollToEl(".seg", 380, 700);
    await tap("#dlCard");
    await sleep(700);
    await tap("#icsDates");
    await sleep(1200);

    // ---------- Nova responde ----------
    chapter("nova");
    await caption(T("PREGÚNTALE A NOVA", "ASK NOVA"), T("Tu asistente, con datos reales", "Your assistant, with real data"), T("Precios, garantía, horarios… y tu propio plan", "Prices, the guarantee, schedules… and your own plan"));
    await tap("#nova");
    await sleep(1400);
    hideCaption();
    await sleep(300);
    var chips = document.querySelectorAll("#chatQuick button"), gBtn = null;
    for (var ci = 0; ci < chips.length; ci++) if (/garant|guarant/i.test(chips[ci].textContent)) gBtn = chips[ci];
    if (gBtn) { await tap(gBtn); }
    await sleep(3400);
    await type("#chatInput", T("¿Cuánto cuesta QA?", "How much does QA cost?"), 70);
    await tap("#chatSend");
    await sleep(3600);
    await tap("#chatClose");
    await sleep(400);

    // ---------- Lo que aporta TripleTen ----------
    chapter("tripleten");
    finger.classList.remove("on");
    await caption("TRIPLETEN", T("Y no lo haces en solitario", "You won't do it alone"), T("Esto es lo que te aporta TripleTen", "Here's what TripleTen gives you"));
    await scrollToEl(".features", 200, 1000);
    await sleep(1800);
    await scrollY(window.pageYOffset + 380, 1600);
    await sleep(1400);

    // ---------- Growth mode ----------
    chapter("growth");
    await caption(T("PARA EL EQUIPO", "FOR THE TEAM"), "Growth mode", T("Lead score, eventos y embudo en directo", "Lead score, events and funnel, live"));
    await tap("#growthBtn");
    await sleep(3200);
    await tap("#drawerClose");
    await sleep(300);

    // ---------- EE. UU. y México ----------
    chapter("mercados");
    await caption(T("DATOS REALES", "REAL DATA"), T("EE. UU. y México", "US and Mexico"), T("Precios, sueldos y garantía de cada país", "Prices, salaries and guarantee by country"));
    await scrollY(0, 1200);
    await scrollToEl("#market", 330, 600);
    await tap('#market button[data-m="mx"]');
    await sleep(700);
    await scrollY(0, 700);
    await sleep(2600);
    hideCaption();
    finger.classList.remove("on");
    await sleep(300);

    // ---------- Cierre ----------
    chapter("cierre");
    sound("outro");
    var outro = await screen(novaSvg + T('<h1>Tu plan ya existe.<br><em>Solo falta empezar.</em></h1><ul><li><i>✓</i>Programa elegido para ti</li><li><i>✓</i>Coach de carrera y bolsa de empleo</li><li><i>✓</i>Garantía de empleo de 10 meses</li><li><i>✓</i>20 h/semana, sin dejar tu trabajo</li></ul><div class="cta">Cambia tu carrera hoy →</div><div class="foot">Career ROI Lab · concepto independiente para TripleTen</div>', '<h1>Your plan already exists.<br><em>All that\'s left is to start.</em></h1><ul><li><i>✓</i>A program picked for you</li><li><i>✓</i>Career coaching and a job board</li><li><i>✓</i>10-month job guarantee</li><li><i>✓</i>20 h/week, without quitting your job</li></ul><div class="cta">Change your career today →</div><div class="foot">Career ROI Lab · independent concept for TripleTen</div>'), 3600);
    rec.done = true;
  };
})();
