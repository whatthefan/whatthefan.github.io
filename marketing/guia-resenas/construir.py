"""Guia PLEA5E "Como conseguir mas resenas en Google" (PDF A4, 18 paginas).

Para el cliente: se deja impresa o se manda por WhatsApp. Estrellita la cuenta como
un guia, con bocadillos. Portada y contraportada en noche; dentro, crema (se imprime bien).

Reglas del texto: no se promete ninguna cifra de resenas; lo que se dice de Google es lo
de sus normas (pedir a todos, nada a cambio, nada de resenas propias ni de puestos para
escribirlas en el local). Los datos de producto, los de la web.

Desde la raiz del repo:  python3 marketing/guia-resenas/construir.py
y despues:               node marketing/guia-resenas/hacer-pdf.js guia
"""
import sys
sys.path.insert(0, 'marketing/guia-resenas')
from comun import *  # noqa

G = 'marketing/guia-resenas/'
TOTAL = 18
P = []


def cab(n, seccion):
    return (f'<div class="cab"><img src="{LOGO_CLARO}" class="cab-logo"><span>{seccion}</span></div>'
            f'<div class="pie"><span>Cómo conseguir más reseñas en Google · plea5e.es</span><b>{n:02d}</b><i>/ {TOTAL:02d}</i></div>')


def titulo(etq, l1, l2, intro=None, mb=8):
    i = f'<p class="intro" style="margin-bottom:{mb}mm">{intro}</p>' if intro else ''
    return f'<div class="etq">{etq}</div><h2>{l1}<br><em>{l2}</em></h2>{i}'


def ficha(nombre, nota, n, extra='', destacada=False):
    llenas = int(round(float(nota.replace(',', '.'))))
    est = ''.join(estrella(11, '#FBBC04' if i < llenas else '#DADCE0') for i in range(5))
    borde = 'border:.6mm solid var(--oro);' if destacada else ''
    return (f'<div style="background:#fff;border-radius:3mm;padding:4mm 5mm;box-shadow:0 1.5mm 4mm rgba(0,0,0,.12);{borde}">'
            f'<div style="font-weight:800;font-size:11pt">{nombre}</div>'
            f'<div style="display:flex;gap:1.5mm;align-items:center;font-size:9.5pt;margin-top:1mm"><b>{nota}</b>{est}<span style="color:#5f6368">({n})</span></div>'
            f'<div style="font-size:8.3pt;color:#5f6368;margin-top:1mm">Bar · Tapas · Abierto{extra}</div></div>')


# 1 · PORTADA ---------------------------------------------------------------
P.append(f'''<section class="pag oscura" style="padding:22mm 18mm">
<img src="{LOGO}" style="height:11mm">
<div style="margin-top:28mm">
  <div class="etq" style="color:var(--oro)">Guía práctica · para tu local y tu equipo</div>
  <h1 style="font-size:62pt;line-height:1.06">Cómo<br>conseguir<br>más reseñas<br><span style="color:var(--oro)">en Google</span></h1>
  <p style="font-size:12.5pt;color:#C9CEDA;max-width:92mm;margin-top:7mm">Sin trucos raros: <b style="color:#fff">pedirlo bien, ponerlo fácil y contestar</b>. Todo lo que hacen los locales con buena ficha, explicado paso a paso.</p>
  <div style="margin-top:6mm">{CINCO(30)}</div>
</div>
<div style="position:absolute;right:-12mm;bottom:12mm;width:125mm;height:125mm;border-radius:50%;background:radial-gradient(circle,rgba(233,188,70,.24),transparent 65%)"></div>
{bicho('lupa', 'right:8mm;bottom:26mm;width:86mm;height:96mm', '¿Empezamos?', 'der', 'right:14mm;bottom:124mm;font-size:19pt;transform:rotate(-4deg)')}
<div style="position:absolute;left:18mm;bottom:20mm;width:92mm">
  <div style="font-size:7.5pt;letter-spacing:.2em;text-transform:uppercase;color:#8C93A5;font-weight:700">Preparada para</div>
  <div style="border-bottom:.35mm dashed #56607A;height:12mm"></div>
</div>
</section>''')

# 2 · HOLA + INDICE ---------------------------------------------------------
indice = [('Por qué importa tu ficha', 3), ('El problema: los contentos no escriben', 4), ('El método en tres pasos', 5),
          ('Así funciona la placa, paso a paso', 6), ('Paso 1 · Cuándo pedir la reseña', 7), ('Paso 1 · Qué decir', 8),
          ('Paso 1 · La conversación, en viñetas', 9), ('Paso 2 · Dónde poner cada cosa', 10), ('Paso 2 · Bien colocada, mal colocada', 11),
          ('Paso 2 · Tu equipo en 5 minutos', 12), ('Las normas de Google', 13), ('Paso 3 · Cómo contestar, paso a paso', 14),
          ('Paso 3 · Respuestas listas y reseñas falsas', 15), ('Tu plan de 30 días', 16), ('Preguntas frecuentes', 17)]
P.append(f'''<section class="pag">{cab(2, 'Antes de empezar')}
<div style="position:relative;height:60mm">
  {bicho('saluda', 'left:-2mm;top:0;width:52mm;height:60mm')}
  <div class="bocadillo pico-izq" style="left:56mm;top:2mm;width:116mm;font-size:16pt;line-height:1.2;padding:4mm 6mm">¡Hola! Soy <span style="color:var(--oro-os)">Estrellita</span>, la de PLEA5E. En diez minutos te cuento cómo hacen los locales con buena ficha para que sus clientes les escriban. Sin trucos y sin pagar por reseñas.</div>
</div>
<div class="etq" style="margin-top:4mm">Qué hay dentro</div>
<div class="caja" style="padding:4mm 6mm">
  {''.join(f'<div style="display:flex;align-items:baseline;gap:3mm;padding:1.5mm 0;border-bottom:.3mm dashed var(--linea);font-size:9.8pt"><span style="flex:none;font-weight:{800 if not t.startswith("Paso") else 600}">{t}</span><span style="flex:1;border-bottom:.3mm dotted #CFC3AB;transform:translateY(-1mm)"></span><b style="font-family:Anton;color:var(--oro-os);font-weight:400;font-size:12pt">{p:02d}</b></div>' for t, p in indice)}
</div>
<div class="fila" style="grid-template-columns:repeat(3,1fr);gap:4mm;margin-top:5mm">
  <div class="caja" style="padding:3.5mm 5mm"><b>10 minutos</b><p class="nota">para leerla entera</p></div>
  <div class="caja" style="padding:4mm 5mm"><b>5 minutos</b><p class="nota">para explicársela al equipo (pág. 12)</p></div>
  <div class="caja" style="padding:4mm 5mm"><b>30 días</b><p class="nota">para que salga solo (pág. 16)</p></div>
</div>
</section>''')

