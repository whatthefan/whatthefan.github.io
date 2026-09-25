"""Guia PLEA5E "Como conseguir mas resenas en Google" (PDF A4, 10 paginas).

Para llevarla en persona (impresa) o mandarla por WhatsApp o correo. Portada y
contraportada en noche; las paginas de dentro en crema, que se imprimen bien.

Reglas del texto: no se promete ninguna cifra de resenas, y lo que se dice de Google
es lo que dicen sus normas (pedir a todos, nada a cambio, nada de resenas propias ni
de puestos para escribirlas en el local).

Desde la raiz del repo:  python3 marketing/guia-resenas/construir.py
y despues:               node marketing/guia-resenas/hacer-pdf.js
"""
import base64
import math

G = 'marketing/guia-resenas/'
b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
svg = lambda f: 'data:image/svg+xml;base64,' + b64(f)
jpg = lambda f: 'data:image/jpeg;base64,' + b64(f)
png = lambda f: 'data:image/png;base64,' + b64(f)
E = 'marketing/instagram/personaje/svg/'
LOGO = svg('public/marca/marca-plea5e.svg')
LOGO_CLARO = svg('public/marca/marca-plea5e-claro.svg')
QR = svg('public/qr/qr-plea5e-es-plano.svg')
FUENTE = lambda n, f, w='400': f"@font-face{{font-family:{n};font-weight:{w};src:url(data:font/woff2;base64,{b64('fuente/' + f)})}}"


def estrella(tam, color='#E9BC46'):
    p = []
    for k in range(10):
        r = 10 if k % 2 == 0 else 4.2
        p.append(f'{10 + r * math.sin(math.pi * k / 5):.2f} {10 - r * math.cos(math.pi * k / 5):.2f}')
    return f'<svg class="est" width="{tam}" height="{tam}" viewBox="0 0 20 20"><path d="M{"L".join(p)}Z" fill="{color}"/></svg>'


CINCO = lambda tam, c='#E9BC46': '<span class="cinco">' + ''.join(estrella(tam, c) for _ in range(5)) + '</span>'
BICHO = lambda pose, estilo: f'<img class="bicho" src="{svg(E + pose + ".svg")}" style="{estilo}">'
SI = '<svg viewBox="0 0 20 20" class="ico"><circle cx="10" cy="10" r="10" fill="#2F8F5B"/><path d="M5.5 10.5l3 3 6-7" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
NO = '<svg viewBox="0 0 20 20" class="ico"><circle cx="10" cy="10" r="10" fill="#C0392B"/><path d="M6.5 6.5l7 7M13.5 6.5l-7 7" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/></svg>'

total = 10


def cab(n, seccion):
    return (f'<div class="cab"><img src="{LOGO_CLARO}" class="cab-logo"><span>{seccion}</span></div>'
            f'<div class="pie"><span>Guía de reseñas · plea5e.es</span><b>{n:02d}</b><i>/ {total:02d}</i></div>')


