---
name: edicion-pro
description: Editar vídeos cortos (Reels, TikTok, Shorts) como un editor profesional y hacer miniaturas. Incluye también el estilo TARJETAS (voz en off sin cara, cuadrícula crema, tarjetas que entran con muelle). Estilo por defecto REFERENCIAS (aprendido de @solazzox, @ruy_r.s, @johan.mttz y @milah.edicion) — fondo papel gris u oscuro, una sola tipografía, texto que entra letra a letra desde desenfocado y sale con desenfoque vertical, capturas y producto real flotando en perspectiva, destello cálido en las transiciones y cristal sobre la persona desenfocada. Incluye recorte de persona, grabación de capas, montaje con ffmpeg, sonidos y lista de control. Úsala siempre que haya que editar un vídeo o hacer una miniatura/portada de PLEA5E, o cuando Juan pida «edición profesional», «como las referencias», «motion», «transiciones así» o «una miniatura».
---

# Edición pro

## ★ Estilo PLEA5E = la MEZCLA (el de por defecto)

No se copia un vídeo: se mezcla lo mejor de todas las referencias que ha pasado Juan.
- **Base (estilo 0, referencias)**: papel gris u oscuro, una tipografía (Inter), texto pequeño + grande palabra a
  palabra, salida con desenfoque vertical, destello cálido en los cortes, cristal sobre la cara desenfocada.
- **Escenas con historia (anatomía de escena)**: personajes a tinta, producto REAL de la web, cursor, chat, visor QR;
  entrada → anticipación → acción clavada a la palabra → remate.
- **Ritmo de las tarjetas (estilo 1)**: cambio cada 1,5-2,5 s; objetos que entran con muelle, abanicos de productos,
  capturas que hacen scroll, tachados en rojo.
- **Energía de @carlosdinamics (con medida)**: una palabra que golpea y un icono que se dibuja como mucho 1-2 veces por vídeo.
- **Elemento de marca**: la estrella PLEA5E (negra o dorada) como detalle que gira en una esquina en las escenas de papel, no en todas.
- **Cara**: 30-40 % como mucho; si Juan no graba cara, voz en off con las mismas escenas.
- **Sonido**: tics/pops/aire de `sonidos/referencias` y `sonidos/ui`, suaves.
- **Verdad**: diseños y precios reales; «Demostración» si no es un caso real.

## 0. Estilo REFERENCIAS (base de la mezcla)

Aprendido fotograma a fotograma de los 4 vídeos que Juan considera «edición increíble». Ejemplos: `ejemplo-escenas.html` (el modelo actual), `ejemplo-referencias.html` (demo 1) y `monta-referencias.py`.

**Lo que NO se hace (Juan lo rechazó: «parece hecho con IA»)**: oro metálico, relieves, cromo, contornos
de pegatina, neón, rayos, láseres, bokeh, destellos de estrella, polvo brillante, estrellas 3D, mesas 3D,
varios efectos a la vez, persona recortada con borde. Menos es más: una idea por escena.

