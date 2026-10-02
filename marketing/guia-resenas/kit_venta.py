"""Kit de venta PLEA5E (PDF A4, para ti, no para el cliente): el plan del dia, como
vender sin tener el producto en la mano, el guion, las objeciones, precios, como
cerrar el pedido, la hoja de pedido y el registro de visitas.

Precios: los de la web (public/index.html, CAT y ENVIO). Si cambian alli, cambialos aqui.
Nada de prometer resenas: se promete que dejarla cueste diez segundos.

Desde la raiz del repo:  python3 marketing/guia-resenas/kit_venta.py
y despues:               node marketing/guia-resenas/hacer-pdf.js kit
"""
import sys
sys.path.insert(0, 'marketing/guia-resenas')
from comun import *  # noqa

G = 'marketing/guia-resenas/'
TOTAL = 10
P = []


def cab(n, seccion):
    return (f'<div class="cab"><img src="{LOGO_CLARO}" class="cab-logo"><span>Kit de venta · {seccion}</span></div>'
            f'<div class="pie"><span>Uso interno · no se entrega al cliente</span><b>{n:02d}</b><i>/ {TOTAL:02d}</i></div>')


def placa(n): return 15 if n >= 200 else 15.5 if n >= 100 else 16.5 if n >= 50 else 19 if n >= 20 else 21 if n >= 10 else 23 if n >= 5 else 25
def stand(n): return 17 if n >= 200 else 17.5 if n >= 100 else 18.5 if n >= 50 else 21.5 if n >= 20 else 23.5 if n >= 10 else 26 if n >= 5 else 28