CSS = '''
''' + FUENTE('Anton', 'anton-latin.woff2') + FUENTE('Mont', 'montserrat-latin.woff2', '100 900') + FUENTE('Caveat', 'caveat-latin.woff2', '400 700') + '''
@page{size:A4;margin:0}
*{margin:0;padding:0;box-sizing:border-box}
:root{--noche:#06080E;--noche2:#10141F;--oro:#E9BC46;--oro-os:#A47A12;--crema:#FBF7EE;--crema2:#F3EBDB;--tinta:#161A24;--gris:#5A5F6B;--linea:#E3D8C2}
html,body{background:#888}
body{font-family:Mont;color:var(--tinta);font-size:10.5pt;line-height:1.5}
.pag{width:210mm;height:297mm;position:relative;overflow:hidden;background:var(--crema);page-break-after:always;padding:24mm 18mm 20mm}
.pag:last-child{page-break-after:auto}
/* papel: grano muy fino */
.pag::before{content:"";position:absolute;inset:0;pointer-events:none;opacity:.35;mix-blend-mode:multiply;
  background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='260' height='260'><filter id='r'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .55  0 0 0 0 .5  0 0 0 0 .42  0 0 0 .22 0'/></filter><rect width='260' height='260' filter='url(%23r)'/></svg>")}
.oscura{background:radial-gradient(ellipse 90% 60% at 70% 20%,#1A2136 0%,#0B0F1A 55%,var(--noche) 100%);color:#fff}
.oscura::before{mix-blend-mode:overlay;opacity:.5}
.cab{position:absolute;top:9mm;left:18mm;right:18mm;display:flex;align-items:center;gap:4mm;font-size:7.5pt;letter-spacing:.18em;text-transform:uppercase;color:var(--gris);font-weight:600}
.cab-logo{height:4.2mm}
.cab::after{content:"";flex:1;height:.3mm;background:var(--linea)}
.pie{position:absolute;bottom:9mm;left:18mm;right:18mm;display:flex;align-items:baseline;gap:1.5mm;font-size:7.5pt;color:var(--gris)}
.pie span{flex:1}
.pie b{font-family:Anton;font-size:12pt;color:var(--oro-os);font-weight:400}
.etq{display:inline-block;font-weight:800;font-size:8pt;letter-spacing:.22em;text-transform:uppercase;color:var(--oro-os);margin-bottom:3mm}
.etq::before{content:"";display:inline-block;width:9mm;height:.5mm;background:var(--oro-os);vertical-align:middle;margin-right:3mm}
h1,h2,h3{font-family:Anton;font-weight:400;text-transform:uppercase;line-height:1.12;letter-spacing:.005em}
h2{font-size:34pt;margin-bottom:5mm}
h2 em{font-style:normal;color:var(--oro-os)}
h3{font-size:14pt;margin-bottom:1.5mm}
.intro{font-size:12pt;color:#383D49;max-width:150mm;margin-bottom:8mm}
.intro b{color:var(--tinta)}
.mano{font-family:Caveat;font-weight:700}
.bicho{position:absolute;filter:drop-shadow(0 3mm 3mm rgba(0,0,0,.18))}
.est{display:inline-block;vertical-align:middle}
.cinco{display:inline-flex;gap:1mm}
.ico{width:5.5mm;height:5.5mm;flex:none;margin-top:.4mm}
.caja{background:#fff;border:.3mm solid var(--linea);border-radius:3mm;padding:6mm;box-shadow:0 1mm 0 var(--linea)}
.caja-oro{background:var(--noche);color:#fff;border-radius:3mm;padding:6mm 7mm}
.caja-oro h3{color:var(--oro)}
.num{font-family:Anton;color:var(--oro);font-size:40pt;line-height:.9}
.fila{display:grid;gap:5mm}
.lista{list-style:none;display:flex;flex-direction:column;gap:3mm}
.lista li{display:flex;gap:3mm;align-items:flex-start}
.linea-rell{border-bottom:.35mm dashed #B9AE98;height:9mm}
.cita{font-family:Caveat;font-weight:700;font-size:17pt;line-height:1.15;color:var(--tinta)}
.cita::before{content:"«";color:var(--oro-os)}.cita::after{content:"»";color:var(--oro-os)}
.chip{display:inline-block;font-weight:800;font-size:7.5pt;letter-spacing:.16em;text-transform:uppercase;background:var(--oro);color:var(--noche);padding:1mm 2.5mm;border-radius:1mm;margin-bottom:2mm}
.foto{border-radius:3mm;overflow:hidden;box-shadow:0 2mm 5mm rgba(0,0,0,.18)}
.foto img{display:block;width:100%;height:100%;object-fit:cover}
.nota{font-size:9pt;color:var(--gris)}
table{border-collapse:collapse;width:100%;font-size:9.5pt}
td,th{border:.3mm solid var(--linea);padding:3mm;text-align:left;background:#fff}
th{background:var(--crema2);font-weight:800;font-size:8pt;letter-spacing:.1em;text-transform:uppercase}
'''

P = []