# 3 · POR QUE IMPORTA -------------------------------------------------------
P.append(f'''<section class="pag">{cab(3, 'Por qué importa')}
{titulo('Por qué importa', 'Tu ficha de Google', 'es tu escaparate', 'Antes de entrar en un sitio que no conocen, mucha gente saca el móvil y busca en Google Maps. En un segundo mira tres cosas: <b>la nota</b>, <b>cuántas reseñas hay</b> y <b>de cuándo son</b>.')}
<div style="position:relative;background:#E8EEF3;border-radius:4mm;padding:8mm 8mm 8mm 8mm">
  <div class="nota" style="margin-bottom:3mm;font-weight:700;letter-spacing:.1em;text-transform:uppercase;font-size:7.5pt">Ejemplo · dos bares en la misma calle</div>
  <div class="fila" style="grid-template-columns:1fr 1fr;gap:5mm">
    {ficha('Bar La Esquina', '4,6', '17', ' · Última reseña: hace 5 meses')}
    {ficha('Bar El Patio', '4,5', '312', ' · Última reseña: ayer', True)}
  </div>
  <p class="mano" style="font-size:19pt;margin-top:5mm;text-align:center">Casi la misma nota… ¿en cuál entrarías tú?</p>
</div>
<div class="fila" style="grid-template-columns:repeat(3,1fr);gap:4mm;margin-top:8mm">
  <div class="caja" style="padding:5mm"><span class="num" style="font-size:26pt">★</span><h3>La nota</h3><p style="font-size:9.5pt">Es lo primero que se ve, al lado de tu nombre.</p></div>
  <div class="caja" style="padding:5mm"><span class="num" style="font-size:26pt">#</span><h3>Cuántas</h3><p style="font-size:9.5pt">Muchas reseñas dan confianza: una nota con 300 opiniones pesa más que con 17.</p></div>
  <div class="caja" style="padding:5mm"><span class="num" style="font-size:26pt">⏱</span><h3>De cuándo</h3><p style="font-size:9.5pt">Si la última es de hace meses, parece que ya no va nadie.</p></div>
</div>
<div style="position:relative;margin-top:6mm;height:40mm">
  {bicho('senala', 'left:0;top:0;width:36mm;height:40mm', 'Y las tres cosas mejoran igual: con más clientes que escriban.', 'izq', 'left:40mm;top:6mm;width:120mm;font-size:16pt')}
</div>
</section>''')

# 4 · EL PROBLEMA (vinetas) --------------------------------------------------
vinetas = [('pulgar', '¡Todo buenísimo! Ya os pondré una reseña.', 'En la mesa'),
           ('saluda-izq', '¡Hasta luego!', 'Paga y se va'),
           ('gota', '…¿qué tenía que hacer yo?', 'Esa noche')]
P.append(f'''<section class="pag">{cab(4, 'El problema')}
{titulo('El problema', 'Los contentos', 'no escriben', 'No es que no quieran. Es que se les olvida. En cambio, quien ha tenido un mal día sí se acuerda de escribir. Por eso muchas fichas cuentan solo una parte de lo que pasa en el local.')}
<div class="fila" style="grid-template-columns:repeat(3,1fr);gap:4mm">
  {''.join(f'<div style="position:relative;height:92mm;background:#fff;border:.6mm solid var(--tinta);border-radius:2mm;box-shadow:1.2mm 1.4mm 0 var(--tinta);overflow:hidden"><span class="chip gris" style="position:absolute;left:3mm;top:3mm">{i}. {e}</span>{bicho(p, "left:50%;bottom:3mm;width:40mm;height:46mm;transform:translateX(-50%)")}<div class="bocadillo pico-izq" style="left:4mm;right:4mm;top:14mm;font-size:14pt;box-shadow:none">{t}</div></div>' for i, (p, t, e) in enumerate(vinetas, 1))}
</div>
<div class="fila" style="grid-template-columns:1fr 1fr;gap:5mm;margin-top:9mm">
  <div class="caja"><span class="chip rojo">Lo que pasa</span><h3>Nadie se lo pide</h3><p>El cliente contento se va con la intención de escribir, pero entre buscarte, abrir la ficha y encontrar el botón… lo deja para luego. Y luego no llega.</p></div>
  <div class="caja-os"><span class="chip">La solución</span><h3>Pedirlo y ponerlo fácil</h3><p>Que alguien se lo pida en el momento bueno y que dejarla cueste diez segundos, con el móvil que ya tiene en la mano.</p></div>
</div>
</section>''')

# 5 · EL METODO --------------------------------------------------------------
met = [('01', 'Pedir', 'Cuándo pedir la reseña y qué decir exactamente. Con frases para cada tipo de negocio.', 'Págs. 7 a 9', 'megafono'),
       ('02', 'Facilitar', 'Que dejarla cueste diez segundos: la placa, dónde ponerla y tu equipo preparado.', 'Págs. 10 a 12', 'tachan'),
       ('03', 'Contestar', 'Responder a todas las reseñas, también a las malas, y qué hacer con las falsas.', 'Págs. 14 y 15', 'elegante')]
