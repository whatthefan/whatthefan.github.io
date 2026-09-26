---
name: edicion-pro
description: Editar vídeos cortos (Reels, TikTok, Shorts) como un editor profesional y hacer miniaturas trabajadas. Dos estilos — DINÁMICO (persona a cámara con cambios de fondo, persona recortada, iconos neón que se dibujan, palabras que golpean, flashes de color, texto detrás de la persona; el favorito de Juan) y PREMIUM SaaS (motion design oscuro y elegante). Incluye recorte de persona sin CapCut, capas, sonidos y lista de control. Úsala siempre que haya que editar un vídeo o hacer una miniatura/portada de PLEA5E, o cuando Juan pida «edición profesional», «como el vídeo de referencia», «estilo CapCut», «transiciones así» o «una miniatura currada».
---

# Edición pro

Dos estilos. **Por defecto, en vídeos de persona a cámara, usa el DINÁMICO (A).** El PREMIUM (B) es para
anuncios de producto sin persona. Todo lo que hace CapCut se hace aquí con código (tabla del apartado 4).

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

## C. Miniatura / portada

Plantilla aprobada: `miniatura.html`. Qué la hace funcionar:

1. **Foto buena de verdad**: cara quieta, mirando a cámara, nítida y sin gafas (Juan no quiere gafas ni caras en movimiento). Mejor una foto que un fotograma de webcam; si es pequeña, ampliar x1,7 con LANCZOS antes de recortar.
2. `python3 recorte.py foto.png persona.png` → recorte + `persona-borde.png`. Quitar manchas sueltas (quedarse con la mancha más grande del alfa).
3. Composición: título arriba (y 300-830), cabeza desde y≈880 y el cuerpo hasta abajo, placa real a la derecha sobre el hombro (nunca tapando la cara), icono NFC y «1 toque» con flecha a los lados sin tocar el pelo.
4. Todo lo importante entre y = 240 y 1680.
5. `node grabar.js miniatura.html prueba x 0`.

Si el recorte deja halo en el pelo (fondo claro detrás), no recortar: dejar la foto con su fondo desenfocado y oscurecido.

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

## 6. Sonido

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
- [ ] ¿Miniatura trabajada (apartado C), no un fotograma?
- [ ] Antes del render completo: 8-10 fotogramas clave compuestos y revisados.