# 1 · PORTADA
P.append(f'''<section class="pag oscura" style="padding:22mm 18mm">
<img src="{LOGO}" style="height:11mm">
<div style="margin-top:30mm">
  <div class="etq" style="color:var(--oro)">Guía práctica · para tu local</div>
  <h1 style="font-size:64pt;line-height:1.06">Cómo<br>conseguir<br>más reseñas<br><span style="color:var(--oro)">en Google</span></h1>
  <p style="font-size:13pt;color:#C9CEDA;max-width:105mm;margin-top:8mm">Sin trucos raros: <b style="color:#fff">pedirlo bien, ponerlo fácil y contestar</b>. Lo que hacen los locales con buena ficha, paso a paso, para ti y tu equipo.</p>
  <div style="margin-top:7mm">{CINCO(30)}</div>
</div>
<div style="position:absolute;right:-10mm;bottom:10mm;width:120mm;height:120mm;border-radius:50%;background:radial-gradient(circle,rgba(233,188,70,.22),transparent 65%)"></div>{BICHO('lupa', 'right:6mm;bottom:24mm;width:92mm;transform:rotate(-4deg)')}
<div style="position:absolute;left:18mm;bottom:20mm;width:95mm">
  <div style="font-size:7.5pt;letter-spacing:.2em;text-transform:uppercase;color:#8C93A5;font-weight:700">Preparada para</div>
  <div style="border-bottom:.35mm dashed #56607A;height:12mm"></div>
</div>
</section>''')

# 2 · POR QUE IMPORTA + EL METODO
P.append(f'''<section class="pag">{cab(2, 'Por qué importa')}
<div class="etq">Por qué importa</div>
<h2>Tu ficha de Google<br>es tu <em>escaparate</em></h2>
<p class="intro">Antes de entrar en un sitio que no conocen, mucha gente saca el móvil y mira dos cosas: <b>las estrellas</b> y <b>las últimas reseñas</b>. Tu ficha habla por ti aunque tú no estés.</p>
<div class="fila" style="grid-template-columns:1.15fr 1fr;align-items:stretch">
  <div class="caja" style="position:relative;padding-right:40mm">
    <span class="chip" style="background:#F2D6D2;color:#8A2A1E">El problema</span>
    <h3>Los contentos no escriben</h3>
    <p>No es que no quieran: pagan, se levantan y se les olvida. Quien ha tenido un mal día, en cambio, sí se acuerda. Así tu ficha cuenta solo <b>una parte</b> de lo que pasa en tu local.</p>
    {BICHO('gota', 'right:-4mm;bottom:-4mm;width:44mm')}
  </div>
  <div class="caja-oro" style="position:relative;padding-bottom:40mm">
    <span class="chip">La solución</span>
    <h3>Pedirlo. Bien.</h3>
    <p style="color:#D5DAE5">En el momento bueno, con una frase corta, y poniéndolo tan fácil que no cueste nada. Nada más… y nada menos.</p>
    {BICHO('pulgar', 'right:6mm;bottom:-3mm;width:40mm')}
  </div>
</div>
<div class="etq" style="margin-top:11mm">El método en tres pasos</div>
<div class="fila" style="grid-template-columns:repeat(3,1fr)">
  <div class="caja"><div class="num" style="color:var(--oro-os)">01</div><h3>Pedir</h3><p>Cuándo pedir la reseña y qué decir exactamente. <span class="nota" style="white-space:nowrap">Págs. 3 y 4</span></p></div>
  <div class="caja"><div class="num" style="color:var(--oro-os)">02</div><h3>Facilitar</h3><p>Que dejarla cueste diez segundos: dónde poner cada cosa. <span class="nota" style="white-space:nowrap">Págs. 5 y 6</span></p></div>
  <div class="caja"><div class="num" style="color:var(--oro-os)">03</div><h3>Contestar</h3><p>Responder a todas, también a las malas, y cómo. <span class="nota">Pág. 8</span></p></div>
</div>
<p class="mano" style="font-size:17pt;color:var(--oro-os);margin-top:9mm;transform:rotate(-1.5deg)">Y todo dentro de las normas de Google (pág. 7).</p>
</section>''')