P.append(f'''<section class="pag">{cab(5, 'El método')}
{titulo('El método', 'Tres pasos,', 'todos los días', 'No hace falta nada más. Lo difícil no es hacerlo: es hacerlo <b>siempre</b>, hasta que en tu local salga solo.')}
<div class="lista" style="gap:6mm">
  {''.join(f'<div class="caja" style="position:relative;display:grid;grid-template-columns:30mm 1fr;gap:6mm;align-items:center;padding:7mm 50mm 7mm 8mm;min-height:52mm"><div class="num" style="font-size:58pt">{n}</div><div><h3 style="font-size:22pt">{t}</h3><p style="font-size:10.5pt">{d}</p><p class="nota" style="margin-top:1.5mm">{pg}</p></div>{bicho(p, "right:5mm;bottom:3mm;width:40mm;height:46mm")}</div>' for n, t, d, pg, p in met)}
</div>
<p class="mano" style="font-size:18pt;color:var(--oro-os);margin-top:7mm;transform:rotate(-1.5deg)">Y todo dentro de las normas de Google (pág. 13): así las reseñas se quedan.</p>
</section>''')

# 6 · ASI FUNCIONA LA PLACA (4 moviles) --------------------------------------
bloqueo = ('<div style="position:absolute;inset:0;background:linear-gradient(160deg,#2B3A67,#0E1426)"></div>'
           '<div style="position:absolute;top:13mm;left:0;right:0;text-align:center;color:#fff;font-size:20pt;font-weight:300">20:41</div>'
           f'<div style="position:absolute;top:30mm;left:2.5mm;right:2.5mm;background:rgba(255,255,255,.88);border-radius:3mm;padding:2.5mm;display:flex;gap:2mm;align-items:center">{G_LOGO}<div style="font-size:6.6pt;line-height:1.25"><b>NFC · Google</b><br>Toca para abrir: escribe una reseña de Tu negocio</div></div>')
moviles = [(bloqueo, 'Acerca el móvil', 'A la placa, por la parte de arriba del móvil. En iPhone, con la pantalla encendida. O escanea el QR con la cámara.'),
           (pantalla_resena(0), 'Se abre sola', 'Aparece directamente la ventana para escribir la reseña de tu negocio. Sin buscarte y sin apps.'),
           (pantalla_resena(5), 'Pone las estrellas', 'Las que quiera: la reseña es suya. Tú solo le has ahorrado buscarte.'),
           (pantalla_resena(5, 'Todo buenísimo, el salmorejo de 10 y el trato de lujo. ¡Volveremos!', True), 'Escribe y publica', 'Unas palabras y «Publicar». En diez segundos ha terminado.')]
P.append(f'''<section class="pag">{cab(6, 'Así funciona')}
{titulo('Así funciona la placa', 'Toca. Escribe.', 'Ya está.', 'Esto es lo que ve tu cliente. Enséñaselo a tu equipo: si lo entienden ellos, lo explican mejor.', 6)}
<div style="position:relative;height:150mm">
  {''.join(f'<div style="position:absolute;left:{i * 44}mm;top:{(i % 2) * 10}mm;width:40mm">{movil(pant, "position:relative;width:40mm;height:82mm;border-radius:6mm;padding:1.6mm")}<div style="display:flex;gap:2mm;align-items:center;margin-top:4mm"><span class="paso-n" style="width:7.5mm;height:7.5mm;font-size:11pt">{i + 1}</span><b style="font-size:10pt;line-height:1.15">{t}</b></div><p style="font-size:8.6pt;margin-top:1.5mm;color:#383D49">{d}</p></div>' for i, (pant, t, d) in enumerate(moviles))}
</div>
<div class="caja-os" style="position:relative;padding-right:44mm;margin-top:2mm">
  <h3>¿Y si su móvil no lee NFC?</h3><p>La mayoría de los móviles de los últimos años lo leen de fábrica. Si alguien lleva uno más antiguo, <b style="color:#fff">ahí está el QR</b>: lo escanea con la cámara y llega al mismo sitio.</p>
  {bicho('guino-izq', 'right:4mm;bottom:-3mm;width:34mm;height:40mm')}
</div>
</section>''')

# 7 · CUANDO -----------------------------------------------------------------
bien = ['<b>Al llevar la cuenta o el datáfono</b>: el cliente ya tiene el móvil en la mano.',
        '<b>Justo cuando te dicen «estaba todo buenísimo».</b> Ese es EL momento.',
        '<b>Al despedir a un cliente de siempre</b>: te lo hará con gusto.',
        '<b>Después de arreglar bien un problema.</b> Quien ve que te importa, lo cuenta.']
mal = ['<b>Con el local a tope</b> y el cliente esperando para pagar.',
       '<b>Si algo ha salido mal</b> y todavía no se ha arreglado.',
       '<b>Nada más sentarse</b>, antes de que haya probado nada.',
       '<b>Insistiendo.</b> Se pide una vez, con una sonrisa, y ya.']
P.append(f'''<section class="pag">{cab(7, 'Paso 1 · Pedir')}
{titulo('Paso 1 · Pedir', 'El cuándo importa', 'más que el cómo', 'La misma frase funciona o no según el momento. Pídela cuando el cliente está contento <b>y</b> tiene un segundo.')}
<div class="fila" style="grid-template-columns:1fr 1fr">
  <div class="caja"><span class="chip verde">Momentos buenos</span><ul class="lista" style="margin-top:2mm">{''.join(f'<li>{SI}<span>{t}</span></li>' for t in bien)}</ul></div>
  <div class="caja"><span class="chip rojo">Mejor no</span><ul class="lista" style="margin-top:2mm">{''.join(f'<li>{NO}<span>{t}</span></li>' for t in mal)}</ul></div>
</div>
<div class="caja-os" style="margin-top:8mm;position:relative;padding-right:60mm;min-height:54mm">
  <span class="chip">El truco</span><h3 style="font-size:17pt">Que lo pida quien cobra</h3>
  <p>Es el último que habla con el cliente y el que tiene la placa o el expositor al lado. Si además es quien le ha atendido, mejor todavía: a quien te ha tratado bien se le dice que sí más fácil.</p>
  {bicho('senala-izq', 'right:4mm;bottom:-5mm;width:52mm;height:58mm')}
</div>
<div style="position:relative;margin-top:9mm;height:32mm">
  {bicho('palomitas', 'left:0;top:-4mm;width:30mm;height:36mm')}
  <p class="mano" style="position:absolute;left:36mm;top:4mm;font-size:18pt;color:var(--oro-os);transform:rotate(-1.5deg)">Piénsalo como el «¿queréis postre?»: una pregunta más del servicio.<br>Nadie se molesta porque se la hagan.</p>
</div>
</section>''')

