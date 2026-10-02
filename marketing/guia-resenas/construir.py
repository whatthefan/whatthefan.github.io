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
CSS_GUIA = ('body{font-size:11pt;line-height:1.62}p{line-height:1.6}.intro{font-size:12.2pt;line-height:1.6}'
            '.lista{gap:4mm}.lista li{gap:3.5mm}.caja{padding:7mm}.caja-os{padding:7mm 8mm}h3{margin-bottom:2.5mm}'
            '.nota{font-size:9.6pt;line-height:1.55}.cita{line-height:1.3}h2{margin-bottom:6mm}')
P = []
PAG = {}   # clave de sección -> número de página real (se rellena al montar)


import segno
VIDEOS = {1: ('Así funciona', 35), 2: ('Cuándo pedirla', 31), 3: ('Qué decir', 28), 4: ('Dónde ponerla', 26), 5: ('Cómo contestar', 30), 6: ('Las normas', 26)}


def qr(url, mm):
    svg = segno.make(url, error='m').svg_inline(scale=4, border=0, dark='#06080E')
    return svg.replace('<svg ', f'<svg style="width:{mm}mm;height:{mm}mm;display:block" ', 1)


def video(n):
    """Tarjeta con el QR del vídeo de la sección: se escanea en papel y se pulsa en el PDF."""
    t, seg = VIDEOS[n]
    url = f'https://plea5e.es/guia#v{n}'
    return (f'<a href="{url}" style="position:absolute;top:19mm;right:18mm;width:31mm;text-decoration:none;color:inherit;z-index:5;'
            f'background:#fff;border:.6mm solid var(--oro);border-radius:3.5mm;padding:2.6mm;box-shadow:0 1.5mm 4mm rgba(0,0,0,.12);text-align:center">'
            f'{qr(url, 24.5)}<div style="font-family:Anton;font-size:10.5pt;letter-spacing:.02em;margin-top:1.8mm;color:#06080E">▶ VÍDEO {n}</div>'
            f'<div style="font-size:6.6pt;color:#5f6368;font-weight:600">{t} · {seg} s</div></a>')


def cab(clave, seccion, vid=None):
    n = len(P) + 1; PAG[clave] = n
    return ((video(vid) if vid else '') + f'<div class="cab"><img src="{LOGO_CLARO}" class="cab-logo"><span>{seccion}</span></div>'
            f'<div class="pie"><span>Cómo conseguir más reseñas en Google · plea5e.es</span><b>{n:02d}</b><i>/ @@TOTAL@@</i></div>')


def pg(clave):
    return f'@@p{clave}@@'


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
<div style="position:absolute;left:18mm;bottom:20mm;width:96mm;display:flex;gap:3mm;flex-wrap:wrap">
  <span style="border:.35mm solid rgba(233,188,70,.55);border-radius:20mm;padding:1.6mm 4mm;font-size:8.5pt;font-weight:700;color:#F4E3B0">▶ Con 6 vídeos de 30 segundos</span>
  <span style="border:.35mm solid rgba(255,255,255,.25);border-radius:20mm;padding:1.6mm 4mm;font-size:8.5pt;font-weight:700;color:#C9CEDA">Para ti y tu equipo</span>
</div>
</section>''')

# 2 · HOLA + INDICE ---------------------------------------------------------
indice = [('Por qué importa tu ficha', 3), ('El problema: los contentos no escriben', 4), ('El método en tres pasos', 5),
          ('Así funciona la placa, paso a paso', 6), ('Paso 1 · Cuándo pedir la reseña', 7), ('Paso 1 · Qué decir', 8),
          ('Paso 1 · Las tres claves', '8b'), ('Paso 1 · La conversación, en viñetas', 9), ('Paso 2 · Dónde poner cada cosa', 10),
          ('Paso 2 · Bien colocada, mal colocada', 11), ('Paso 2 · Pegarla y cuidarla', '11b'), ('Paso 2 · Tu equipo en 5 minutos', 12),
          ('Paso 2 · La frase de la casa', '12b'), ('Las normas de Google', 13), ('Paso 3 · Cómo contestar, paso a paso', 14),
          ('Paso 3 · Respuestas listas', 15), ('Paso 3 · Reseñas falsas u ofensivas', '15b'), ('Tu plan de 30 días', 16),
          ('Cómo saber si funciona', '16b'), ('Preguntas frecuentes', 17), ('Los 6 vídeos de la guía', 19)]
P.append(f'''<section class="pag">{cab(2, 'Antes de empezar')}
<div style="position:relative;height:50mm">
  {bicho('saluda', 'left:-2mm;top:0;width:44mm;height:50mm')}
  <div class="bocadillo pico-izq" style="left:56mm;top:2mm;width:116mm;font-size:16pt;line-height:1.2;padding:4mm 6mm">¡Hola! Soy <span style="color:var(--oro-os)">Estrellita</span>, la de PLEA5E. En diez minutos te cuento cómo hacen los locales con buena ficha para que sus clientes les escriban. Sin trucos y sin pagar por reseñas.</div>