# 3 · CUANDO
bien = ['Al llevar la cuenta o el datáfono: el cliente ya tiene el móvil en la mano.',
        'Justo cuando te dicen «estaba todo buenísimo». Ese es EL momento.',
        'Al despedir a un cliente de siempre: a ti te lo hará con gusto.',
        'Después de arreglar bien un problema. Quien ve que te importa, lo cuenta.']
mal = ['Con el local a tope y el cliente esperando para pagar.',
       'Si algo ha salido mal y todavía no se ha arreglado.',
       'Nada más sentarse, antes de que haya probado nada.',
       'Insistiendo. Se pide una vez, con una sonrisa, y ya.']
P.append(f'''<section class="pag">{cab(3, '01 · Pedir')}
<div class="etq">Paso 01 · Pedir</div>
<h2>El cuándo importa<br><em>más que el cómo</em></h2>
<p class="intro">La misma frase funciona o no según el momento. Pídela cuando el cliente está contento <b>y</b> tiene un segundo.</p>
<div class="fila" style="grid-template-columns:1fr 1fr">
  <div class="caja"><span class="chip" style="background:#D5EBDD;color:#1F6B42">Momentos buenos</span>
    <ul class="lista" style="margin-top:2mm">{''.join(f'<li>{SI}<span>{t}</span></li>' for t in bien)}</ul></div>
  <div class="caja"><span class="chip" style="background:#F2D6D2;color:#8A2A1E">Mejor no</span>
    <ul class="lista" style="margin-top:2mm">{''.join(f'<li>{NO}<span>{t}</span></li>' for t in mal)}</ul></div>
</div>
<div class="caja-oro" style="margin-top:9mm;position:relative;padding-right:62mm;min-height:52mm">
  <span class="chip">El truco</span>
  <h3>Que lo pida quien cobra</h3>
  <p style="color:#D5DAE5">Es el último que habla con el cliente y el que tiene la placa o el expositor al lado. Si además es quien le ha atendido, mejor todavía: a una persona que conoce se le dice que sí más fácil.</p>
  {BICHO('senala-izq', 'right:4mm;bottom:-6mm;width:54mm')}
</div>
<p class="mano" style="font-size:18pt;color:var(--oro-os);margin-top:12mm;transform:rotate(-1.5deg)">Piensa en ello como el «¿queréis postre?»: una pregunta más del servicio. Nadie se molesta por que se la hagan.</p>
</section>''')

# 4 · QUE DECIR
frases = [('Bar', '¿Todo bien? Si os ha gustado, nos ayuda un montón una reseña. Es acercar el móvil aquí.'),
          ('Restaurante', 'Me alegro de que os haya gustado. Si queréis contarlo en Google, acercáis el móvil a la placa y listo.'),
          ('Cafetería', 'Si te ha gustado el café, una reseña nos ayuda mucho. Acerca el móvil aquí, son diez segundos.'),
          ('Peluquería y estética', '¿Te gusta cómo ha quedado? Si nos dejas una reseña, nos ayudas muchísimo. Aquí mismo, con el móvil.'),
          ('Tienda', 'Si te hemos atendido bien, nos ayuda mucho que lo cuentes en Google. Acercas el móvil y ya.'),
          ('Alojamiento', 'Ha sido un placer teneros. Si os ha gustado la estancia, nos ayuda mucho una reseña. Os dejo la tarjeta.')]