# 8 · QUE DECIR --------------------------------------------------------------
frases = [('Bar', '¿Todo bien? Si os ha gustado, nos ayuda un montón una reseña. Es acercar el móvil aquí.'),
          ('Restaurante', 'Me alegro de que os haya gustado. Si queréis contarlo en Google, acercáis el móvil a la placa y listo.'),
          ('Cafetería', 'Si te ha gustado el café, una reseña nos ayuda mucho. Acerca el móvil aquí, son diez segundos.'),
          ('Peluquería y estética', '¿Te gusta cómo ha quedado? Si nos dejas una reseña, nos ayudas muchísimo. Aquí mismo, con el móvil.'),
          ('Tienda', 'Si te hemos atendido bien, nos ayuda mucho que lo cuentes en Google. Acercas el móvil y ya.'),
          ('Alojamiento', 'Ha sido un placer teneros. Si os ha gustado la estancia, nos ayuda mucho una reseña. Os dejo la tarjeta.')]
P.append(f'''<section class="pag">{cab(8, 'Paso 1 · Pedir')}
{titulo('Paso 1 · Pedir', 'Qué decir:', 'frases que funcionan', 'Corta, con una sonrisa <b>y señalando dónde</b>. Coge la de tu negocio y dila con tus palabras: suena mejor la tuya que una aprendida.', 6)}
<div class="fila" style="grid-template-columns:1fr 1fr;gap:4mm">
  {''.join(f'<div class="caja" style="padding:4.5mm 5.5mm"><span class="chip">{t}</span><p class="cita" style="font-size:15pt">{f}</p></div>' for t, f in frases)}
</div>
<div class="etq" style="margin-top:7mm">Las tres claves</div>
<div class="fila" style="grid-template-columns:repeat(3,1fr);gap:4mm">
  <div class="caja" style="padding:4.5mm"><span class="paso-n">1</span><h3 style="margin-top:2mm">Pide ayuda</h3><p style="font-size:9.3pt">«Nos ayuda mucho» funciona. «Ponnos cinco estrellas» no se puede decir: la nota la elige el cliente.</p></div>
  <div class="caja" style="padding:4.5mm"><span class="paso-n">2</span><h3 style="margin-top:2mm">Di lo fácil que es</h3><p style="font-size:9.3pt">«Acercar el móvil», «diez segundos». Que suene a nada, porque es nada.</p></div>
  <div class="caja" style="padding:4.5mm"><span class="paso-n">3</span><h3 style="margin-top:2mm">Señala</h3><p style="font-size:9.3pt">La placa, el expositor o dale la tarjeta. Que no tenga que buscar.</p></div>
</div>
</section>''')

# 9 · LA CONVERSACION EN VINETAS ---------------------------------------------
conv = [('curiosa', 'Camarero', '¿Qué tal todo?', 'der'),
        ('pulgar-izq', 'Cliente', '¡Buenísimo, de verdad!', 'izq'),
        ('senala', 'Camarero', '¡Qué bien! Si os apetece contarlo, nos ayuda mucho: acercad el móvil aquí.', 'der'),
        ('asombro-izq', 'Cliente', '¿Ya? ¡Qué fácil!', 'izq')]
P.append(f'''<section class="pag">{cab(9, 'Paso 1 · Pedir')}
{titulo('Paso 1 · Pedir', 'La conversación', 'en viñetas', 'Así suena en la mesa. Diez segundos, sin incomodar a nadie.', 6)}
<div class="fila" style="grid-template-columns:1fr 1fr;gap:4mm">
  {''.join(f'<div style="position:relative;height:50mm;background:{"#fff" if q == "Camarero" else "#FFF6DC"};border:.6mm solid var(--tinta);border-radius:2mm;box-shadow:1.2mm 1.4mm 0 var(--tinta);overflow:hidden"><span class="chip {"gris" if q == "Camarero" else ""}" style="position:absolute;{"left" if l == "der" else "right"}:3mm;bottom:3mm">{q}</span>{bicho(p, ("right" if l == "der" else "left") + ":3mm;bottom:2mm;width:30mm;height:34mm")}<div class="bocadillo pico-{l}" style="{"left" if l == "der" else "right"}:4mm;{"right" if l == "der" else "left"}:30mm;top:5mm;font-size:14.5pt;box-shadow:none">{t}</div></div>' for p, q, t, l in conv)}
</div>
<div class="fila" style="grid-template-columns:1fr 1fr;gap:5mm;margin-top:6mm">
  <div class="caja" style="padding:5mm"><span class="chip">Si te dicen «luego lo hago»</span><p class="cita" style="font-size:15pt">¡Gracias! Te dejo la tarjeta y lo haces cuando quieras.</p><p class="nota" style="margin-top:1.5mm">Sin insistir. Con la tarjeta en el bolsillo, luego es fácil.</p></div>
  <div class="caja" style="padding:5mm"><span class="chip gris">Si te dicen que no</span><p class="cita" style="font-size:15pt">¡Nada, faltaría más! Gracias por venir.</p><p class="nota" style="margin-top:1.5mm">Y sigue igual de simpático. El que se va a gusto vuelve.</p></div>
</div>
<div class="caja-os" style="margin-top:5mm;padding:5mm 7mm"><h3>Palabras que ayudan… y palabras que no</h3>
  <div class="fila" style="grid-template-columns:1fr 1fr;gap:4mm;margin-top:2mm">
    <ul class="lista" style="gap:1.8mm">{''.join(f'<li>{SI}<span>{t}</span></li>' for t in ['«Nos ayuda mucho»', '«Si os apetece»', '«Diez segundos», «acercar el móvil»'])}</ul>
    <ul class="lista" style="gap:1.8mm">{''.join(f'<li>{NO}<span>{t}</span></li>' for t in ['«Ponnos cinco estrellas»', '«Si la dejas, te invito a…»', '«Es obligatorio», «hazla ahora»'])}</ul>
  </div></div>
</section>''')