### Lenguaje visual
- **Fondos**: papel gris claro (`radial-gradient` #f3f3f1 → #c3c3c1 con viñeta + grano muy suave) u oscuro casi negro (#1b1c20 → #060607). Nada más.
- **Tipografía**: UNA sola (Inter). Estructura fija: línea pequeña (600, ~54 px, -1,6 px) encima de línea grande (800, ~134 px, -6 px, interlineado 0,98). Texto negro en papel, blanco en oscuro. Solo una palabra de color plano (oro #D39B16 en papel, #E9BC46 en oscuro). Sin sombras duras ni degradados.
- **Subtítulos sobre la persona**: minúscula, blancos, 700 ~46 px con sombra suave, a la altura del pecho (y≈1190); la palabra clave debajo en grande y en oro. Nada de mayúsculas ni cajas.
- **Objetos reales**: capturas de UI (buscador de Google, pantalla de reseña, notificación), el producto real (foto de la placa), un móvil sencillo. Siempre flotando en perspectiva (rotateY -26→-10, rotateX 6-8), con sombra suave doble y deriva lenta (se giran 1-2°/s y suben/bajan 4-6 px).
- **Números gigantes** (900-1000 px) cortados por el borde, con el texto a su lado.
- **Cristal**: sobre la persona desenfocada (gblur fuerte + velo negro 40 %), tarjetas y pastillas de cristal (blanco 10-20 % con borde de luz arriba) que entran escalonadas. Un detalle de color (pastilla oro).
- **Ritmo**: se alterna persona ↔ escena gráfica cada 1-3 s. Las escenas gráficas tapan la pantalla entera mientras la voz sigue. Se vuelve siempre a la persona.

### Animaciones (medidas de las referencias)
| Animación | Cómo | Tiempos |
|---|---|---|
| Entrada de texto | cada letra: opacidad 0→1, `blur(12px)`→0, 10 px abajo→0, desfase 18 ms por letra, cada palabra en su tiempo de Whisper | 0,24 s por letra, `outCubic` |
| Salida de texto | todo el bloque: desenfoque SOLO vertical (filtro SVG `feGaussianBlur stdDeviation="0 N"`, N 0→26) + sube 40 px + se desvanece | 0,16 s, `inCubic` |
| Entrada de objeto | desde `blur(16px)`, escala 0,92→1, opacidad, enderezando la perspectiva | 0,4-0,6 s, `outExpo` |
| Deriva | giro y flote lentos mientras está en pantalla | continuo |
| Destello de transición | capa radial blanco→crema→naranja: sube en 2 fotogramas, baja en 6 (opacidad máx. 0,92). Persona → escena gráfica | 0,27 s |
| Desenfoque de fondo | la persona se desenfoca (fundido del gblur en 0,2 s) y encima entra el cristal escalonado (90 ms entre piezas) | 0,2 s + 0,35 s |
| Escalonado de UI | tarjetas, filas y pastillas entran una a una en la palabra que las nombra | 0,35-0,42 s cada una |
| Móvil que se acerca | `inOutCubic` desde fuera de cuadro hasta junto al producto, anillo oro que se expande al «tocar» | 0,65 s + 0,45 s |
| Cortes | persona ↔ persona y escena → persona: corte seco. Final: corte a negro seco | — |

### Tú hablas, las representaciones mandan
Juan no es el foco: la cara sale como mucho un 30-40 % del vídeo (gancho, preguntas, remate). El resto son
**representaciones** de lo que dice, cada una una pequeña historia completa. Modelo actual:
`ejemplo-escenas.html` (demo 3, aprobada como dirección). `anatomia-escena.png` lo explica en 4 fotogramas.

**Prohibido** (Juan lo rechazó): fondos «liminales» (salas vacías con haz de luz), la mascota Estrellita en
las escenas, swooshes fuertes en cada corte, efectos decorativos sin historia.

### Anatomía de una escena (obligatoria)
1. **Una idea, un foco.** Soporte (papel u oscuro) + UN objeto protagonista + como mucho un personaje + el texto arriba.
2. **Entrada 0,3-0,6 s por jerarquía**: soporte (línea de mesa que se dibuja, lienzo) → objeto (cae con muelle) →
   personaje (entra de lado con muelle amortiguado) → detalles. 80-120 ms entre piezas (`E.entra`, `E.muelle`).
3. **Anticipación**: algo prepara el ojo justo antes (línea punteada que se traza, cursor que viaja, «escribiendo…»).
4. **Acción clavada a la palabra**: UN suceso (visor que escanea en «QR», clic que cambia el color en «colores»,
   burbuja en «verde», tachado en «y ya»). Solo una cosa se mueve a la vez. `E.golpe` para el pulso de clic.
5. **Remate**: consecuencia visible (la cara del personaje cambia a sonrisa, píldora «Reseña abierta», «¡Perfecta!»).
6. **Mantenimiento**: cámara que empuja 3-4 % (`E.camara`) y flote leve; nunca congelado.
7. **Salida**: a otra escena → el contenido sube con desenfoque vertical 0,18 s y el fondo se queda (`E.salida`
   sobre `.cam`); a la cara → corte seco.

| Si la frase habla de… | Escena |
|---|---|
| cómo se usa (tocar, escanear, QR) | mesa + producto real + clienta con el móvil; trazo al QR, visor, «Reseña abierta», sonríe |
| personalización (logo, colores, nombre) | **editor**: lienzo con asas, la placa, barra de colores; el cursor marca «tu logo» y hace clic en cada color |
| precio, gratis, aprobación | móvil con WhatsApp + la dueña del bar reaccionando (desconfiada → tranquila → encantada) |
| enumeraciones | cartas que caen en mazo y se reparten a su sitio en la palabra de cada una |
| lo que NO es | el objeto flota y en la palabra se tacha la frase y el objeto se va |
| formación, equipo | la guía real entra girando + el equipo sube desde abajo uno a uno + bocadillo que se escribe |
| un dato / un cero | número gigante cortado por el borde |
| rapidez, se abre solo | móvil con la pantalla de reseña: se enciende y las estrellas se rellenan en la palabra |

### Personajes (cuando hay que enseñar algo que ocurre)
Personas dibujadas a tinta (Open Peeps, CC0/MIT) en grises cálidos con **un solo acento oro** (el móvil, la taza,
la camiseta). Reparto listo en `personajes/reparto/` (clienta, dueña, camarero, camarera, cocinero, de pie,
sentado) con varias caras cada uno para el remate. Para nuevos: `personajes/registro.py` + `genera.mjs` (ver
instrucciones dentro): tipo busto, de pie o sentado; 53 peinados, 33 caras, 27 bustos, 23 cuerpos de pie, 11
sentados. Los bustos se cortan con el borde de la pantalla o con la línea de mesa, nunca flotando.

### Diseños de producto (siempre los originales)
Las placas, expositores y tarjetas que salen en los vídeos son **los diseños reales de la web**, sacados del
generador (`public/taller/generador.html`) con
`node disenos/desde-web.js salida/ '[{"f":"placa","negocio":"Bar Manolo","lema":"Bar · Tapas","banda":"#7A1E2B","n":"placa-granate"}]'`
(f: placa | stand | tarjeta; banda, fondo y acento opcionales). Nunca recreaciones hechas a mano.
`disenos/exporta.js` solo para la pantalla de reseña del móvil y la notificación.
Precios: los de la web en ese momento (hoy: placa de mesa 25 €, expositor 28 €, tarjeta de mano 15 € en packs de 20 a 100).
Si un vídeo cuenta una visita que no ha pasado, va con la etiqueta «Demostración»; «caso real» solo si lo es.


### Vídeo hablado v2 (preferencias de Juan, 26-9)
- Cara **más lejos**: dentro de una tarjeta redondeada sobre papel, NO a pantalla completa. Sin espejo.
- Si enseña la placa física en blanco: **meterle el diseño dentro** (`capas/placa_quad.py` + `placa_pinta.py`).
- **Nada del sello de la estrella**: la marca va en letras PLEA5E.
- Sonidos: los de `edicion/` y algún viral puntual, alineados por el golpe (`capas/mezcla2.py`).
- Motion más currado: `capas/kit2.js` (ver `capas/LEEME.md`).
- **Actualización (v3, la que más le gusta)**: vídeo en espejo; Juan RECORTADO sobre papel, más lejos, con las letras
  alrededor por niveles (palabra grande detrás de la cabeza, frase delante, pegatinas). Tipografía: Bricolage Grotesque +
  Instrument Serif cursiva (no Inter en las frases). Base: `capas/kit3.*`, ejemplos `mosca3.html` y `uber3.html`.

### Sonido (lo que usan las referencias: sutil, de interfaz)
- `sonidos/referencias/`: tics, clics y pops **extraídos** de los 4 vídeos (`separa.py` quita la voz con UVR
  MDX-Net y se recorta cada golpe). Uso de perfil, no anuncios de pago.
- `sonidos/ui/`: versiones limpias sintetizadas (`sintetiza.py`): `aire-corto` (transición), `pop`, `tic`,
  `golpe-suave` (algo cae), `brillo` (acierto), `subida`.
- Reparto: transición cara→escena `aire-corto` 0,2; escena→escena `aire-corto` 0,16; objeto o personaje que llega
  `pop` 0,2-0,25; acción (visor, clic, carta) `tic` 0,3-0,35; remate `brillo` 0,2; burbujas de chat `pop` 0,22.
  Nada de `woah-drop` ni swooshes largos en este estilo. La voz siempre por encima.

### Proceso
1. Transcribir (Whisper) → palabras con tiempo. 2. Decidir escenas: qué frases van con persona y cuáles con escena gráfica (una idea visual por frase). 3. Copiar `ejemplo-referencias.html` y cambiar `ESC`, `BLUR`, `TX` y los objetos. 4. Revisar 12-14 fotogramas compuestos. 5. `node grabar.js pagina.html todo capa.mov`. 6. `monta-referencias.py` (tramos de desenfoque; si el tramo es pantalla partida, ampliar la mitad de abajo). 7. Comprimir < 30 MB.

## 1. Estilo TARJETAS (voz en off, sin cara; solo como ingrediente de la mezcla) — ejemplo `ejemplo-tarjetas.html`

Aprendido de un reel viral de tutorial (voz en off, 34 s, ~20 cortes). Útil cuando Juan no quiere salir o para
explicar un proceso. Mismo criterio de sobriedad que el estilo 0.

- **Fondo fijo** todo el vídeo: crema `#FBF4DC` con cuadrícula fina (54 px, negro al 4,5 %).
- **Elemento de marca en las esquinas**: formas negras grandes con brillo 3D (aquí la estrella de PLEA5E) cortadas por
  los bordes, girando despacio; en cada corte aceleran con desenfoque de movimiento. Es lo único que se mueve siempre.
- **Texto**: UNA línea arriba (y≈300), Inter 800 ~58 px, palabra a palabra con la voz, palabra clave en oro. No hay subtítulos abajo.
- **Cada frase = una tarjeta** (esquinas 34 px, sombra suave cálida) en el centro: captura de la web, el producto real,
  la pantalla del móvil, un buscador, un personaje. Entra con muelle desde abajo/lado (girada 6-8° que se endereza) y
  sale subiendo con desenfoque. Cambio de tarjeta cada 1,5-2,5 s.
- **Recursos**: abanico de productos (3 tarjetas que se abren en la palabra), capturas largas que hacen scroll solas,
  un objeto que entra a la tarjeta (móvil hacia la placa), chips negros que se tachan en rojo, un golpe (estrella que cae en «¡boom!»).
- **Sonido**: la voz manda; pop en cada tarjeta, tic en cada acción, aire corto en cada corte, brillo en el acierto.

## C. Miniatura

Plantilla aprobada: `miniatura.html` (estilo REFERENCIAS). Foto real de Juan SIN recortar (quieta, mirando a
cámara, sin gafas), a lo ancho arriba y fundida a negro; debajo línea pequeña «reseñas en Google en» + grande
«**10** segundos» (10 en oro) + línea gris pequeña. Marca PLEA5E arriba, discreta. Nada más: sin contornos, sin
brillos, sin collage. Si la foto es pequeña, ampliar a 1080 con LANCZOS + nitidez suave + grano ligero.

---

## Estilos antiguos (solo si Juan los pide expresamente)

Estos estilos quedan como referencia; el de por defecto es REFERENCIAS (apartado 0). Las herramientas
(apartados 4 y 5) sirven para todos.

## A. Estilo DINÁMICO (referencia: @carlosdinamics, «antes/después»)

La idea: **la persona habla sin parar y la pantalla cambia cada 1,5-3 s**. Nunca más de 3 s con el mismo
plano sin que pase algo. Cada frase importante tiene su «evento visual» justo en la palabra.

### A1. Los recursos (lo que se ve en la referencia, con el tiempo exacto)

| Recurso | Cómo es | Cuándo | Herramienta |
|---|---|---|---|
| **Cambio de fondo + persona pequeña** | el fondo de la habitación desaparece: fondo oscuro con **cuadrícula** fina y un resplandor; la persona recortada, **reducida al 60 %** y pegada abajo; arriba, iconos | para explicar un concepto (1-2,5 s) | `recorte.py` + capa `#detras` + `pequeno` en `compone.py` |
| **Iconos de línea que se dibujan** | iconos blancos de trazo (sin relleno) con brillo, que se dibujan trazo a trazo; a veces 2 iconos y uno se mueve (sobre que entra con líneas de velocidad, manecilla que gira, hacha que golpea) | en el sustantivo que dice | `iconos.js` + `M.dibuja` + clase `.neon` |
| **Iconos neón de color** | 2-3 iconos iguales con brillo de color (rosa en la ref., **oro** en PLEA5E) que salen con rebote uno detrás de otro + la palabra debajo en mayúsculas | enumeraciones («tres motivos») | `M.pop` con 0,1 s de desfase |
| **Palabra que golpea** | una sola palabra ENORME (Anton) que aparece en blanco, pasa a color con una sacudida y luego se inclina | órdenes y palabras clave («PARA», «PEREZA») | `M.pop`/`M.sacude`, cambiar color a los 0,2 s |
| **Flash de color** | 2 fotogramas de tinte rojo sobre la imagen + 2 fotogramas de destello naranja/oro casi opaco, y corte | antes de un cambio fuerte de escena | `M.flash(el, t, t0, ['rgba(229,72,77,.45)','rgba(255,190,70,.85)'])` + `glitch.mp3` |
| **Haz de luz** | un arco blanco brillante que cruza la pantalla en 0,4 s | transición entre escenas | `M.arcoLuz` + `arrow-swoosh-2.mp3` |
| **Texto detrás de la persona** | una palabra gigante (marca, concepto) cruza de derecha a izquierda POR DETRÁS de la cabeza; a la vez el fondo se funde a una imagen de IA a juego | al nombrar una herramienta o la marca | `M.marquesina` en `#detras` + mate |
| **Barrido de cámara** | la imagen se desliza de lado, la persona sale de cuadro y queda la pared con una palabra en serif («TIEMPO») y un icono brillando | frases reflexivas | desplazar la base con `crop` en ffmpeg o recortar la persona y moverla |
| **Fondo de rayos/energía** | fondo negro con rayos o chispas de color (morado en la ref.) y un icono gigante brillante («1h») encima de la persona pequeña | la cifra o el dato más fuerte | fondo en `#detras` (CSS o imagen de IA) |
| **Subtítulos mínimos** | MAYÚSCULAS, Inter 800, 44-52 px, 1-3 palabras, blanco con sombra, a ~77 % de alto; la palabra clave en oro | siempre | `SUBS` del plan (Whisper) |

### A2. Ritmo

- Un evento visual cada **1,5-3 s**; entre medias, plano normal (la referencia vuelve siempre a la persona a pantalla completa, eso da respiro).
- Los eventos van **en la palabra**, no antes ni después (tiempos palabra a palabra de Whisper).
- Máximo 1 flash de color cada 10 s. Máximo 2 «palabras que golpean» por vídeo.
- Los fondos nuevos duran lo que dura la frase y se van con **corte seco** o con el haz de luz.

### A3. Capas (de atrás hacia delante)

1. `base.mp4` — la persona (cortes, encuadre, voz limpia: ver apartado 5).
2. `#detras` — fondos nuevos opacos (cuadrícula, rayos, imagen de IA) y texto que va detrás de la persona.
3. **persona** — `base` + `mate.mp4` de `recorte.py`. En las ventanas `pequeno` se dibuja reducida y abajo, con los laterales difuminados (por si la toma es cerrada).
4. `#delante` — iconos, palabras, subtítulos, flashes, haz de luz, marca `PLEA5E.es`.
5. Sonidos.

Una sola página HTML con `render(t)` pinta las dos capas (`#detras` y `#delante`, según `location.hash`).
`ejemplo-dinamico.html` es un ejemplo completo y probado de 6 s: cópialo y cambia escenas y tiempos.

### A4. Imágenes de IA (Grok, Flow…)

Claude no tiene acceso a Grok ni a CapCut. Si una escena necesita una foto concreta («un camarero
sirviendo», «un cliente mirando el móvil en una terraza»), **escribe el prompt** para que Juan la genere y la
pase; mientras tanto usa fondos de CSS (cuadrícula, rayos, degradados) e iconos de línea, que es lo que más
usa la referencia. Prompt tipo: *«fotografía vertical 9:16, [escena concreta], luz cálida de bar al
atardecer, estilo cinematográfico, profundidad de campo, sin texto, sin logotipos, tonos oscuros con acentos
dorados»*. Imágenes de IA en un vídeo → marcar el contenido como generado con IA en TikTok/Instagram.

## B. Estilo PREMIUM SaaS (referencia: anuncio de «Marz»)

| Regla | Cómo se hace |
|---|---|
| Fondo casi negro | `#0A0B0F` con degradado radial y viñeta |
| Un solo acento | oro `#E9BC46`; rojo `#E5484D` solo para lo negativo |
| Texto pequeño y fino | Inter 44-64 px, peso 400-500, mucho aire; palabra a palabra desde desenfoque (`M.palabras`), una palabra en oro |
| Profundidad | pantallas de app en 3D que se enderezan (`M.tilt`), todo flota un poco |
| Interfaces vivas | campo que se escribe (`M.teclea`), cursor que pulsa (`M.cursor`), contadores (`M.cuenta`) |
| Transiciones | desenfoque cruzado (`M.blurIO`), barrido (`M.whip`), empuje hacia la interfaz, tarjetas apiladas |

Curvas: entradas `outExpo` 0,4-0,6 s, salidas `inCubic` 0,25-0,3 s. Juan prefiere el DINÁMICO para vídeos con él.

## 4. CapCut → aquí

| CapCut | Aquí |
|---|---|
| Eliminar fondo / recorte automático | `recorte.py` (RobustVideoMatting, 15 MB, CPU, ~6 fps) |
| Fotogramas clave | `render(t)`: todo es función del tiempo |
| Brillo / neón | `filter: drop-shadow(...)` en capas (clase `.neon`) |
| Efectos «Flash», «Destello» | `M.flash` |
| Sacudida | `M.sacude` |
| Texto animado / plantillas | `M.palabras`, `M.pop`, `M.dibuja` |
| Pegatinas / iconos | `iconos.js` (línea blanca, se dibujan solos) |
| Superposición / capas | `compone.py` (detrás → persona → delante) |

## 5. Cómo se hace (herramientas)

Si la skill se usa fuera del repo de PLEA5E (versión global en zip), los sonidos están en `sonidos/` y las
fuentes en `fuente/` dentro de la propia carpeta de la skill.

Carpeta de trabajo en `/tmp` (los vídeos y fotos de Juan NO van al repo, que es público). ffmpeg: si no
está en el PATH, usar el de `imageio-ffmpeg` (`python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"`).
Scripts completos de un short real en `marketing/instagram/short-juan/`.

1. **Transcribir** con Whisper local (sherpa-onnx + `sherpa-onnx-whisper-small`, de las releases de GitHub de k2-fsa) → palabras con tiempos.
2. **plan.py**: cortes en los valles de energía (nunca a mitad de palabra), escenas, eventos y sonidos en tiempo de salida.
3. **base.py**: recorta, `hflip` si la cámara graba en espejo (Mac), encuadra siguiendo la cara (OpenCV haar), empuje lento y voz limpia (paso alto 85 Hz, reducción de ruido, compresor, `loudnorm` -14 LUFS).
4. **Recorte**: `python3 recorte.py base.mp4 mate.mp4`.
5. **Capas**: página HTML con `motion.js` + `iconos.js` → `node grabar.js pagina.html prueba todo 1.2 3.4` para revisar fotogramas; luego `node grabar.js pagina.html detras detras.mov` y `... delante delante.mov`.
6. **Montaje**: `python3 compone.py montaje.json` (ver docstring: base, mate, capas, ventanas `pequeno`, escala, sonidos).
7. Comprimir a < 30 MB para mandarlo (vídeo a 3400-3600k).

Si hay que sustituir una frase, se cambia **solo la voz** (`atempo` ≤ 1,12 y volumen igualado al original
menos 1,5 dB); la imagen se queda.

## 6. Sonido (solo estilos antiguos; el actual está en el apartado 0)

Carpeta `marketing/instagram/sonidos/edicion/`: `arrow-swoosh`/`arrow-swoosh-2` en barridos y haz de luz,
`glitch` en el flash de color, `woah-drop` en la revelación fuerte (máx. 2-3), `mouse-click` cuando se
dibuja un icono, `ding` en un acierto, `cinematic-impact` en la palabra que golpea o en la cruz roja,
`punch-riser` justo antes, `camera-shutter` cuando aparece el producto, `mac-typing` al escribir.
**Nada de memes.** Efectos a 0,3-0,5 frente a la voz; la voz siempre manda. Nada de «sonido de cortar» en
cada corte: los cortes van secos con 30-50 ms de fundido de audio.

## 7. Lista de control antes de entregar

- [ ] ¿Pasa algo en pantalla cada 1,5-3 s, clavado en la palabra?
- [ ] ¿Hay al menos: un cambio de fondo con persona pequeña, iconos que se dibujan, una palabra que golpea y una transición de luz o flash?
- [ ] ¿Subtítulos pequeños, en mayúsculas, 1-3 palabras, una clave en oro? ¿Nada de emojis?
- [ ] ¿El recorte de la persona es limpio (pelo, gafas, manos)? ¿Sin bordes rectos visibles?
- [ ] ¿Sonidos de edición a volumen por debajo de la voz?
- [ ] ¿Nada importante en los 250 px de abajo? ¿Marca `PLEA5E.es` discreta?
- [ ] ¿Final a negro seco (sin fundido lento), sin subtítulos ni barra encima, sin que se vea levantar la mano?
- [ ] ¿Cámara en espejo corregida?
- [ ] ¿Nada inventado ni promesas de reseñas? («Las placas: pago único», nunca «sin cuotas»). ¿La «5» de PLEA5E nunca en espejo?
- [ ] ¿Miniatura como la plantilla (apartado C): foto real sin recortar, texto limpio, nada de brillos?
- [ ] ¿Parece editado por una persona y no «hecho con IA»? (una tipografía, un color, una idea por escena)
- [ ] Antes del render completo: 8-10 fotogramas clave compuestos y revisados.