P.append(f'''<section class="pag">{cab(4, '01 · Pedir')}
<div class="etq">Paso 01 · Pedir</div>
<h2>Qué decir:<br><em>frases que funcionan</em></h2>
<p class="intro" style="margin-bottom:6mm">Corta, con una sonrisa, <b>y señalando dónde</b>. Coge la de tu negocio y dila con tus palabras: suena mejor la tuya que una aprendida.</p>
<div class="fila" style="grid-template-columns:1fr 1fr;gap:4mm">
  {''.join(f'<div class="caja" style="padding:4mm 5.5mm"><span class="chip">{t}</span><p class="cita" style="font-size:15pt">{f}</p></div>' for t, f in frases)}
</div>
<div class="fila" style="grid-template-columns:1fr 1fr;margin-top:6mm;gap:6mm;font-size:9.5pt">
  <div><h3 style="font-size:12pt">Las tres claves</h3>
    <ul class="lista" style="margin-top:2mm">
      <li>{SI}<span><b>Pide ayuda</b>, no estrellas. «Nos ayuda mucho» funciona; «ponnos cinco estrellas» no se puede decir.</span></li>
      <li>{SI}<span><b>Di lo fácil que es</b>: «acercar el móvil», «diez segundos».</span></li>
      <li>{SI}<span><b>Señala</b> la placa o da la tarjeta. Que no tengan que buscar.</span></li></ul></div>
  <div class="caja" style="background:var(--crema2)"><h3 style="font-size:12pt">Si te dicen: luego lo hago</h3>
    <p>Perfecto: «¡Gracias! Te dejo la tarjeta y lo haces cuando quieras». Sin insistir. Con la tarjeta en el bolsillo, luego es fácil.</p></div>
</div>
</section>''')

# 5 · DONDE (productos)
P.append(f'''<section class="pag">{cab(5, '02 · Facilitar')}
<div class="etq">Paso 02 · Facilitar</div>
<h2>Que dejarla cueste<br><em>diez segundos</em></h2>
<p class="intro">Si para dejar la reseña hay que buscarte en Google, abrir la ficha y encontrar el botón, se pierde por el camino. Con NFC y QR <b>se abre directamente la ventana de escribir</b>.</p>
<div class="fila" style="grid-template-columns:1fr 1fr;gap:6mm">
  <div class="foto" style="height:92mm"><img src="{jpg(G + 'img/placa-mano.jpg')}" style="object-position:50% 45%"></div>
  <div class="foto" style="height:92mm"><img src="{jpg(G + 'img/expositor.jpg')}" style="object-position:55% 50%"></div>
</div>
<div class="fila" style="grid-template-columns:1fr 1fr 1fr;gap:5mm;margin-top:6mm">
  <div><span class="chip">Placa de mesa</span><p><b>En cada mesa</b>, donde se vea al sentarse: junto al servilletero mejor que en una esquina.</p></div>
  <div><span class="chip">Expositor de pie</span><p><b>En la barra o junto a la caja</b>: justo donde se paga. 76 × 118 mm, no se pega a nada.</p></div>
  <div style="position:relative"><span class="chip">Tarjeta de mano</span><p><b>En el delantal o con la cuenta.</b> Ideal para terrazas y para el «luego lo hago». 85 × 54 mm.</p></div>
</div>
<div style="position:absolute;right:16mm;bottom:22mm;width:62mm;transform:rotate(-7deg)"><img src="{png(G + 'img/tarjeta.png')}" style="width:100%;filter:drop-shadow(0 2mm 3mm rgba(0,0,0,.25))"></div>
<p class="mano" style="position:absolute;left:18mm;bottom:26mm;font-size:16pt;color:var(--oro-os);width:100mm;transform:rotate(-1.5deg)">Todo con tu logo y tus colores: que parezca de tu local, no un cartel más.</p>
</section>''')