# 10 · DONDE PONER CADA COSA -------------------------------------------------
P.append(f'''<section class="pag">{cab(10, 'Paso 2 · Facilitar')}
{titulo('Paso 2 · Facilitar', 'Dónde poner', 'cada cosa', 'Si para dejar la reseña hay que buscarte en Google, abrir la ficha y encontrar el botón, se pierde por el camino. Con NFC y QR <b>se abre directamente la ventana de escribir</b>.', 6)}
<div class="fila" style="grid-template-columns:1fr 1fr;gap:6mm">
  <div class="foto" style="height:88mm"><img src="{jpg(G + 'img/placa-mano.jpg')}" style="object-position:50% 45%"></div>
  <div class="foto" style="height:88mm"><img src="{jpg(G + 'img/expositor.jpg')}" style="object-position:55% 50%"></div>
</div>
<div class="fila" style="grid-template-columns:1fr 1fr 1fr;gap:5mm;margin-top:6mm">
  <div><span class="chip">Placa de mesa</span><p><b>En cada mesa</b>, donde se vea al sentarse: junto al servilletero mejor que en una esquina.</p></div>
  <div><span class="chip">Expositor de pie</span><p><b>En la barra o junto a la caja</b>: justo donde se paga. 76 × 118 mm, no se pega a nada.</p></div>
  <div><span class="chip">Tarjeta de mano</span><p><b>En el delantal o con la cuenta.</b> Para terrazas, domicilio y el «luego lo hago». 85 × 54 mm.</p></div>
</div>
<div style="position:absolute;right:16mm;bottom:20mm;width:60mm;transform:rotate(-7deg)"><img src="{png(G + 'img/tarjeta.png')}" style="width:100%;filter:drop-shadow(0 2mm 3mm rgba(0,0,0,.25))"></div>
{bicho('tachan', 'left:16mm;bottom:17mm;width:34mm;height:40mm')}
<p class="mano" style="position:absolute;left:54mm;bottom:30mm;font-size:16pt;color:var(--oro-os);width:70mm;transform:rotate(-1.5deg)">Todo con tu logo y tus colores: que parezca de tu local, no un cartel más.</p>
</section>''')

# 11 · BIEN / MAL COLOCADA ---------------------------------------------------
sis = ['<b>A la vista</b> al sentarse o al pagar, sin mover nada.', '<b>De pie o en plano</b>, pero que se lea: sin servilleteros ni cartas encima.',
       '<b>Una en cada punto de pago</b>: barra, caja, terraza.', '<b>Probada</b>: acerca tu móvil el primer día y una vez al mes.']
nos = ['<b>Escondida</b> detrás del servilletero o bajo la carta.', '<b>Junto a otros diez carteles</b>: se pierde entre todos.',
       '<b>Pegada sobre metal</b> directamente: el metal puede estorbar al chip.', '<b>Sucia o despegada</b>: mejor quitarla que tenerla así.']
P.append(f'''<section class="pag">{cab(11, 'Paso 2 · Facilitar')}
{titulo('Paso 2 · Facilitar', 'Bien colocada,', 'mal colocada', 'Una placa que no se ve no existe. Dos minutos de colocación marcan la diferencia.')}
<div class="fila" style="grid-template-columns:1fr 1fr">
  <div class="caja" style="border-top:1.4mm solid var(--verde)"><h3 style="color:#1F6B42">Así sí</h3><ul class="lista" style="margin-top:3mm">{''.join(f'<li>{SI}<span>{t}</span></li>' for t in sis)}</ul></div>
  <div class="caja" style="border-top:1.4mm solid var(--rojo)"><h3 style="color:#8A2A1E">Así no</h3><ul class="lista" style="margin-top:3mm">{''.join(f'<li>{NO}<span>{t}</span></li>' for t in nos)}</ul></div>
</div>
<div class="etq" style="margin-top:9mm">Cuidarla, paso a paso</div>
<div class="fila" style="grid-template-columns:repeat(3,1fr);gap:4mm">
  <div class="caja" style="padding:5mm"><span class="paso-n">1</span><h3 style="margin-top:2mm">Pegarla</h3><p style="font-size:9.3pt">Limpia y seca la mesa, quita el papel del adhesivo y aprieta 30 segundos. Lleva adhesivo de montaje 3M.</p></div>
  <div class="caja" style="padding:5mm"><span class="paso-n">2</span><h3 style="margin-top:2mm">Limpiarla</h3><p style="font-size:9.3pt">Con el trapo húmedo de siempre. Aguanta el día a día.</p></div>
  <div class="caja" style="padding:5mm"><span class="paso-n">3</span><h3 style="margin-top:2mm">Quitarla</h3><p style="font-size:9.3pt">Con calor de secador sale sin dejar marca en la mesa.</p></div>
</div>
<div style="position:relative;margin-top:9mm;height:44mm">
  {bicho('monoculo', 'left:0;top:0;width:38mm;height:44mm', 'Una vez al mes, acerca tu móvil a cada placa. Si abre tu ficha, todo en orden.', 'izq', 'left:44mm;top:6mm;width:116mm;font-size:16pt')}
</div>
</section>''')

# 12 · EL EQUIPO -------------------------------------------------------------
reunion = [('Explica el porqué', '1 min', 'La ficha de Google es el escaparate: más reseñas recientes, más gente que se anima a entrar.'),
           ('Elegid la frase de la casa', '1 min', 'Una sola, corta, que todos digan igual. Apuntadla abajo.'),
           ('Probad la placa', '1 min', 'Cada uno acerca su móvil: que vean que se abre la ventana de escribir.'),
           ('Decid quién la pide', '1 min', 'Lo normal: quien lleva la cuenta o cobra.'),
           ('Quedad para repasar', '1 min', 'Cada semana, mirad juntos las reseñas nuevas. Si alguna nombra a alguien del equipo, díselo delante de todos.')]
