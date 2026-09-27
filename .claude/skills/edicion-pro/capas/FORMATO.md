# FORMATO PLEA5E v7 — «motion design» (POR DEFECTO, 26-9 noche)
Referencias: vídeo tipo Spotify «Purity of Motion» (movimiento UI) + JoeEditor (cara con texto detrás).
- **Fondo** noche #06080E con 3 resplandores (verde placa #1C5A40, oro oscuro, verde profundo) que respiran.
- **Una sola tipografía: Figtree** (parecida a la de Spotify). Titular 600/96 px blanco con palabra clave en oro #E9BC46;
  frase pequeña 500/44 px gris claro. Letras que entran con desenfoque, subida y escala (22 ms entre letras).
- **La forma M**: un único elemento que se transforma (punto oro → píldora → marco redondeado con metraje real → se
  cierra en punto / se abre a pantalla completa). Nunca hay cortes secos: todo es la misma forma moviéndose (easeInOutExpo).
- **Metraje real de Mixkit** (licencia gratuita, uso comercial) dentro de la forma: aeropuerto 22613, baño 22089, camarero
  13258, móvil croma 28300 (`movil_key.py` mete la pantalla de reseña en el croma siguiendo el móvil).
- **UI**: chips tipo Spotify (el indicador oro pasa de «Obligar» a «Ponérselo fácil»), lista de reseñas con filas que suben con muelle.
- **Cara** (solo 4 tramos): se abre desde un recorte redondeado y se cierra en píldora; palabra gigante Figtree 800 detrás de la cabeza.
- **Cámara global** siempre viva (deriva + empujón en cada golpe).
- Sonido: whooshes y clics de Mixkit (`marketing/instagram/sonidos/mixkit`) + música «Hazy After Hours» a −19 dB con
  sidechain bajo la voz (`musica.py`).
Ejemplos completos: `mosca7.html`, `uber7.html`.
- **Producto en 3D, no fotos retocadas**: Juan no quiere la foto de la placa en mármol (hecha con IA). La placa se enseña en
  3D real con three.js (`placa3d.html` + `graba3d.js`): entra dando una vuelta completa, se ve la trasera, se asienta flotando.
  Diseño = `w-placa.png` del generador de la web. Tone mapping **Neutral** (ACES apaga el verde).
- **Nunca escenas vacías** (Juan, 27-9): cada escena lleva el marco con metraje real; los chips, barras y números van ENCIMA
  del metraje (capa `ui2`), con fondo oscuro translúcido y desenfoque.
- **SFX (27-9, definitivo): SIEMPRE `sonidos/packs/`** (ver su LEEME; woah-drop en producto/palabra clave/CTA, iphone-charging en el toque NFC). **Sin música.** Listas `sfx9-*.json`; remezclar sin re-render: `mezcla3.py` (copia el vídeo).
- (antes) **SFX: solo los buenos sacados de los vídeos** (`referencias/` tics, pops, clic-doble; `edicion/` arrow-swoosh, woah-drop,
  cinematic-impact, mouse-click, ding; `virales/` puntual). **Nada de efectos de Mixkit** (le parecen malos). Listas: `sfx8-*.json`.
- **Letras grandes**: titular Figtree 700/128 px, frase 600/58 px, subtítulos 700/66 px. Las palabras no se parten (`.wd`).

---
# FORMATO PLEA5E v6 — estilo JoeEditor (POR DEFECTO, referencia que mandó Juan el 26-9)
Juan: «este es el estilo que quiero» (vídeo de @JoeEditor). Rechazó v5 (gris/Inter, «fatal») y el bocadillo de comentario («se ve IA»);
v4 le parecía «más currado» pero con emojis de móvil. Lo que hay que hacer:
- **Metraje real** siempre que se pueda: su cara, fotos reales del producto (empuje + giro lento), grabaciones de pantalla,
  el momento real del móvil acercándose. Nada de emojis 3D.
- **Cara con texto detrás** (el «green screen» de CapCut, pero con su fondo real): plano completo abajo (960×1080 → 1080×1215,
  top 705) + el mismo fotograma desenfocado arriba; palabra grande entre el fondo y la persona (`#detras`), a la altura del pelo.
- **Tipografía**: subtítulos Poppins 600 blancos con sombra (1-4 palabras, aparecen palabra a palabra con «pop»); títulos
  **Noto Serif Display condensada 900 en oro #F2C230** (MAYÚSCULAS, estilo «MOSTRÁNDOTE»); acento manuscrito **Yellowtail** oro
  (palabra grande, se «escribe» con barrido) o **Mrs Saint Delafield** rojo #E0342B (detalle); números en serif cursiva roja («40»).
- **Transiciones**: fuga de luz cálida (naranja/blanca) en casi cada corte + whoosh; zoom de entrada; látigo; flash blanco en el ¡pum!.
- **Fondos**: negro con viñeta para títulos; **patrón de marca** verde placa #123D2D con estrellas grandes #195340 para pantallas
  (como el fondo azul con estrellas de JoeEditor); fotos reales oscurecidas para que se lean los subtítulos.