# 6 · EL EQUIPO
P.append(f'''<section class="pag">{cab(6, '02 · Facilitar')}
<div class="etq">Paso 02 · Facilitar</div>
<h2>Si solo lo pide uno,<br><em>se nota</em></h2>
<p class="intro">Una reunión de cinco minutos antes de abrir y todo el equipo sabe qué hacer. Esta es la receta:</p>
<ol class="lista" style="list-style:none;gap:4mm">
  {''.join(f'<li><span class="num" style="font-size:22pt;color:var(--oro-os);width:10mm;flex:none">{i}</span><span style="padding-top:1.5mm"><b>{a}</b> {b}</span></li>' for i, (a, b) in enumerate([
      ('Explica el porqué.', 'La ficha de Google es el escaparate: más reseñas recientes, más gente que se anima a entrar.'),
      ('Elegid la frase de la casa.', 'Una sola, corta, que todos digan igual (apuntadla abajo).'),
      ('Probad la placa.', 'Cada uno acerca su móvil: que vean que se abre la ventana de escribir. En iPhone, con la pantalla encendida y acercando la parte de arriba.'),
      ('Decid quién la pide.', 'Lo normal: quien lleva la cuenta o cobra.'),
      ('Repasad cada semana.', 'Mirad juntos las reseñas nuevas. Si alguna nombra a alguien del equipo, díselo delante de todos.')], 1))}
</ol>
<div class="caja" style="margin-top:9mm;position:relative;padding-right:52mm">
  <span class="chip">Nuestra frase de la casa</span>
  <div class="linea-rell"></div><div class="linea-rell"></div><div class="linea-rell"></div>
  {BICHO('susurra-izq', 'right:2mm;bottom:-3mm;width:46mm')}
</div>
<div class="caja-oro" style="margin-top:7mm"><span class="chip">Ideas que funcionan</span>
  <ul class="lista" style="color:#D5DAE5;margin-top:2mm">{''.join(f'<li>{estrella(16)}<span>{t}</span></li>' for t in ['Pasad las reseñas nuevas al grupo del equipo: da gusto leerlas.', 'Cuando alguien lo pida bien, díselo. Se contagia.', 'Una vez al mes, probad las placas: que sigan abriendo tu ficha.'])}</ul></div>
</section>''')

# 7 · LAS REGLAS DE GOOGLE
si = ['Pedir reseña a <b>todos</b> tus clientes, les haya ido como les haya ido.',
      'Tener placas, QR y tarjetas a la vista.',
      'Recordarlo con educación, una vez.',
      'Contestar a todas las reseñas, buenas y malas.']
no = ['Dar algo a cambio: descuentos, un chupito, sorteos, puntos…',
      'Pedirla solo a los contentos, o pedir que sea de 5 estrellas.',
      'Escribir reseñas tú, tu familia o tu equipo.',
      'Comprar reseñas o pedírselas a quien no ha venido.',
      'Poner una tablet o un móvil del local para que escriban ahí.']
P.append(f'''<section class="pag">{cab(7, 'Las normas')}
<div class="etq">Lo que dice Google</div>
<h2>Las normas:<br><em>lo que sí y lo que no</em></h2>
<p class="intro">Google quiere reseñas de clientes de verdad, escritas libremente. Si detecta trampas puede <b>borrar reseñas</b> e incluso limitar tu ficha. Estas son las reglas básicas:</p>
<div class="fila" style="grid-template-columns:1fr 1fr">
  <div class="caja" style="border-top:1.4mm solid #2F8F5B"><h3 style="color:#1F6B42">Sí se puede</h3>
    <ul class="lista" style="margin-top:3mm">{''.join(f'<li>{SI}<span>{t}</span></li>' for t in si)}</ul></div>
  <div class="caja" style="border-top:1.4mm solid #C0392B"><h3 style="color:#8A2A1E">No se puede</h3>
    <ul class="lista" style="margin-top:3mm">{''.join(f'<li>{NO}<span>{t}</span></li>' for t in no)}</ul></div>
</div>
<div class="caja-oro" style="margin-top:9mm;position:relative;padding-right:58mm;min-height:50mm">
  <span class="chip">¿Y la placa?</span>
  <h3>Está dentro de las normas</h3>
  <p style="color:#D5DAE5">No regala nada ni elige a quién se le pide: solo le ahorra al cliente tener que buscarte. Es lo mismo que decir «¿nos dejas una reseña?», pero sin que cueste.</p>
  {BICHO('elegante-izq', 'right:4mm;bottom:-5mm;width:50mm')}
</div>
<p class="nota" style="margin-top:5mm">Resumen de la política de contenido de reseñas de Google. Las normas completas están en la ayuda de Google Business Profile.</p>
</section>''')