</div>
<div class="etq" style="margin-top:2mm">Qué hay dentro</div>
<div class="caja" style="padding:5mm 7mm;display:grid;grid-template-columns:1fr 1fr;column-gap:9mm">
  {''.join(f'<div style="display:flex;align-items:baseline;gap:2mm;padding:1.6mm 0;border-bottom:.3mm dashed var(--linea);font-size:9.4pt;line-height:1.3"><span style="flex:1;font-weight:{800 if not t.startswith("Paso") else 600}">{t}</span><b style="font-family:Anton;color:var(--oro-os);font-weight:400;font-size:12pt">@@p{p}@@</b></div>' for t, p in indice)}
</div>
<a href="https://plea5e.es/guia" class="caja-os" style="display:flex;gap:6mm;align-items:center;margin-top:5mm;padding:4mm 6mm;text-decoration:none">
  <div style="background:#fff;border-radius:2.5mm;padding:2mm">{qr('https://plea5e.es/guia', 20)}</div>
  <div><h3 style="font-size:15pt;color:#fff">▶ 10 minutos de lectura y 6 vídeos de 30 segundos</h3><p style="margin-top:1mm">Busca el código <b style="color:var(--oro)">VÍDEO</b> en cada sección y escanéalo con la cámara. Están todos en la pág. @@p19@@ y en <b style="color:#fff">plea5e.es/guia</b>.</p></div>
</a>
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
met = [('01', 'Pedir', 'Cuándo pedir la reseña y qué decir exactamente. Con frases para cada tipo de negocio.', f'Págs. @@p7@@ a @@p9@@', 'megafono'),
       ('02', 'Facilitar', 'Que dejarla cueste diez segundos: la placa, dónde ponerla y tu equipo preparado.', f'Págs. @@p10@@ a @@p12b@@', 'tachan'),
       ('03', 'Contestar', 'Responder a todas las reseñas, también a las malas, y qué hacer con las falsas.', f'Págs. @@p14@@ a @@p15b@@', 'elegante')]
P.append(f'''<section class="pag">{cab(5, 'El método')}
{titulo('El método', 'Tres pasos,', 'todos los días', 'No hace falta nada más. Lo difícil no es hacerlo: es hacerlo <b>siempre</b>, hasta que en tu local salga solo.')}
<div class="lista" style="gap:6mm">
  {''.join(f'<div class="caja" style="position:relative;display:grid;grid-template-columns:30mm 1fr;gap:6mm;align-items:center;padding:7mm 50mm 7mm 8mm;min-height:52mm"><div class="num" style="font-size:58pt">{n}</div><div><h3 style="font-size:22pt">{t}</h3><p style="font-size:10.5pt">{d}</p><p class="nota" style="margin-top:1.5mm">{pg}</p></div>{bicho(p, "right:5mm;bottom:3mm;width:40mm;height:46mm")}</div>' for n, t, d, pg, p in met)}
</div>
<p class="mano" style="font-size:18pt;color:var(--oro-os);margin-top:7mm;transform:rotate(-1.5deg)">Y todo dentro de las normas de Google (pág. @@p13@@): así las reseñas se quedan.</p>
</section>''')

# 6 · ASI FUNCIONA LA PLACA (4 moviles) --------------------------------------
bloqueo = ('<div style="position:absolute;inset:0;background:linear-gradient(160deg,#2B3A67,#0E1426)"></div>'
           '<div style="position:absolute;top:13mm;left:0;right:0;text-align:center;color:#fff;font-size:20pt;font-weight:300">20:41</div>'
           f'<div style="position:absolute;top:30mm;left:2.5mm;right:2.5mm;background:rgba(255,255,255,.88);border-radius:3mm;padding:2.5mm;display:flex;gap:2mm;align-items:center">{G_LOGO}<div style="font-size:6.6pt;line-height:1.25"><b>NFC · Google</b><br>Toca para abrir: escribe una reseña de Tu negocio</div></div>')
moviles = [(bloqueo, 'Acerca el móvil', 'A la placa, por la parte de arriba del móvil. En iPhone, con la pantalla encendida. O escanea el QR con la cámara.'),
           (pantalla_resena(0), 'Se abre sola', 'Aparece directamente la ventana para escribir la reseña de tu negocio. Sin buscarte y sin apps.'),
           (pantalla_resena(5), 'Pone las estrellas', 'Las que quiera: la reseña es suya. Tú solo le has ahorrado buscarte.'),
           (pantalla_resena(5, 'Todo buenísimo, el salmorejo de 10 y el trato de lujo. ¡Volveremos!', True), 'Escribe y publica', 'Unas palabras y «Publicar». En diez segundos ha terminado.')]