P.append(f'''<section class="pag">{cab(12, 'Paso 2 · Facilitar')}
{titulo('Paso 2 · Facilitar', 'Tu equipo', 'en 5 minutos', 'Si solo lo pide uno, se nota. Una reunión cortita antes de abrir y todo el equipo sabe qué hacer:', 6)}
<div class="lista" style="gap:2.5mm">
  {''.join(f'<div class="caja" style="display:grid;grid-template-columns:10mm 1fr 16mm;gap:4mm;align-items:center;padding:3mm 5mm"><span class="paso-n">{i}</span><div><b>{a}</b><p style="font-size:9.2pt;color:#383D49">{d}</p></div><span class="chip gris" style="margin:0;text-align:center">{t}</span></div>' for i, (a, t, d) in enumerate(reunion, 1))}
</div>
<div class="caja" style="margin-top:5mm;position:relative;padding:5mm 44mm 5mm 6mm">
  <span class="chip">Nuestra frase de la casa</span>
  <div class="linea-rell"></div><div class="linea-rell"></div>
  {bicho('susurra-izq', 'right:3mm;bottom:-2mm;width:34mm;height:40mm')}
</div>
<div class="caja-os" style="margin-top:5mm;padding:5mm 7mm"><span class="chip">Ideas que funcionan</span>
  <ul class="lista" style="margin-top:2mm;gap:2mm">{''.join(f'<li>{estrella(16)}<span>{t}</span></li>' for t in ['Pasad las reseñas nuevas al grupo del equipo: da gusto leerlas.', 'Cuando alguien lo pida bien, díselo. Se contagia.', 'Al que entra nuevo, dale esta guía el primer día.'])}</ul></div>
</section>''')

# 13 · NORMAS DE GOOGLE ------------------------------------------------------
si = ['Pedir reseña a <b>todos</b> tus clientes, les haya ido como les haya ido.', 'Tener placas, QR y tarjetas a la vista.',
      'Recordarlo con educación, una vez.', 'Contestar a todas las reseñas, buenas y malas.']
no = ['Dar algo a cambio: descuentos, un chupito, sorteos, puntos…', 'Pedirla solo a los contentos, o pedir que sea de 5 estrellas.',
      'Escribir reseñas tú, tu familia o tu equipo.', 'Comprar reseñas o pedírselas a quien no ha venido.', 'Poner una tablet o un móvil del local para que escriban ahí.']
P.append(f'''<section class="pag">{cab(13, 'Las normas')}
{titulo('Lo que dice Google', 'Las normas:', 'lo que sí y lo que no', 'Google quiere reseñas de clientes de verdad, escritas libremente. Si detecta trampas puede <b>borrar reseñas</b> e incluso limitar tu ficha. Estas son las reglas básicas:')}
<div class="fila" style="grid-template-columns:1fr 1fr">
  <div class="caja" style="border-top:1.4mm solid var(--verde)"><h3 style="color:#1F6B42">Sí se puede</h3><ul class="lista" style="margin-top:3mm">{''.join(f'<li>{SI}<span>{t}</span></li>' for t in si)}</ul></div>
  <div class="caja" style="border-top:1.4mm solid var(--rojo)"><h3 style="color:#8A2A1E">No se puede</h3><ul class="lista" style="margin-top:3mm">{''.join(f'<li>{NO}<span>{t}</span></li>' for t in no)}</ul></div>
</div>
<div class="caja-os" style="margin-top:8mm;position:relative;padding-right:56mm;min-height:52mm">
  <span class="chip">¿Y la placa?</span><h3 style="font-size:17pt">Está dentro de las normas</h3>
  <p>No regala nada ni elige a quién se le pide: solo le ahorra al cliente tener que buscarte. Es lo mismo que decir «¿nos dejas una reseña?», pero sin que cueste.</p>
  {bicho('elegante-izq', 'right:4mm;bottom:-4mm;width:48mm;height:56mm')}
</div>
<p class="nota" style="margin-top:5mm">Resumen de la política de contenido de reseñas de Google. Las normas completas están en la ayuda de Google Business Profile.</p>
</section>''')

# 14 · COMO CONTESTAR PASO A PASO -------------------------------------------
res = ('<div style="padding:10mm 3mm 3mm">'
       f'<div style="display:flex;gap:2mm;align-items:center;margin-bottom:2mm"><div style="width:6mm;height:6mm;border-radius:50%;background:#7B61FF;color:#fff;font-size:7pt;display:grid;place-items:center;font-weight:800">L</div><div style="font-size:7pt"><b>Laura M.</b><br><span style="color:#5f6368">hace 2 horas</span></div></div>'
       f'<div>{"".join(estrella(10, "#FBBC04") for _ in range(5))}</div>'
       '<p style="font-size:6.8pt;margin:1.5mm 0 3mm;line-height:1.35">El salmorejo, de lo mejor que he probado. Y el trato, un diez.</p>'
       '<div style="display:inline-block;border:.3mm solid #dadce0;border-radius:3mm;padding:1mm 3mm;font-size:6.8pt;color:#1a73e8;font-weight:700">Responder</div>'
       '<div style="border:.3mm solid #1a73e8;border-radius:2mm;margin-top:3mm;padding:2mm;font-size:6.6pt;min-height:20mm;line-height:1.35">¡Muchas gracias, Laura! Nos alegra que te gustara el salmorejo. ¡Te esperamos pronto!<span class="pr-cursor"></span></div>'
       '<div style="margin:2.5mm 0 0 auto;width:16mm;text-align:center;border-radius:3mm;background:#1a73e8;color:#fff;font-size:6.8pt;font-weight:700;padding:1.2mm 0">Publicar</div></div>')
pasos_resp = [('Entra en tu ficha', 'Busca el nombre de tu negocio en Google con la cuenta con la que lo gestionas. Te sale tu panel de empresa. También desde la app de Google Maps, en tu perfil de empresa.'),
              ('Abre «Reseñas»', 'En el panel, toca «Reseñas» (o «Leer reseñas»). Verás las nuevas arriba.'),
              ('Toca «Responder»', 'Debajo de cada reseña. Escribe tu respuesta (ideas en la página siguiente).'),
              ('Publicar', 'Tu respuesta sale debajo de la reseña, a la vista de todos, y al cliente le llega un aviso.')]