# 8 · CONTESTAR
resp = [('Buena', '#D5EBDD', '#1F6B42', '¡Muchas gracias, Laura! Nos alegra mucho que te gustara el salmorejo. Te esperamos pronto.'),
        ('Regular', '#F6E8C4', '#7A5A00', 'Gracias por contarlo, Pedro. Tomamos nota de la espera para mejorarla. Ojalá verte otra vez y que todo salga redondo.'),
        ('Mala', '#F2D6D2', '#8A2A1E', 'Sentimos mucho tu experiencia, Ana: no es lo que queremos para nadie. Escríbenos al 600 000 000 y lo hablamos con calma.')]
P.append(f'''<section class="pag">{cab(8, '03 · Contestar')}
<div class="etq">Paso 03 · Contestar</div>
<h2>Contesta todas.<br><em>También las malas.</em></h2>
<p class="intro">Quien lee tu ficha no solo lee las reseñas: <b>lee cómo contestas</b>. Una buena respuesta a una mala reseña dice mucho de tu local. Hazlo en uno o dos días.</p>
<div class="fila" style="gap:4.5mm">
  {''.join(f'<div class="caja" style="display:grid;grid-template-columns:28mm 1fr;gap:5mm;align-items:center;padding:5mm 6mm"><span class="chip" style="background:{c1};color:{c2};text-align:center">{t}</span><p class="cita" style="font-size:16pt">{r}</p></div>' for t, c1, c2, r in resp)}
</div>
<div class="fila" style="grid-template-columns:1fr 1fr;margin-top:9mm;gap:6mm">
  <ul class="lista">
    <li>{SI}<span><b>Usa su nombre</b> y un detalle de lo que cuenta: se nota que la has leído.</span></li>
    <li>{SI}<span><b>Corta y amable.</b> Dos o tres frases bastan.</span></li>
    <li>{SI}<span>En las malas, <b>lleva la conversación a privado</b>.</span></li></ul>
  <ul class="lista">
    <li>{NO}<span><b>Nunca en caliente.</b> Si te ha dolido, contesta mañana.</span></li>
    <li>{NO}<span><b>No discutas</b> en público, aunque tengas razón.</span></li>
    <li>{NO}<span>Si es falsa u ofensiva, no la contestes con otra: <b>denúnciala</b> desde tu ficha.</span></li></ul>
</div>
<div style="position:relative;margin-top:10mm;height:60mm">{BICHO('guino', 'left:0;top:0;width:52mm')}
<p class="mano" style="position:absolute;left:60mm;top:16mm;font-size:19pt;color:var(--oro-os);transform:rotate(-2deg);width:100mm">Guarda estas tres en las notas del móvil y cámbiales el nombre y el detalle. En un minuto, contestada.</p></div>
</section>''')

# 9 · PLAN DE 30 DIAS
semanas = [('Semana 1', ['Coloca las placas y pruébalas con tu móvil.', 'Reunión de 5 minutos con el equipo.', 'Apunta abajo tus reseñas y tu nota de hoy.']),
           ('Semana 2', ['Todo el equipo pide con la frase de la casa.', 'Contesta todas las reseñas nuevas.']),
           ('Semana 3', ['Mira qué funciona: ¿qué momento, quién lo pide mejor?', 'Si una placa no se usa, cámbiala de sitio.']),
           ('Semana 4', ['Compara con el día 1.', 'Cuéntaselo al equipo y celebradlo.'])]