P.append(f'''<section class="pag">{cab(6, 'Así funciona', 1)}
{titulo('Así funciona la placa', 'Toca. Escribe.', 'Ya está.', 'Esto es lo que ve tu cliente. Enséñaselo a tu equipo: si lo entienden ellos, lo explican mejor.', 6)}
<div style="position:relative;height:150mm">
  {''.join(f'<div style="position:absolute;left:{i * 44}mm;top:{(i % 2) * 10}mm;width:40mm">{movil(pant, "position:relative;width:40mm;height:82mm;border-radius:6mm;padding:1.6mm")}<div style="display:flex;gap:2mm;align-items:center;margin-top:4mm"><span class="paso-n" style="width:7.5mm;height:7.5mm;font-size:11pt">{i + 1}</span><b style="font-size:10pt;line-height:1.15">{t}</b></div><p style="font-size:10pt;margin-top:1.5mm;color:#383D49">{d}</p></div>' for i, (pant, t, d) in enumerate(moviles))}
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
P.append(f'''<section class="pag">{cab(7, 'Paso 1 · Pedir', 2)}
{titulo('Paso 1 · Pedir', 'El cuándo importa', 'más que el cómo', 'La misma frase funciona o no según el momento. Pídela cuando el cliente está contento <b>y</b> tiene un segundo.')}
<div class="fila" style="grid-template-columns:1fr 1fr">
  <div class="caja"><span class="chip verde">Momentos buenos</span><ul class="lista" style="margin-top:2mm">{''.join(f'<li>{SI}<span>{t}</span></li>' for t in bien)}</ul></div>
  <div class="caja"><span class="chip rojo">Mejor no</span><ul class="lista" style="margin-top:2mm">{''.join(f'<li>{NO}<span>{t}</span></li>' for t in mal)}</ul></div>
</div>
<div class="caja-os" style="margin-top:8mm;position:relative;padding-right:60mm;min-height:54mm">
  <span class="chip">El truco</span><h3 style="font-size:17pt">Que lo pida quien cobra</h3>
  <p>Es el último que habla con el cliente y el que tiene la placa o el expositor al lado. Si además es quien le ha atendido, mejor todavía. Piénsalo como el «¿queréis postre?»: una pregunta más del servicio.</p>
  {bicho('senala-izq', 'right:4mm;bottom:-5mm;width:52mm;height:58mm')}
</div>
</section>''')

# 8 · QUE DECIR --------------------------------------------------------------
frases = [('Bar', '¿Todo bien? Si os ha gustado, nos ayuda un montón una reseña. Es acercar el móvil aquí.'),
          ('Restaurante', 'Me alegro de que os haya gustado. Si queréis contarlo en Google, acercáis el móvil a la placa y listo.'),
          ('Cafetería', 'Si te ha gustado el café, una reseña nos ayuda mucho. Acerca el móvil aquí, son diez segundos.'),
          ('Peluquería y estética', '¿Te gusta cómo ha quedado? Si nos dejas una reseña, nos ayudas muchísimo. Aquí mismo, con el móvil.'),
          ('Tienda', 'Si te hemos atendido bien, nos ayuda mucho que lo cuentes en Google. Acercas el móvil y ya.'),
          ('Alojamiento', 'Ha sido un placer teneros. Si os ha gustado la estancia, nos ayuda mucho una reseña. Os dejo la tarjeta.')]
P.append(f'''<section class="pag">{cab(8, 'Paso 1 · Pedir', 3)}
{titulo('Paso 1 · Pedir', 'Qué decir:', 'frases que funcionan', 'Corta, con una sonrisa <b>y señalando dónde</b>. Coge la de tu negocio y dila con tus palabras: suena mejor la tuya que una aprendida.', 6)}
<div class="fila" style="grid-template-columns:1fr 1fr;gap:4mm">
  {''.join(f'<div class="caja" style="padding:4.5mm 5.5mm"><span class="chip">{t}</span><p class="cita" style="font-size:15pt">{f}</p></div>' for t, f in frases)}
</div>
</section>''')

# 8b · LAS TRES CLAVES -------------------------------------------------------
claves = [('Pide ayuda', '«Nos ayuda mucho» funciona. «Ponnos cinco estrellas» no se puede decir: la nota la elige el cliente.', 'saluda'),
          ('Di lo fácil que es', '«Acercar el móvil», «diez segundos». Que suene a nada, porque es nada.', 'pulgar'),
          ('Señala', 'La placa, el expositor, o dale la tarjeta. Que no tenga que buscar.', 'senala')]
P.append(f'''<section class="pag">{cab('8b', 'Paso 1 · Pedir')}
{titulo('Paso 1 · Pedir', 'Las tres', 'claves', 'Da igual la frase que elijas: si cumple estas tres cosas, funciona.')}
<div class="lista" style="gap:5mm">
  {''.join(f'<div class="caja" style="position:relative;display:grid;grid-template-columns:14mm 1fr;gap:5mm;align-items:center;padding:7mm 46mm 7mm 7mm;min-height:40mm"><span class="paso-n" style="width:12mm;height:12mm;font-size:17pt">{i}</span><div><h3 style="font-size:17pt">{a}</h3><p>{d}</p></div>{bicho(b, "right:5mm;bottom:2mm;width:32mm;height:36mm")}</div>' for i, (a, d, b) in enumerate(claves, 1))}
</div>
<div class="caja-os" style="margin-top:8mm;padding:7mm 8mm"><h3>Palabras que ayudan… y palabras que no</h3>
  <div class="fila" style="grid-template-columns:1fr 1fr;gap:4mm;margin-top:2mm">
    <ul class="lista" style="gap:3mm">{''.join(f'<li>{SI}<span>{t}</span></li>' for t in ['«Nos ayuda mucho»', '«Si os apetece»', '«Diez segundos», «acercar el móvil»'])}</ul>
    <ul class="lista" style="gap:3mm">{''.join(f'<li>{NO}<span>{t}</span></li>' for t in ['«Ponnos cinco estrellas»', '«Si la dejas, te invito a…»', '«Es obligatorio», «hazla ahora»'])}</ul>
  </div></div>
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
</section>''')

# 10 · DONDE PONER CADA COSA -------------------------------------------------
P.append(f'''<section class="pag">{cab(10, 'Paso 2 · Facilitar', 4)}
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
<div style="position:relative;margin-top:12mm;height:44mm">
  {bicho('monoculo', 'left:0;top:0;width:38mm;height:44mm', 'Una vez al mes, acerca tu móvil a cada placa. Si abre tu ficha, todo en orden.', 'izq', 'left:44mm;top:6mm;width:116mm;font-size:16pt')}
</div>
</section>''')

# 11b · PEGARLA Y CUIDARLA ---------------------------------------------------
cuidar = [('Pegarla', 'Limpia y seca bien la superficie. Quita el papel del adhesivo, colócala y aprieta 30 segundos. Lleva adhesivo de montaje 3M.'),
          ('Limpiarla', 'Con el trapo húmedo de siempre. Aguanta el día a día del local sin problema.'),
          ('Probarla', 'El primer día y una vez al mes: acerca tu móvil. Si se abre tu ficha para escribir, está perfecta.'),
          ('Quitarla', 'Si un día la cambias de sitio: con calor de secador sale sin dejar marca en la mesa.')]
P.append(f'''<section class="pag">{cab('11b', 'Paso 2 · Facilitar')}
{titulo('Paso 2 · Facilitar', 'Pegarla', 'y cuidarla', 'Dos minutos el primer día y casi nada después.')}
<div class="fila" style="grid-template-columns:1fr 1fr;gap:5mm">
  {''.join(f'<div class="caja" style="padding:7mm"><span class="paso-n" style="width:11mm;height:11mm;font-size:15pt">{i}</span><h3 style="margin-top:3mm;font-size:16pt">{a}</h3><p>{d}</p></div>' for i, (a, d) in enumerate(cuidar, 1))}
</div>
<div class="caja-os" style="margin-top:8mm;position:relative;padding:7mm 50mm 7mm 8mm;min-height:46mm">
  <span class="chip">Ojo con el metal</span><h3 style="font-size:16pt">Sobre metal, mejor no</h3>
  <p>El metal puede estorbar al chip. Si tu barra o tus mesas son metálicas, pon el expositor de pie o pega la placa sobre otra superficie.</p>
  {bicho('lupa-izq', 'right:4mm;bottom:-3mm;width:40mm;height:46mm')}
</div>
</section>''')

# 12 · EL EQUIPO -------------------------------------------------------------
reunion = [('Explica el porqué', '1 min', 'La ficha de Google es el escaparate: más reseñas recientes, más gente que se anima a entrar.'),
           ('Elegid la frase de la casa', '1 min', 'Una sola, corta, que todos digan igual. Abajo tenéis un ejemplo.'),
           ('Probad la placa', '1 min', 'Cada uno acerca su móvil: que vean que se abre la ventana de escribir.'),
           ('Decid quién la pide', '1 min', 'Lo normal: quien lleva la cuenta o cobra.'),
           ('Quedad para repasar', '1 min', 'Cada semana, mirad juntos las reseñas nuevas. Si alguna nombra a alguien del equipo, díselo delante de todos.')]
P.append(f'''<section class="pag">{cab(12, 'Paso 2 · Facilitar')}
{titulo('Paso 2 · Facilitar', 'Tu equipo', 'en 5 minutos', 'Si solo lo pide uno, se nota. Una reunión cortita antes de abrir y todo el equipo sabe qué hacer:', 6)}
<div class="lista" style="gap:4mm">
  {''.join(f'<div class="caja" style="display:grid;grid-template-columns:10mm 1fr 16mm;gap:5mm;align-items:center;padding:5mm 6mm"><span class="paso-n">{i}</span><div><b>{a}</b><p style="font-size:10.4pt;color:#383D49">{d}</p></div><span class="chip gris" style="margin:0;text-align:center">{t}</span></div>' for i, (a, t, d) in enumerate(reunion, 1))}
</div>
<div style="position:relative;margin-top:9mm;height:40mm">
  {bicho('megafono', 'left:0;top:0;width:36mm;height:40mm', 'Cinco minutos antes de abrir. Y repetidlo cuando entre alguien nuevo.', 'izq', 'left:42mm;top:6mm;width:118mm;font-size:16pt')}
</div>
</section>''')

# 12b · LA FRASE DE LA CASA ----------------------------------------------------
P.append(f'''<section class="pag">{cab('12b', 'Paso 2 · Facilitar')}
{titulo('Paso 2 · Facilitar', 'La frase', 'de la casa', 'Una sola frase que todo el equipo diga igual. Así el cliente la oye natural, la pida quien la pida.')}
<div class="caja" style="position:relative;padding:8mm 48mm 8mm 8mm;min-height:60mm">
  <span class="chip">Ejemplo de frase de la casa</span>
  <p class="mano" style="font-size:21pt;line-height:1.25;margin-top:3mm">«Si os ha gustado, nos ayuda muchísimo una reseña. Es acercar el móvil aquí, son dos segundos.»</p>
  <p class="nota" style="margin-top:1.5mm">Cambiad lo que queráis para que suene a vuestro local. Lo importante: corta, con una sonrisa y señalando la placa.</p>
  {bicho('susurra-izq', 'right:3mm;bottom:-2mm;width:40mm;height:46mm')}
</div>
<div class="caja-os" style="margin-top:9mm;padding:8mm 9mm"><span class="chip">Ideas que funcionan</span>
  <ul class="lista" style="margin-top:3mm;gap:4mm">{''.join(f'<li>{estrella(16)}<span>{t}</span></li>' for t in ['Pasad las reseñas nuevas al grupo del equipo: da gusto leerlas.', 'Cuando alguien lo pida bien, díselo. Se contagia.', 'Al que entra nuevo, dale esta guía el primer día.'])}</ul></div>
<div style="position:relative;margin-top:10mm;height:42mm">
  {bicho('pulgar', 'left:0;top:0;width:36mm;height:42mm', 'Cuando alguien del equipo lo pide bien, que se note: se contagia.', 'izq', 'left:42mm;top:6mm;width:118mm;font-size:16pt')}
</div>
</section>''')

# 13 · NORMAS DE GOOGLE ------------------------------------------------------
si = ['Pedir reseña a <b>todos</b> tus clientes, les haya ido como les haya ido.', 'Tener placas, QR y tarjetas a la vista.',
      'Recordarlo con educación, una vez.', 'Contestar a todas las reseñas, buenas y malas.']
no = ['Dar algo a cambio: descuentos, un chupito, sorteos, puntos…', 'Pedirla solo a los contentos, o pedir que sea de 5 estrellas.',
      'Escribir reseñas tú, tu familia o tu equipo.', 'Comprar reseñas o pedírselas a quien no ha venido.', 'Poner una tablet o un móvil del local para que escriban ahí.']
P.append(f'''<section class="pag">{cab(13, 'Las normas', 6)}
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
              ('Toca «Responder»', 'Debajo de cada reseña. Escribe tu respuesta (ideas en la pág. @@p15@@).'),
              ('Publicar', 'Tu respuesta sale debajo de la reseña, a la vista de todos, y al cliente le llega un aviso.')]