P.append(f'''<section class="pag">{cab(14, 'Paso 3 · Contestar')}
{titulo('Paso 3 · Contestar', 'Contesta todas.', 'También las malas.', 'Quien lee tu ficha no solo lee las reseñas: <b>lee cómo contestas</b>. Hazlo en uno o dos días. Así se hace:', 6)}
<div style="display:grid;grid-template-columns:1fr 58mm;gap:8mm;align-items:start">
  <div class="lista" style="gap:4.5mm">
    {''.join(f'<div style="display:flex;gap:4mm;align-items:flex-start"><span class="paso-n">{i}</span><div><b style="font-size:11pt">{a}</b><p style="font-size:9.8pt;color:#383D49">{d}</p></div></div>' for i, (a, d) in enumerate(pasos_resp, 1))}
  </div>
  {movil(res, "position:relative;width:56mm;height:114mm")}
</div>
<div class="fila" style="grid-template-columns:1fr 1fr;margin-top:8mm;gap:6mm">
  <ul class="lista">
    <li>{SI}<span><b>Usa su nombre</b> y un detalle de lo que cuenta: se nota que la has leído.</span></li>
    <li>{SI}<span><b>Corta y amable.</b> Dos o tres frases bastan.</span></li>
    <li>{SI}<span>En las malas, <b>lleva la conversación a privado</b>.</span></li></ul>
  <ul class="lista">
    <li>{NO}<span><b>Nunca en caliente.</b> Si te ha dolido, contesta mañana.</span></li>
    <li>{NO}<span><b>No discutas</b> en público, aunque tengas razón.</span></li>
    <li>{NO}<span><b>No copies</b> la misma respuesta en todas.</span></li></ul>
</div>
</section>''')

# 15 · RESPUESTAS LISTAS + RESENAS FALSAS -----------------------------------
resp = [('Buena', 'verde', '¡Muchas gracias, Laura! Nos alegra mucho que te gustara el salmorejo. Te esperamos pronto.'),
        ('Regular', '', 'Gracias por contarlo, Pedro. Tomamos nota de la espera para mejorarla. Ojalá verte otra vez y que todo salga redondo.'),
        ('Mala', 'rojo', 'Sentimos mucho tu experiencia, Ana: no es lo que queremos para nadie. Escríbenos al [teléfono] y lo hablamos con calma.')]
falsa = [('Busca la reseña', 'En tu ficha, en «Reseñas».'), ('Toca los tres puntos ⋮', 'Al lado de la reseña.'),
         ('«Denunciar reseña»', 'Elige el motivo: spam, ofensiva, no es un cliente…'), ('Espera la revisión', 'Google la revisa. Mientras, no la contestes con otra reseña.')]
P.append(f'''<section class="pag">{cab(15, 'Paso 3 · Contestar')}
{titulo('Paso 3 · Contestar', 'Respuestas listas', 'y reseñas falsas', 'Cópialas, cámbiales el nombre y el detalle, y listo. Guárdalas en las notas del móvil.', 6)}
<div class="lista" style="gap:4mm">
  {''.join(f'<div class="caja" style="display:grid;grid-template-columns:26mm 1fr;gap:5mm;align-items:center;padding:5mm 6mm"><span class="chip {c}" style="text-align:center;margin:0">{t}</span><p class="cita" style="font-size:15.5pt">{r}</p></div>' for t, c, r in resp)}
</div>
<div class="etq" style="margin-top:9mm">¿Una reseña falsa u ofensiva?</div>
<div class="fila" style="grid-template-columns:repeat(4,1fr);gap:4mm">
  {''.join(f'<div class="caja" style="padding:4.5mm"><span class="paso-n">{i}</span><h3 style="margin-top:2mm;font-size:11.5pt">{a}</h3><p style="font-size:9pt">{d}</p></div>' for i, (a, d) in enumerate(falsa, 1))}
</div>
<div style="position:relative;margin-top:8mm;height:44mm">
  {bicho('gota-izq', 'right:0;top:0;width:38mm;height:44mm', 'Una mala reseña bien contestada da más confianza que diez sin respuesta.', 'der', 'right:44mm;top:6mm;width:116mm;font-size:16pt')}
</div>
</section>''')

# 16 · PLAN DE 30 DIAS -------------------------------------------------------
semanas = [('Semana 1', ['Coloca las placas y pruébalas con tu móvil.', 'Reunión de 5 minutos con el equipo (pág. 12).', 'Apunta abajo tus reseñas y tu nota de hoy.']),
           ('Semana 2', ['Todo el equipo pide con la frase de la casa.', 'Contesta todas las reseñas nuevas.']),
           ('Semana 3', ['Mira qué funciona: ¿qué momento, quién lo pide mejor?', 'Si una placa no se usa, cámbiala de sitio.']),
           ('Semana 4', ['Compara con el día 1.', 'Cuéntaselo al equipo y celebradlo.'])]
P.append(f'''<section class="pag">{cab(16, 'Plan de 30 días')}
{titulo('Ponlo en marcha', 'Tu plan de', '30 días', 'Ve marcando. Lo importante no es hacerlo perfecto: es <b>hacerlo todos los días</b> hasta que salga solo.', 6)}
<div class="fila" style="grid-template-columns:1fr 1fr;gap:4mm">
  {''.join(f'<div class="caja" style="padding:5mm 6mm"><h3 style="color:var(--oro-os)">{s}</h3><ul class="lista" style="gap:2mm;margin-top:1mm">' + ''.join(f'<li>{CASILLA}<span>{t}</span></li>' for t in ts) + '</ul></div>' for s, ts in semanas)}
</div>
<div class="etq" style="margin-top:8mm">Apunta aquí</div>
<table>
  <tr><th></th><th>Día 1</th><th>Semana 1</th><th>Semana 2</th><th>Semana 3</th><th>Semana 4</th></tr>
  <tr><th>Reseñas en total</th>{'<td style="height:9mm"></td>' * 5}</tr>
  <tr><th>Nota media</th>{'<td style="height:9mm"></td>' * 5}</tr>
  <tr><th>Reseñas nuevas</th><td style="background:var(--crema2)"></td>{'<td style="height:11mm"></td>' * 4}</tr>
</table>
<p class="nota" style="margin-top:3mm">¿Dónde se miran? Busca tu negocio en Google Maps: al lado de la nota sale el número de reseñas entre paréntesis. Con el seguimiento PLEA5E (opcional) sabes además cuánta gente ha acercado el móvil a cada placa.</p>
<div style="position:relative;margin-top:2mm;height:26mm">
  {bicho('salta', 'left:0;top:-2mm;width:24mm;height:28mm', '¡A por el día 1!', 'izq', 'left:32mm;top:4mm;font-size:17pt')}
</div>
</section>''')