caja = '<span style="display:inline-block;width:4.2mm;height:4.2mm;border:.4mm solid var(--oro-os);border-radius:1mm;flex:none;margin-top:.8mm"></span>'
P.append(f'''<section class="pag">{cab(9, 'Plan de 30 días')}
<div class="etq">Ponlo en marcha</div>
<h2>Tu plan de<br><em>30 días</em></h2>
<p class="intro">Ve marcando. Lo importante no es hacerlo perfecto: es <b>hacerlo todos los días</b> hasta que salga solo.</p>
<div class="fila" style="grid-template-columns:1fr 1fr;gap:4.5mm">
  {''.join(f'<div class="caja" style="padding:5mm 6mm"><h3 style="color:var(--oro-os)">{s}</h3><ul class="lista" style="gap:2mm;margin-top:1mm">' + ''.join(f'<li>{caja}<span>{t}</span></li>' for t in ts) + '</ul></div>' for s, ts in semanas)}
</div>
<div class="etq" style="margin-top:10mm">Apunta aquí</div>
<table>
  <tr><th></th><th>Día 1</th><th>Semana 1</th><th>Semana 2</th><th>Semana 3</th><th>Semana 4</th></tr>
  <tr><th>Reseñas en total</th><td></td><td></td><td></td><td></td><td></td></tr>
  <tr><th>Nota media</th><td></td><td></td><td></td><td></td><td></td></tr>
  <tr><th>Reseñas nuevas</th><td style="background:var(--crema2)"></td><td></td><td></td><td></td><td></td></tr>
</table>
<p class="nota" style="margin-top:3mm">Los números están en tu ficha de Google Business Profile. Con el seguimiento PLEA5E (opcional) sabes además cuánta gente ha acercado el móvil a cada placa.</p>
</section>''')

# 10 · CONTRAPORTADA
P.append(f'''<section class="pag oscura" style="padding:22mm 18mm">
<img src="{LOGO}" style="height:11mm">
<div style="margin-top:22mm">
  <div class="etq" style="color:var(--oro)">¿Lo ponemos en marcha?</div>
  <h1 style="font-size:50pt;line-height:1.06">Tú lo pides.<br><span style="color:var(--oro)">Nosotros<br>lo ponemos fácil.</span></h1>
</div>
<div style="margin-top:12mm;display:flex;flex-direction:column;gap:4mm;max-width:110mm">
  {''.join(f'<div style="display:flex;gap:4mm;align-items:baseline;border-bottom:.3mm solid #283049;padding-bottom:3mm"><span style="font-family:Anton;color:var(--oro);font-size:13pt;width:8mm">{estrella(12)}</span><span><b style="font-size:12pt">{a}</b><br><span style="color:#AEB5C6;font-size:9.5pt">{b}</span></span></div>' for a, b in [
      ('Placa de mesa', 'Con NFC y QR. Para cada mesa.'),
      ('Expositor de pie', '76 × 118 mm. Para la barra o la caja.'),
      ('Tarjeta de mano', '85 × 54 mm. Para el delantal o la cuenta.')])}
  <p style="color:#C9CEDA;margin-top:2mm">Con tu logo y tus colores. <b style="color:#fff">Las placas: pago único.</b> Te enseñamos el diseño antes de hacer nada.</p>
</div>
<div style="position:absolute;right:-16mm;top:118mm;width:110mm;height:110mm;border-radius:50%;background:radial-gradient(circle,rgba(233,188,70,.25),transparent 65%)"></div>{BICHO('megafono-izq', 'right:4mm;top:130mm;width:70mm;transform:rotate(4deg)')}
<div style="position:absolute;left:18mm;right:18mm;bottom:20mm;display:flex;align-items:center;gap:7mm;background:#fff;color:var(--tinta);border-radius:3mm;padding:5mm 6mm">
  <img src="{QR}" style="width:30mm;height:30mm">
  <div style="flex:1">
    <div class="mano" style="font-size:20pt;color:var(--oro-os);line-height:1">Escríbenos, respondemos en minutos</div>
    <div style="font-family:Anton;font-size:22pt;margin-top:2mm">WhatsApp 661 40 32 19</div>
    <div style="font-weight:700;font-size:12pt">plea5e.es</div>
    <div class="nota">Hechas en Córdoba · Envío a toda España</div>
  </div>
</div>
</section>''')

assert len(P) == total
open(G + 'guia.html', 'w').write(f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>PLEA5E · Cómo conseguir más reseñas en Google</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>')
print(total, 'paginas')