P.append(f'''<section class="pag">{cab(14, 'Paso 3 · Contestar', 5)}
{titulo('Paso 3 · Contestar', 'Contesta todas.', 'También las malas.', 'Quien lee tu ficha no solo lee las reseñas: <b>lee cómo contestas</b>. Hazlo en uno o dos días. Así se hace:', 6)}
<div style="display:grid;grid-template-columns:1fr 58mm;gap:8mm;align-items:start">
  <div class="lista" style="gap:4.5mm">
    {''.join(f'<div style="display:flex;gap:4mm;align-items:flex-start"><span class="paso-n">{i}</span><div><b style="font-size:11pt">{a}</b><p style="font-size:10.8pt;color:#383D49">{d}</p></div></div>' for i, (a, d) in enumerate(pasos_resp, 1))}
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
{titulo('Paso 3 · Contestar', 'Respuestas', 'listas para usar', 'Una para cada caso. Cámbiales el nombre y el detalle, y listo.')}
<div class="lista" style="gap:6mm">
  {''.join(f'<div class="caja" style="display:grid;grid-template-columns:26mm 1fr;gap:6mm;align-items:center;padding:8mm 7mm"><span class="chip {c}" style="text-align:center;margin:0">{t}</span><p class="cita" style="font-size:15.5pt">{r}</p></div>' for t, c, r in resp)}
</div>
<div class="caja-os" style="margin-top:9mm;padding:7mm 8mm"><span class="chip">Truco</span><h3 style="font-size:15pt">Guárdalas en el móvil</h3><p>Pégalas en las notas del móvil. Cuando llegue una reseña, copias la que toque, cambias el nombre y el detalle, y en un minuto está contestada.</p></div>
</section>''')