# 17 · PREGUNTAS FRECUENTES --------------------------------------------------
faq = [('¿El cliente tiene que descargarse algo?', 'No. Los móviles de los últimos años leen NFC de fábrica. Y si alguien lleva uno viejo, tiene el QR.'),
       ('¿Y si me deja una mala reseña?', 'Puede pasar, y es normal: contéstala con calma (pág. 14). Una ficha con alguna nota más baja parece más real.'),
       ('¿Solo sirve para Google?', 'Puede llevar a Tripadvisor, Facebook, Instagram, X o tu Airbnb: se elige al pedirla.'),
       ('¿Esto no es comprar reseñas?', 'No. No se regala nada ni se elige a quién se le pide, que es lo que Google penaliza. Solo se le pone fácil a quien ya ha venido.'),
       ('¿Hay que pagar algo cada mes?', 'Las placas: pago único. Aparte hay un seguimiento opcional de 35 € al mes para ver cuánta gente las usa; sin él funcionan igual.'),
       ('¿Y si cambio de ficha o de local?', 'Con el seguimiento se cambia a dónde lleva en un minuto, sin tocar la placa.'),
       ('¿Se despega? ¿Estropea la mesa?', 'Lleva adhesivo de montaje 3M. Aguanta el trapo del día a día y sale con calor de secador sin dejar marca.'),
       ('¿Cuánto tarda en llegar?', 'Desde que apruebas el diseño: de 2 a 7 días laborables de preparación y de 1 a 3 de envío.')]
P.append(f'''<section class="pag">{cab(17, 'Preguntas frecuentes')}
{titulo('Dudas', 'Lo que siempre', 'nos preguntan', None)}
<div class="fila" style="grid-template-columns:1fr 1fr;gap:4mm">
  {''.join(f'<div class="caja" style="padding:4.5mm 5.5mm"><p style="font-weight:800;font-size:10.3pt">{q}</p><p style="font-size:9.4pt;margin-top:1.2mm;color:#383D49">{r}</p></div>' for q, r in faq)}
</div>
<div class="caja-os" style="margin-top:7mm;position:relative;padding-right:48mm;min-height:44mm">
  <h3 style="font-size:16pt">¿Otra duda?</h3><p>Escríbenos por WhatsApp al <b style="color:#fff">661 40 32 19</b> o a <b style="color:#fff">hola@plea5e.es</b>. Respondemos en minutos, de lunes a sábado.</p>
  {bicho('apunta-izq', 'right:4mm;bottom:-3mm;width:40mm;height:46mm')}
</div>
</section>''')

# 18 · CONTRAPORTADA ---------------------------------------------------------
P.append(f'''<section class="pag oscura" style="padding:22mm 18mm">
<img src="{LOGO}" style="height:11mm">
<div style="margin-top:20mm">
  <div class="etq" style="color:var(--oro)">¿Lo ponemos en marcha?</div>
  <h1 style="font-size:50pt;line-height:1.06">Tú lo pides.<br><span style="color:var(--oro)">Nosotros<br>lo ponemos fácil.</span></h1>
</div>
<div style="margin-top:10mm;display:flex;flex-direction:column;gap:4mm;max-width:108mm">
  {''.join(f'<div style="display:flex;gap:4mm;align-items:baseline;border-bottom:.3mm solid #283049;padding-bottom:3mm"><span style="width:6mm">{estrella(14)}</span><span><b style="font-size:12pt">{a}</b><br><span style="color:#AEB5C6;font-size:9.5pt">{b}</span></span></div>' for a, b in [
      ('Placa de mesa', 'Con NFC y QR. Para cada mesa.'), ('Expositor de pie', '76 × 118 mm. Para la barra o la caja.'), ('Tarjeta de mano', '85 × 54 mm. Para el delantal, la cuenta o la terraza.')])}
  <p style="color:#C9CEDA;margin-top:2mm">Con tu logo y tus colores. <b style="color:#fff">Las placas: pago único.</b> No se imprime nada sin tu visto bueno.</p>
</div>
<div style="position:absolute;right:-16mm;top:112mm;width:110mm;height:110mm;border-radius:50%;background:radial-gradient(circle,rgba(233,188,70,.25),transparent 65%)"></div>
{bicho('megafono-izq', 'right:6mm;top:124mm;width:68mm;height:78mm')}
<div style="position:absolute;left:18mm;right:18mm;bottom:20mm;display:flex;align-items:center;gap:7mm;background:#fff;color:var(--tinta);border-radius:3mm;padding:5mm 6mm">
  <img src="{QR}" style="width:30mm;height:30mm">
  <div style="flex:1">
    <div class="mano" style="font-size:20pt;color:var(--oro-os);line-height:1">Escríbenos, respondemos en minutos</div>
    <div style="font-family:Anton;font-size:22pt;margin-top:2mm">WhatsApp 661 40 32 19</div>
    <div style="font-weight:700;font-size:12pt">plea5e.es · hola@plea5e.es</div>
    <div class="nota">Hechas en Córdoba · Envío a toda España</div>
  </div>
</div>
</section>''')

assert len(P) == TOTAL, len(P)
open(G + 'guia.html', 'w').write(html('PLEA5E · Cómo conseguir más reseñas en Google', '', P))
print(TOTAL, 'paginas')