eur = lambda v: (f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.').replace(',00', '')) + ' €'

# 1 · PORTADA
P.append(f'''<section class="pag oscura" style="padding:22mm 18mm">
<img src="{LOGO}" style="height:11mm">
<div style="margin-top:34mm">
  <div class="etq" style="color:var(--oro)">Kit de venta · uso interno</div>
  <h1 style="font-size:70pt;line-height:1.02">Hoy<br>se <span style="color:var(--oro)">vende.</span></h1>
  <p style="font-size:13pt;color:#C9CEDA;max-width:110mm;margin-top:7mm">Todo lo que necesitas para salir a la calle: el plan, lo que hay que decir, qué contestar, los precios y cómo cerrar el pedido <b style="color:#fff">aunque el producto llegue en una semana</b>.</p>
</div>
<div style="position:absolute;right:-12mm;bottom:8mm;width:130mm;height:130mm;border-radius:50%;background:radial-gradient(circle,rgba(233,188,70,.25),transparent 65%)"></div>
{bicho('megafono-izq', 'right:10mm;bottom:26mm;width:86mm;height:100mm', '¡Vamos a por ellos!', 'der', 'right:62mm;bottom:122mm;font-size:19pt;transform:rotate(-4deg)')}
<div style="position:absolute;left:18mm;bottom:22mm;width:80mm;font-size:8pt;letter-spacing:.18em;text-transform:uppercase;color:#8C93A5;font-weight:700">Fecha<div style="border-bottom:.35mm dashed #56607A;height:10mm"></div></div>
</section>''')

# 2 · EL PLAN DEL DIA
horario = [('10:00', 'Salida', 'Primera vuelta: cafeterías y tiendas. Los bares aún están tranquilos.'),
           ('10:30 – 12:30', 'Hora buena', 'Bares y restaurantes antes del servicio: el dueño suele estar y tiene un rato.'),
           ('13:00 – 16:00', 'No entres', 'Comidas. Aprovecha para comer, mandar los diseños prometidos y apuntar las visitas.'),
           ('16:30 – 19:30', 'Hora buena', 'Segunda vuelta: bares de tarde, peluquerías, tiendas. Vuelve a los que te dijeron «pásate luego».'),
           ('20:30 en adelante', 'No entres', 'Cenas. Repaso del día, mensajes de seguimiento y preparar mañana.')]
llevar = ['Móvil cargado y batería externa', 'La web abierta en plea5e.es (productos y pedido)', 'Fotos reales: placa en la mano y expositor (en favoritos)',
          'El reel de la placa girando, descargado', 'La guía PDF lista para reenviar por WhatsApp', '10 guías impresas (para dejar)',
          '10 hojas de pedido (pág. 9) y 1 registro de visitas (pág. 10)', 'Bolígrafo', 'Bizum a mano para la fianza']
P.append(f'''<section class="pag">{cab(2, 'El plan')}
<div class="etq">El plan del día</div>
<h2>Horario, ruta<br><em>y qué llevar</em></h2>
<p class="intro" style="margin-bottom:5mm">En hostelería el cuándo lo es todo: con el local lleno nadie te escucha. Entra en las horas tranquilas y usa las de servicio para <b>mandar diseños y apuntar</b>.</p>
<table style="font-size:9pt">
  {''.join(f'<tr><th style="padding:2mm 3mm;width:34mm;font-size:9pt;letter-spacing:0;text-transform:none">{h}</th><td style="width:26mm"><span class="chip {"verde" if e == "Hora buena" else "rojo" if e == "No entres" else ""}" style="margin:0">{e}</span></td><td>{t}</td></tr>' for h, e, t in horario)}
</table>
<div class="fila" style="grid-template-columns:1.1fr 1fr;margin-top:5mm;gap:6mm;font-size:9.5pt">
  <div class="caja" style="padding:5mm"><h3>Qué llevar</h3><ul class="lista" style="gap:1.5mm;margin-top:1mm">{''.join(f'<li>{CASILLA}<span>{t}</span></li>' for t in llevar)}</ul></div>
  <div>
    <div class="caja-os"><h3>El objetivo de hoy</h3>
      <table style="margin-top:2mm"><tr><td style="background:#141B2B;color:#fff;border-color:#283049">Locales visitados</td><td style="background:#141B2B;color:var(--oro);border-color:#283049;font-family:Anton;font-size:14pt;width:18mm">15-20</td></tr>
      <tr><td style="background:#141B2B;color:#fff;border-color:#283049">Conversaciones con el dueño</td><td style="background:#141B2B;color:var(--oro);border-color:#283049;font-family:Anton;font-size:14pt">8-10</td></tr>
      <tr><td style="background:#141B2B;color:#fff;border-color:#283049">Diseños prometidos</td><td style="background:#141B2B;color:var(--oro);border-color:#283049;font-family:Anton;font-size:14pt">4-5</td></tr>
      <tr><td style="background:#141B2B;color:#fff;border-color:#283049">Pedidos con fianza</td><td style="background:#141B2B;color:var(--oro);border-color:#283049;font-family:Anton;font-size:14pt">1-2</td></tr></table>
      <p style="font-size:8.5pt;margin-top:2.5mm">Es una meta tuya, orientativa. El primer día se aprende más de lo que se vende.</p></div>
    <div class="caja" style="margin-top:4mm;padding:4.5mm"><h3>La ruta</h3><p>Una sola zona, a pie: una calle de bares o una plaza. Mejor 20 locales en 1 km que 5 en coche.</p></div>
  </div>
</div>
</section>''')

# 3 · VENDER SIN TENER EL PRODUCTO
P.append(f'''<section class="pag">{cab(3, 'Sin producto en la mano')}
<div class="etq">La clave de hoy</div>
<h2>Vender lo que llega<br><em>en una semana</em></h2>
<p class="intro">No llevas la placa, y no pasa nada: <b>cada placa se hace para ese local</b>, con su logo y sus colores. Nadie compra una placa de otro bar. Lo que vendes es <b>su</b> placa, y esa todavía no existe para nadie.</p>
<div class="fila" style="grid-template-columns:repeat(4,1fr);gap:4mm">
  {''.join(f'<div class="caja" style="padding:5mm"><span class="paso-n">{i}</span><h3 style="margin-top:3mm;font-size:12pt">{a}</h3><p style="font-size:9.3pt">{b}</p></div>' for i, (a, b) in enumerate([
      ('Su ficha', 'Búscale en Google Maps delante de él: sus reseñas, su nota y las del de al lado. Eso convence más que cualquier placa.'),
      ('Las fotos', 'La placa en la mano y el expositor: son reales. Y el reel de la placa girando.'),
      ('La demo', 'En plea5e.es, «Toca. Escribe. Ya está.»: ve en tu móvil lo que verá su cliente.'),
      ('La guía', 'Enséñale la guía impresa: no le vendes una placa, le enseñas a conseguir reseñas.')], 1))}
</div>
<div class="caja-os" style="margin-top:8mm;position:relative;padding-right:62mm;min-height:66mm">
  <span class="chip">La jugada</span>
  <h3 style="font-size:17pt">«Te hago el diseño y te lo mando esta tarde»</h3>
  <p>Hazle una foto a su logo (el cartel, la carta o su Instagram) y apunta sus colores. Esa misma tarde le mandas por WhatsApp <b style="color:#fff">cómo quedaría SU placa</b>. Ver su logo en la placa es lo que cierra la venta.</p>
  <p style="margin-top:2mm">Así el «ya lo pienso» se convierte en «mándamelo y lo vemos».</p>
  {bicho('tachan-izq', 'right:4mm;bottom:-4mm;width:56mm;height:62mm')}
</div>
<div class="fila" style="grid-template-columns:1fr 1fr;gap:6mm;margin-top:7mm">
  <div><h3>El plazo, claro</h3><p>Desde que aprueba el diseño: <b>de 2 a 7 días laborables de preparación y de 1 a 3 de envío</b>. Dile «en torno a una semana» y, si lo pregunta, el rango exacto. No prometas un día fijo.</p></div>
  <div><h3>La confianza</h3><p><b>No se imprime nada sin su visto bueno.</b> La fianza va dentro del precio, no se suma. Y las placas: pago único. Esas tres frases quitan casi todos los miedos.</p></div>
</div>
</section>''')

# 4 · EL GUION
guion = [('Entrar', '5 s', 'Local tranquilo. Pregunta por el dueño o el encargado. Si no está: «¿Cuándo le pillo?» y apúntalo.', None),
         ('Presentarte', '10 s', 'Sonríe, corto y de tú a tú.', 'Hola, soy [tu nombre], de PLEA5E, de aquí de Córdoba. ¿Tienes un minuto? Es sobre tus reseñas de Google.'),
         ('Su ficha', '20 s', 'Móvil en la mano, Google Maps, su local. Enséñale la pantalla.', 'Mira: tienes 86 reseñas y un 4,4. ¿Tus clientes salen contentos? ¿Y cuántos te lo ponen aquí?'),
         ('El problema', '10 s', 'Que asienta. Casi siempre te dará la razón.', 'Pasa en todos los sitios: los contentos no escriben, se les olvida. Y el que se queja sí se acuerda.'),
         ('La solución', '20 s', 'Fotos reales y la demo de la web.', 'Esto va en la mesa, con tu logo. El cliente acerca el móvil y se le abre directamente la ventana para escribirte la reseña. Sin buscarte y sin apps: diez segundos.'),
         ('Lo que le diferencia', '10 s', 'Saca la guía.', 'Y no es solo la placa: te doy esta guía para ti y tu equipo, cuándo pedirla y qué decir. Con eso es con lo que se nota.'),
         ('El precio', '10 s', 'Sin rodeos, y luego calla.', 'Cada placa, con tu diseño, desde 25 €, y baja si pides más. Las placas: pago único.'),
         ('El cierre', '10 s', 'Siempre una pregunta que se conteste con un sí fácil.', '¿Te hago el diseño con tu logo y te lo mando esta tarde por WhatsApp? Si te gusta, lo pedimos y en una semana lo tienes.')]
P.append(f'''<section class="pag">{cab(4, 'El guion')}
<div class="etq">El guion · 90 segundos</div>
<h2>Qué decir,<br><em>paso a paso</em></h2>
<div class="lista" style="gap:3.2mm">
  {''.join(f'<div style="display:grid;grid-template-columns:10mm 34mm 1fr;gap:3mm;align-items:start;border-bottom:.3mm solid var(--linea);padding-bottom:3mm"><span class="paso-n">{i}</span><div><b style="font-size:10.5pt">{a}</b><div class="nota">{t}</div></div><div><p style="font-size:9.2pt;color:var(--gris)">{c}</p>' + (f'<p class="cita" style="font-size:14.5pt;margin-top:1mm">{d}</p>' if d else '') + '</div></div>' for i, (a, t, c, d) in enumerate(guion, 1))}
</div>
<p class="nota" style="margin-top:4mm">Los números de la ficha (86 reseñas, 4,4) son de ejemplo: di los suyos de verdad. Nunca le prometas cuántas reseñas va a tener: lo que prometes es que dejarla cueste diez segundos.</p>
</section>''')

# 5 · OBJECIONES
obj = [('«No lo veo, ¿funciona esto?»', 'Normal que dudes. Mira el vídeo y lo que ve tu cliente en el móvil (la demo de la web). Y te mando el diseño sin compromiso: si no lo ves, no lo pides.'),
       ('«Es caro»', 'Es un pago único: la placa se queda en la mesa años. Y no tienes que poner todas: empieza por la barra con un expositor o por las mesas de dentro.'),
       ('«Ya tengo un QR»', 'El QR sirve, y la nuestra también lo lleva. Pero con NFC solo hay que acercar el móvil, sin abrir la cámara. Y los dos van directos a la ventana de escribir la reseña, no a tu ficha.'),
       ('«Mis clientes no lo van a usar»', 'Solos, pocos. Por eso va con la guía: cuando tu camarero lo pide al cobrar, ya tienen el móvil en la mano. La placa es para que el «vale» no se pierda.'),
       ('«No tengo sitio en las mesas»', 'Entonces el expositor en la barra o en la caja, y tarjetas para el camarero o para la terraza.'),
       ('«Me lo pienso»', 'Claro. ¿Te hago el diseño y lo piensas con él delante? Te lo mando esta tarde, sin compromiso.'),
       ('«¿Y si Google me penaliza?»', 'Lo que Google prohíbe es regalar cosas por reseñas o pedirlas solo a los contentos. La placa no hace nada de eso: solo ahorra buscarte. Viene explicado en la guía.'),
       ('«No quiero pagar por adelantado»', 'La fianza va dentro del precio y no se imprime nada sin tu visto bueno. Y el diseño primero te lo enseño gratis.'),
       ('«Ya lo haré por internet»', 'Perfecto: plea5e.es. Pero si me das tu WhatsApp, te mando el diseño y te ahorras rellenarlo.')]
P.append(f'''<section class="pag">{cab(5, 'Objeciones')}
<div class="etq">Lo que te van a decir</div>
<h2>Objeciones<br><em>y qué contestar</em></h2>
<p class="intro" style="margin-bottom:5mm">Primero dale la razón («normal», «claro»), luego la respuesta y acaba con una pregunta. <b>Nunca discutas.</b></p>
<div class="fila" style="grid-template-columns:1fr 1fr;gap:3.5mm">
  {''.join(f'<div class="caja" style="padding:4mm 5mm"><p style="font-weight:800;font-size:10pt;color:#8A2A1E">{o}</p><p style="font-size:9.3pt;margin-top:1.2mm">{r}</p></div>' for o, r in obj)}
  <div class="caja-os" style="position:relative;padding:4mm 5mm">{bicho('guino-izq', 'right:2mm;bottom:-2mm;width:30mm;height:34mm')}<p style="font-weight:800;color:var(--oro)">Si dice que no</p><p style="font-size:9.3pt;padding-right:26mm">«Sin problema, gracias por el rato.» Déjale la guía. Se acordará de ti.</p></div>
</div>
</section>''')

# 6 · PRECIOS
tramos = [(1, '1 a 4'), (5, '5 a 9'), (10, '10 a 19'), (20, '20 a 49'), (50, '50 a 99'), (100, '100 a 199'), (200, '200 o más')]
ejemplos = [('Cafetería pequeña', [('Expositor de pie', 1, stand(1))]),
            ('Bar con 6 mesas', [('Placa de mesa', 6, placa(6)), ('Expositor de pie', 1, stand(1))]),
            ('Restaurante con 12 mesas', [('Placa de mesa', 12, placa(12)), ('Expositor de pie', 1, stand(1))])]
filas_ej = ''
for nombre, items in ejemplos:
    total = sum(n * p for _, n, p in items)
    envio = 0 if total >= 60 else 3.99
    fianza = max(15, total * .5)
    det = ' + '.join(f'{n} × {q.lower()} a {eur(p)}' for q, n, p in items)
    filas_ej += f'<tr><td><b>{nombre}</b><br><span class="nota">{det}</span></td><td style="white-space:nowrap"><b>{eur(total)}</b></td><td>{"gratis" if not envio else eur(envio)}</td><td>{eur(fianza)}</td></tr>'
P.append(f'''<section class="pag">{cab(6, 'Precios')}
<div class="etq">Precios de la web · hoy</div>
<h2>Precios y<br><em>cuentas rápidas</em></h2>
<p class="intro" style="margin-bottom:6mm">Son los precios de lanzamiento que salen en plea5e.es. Precio por unidad, con el diseño con su marca incluido. <b>Antes de salir, mira que no hayan cambiado.</b></p>
<table>
  <tr><th>Cantidad</th>{''.join(f'<th style="text-align:center">{t}</th>' for _, t in tramos)}</tr>
  <tr><td><b>Placa de mesa</b></td>{''.join(f'<td style="text-align:center">{eur(placa(n))}</td>' for n, _ in tramos)}</tr>
  <tr><td><b>Expositor de pie</b><br><span class="nota">76 × 118 mm</span></td>{''.join(f'<td style="text-align:center">{eur(stand(n))}</td>' for n, _ in tramos)}</tr>
</table>
<p class="nota" style="margin-top:2mm"><b>Tarjetas de mano</b> (85 × 54 mm): van en packs de 20, 30, 50 o 100. El precio exacto sale en el pedido de la web al elegir el pack.</p>
<div class="fila" style="grid-template-columns:repeat(3,1fr);gap:4mm;margin-top:6mm">
  <div class="caja" style="padding:4.5mm"><span class="chip">Envío</span><p>3,99 € a península. <b>Gratis desde 60 €.</b></p></div>
  <div class="caja" style="padding:4.5mm"><span class="chip">Fianza</span><p><b>50 % del pedido, mínimo 15 €.</b> Va dentro del precio. El resto, al aprobar el diseño.</p></div>
  <div class="caja" style="padding:4.5mm"><span class="chip">Seguimiento</span><p>Opcional: <b>35 € al mes</b>, sin permanencia. Ver cuánta gente usa cada placa.</p></div>
</div>
<div class="etq" style="margin-top:8mm">Ejemplos para decir de cabeza</div>
<table><tr><th>Local</th><th>Total</th><th>Envío</th><th>Fianza</th></tr>{filas_ej}</table>
<p class="mano" style="font-size:16pt;color:var(--oro-os);margin-top:5mm;transform:rotate(-1deg)">Truco: el pedido de la web calcula todo solo. Si dudas, móntalo delante de él en plea5e.es → Pedido.</p>
</section>''')

# 7 · CERRAR EL PEDIDO
pasos = [('Foto del logo', 'Del cartel, la carta, una servilleta o su Instagram. Si está en mala calidad, lo redibujamos gratis.'),
         ('Sus colores y su texto', 'Por defecto: «¡Nos encantaría tu reseña en Google!». Pregunta si quiere otro.'),
         ('Su ficha de Google', 'El nombre exacto en Google Maps (o el enlace). Es a donde llevará la placa. Si prefiere Tripadvisor, se puede.'),
         ('Qué y cuántos', 'Placas, expositores o tarjetas. Cuenta las mesas con él.'),
         ('WhatsApp y dirección', 'Su número para mandarle el diseño y la dirección de envío.'),
         ('La fianza', 'Cuando apruebe el diseño (o en el momento, si lo quiere ya): 50 %, mínimo 15 €, por Bizum o desde la web.')]
P.append(f'''<section class="pag">{cab(7, 'Cerrar el pedido')}
<div class="etq">Cuando dice que sí</div>
<h2>Cómo cerrar<br><em>el pedido ahí mismo</em></h2>
<p class="intro" style="margin-bottom:6mm">Con la hoja de pedido (pág. 9) delante: rellénala con él en dos minutos. Lo que necesitas:</p>
<div class="lista" style="gap:3.5mm">
  {''.join(f'<div style="display:flex;gap:4mm;align-items:flex-start"><span class="paso-n">{i}</span><div><b>{a}</b><p style="font-size:9.8pt;color:#383D49">{b}</p></div></div>' for i, (a, b) in enumerate(pasos, 1))}
</div>
<div class="fila" style="grid-template-columns:1fr 1fr;gap:5mm;margin-top:7mm">
  <div class="caja"><h3>Y después</h3><ul class="lista" style="gap:2mm">
    <li>{CASILLA}<span>Esa tarde: el diseño por WhatsApp.</span></li>
    <li>{CASILLA}<span>Cambios hasta que le guste.</span></li>
    <li>{CASILLA}<span>Aprueba: fianza y resto según condiciones.</span></li>
    <li>{CASILLA}<span>A fabricar: 2-7 días + 1-3 de envío.</span></li>
    <li>{CASILLA}<span>Al llegar: pásate a probarla con él. Ahí le enseñas la guía otra vez y le pides que te deje una reseña a ti.</span></li></ul></div>
  <div class="caja-os" style="position:relative;min-height:70mm"><h3>Pásate a instalarla</h3><p style="padding-right:2mm">Es lo que ninguna tienda online hace: la llevas, la pegáis juntos, la probáis y le explicas la guía a su equipo en 5 minutos. <b style="color:#fff">Así vuelve a pedirte</b> y te recomienda al de al lado.</p>
    {bicho('pulgar-izq', 'right:3mm;bottom:-3mm;width:34mm;height:40mm')}</div>
</div>
</section>''')

# 8 · MENSAJES DE WHATSAPP
msgs = [('Esa misma tarde', 'Hola, [nombre]. Soy [tu nombre], de PLEA5E, nos vimos esta mañana en [local]. Aquí tienes cómo quedaría tu placa 👇 ¿Qué te parece? Si quieres cambiar algo, me dices. Te dejo también la guía para pedir reseñas.'),
        ('A los 2 días, si no contesta', 'Hola, [nombre]. ¿Pudiste ver el diseño? Si quieres lo ajustamos. Y si ahora no es el momento, sin problema: aquí me tienes.'),
        ('Cuando aprueba', '¡Genial! Para ponernos: la fianza son [importe] por Bizum al 661 40 32 19, concepto [local]. Va dentro del precio. En cuanto llegue, a fabricar: en torno a una semana la tienes.'),
        ('Cuando la recibe', '¿Qué tal la placa? Si me dices una hora, me paso a probarla contigo y le explico al equipo cómo pedir las reseñas. Son cinco minutos.'),
        ('Pedirle una reseña a él', 'Me alegra que te haya gustado. Si te apetece contarlo, me ayuda mucho una reseña de PLEA5E en Google: [enlace]. ¡Gracias!')]
P.append(f'''<section class="pag">{cab(8, 'Mensajes')}
<div class="etq">Seguimiento</div>
<h2>Mensajes listos<br><em>para WhatsApp</em></h2>
<p class="intro" style="margin-bottom:6mm">La venta casi nunca se cierra en la puerta: se cierra en el WhatsApp de esa tarde. Copia, cambia lo de los corchetes y manda.</p>
<div class="lista" style="gap:4mm">
  {''.join(f'<div class="caja" style="padding:4.5mm 5.5mm;display:grid;grid-template-columns:38mm 1fr;gap:4mm;align-items:center"><span class="chip" style="margin:0;text-align:center">{t}</span><p style="font-size:9.8pt;background:#DCF8C6;border-radius:2.5mm;padding:3mm 4mm;color:#1b1b1b">{m}</p></div>' for t, m in msgs)}
</div>
<p class="nota" style="margin-top:4mm">Guarda estos mensajes como respuestas rápidas en WhatsApp Business: así los tienes a dos toques.</p>
</section>''')

# 9 · HOJA DE PEDIDO (para imprimir varias)
campo = lambda t, w='1fr': f'<div><div style="font-size:7.5pt;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--gris)">{t}</div><div class="linea-rell" style="height:8mm"></div></div>'
P.append(f'''<section class="pag">{cab(9, 'Hoja de pedido')}
<div style="display:flex;justify-content:space-between;align-items:flex-end">
  <div><div class="etq">Imprime varias</div><h2 style="margin-bottom:2mm">Hoja de pedido</h2></div>
  <div style="text-align:right" class="nota">Nº ______ · Fecha ___ / ___ / ______</div>
</div>
<div class="fila" style="grid-template-columns:1fr 1fr;gap:1mm 8mm">
  {campo('Negocio')}{campo('Persona de contacto')}{campo('WhatsApp')}{campo('Correo (opcional)')}
</div>
{campo('Dirección de envío')}
{campo('Nombre exacto en Google Maps (o enlace)')}
<div class="etq" style="margin-top:6mm">Qué quiere</div>
<table><tr><th>Producto</th><th style="width:26mm">Cantidad</th><th style="width:30mm">Precio/ud</th><th style="width:30mm">Total</th></tr>
  <tr><td>Placa de mesa</td><td></td><td></td><td></td></tr>
  <tr><td>Expositor de pie (76 × 118 mm)</td><td></td><td></td><td></td></tr>
  <tr><td>Tarjetas de mano (pack de ___ )</td><td></td><td></td><td></td></tr>
  <tr><td style="text-align:right" colspan="3"><b>Envío</b> (3,99 € · gratis desde 60 €)</td><td></td></tr>
  <tr><td style="text-align:right" colspan="3"><b>TOTAL</b></td><td></td></tr>
</table>
<div class="etq" style="margin-top:6mm">El diseño</div>
<div class="fila" style="grid-template-columns:1fr 1fr;gap:3mm 8mm">
  <div style="display:flex;gap:2mm;align-items:center">{CASILLA}<span>Foto del logo hecha</span></div>
  <div style="display:flex;gap:2mm;align-items:center">{CASILLA}<span>Lo redibujamos (mala calidad)</span></div>
  {campo('Colores')}{campo('Lleva a: Google / Tripadvisor / otro')}
</div>
{campo('Texto de la placa (por defecto: ¡Nos encantaría tu reseña en Google!)')}
<div class="etq" style="margin-top:6mm">Pago</div>
<div class="fila" style="grid-template-columns:1fr 1fr 1fr;gap:3mm 6mm">
  {campo('Fianza (50 %, mín. 15 €)')}
  <div style="display:flex;gap:2mm;align-items:center;padding-top:4mm">{CASILLA}<span>Pagada por Bizum</span></div>
  <div style="display:flex;gap:2mm;align-items:center;padding-top:4mm">{CASILLA}<span>Diseño aprobado</span></div>
</div>
<p class="nota" style="margin-top:5mm">No se imprime nada sin el visto bueno del cliente. La fianza va dentro del precio. Plazo desde la aprobación: 2-7 días laborables de preparación + 1-3 de envío. PLEA5E · plea5e.es · WhatsApp 661 40 32 19.</p>
</section>''')

# 10 · REGISTRO DE VISITAS
filas = ''.join('<tr>' + '<td style="height:10.6mm"></td>' * 6 + '</tr>' for _ in range(16))
P.append(f'''<section class="pag">{cab(10, 'Registro')}
<div class="etq">Apunta cada visita</div>
<h2 style="margin-bottom:3mm">Registro de visitas</h2>
<p class="nota" style="margin-bottom:4mm">Interés: A (quiere diseño) · B (volver a pasar) · C (no). El «próximo paso» con fecha: sin fecha, se olvida.</p>
<table style="font-size:8.5pt"><tr><th style="width:38mm">Local</th><th style="width:26mm">Con quién</th><th style="width:28mm">WhatsApp</th><th style="width:14mm">Int.</th><th>Próximo paso</th><th style="width:18mm">Fecha</th></tr>{filas}</table>
</section>''')

assert len(P) == TOTAL
open(G + 'kit-venta.html', 'w').write(html('PLEA5E · Kit de venta', '', P))
print(TOTAL, 'paginas')