# 15b · RESEÑAS FALSAS ------------------------------------------------------
P.append(f'''<section class="pag">{cab('15b', 'Paso 3 · Contestar')}
{titulo('Paso 3 · Contestar', '¿Una reseña falsa', 'u ofensiva?', 'Si alguien que no ha venido te deja una reseña, o insulta, puedes pedir a Google que la revise. Así se hace:')}
<div class="lista" style="gap:5mm">
  {''.join(f'<div class="caja" style="display:grid;grid-template-columns:14mm 1fr;gap:5mm;align-items:center;padding:6mm 7mm"><span class="paso-n" style="width:12mm;height:12mm;font-size:17pt">{i}</span><div><h3 style="font-size:15pt">{a}</h3><p>{d}</p></div></div>' for i, (a, d) in enumerate(falsa, 1))}
</div>
<div class="caja" style="margin-top:7mm;padding:6mm 7mm"><span class="chip rojo">Importante</span><p>Una reseña <b>mala pero real</b> no se puede quitar, y está bien que no se pueda: es lo que hace creíble tu ficha. Lo que sí puedes es contestarla con calma (pág. @@p14@@).</p></div>
</section>''')

# 16 · PLAN DE 30 DIAS -------------------------------------------------------
semanas = [('Semana 1', ['Coloca las placas y pruébalas con tu móvil.', f'Reunión de 5 minutos con el equipo (pág. @@p12@@).', 'Mira en Google Maps cuántas reseñas y qué nota tienes hoy.']),
           ('Semana 2', ['Todo el equipo pide con la frase de la casa.', 'Contesta todas las reseñas nuevas.']),
           ('Semana 3', ['Mira qué funciona: ¿qué momento, quién lo pide mejor?', 'Si una placa no se usa, cámbiala de sitio.']),
           ('Semana 4', ['Compara con el día 1.', 'Cuéntaselo al equipo y celebradlo.'])]