- Dibujo en línea blanca (urinario, diana) solo cuando no hay metraje; nada de pegatinas de colores.
- Sonido: whoosh en fugas, cinematic-impact en títulos, golpe suave en palabras detrás de la cabeza, woah-drop en el ¡pum!.
  JoeEditor lleva además **música de fondo** ~8 dB bajo la voz: añadir una canción en Instagram al publicar (volumen bajo).
Kit: `kit6.css` + `kit6.js` (independiente). Ejemplos: `mosca6.html`, `uber6.html`.

---
# FORMATO PLEA5E v5 — «como las referencias» (POR DEFECTO desde el 26-9 noche)

Juan rechazó la v4 (collage de pegatinas, Montserrat, oro sobre oscuro, recorte de su cara): «se ve IA, tipografía fea,
poco profesional». Lo que hacen de verdad las referencias (estudiado fotograma a fotograma):
- **Cara real a pantalla completa**, SIN recortar (nada de «green screen»). Subtítulos pequeños blancos a la altura del
  pecho (Inter Display 600, ~50 px), 1-4 palabras; «punch-in» (zoom seco 1,08-1,13) en la palabra fuerte.
- **Escenas en gris claro** (degradado suave + textura de papel muy leve). Texto **gris oscuro**, Inter Display
  (500 pequeño / 700 grande), centrado, sin cursivas ni colores. Letra a letra con desenfoque (@solazzox).
- **Objetos en blanco y negro** sin borde (como los recortes de @johan.mttz). **Solo la placa real va en color.**
- **Tipografía cinética 3D**: número o palabra gigante que gira en perspectiva (el «01» de @solazzox): `K.gira`.
- **Transiciones de editor** (`K.escenas5` + `K.efectos`): tinta (manchas que crecen), látigo lateral con desenfoque,
  estrobo blanco/negro + iris, zoom a través, corte con fuga de luz naranja. Una distinta en cada corte.
- Nada de fondo oscuro con oro, nada de pegatinas de colores, nada de chispas/brillos: huele a IA.
- Sonido: látigo = `whoosh-short`, estrobo = `edicion/glitch`, tinta/zoom = `ui/aire`, ¡pum! = `woah-drop`.
Ejemplos: `mosca5.html`, `uber5.html`; kit: `kit5.css` + `kit5.js` (sobre kit + kit2 + kit3).

---
(Formato v4 anterior, descartado:)
# FORMATO PLEA5E (v4) — la plantilla de todos los vídeos hablados

Hoja visual: `identidad.html` (se renderiza con `grabar.js identidad.html prueba id 0`).
Base de código: `kit4.css` + `kit4.js` (sobre kit/kit2/kit3). Ejemplos completos: `mosca4.html`, `uber4.html`.

## Estructura (30 s)
1. **Gancho con cara** (1-3 s): Juan recortado como pegatina (borde blanco), abajo; frase pequeña delante y la palabra
   grande DETRÁS de la cabeza. Un detalle vivo (la mosca volando alrededor).
2. **Historia en collage** (4-7 escenas): papel con fibra, titular arriba a la izquierda, UNA idea por escena,
   máx. 3 elementos (pegatina real/3D, cinta, papel rasgado, sello, garabato).
3. **¡Pum!**: destello + woah drop + la placa REAL (foto recortada) se pega con cinta.
4. **Demo**: el móvil toca la placa → pantalla de reseña con etiqueta «Demostración».
5. **Marca** (1 s, fondo noche): PLEA5E en Montserrat 900 con el 5 en oro. Nunca el sello de la estrella.
6. **CTA con cara**: «comenta PLACA» detrás de la cabeza + comentario que se escribe solo.
La cara no sale en medio: solo gancho y CTA.

## Tipografía (obligatoria)
Montserrat. Frase pequeña 700 / 52 px; palabra grande 900 / 128 px, interletra −5 %, interlínea 0,9;
palabra clave 900 **cursiva** en oro con subrayado. Alineado a la izquierda (margen 90). Detrás de la cabeza: 200-280 px.

## Ritmo
Entrada ≤ 0,45 s (muelle); cada elemento **quieto ≥ 1 s** antes de salir; nada entra mientras otro está a medias.
Si la frase va rápida, menos elementos, no más rápido.

## Zonas
Arriba 0-200 libre · titular 250-600 · contenido 700-1500 · abajo 1650+ libre (texto de Instagram) · derecha abajo libre (botones).

## Sonido
Voz: `voz.py` + cadena de `cadena-voz.txt` (RNNoise `arnndn` modelo std de github.com/richardpl/arnndn-models, puerta suave,
−3 dB a 250 Hz, +2,5 dB a 4 kHz, de-esser, compresor, −14 LUFS). La cadena antigua (afftdn) se comía los agudos: NO usar.
Efectos (`mezcla2.py`, alineados al golpe, base −14 dB): pegar = `ui/pega*.mp3`, cinta = `ui/cinta.mp3`, tachar =
`ui/rotulador.mp3`, cortes = `ui/aire-corto.mp3`, ¡pum! = `edicion/woah-drop.mp3`, toque = `edicion/mouse-click.mp3`,
estrellas = `tic-b` + `ding`, acierto = `cinematic-impact`, viral puntual = `vine-boom` / `nope` / `grillos` (0,6 s).