P.append(f'''<section class="pag">{cab(16, 'Plan de 30 días')}
{titulo('Ponlo en marcha', 'Tu plan de', '30 días', 'Ve marcando. Lo importante no es hacerlo perfecto: es <b>hacerlo todos los días</b> hasta que salga solo.', 6)}
<div class="fila" style="grid-template-columns:1fr 1fr;gap:6mm">
  {''.join(f'<div class="caja" style="padding:7mm;min-height:62mm"><h3 style="color:var(--oro-os);font-size:17pt">{s}</h3><ul class="lista" style="gap:3.5mm;margin-top:2mm">' + ''.join(f'<li>{CASILLA}<span>{t}</span></li>' for t in ts) + '</ul></div>' for s, ts in semanas)}
</div>
<div style="position:relative;margin-top:10mm;height:34mm">
  {bicho('salta', 'left:0;top:-2mm;width:30mm;height:34mm', '¡A por el día 1!', 'izq', 'left:36mm;top:6mm;font-size:18pt')}
</div>
</section>''')

# 16b · COMO SABER SI FUNCIONA --------------------------------------------------
medir = [('Reseñas en total', 'Busca tu negocio en Google Maps: es el número entre paréntesis al lado de la nota. Míralo el día 1 y cada lunes.'),
         ('Reseñas nuevas', 'En tu ficha, ordena las reseñas por «Más recientes». Si cada semana entran más que antes, vais bien.'),
         ('Todas contestadas', 'La meta de cada semana: ninguna reseña sin respuesta. Es lo que más se nota desde fuera.')]
P.append(f'''<section class="pag">{cab('16b', 'Plan de 30 días')}
{titulo('Ponlo en marcha', 'Cómo saber', 'si funciona', 'Tres cosas que mirar cada lunes. Dos minutos con el móvil.')}
<div class="lista" style="gap:5mm">
  {''.join(f'<div class="caja" style="display:grid;grid-template-columns:14mm 1fr;gap:5mm;align-items:center;padding:7mm"><span class="paso-n" style="width:12mm;height:12mm;font-size:17pt">{i}</span><div><h3 style="font-size:16pt">{a}</h3><p>{d}</p></div></div>' for i, (a, d) in enumerate(medir, 1))}
</div>
<div class="caja-os" style="margin-top:8mm;position:relative;padding:7mm 50mm 7mm 8mm;min-height:46mm"><span class="chip">Con el seguimiento PLEA5E</span><h3 style="font-size:15pt">Y cuánta gente usa cada placa</h3><p>Es opcional: un correo al mes con las veces que se ha acercado un móvil a cada placa. Sin él, las placas funcionan igual.</p>
  {bicho('monoculo-izq', 'right:4mm;bottom:-3mm;width:40mm;height:46mm')}</div>
</section>''')

# 17 · PREGUNTAS FRECUENTES --------------------------------------------------
faq = [('¿El cliente tiene que descargarse algo?', 'No. Los móviles de los últimos años leen NFC de fábrica. Y si alguien lleva uno viejo, tiene el QR.'),
       ('¿Y si me deja una mala reseña?', 'Puede pasar, y es normal: contéstala con calma (pág. @@p14@@). Una ficha con alguna nota más baja parece más real.'),
       ('¿Solo sirve para Google?', 'Puede llevar a Tripadvisor, Facebook, Instagram, X o tu Airbnb: se elige al pedirla.'),
       ('¿Esto no es comprar reseñas?', 'No. No se regala nada ni se elige a quién se le pide, que es lo que Google penaliza. Solo se le pone fácil a quien ya ha venido.'),
       ('¿Hay que pagar algo cada mes?', 'Las placas: pago único. Aparte hay un seguimiento opcional de 35 € al mes para ver cuánta gente las usa; sin él funcionan igual.'),
       ('¿Y si cambio de ficha o de local?', 'Con el seguimiento se cambia a dónde lleva en un minuto, sin tocar la placa.'),
       ('¿Se despega? ¿Estropea la mesa?', 'Lleva adhesivo de montaje 3M. Aguanta el trapo del día a día y sale con calor de secador sin dejar marca.'),
       ('¿Cuánto tarda en llegar?', 'Desde que apruebas el diseño: de 2 a 7 días laborables de preparación y de 1 a 3 de envío.')]
# 18 · MAS PREGUNTAS ---------------------------------------------------------
faq2 = [('¿Y si el cliente no tiene cuenta de Google?', 'Para publicar, Google pide iniciar sesión. Casi todos los Android ya la tienen; en iPhone se entra en unos segundos. Si no quiere, dale la tarjeta para hacerlo luego.'),
        ('¿Funciona con iPhone?', 'Sí. Desde el iPhone XS (2018) leen la placa con solo acercarlo. Los más antiguos, con el QR y la cámara.'),
        ('¿La reseña sale al momento?', 'Casi siempre sí. A veces Google la revisa y tarda un poco en aparecer; no depende de la placa.'),
        ('¿Puedo borrar una mala reseña?', 'No. Lo que sí puedes es contestarla (vídeo 5) y, si incumple las normas —insultos, spam o alguien que no ha venido—, denunciarla desde tu perfil de Google.'),
        ('¿Sé quién ha tocado la placa?', 'No. Con el seguimiento ves cuántas veces se ha acercado un móvil, no quién ni si ha escrito. Google no lo dice.'),
        ('¿Cuántas placas necesito?', 'Lo ideal: una por mesa y un expositor donde se cobra. Si empiezas con poco, el expositor de la caja es la que más se usa.'),
        ('¿Y si un chip deja de leer?', 'Te lo reponemos. Escríbenos con una foto y lo arreglamos.'),
        ('¿Puedo cambiar el diseño más adelante?', 'Sí. Te hacemos uno nuevo cuando quieras; con el seguimiento, a mitad de precio.')]
todas = faq + faq2
for k, (a, b) in enumerate([(0, 6), (6, 11), (11, 16)]):
    ultima = k == 2
    pie = (f'''<div class="caja-os" style="margin-top:6mm;position:relative;padding:6mm 48mm 6mm 8mm;min-height:38mm">
  <h3 style="font-size:16pt">¿Otra duda?</h3><p>Escríbenos por WhatsApp al <b style="color:#fff">661 40 32 19</b> o a <b style="color:#fff">hola@plea5e.es</b>. Respondemos en minutos, de lunes a sábado.</p>
  {bicho('apunta-izq', 'right:4mm;bottom:-3mm;width:40mm;height:46mm')}
</div>''' if ultima else '')
    P.append(f'''<section class="pag">{cab(17 if k == 0 else f'17{"bc"[k - 1]}', 'Preguntas frecuentes')}
{titulo(['Dudas', 'Más dudas', 'Más dudas'][k], ['Lo que siempre', 'Y también', 'Y para'][k], ['nos preguntan', 'esto', 'terminar'][k], None)}
<div class="lista" style="gap:4.5mm">
  {''.join(f'<div class="caja" style="padding:5mm 6.5mm"><p style="font-weight:800;font-size:12pt">{q}</p><p style="margin-top:1.5mm;color:#383D49">{r}</p></div>' for q, r in todas[a:b])}
</div>{pie}
</section>''')

# 19 · LOS VIDEOS ----------------------------------------------------------
DESC = {1: 'Acercar el móvil, poner las estrellas y publicar. Y qué hacer si el móvil no lee NFC.', 2: 'Los mejores momentos, cuándo mejor no y quién debería pedirla.',
        3: 'Frases que funcionan en bares, cafeterías y peluquerías, y las tres claves.', 4: 'Placa de mesa, expositor y tarjeta: dónde rinde cada una.',
        5: 'Paso a paso en tu ficha, con respuestas de ejemplo para las buenas y las malas.', 6: 'Lo que nunca hay que hacer y por qué la placa sí está dentro de las normas.'}
def tarjeta_video(n):
    t, seg = VIDEOS[n]; url = f'https://plea5e.es/guia#v{n}'
    return (f'<a href="{url}" class="caja" style="display:grid;grid-template-columns:44mm 1fr;gap:9mm;padding:6mm;align-items:center;text-decoration:none;color:inherit;align-items:start">'
            f'<div style="position:relative;width:44mm;height:78mm;border-radius:3.5mm;overflow:hidden;background:url({jpg(G + "img/video-%d.jpg" % n)}) center/cover">'
            f'<div style="position:absolute;inset:0;background:rgba(6,8,14,.25)"></div>'
            f'<div style="position:absolute;left:50%;top:50%;width:17mm;height:17mm;margin:-8.5mm 0 0 -8.5mm;border-radius:50%;background:rgba(233,188,70,.95);box-shadow:0 1mm 4mm rgba(0,0,0,.5)">'
            f'<div style="position:absolute;left:6.6mm;top:4.8mm;border-left:6mm solid #06080E;border-top:3.7mm solid transparent;border-bottom:3.7mm solid transparent"></div></div>'
            f'<span style="position:absolute;right:1.5mm;bottom:1.5mm;background:rgba(0,0,0,.7);color:#fff;font-size:6.5pt;font-weight:700;padding:.4mm 1.4mm;border-radius:1mm">0:{seg:02d}</span></div>'
            f'<div><div style="font-family:Anton;color:var(--oro-os);font-size:12pt">VÍDEO {n}</div><h3 style="font-size:19pt;margin-top:1mm">{t}</h3>'
            f'<p style="color:#383D49;margin-top:1.5mm">{DESC[n]}</p>'
            f'<div style="display:flex;gap:2.5mm;align-items:center;margin-top:2.5mm">{qr(url, 26)}<span style="font-size:10.2pt;color:#5f6368;font-weight:600">Escanéalo con la cámara<br>o pulsa la imagen</span></div></div></a>')
for k, ns in enumerate([(1, 2), (3, 4), (5, 6)]):
    P.append(f'''<section class="pag">{cab(19 if k == 0 else f'19{"bc"[k - 1]}', 'Los vídeos')}
{titulo('Guía en vídeo', 'Los 6 vídeos' if k == 0 else 'Los vídeos', 'de esta guía' if k == 0 else f'{2 * k + 1} y {2 * k + 2}', 'Treinta segundos cada uno y se entienden sin sonido. Ideales para enseñárselos al equipo el primer día.' if k == 0 else 'Pulsa la imagen o escanea el código con la cámara del móvil.', 6)}
<div class="lista" style="gap:5mm">{''.join(tarjeta_video(n) for n in ns)}</div>
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

import re as _re
TOTAL = len(P)
doc = html('PLEA5E · Cómo conseguir más reseñas en Google', CSS_GUIA, P).replace('@@TOTAL@@', f'{TOTAL:02d}')
doc = _re.sub(r'@@p([^@]+)@@', lambda m: f"{PAG[int(m.group(1)) if m.group(1).isdigit() else m.group(1)]:02d}", doc)
open(G + 'guia.html', 'w').write(doc)
print(TOTAL, 'paginas')
