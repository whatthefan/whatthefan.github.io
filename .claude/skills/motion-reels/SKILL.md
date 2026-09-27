---
name: motion-reels
description: Editar Reels, TikTok o Shorts en el estilo que Juan aprobó (PLEA5E y su canal de emprendimiento). Es motion graphics fotograma a fotograma en HTML, con la cara recortada y la palabra gigante detrás de la cabeza, texto que entra de lado, forma que se transforma y muestra metraje real, y un sistema en el que cada SFX va unido a su transición (flash, whip, glitch, riser+impacto, zoom digital, teclas). Úsala SIEMPRE que Juan pida editar un vídeo, "con la edición chula", "como el de la mosca", motion, transiciones, SFX, o un vídeo para PLEA5E o para su canal. Sustituye como estilo por defecto a edicion-pro.
---

# motion-reels: la edición de la mosca y Uber (v16, aprobada)

Resultado de unas 16 rondas de feedback de Juan. **Primero lee "Reglas de Juan"**: cada una salió de algo que rechazó.
Ejemplos completos que funcionan: `ejemplos/mosca.html` y `ejemplos/uber.html`. Para abrirlos, ponlos junto a `motor/escena.js`, `fx.js` y `fuentes/`; necesitan sus assets en /tmp (cara, `br/`), que no están en el repo. Base limpia: `motor/plantilla.html`.

## Reglas de Juan (no negociables)
1. **Sin música. Solo SFX**, y solo de `marketing/instagram/sonidos/packs/` y `packs2/` (catálogo abajo). Nada de Mixkit SFX ni sonidos sintetizados.
2. **Un sonido por evento con significado.** No se pone sonido de relleno, ni en cada letra o chip, **ni en las estrellas**.
3. **Cada sonido va con su efecto visual** (sistema FX): si suena un whoosh, la imagen hace un whip.
4. **Los sonidos no se cortan nunca.** Solo `teclas` y `contador` llevan `dur`, y siempre con fundido.
5. **Vetados:** booms graves (`braam`, `synth-hit`, `cinematic-impact`, `riser-impacto`), `packs/glitch` y `punch-stop-riser`. Le suenan "raros, de bomb box".
6. **El vídeo empieza con sonido**: `flash` + `camera-shutter` en t=0. En los primeros 3 s, cada cambio de escena lleva su whoosh o swish.
7. **Texto que se escribe = teclado**: `maq: true` + `teclas` con `dur = letras × st + 0,15`.
8. **El `woah-drop` es su favorito**: revelación del producto, nudge y palabra final (PLACA). Máximo 3 por vídeo.
9. **Movimiento de lado a lado** (referencia Marz): el texto entra desde la derecha y sale a la izquierda; la forma M entra por la derecha y sale por la izquierda.
10. **Nada de escenas vacías.** Siempre hay metraje real, un objeto real (placa en 3D, móvil con croma) o una animación explicativa (el urinario con el hombre).
11. **Nada que parezca IA:** sin emojis, sin bocadillos de comentario al final, sin fotos generadas con IA (el producto va en 3D real) y sin el "logo raro de la estrella".
12. **Tipografía:** Figtree 700/800 grande y legible. La palabra clave en color de marca con `*palabra*`.
13. **Cara:** solo en el gancho, a mitad y en el CTA, con la palabra GIGANTE detrás de la cabeza ("lo de la cámara mola"). La cara del vídeo en espejo.
14. **PLEA5E:** sin claims inventados y nunca prometer reseñas. "Las placas: pago único". Colores noche #06080E y oro #E9BC46. El 5 nunca en espejo. "Demostración" en las pantallas simuladas.
15. **Privacidad:** la cara y los vídeos de Juan **nunca van al repo público**. Se quedan en /tmp o en el scratchpad.

## Flujo completo
1. **Voz**: corta los silencios y las tomas malas (`scripts/base2.py`, con los tramos de `scripts/palabras.py`, que usa Whisper local con sherpa-onnx). Limpia con la cadena de `scripts/cadena-voz.txt` (RNNoise, puerta, EQ, de-esser, compresor, loudnorm -14). La duración de la voz = `TOTAL`.
2. **Tiempos por palabra**: con `palabras.py` se sabe en qué segundo cae cada palabra. Los textos y los FX se clavan a esas palabras.
3. **Cara recortada**: pasa la matte de RVM por `scripts/persona.py`, que da el fondo en jpg y la persona en webp con alfa del mismo fotograma. **Preescala a 1080×1215 con lanczos + nitidez** (ver "Calidad").
4. **B-roll**: usa Mixkit (gratis y comercial). `https://assets.mixkit.co/videos/<id>/<id>-720.mp4`; el 1080 da 403. Para buscar, `curl https://mixkit.co/free-stock-video/<tema>/ | grep -o 'videos/[0-9]*/[0-9]*-360.mp4'` y haz una hoja de miniaturas para elegir. Pexels y Pixabay dan 403. Extrae con `ffmpeg -ss 1 -i clip.mp4 -frames:v 90 -vf "fps=30,scale=1920:1080:flags=lanczos,unsharp=5:5:0.6" -q:v 3 br/nombre/%04d.jpg`. Elige clips **que peguen con la frase** (un bar real para hostelería, no una tienda de ropa).
5. **Producto en 3D**: `scripts/placa3d.html` + `graba3d.js` (three.js, RoundedBox, NeutralToneMapping; ACES agrisa los colores). Da 80 PNG. Chromium: `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader`.
6. **Móvil con pantalla**: `scripts/movil_key2.py` hace el croma del clip Mixkit 28300 y pinta la pantalla fotograma a fotograma (estrellas que se rellenan una a una con rebote). En la página, zoom hacia la pantalla mientras se rellenan.
7. **Página**: copia `motor/plantilla.html` (junto a `escena.js`, `fx.js` y `fuentes/`) y escribe el guion (API abajo).
8. **Prueba** fotogramas sueltos antes de grabar: `node motor/grabar.js pagina.html prueba a 1.0 2.5 9.6` y monta una hoja.
9. **Exporta**: `scripts/exporta.sh pagina.html voz.wav salida.mp4`. Graba, mezcla en HQ, borra el .mov (unos 1,8 GB) y, si pasa de 29 MB, saca `-chat.mp4` a dos pasadas para mandarlo por el chat.

## API de la página
- `texto(html, 'h'|'p'|'gig', y, t0, t1, {size, center, capa, st, maq})`: letras que entran de lado con desenfoque y muelle, y salen a la izquierda. `*x*` pone la palabra en color de marca. `maq:true` es a máquina con cursor.
- `sub(txt, t0, t1, tFinal, y)`: subtítulo sobre la cara, palabra a palabra.
- `gigante(txt, t0, t1, y, size)`: palabra enorme **detrás** de la persona (capa `detras`).
- `MK.push([t, x, y, w, h, radio], ...)`: la forma M (punto → píldora → marco) con easeInOutExpo. `IMG = [[t0, t1, 'br/dir/', nFotogramas, 'jpg']]` muestra metraje dentro. El bucle final hace que entre por la derecha y salga por la izquierda.
- `CARA = [[t0, t1], ...]`: la cara se abre desde una píldora y se cierra en píldora.
- `fx(t, efecto, sonido, db, {d, a, dir, dur})`: **la única lista de verdad**. `mezcla4.py` lee de ella el audio, así que el sonido y la imagen nunca se desincronizan. `mezcla2` alinea el **pico** de cada sonido con `t`.
- Capas, de fondo a frente: `fondo` (3 resplandores que respiran) → `ui` → `M` → `p3d` → `ui2` (chips y tarjetas encima del metraje) → `cara` (`detras` + persona) → `subs` → `grano` (.025).

## Efectos FX (motor/fx.js) y su sonido
| efecto | qué hace | sonido | cuándo |
|---|---|---|---|
| `flash` | flash blanco 0,03 s + punch 8 % | `packs2/obturador-flash`, `packs/camera-shutter` (t=0) | a y desde la cara; arranque |
| `whip` | barrido lateral 240 px con desenfoque de movimiento y zoom; `dir` alterna | `packs2/whoosh-b`, `swoosh-a`, `swish-c`, `whoosh-dramatico` | cambio entre escenas de metraje |
| `glitch` | RGB separado + franjas desplazadas | `packs2/glitch` | corte raro, algo que "falla" (NUNCA) |
| `riser` (`d`) | zoom lento, temblor creciente, viñeta oscura | `packs2/riser-metal` (su pico cae al final) | antes de una revelación |
| `impacto` (`a`) | sacudida amortiguada + punch + mini flash | `packs/woah-drop` (revelación), `packs2/whoosh-dramatico` (palabra gigante), `packs2/pop-imagen` (aterriza algo) | justo en el golpe |
| `zoomdig` | zoom a 3 saltos | `packs2/zoom-digital` | marca o logo |
| `null` | solo sonido | ver catálogo | UI, tachar, acierto, teclas |

## Catálogo de sonidos (`marketing/instagram/sonidos/`)
- **Transición**: `packs2/whoosh-b` (-4 dB), `packs2/swoosh-a`, `packs2/swish-c`, `packs2/whoosh-dramatico`, `packs/arrow-swoosh`, `packs/arrow2-swoosh`
- **Revelación**: `packs/woah-drop` (-2 dB; el favorito), precedido de `packs2/riser-metal`
- **Palabra gigante**: `packs2/whoosh-dramatico` (-3 dB) con `riser` visual corto (0,8 s)
- **Acierto / error**: `packs/right` (campanita aguda), `packs/wrong` (zumbido grave). Los nombres ya están corregidos; estaban cambiados.
- **UI**: `packs2/pop-imagen` (aparece algo), `packs/mouse-click`, `packs/iphone-charging` (el móvil toca la placa por NFC), `packs/ding` (llega la reseña o queda limpio)
- **Texto y números**: `packs2/teclas` (con `dur`), `packs2/contador` (chips o días que avanzan, con `dur`), `packs2/carga`
- **Movimiento**: `packs2/whoosh-mov` (alguien entra andando), `packs2/zoom-digital`
- **Vetados**: `packs2/braam`, `packs2/synth-hit`, `packs/cinematic-impact`, `packs2/riser-impacto`, `packs/glitch`, `packs/punch-stop-riser`
- **Sonidos nuevos de un vídeo de referencia**: `scripts/extraer-sfx.py video.mp4 destino nombre:inicio:dur --sin-voz`. Separa la voz con Demucs, alarga el final hasta que el sonido se apaga y añade cola de reverb si la fuente corta. Comprueba siempre la cola: `20·log10(rms_final/pico) < -30 dB`.

## Calidad (Instagram)
- `HQ=1` en mezcla4/mezcla2: x264 crf 15, preset slow, tune film, maxrate 20M, GOP 60 y AAC 256k (unos 9 Mbps). Con crf 19 salía a 4 Mbps y quedaba borroso.
- El grano va a .025, porque el ruido es lo primero que se estropea al recomprimir.
- La cara se preescala en Python (lanczos + unsharp 1,45/-0,45), no la amplía el navegador.
- Para Juan: subir por Wi‑Fi desde el archivo original y activar "Subir con la calidad más alta" en Instagram.

## Operativa (errores que ya pasaron)
- Cada .mov pesa unos 1,8 GB. Mira `df` antes de grabar dos a la vez y borra el .mov después de mezclar.
- **Nunca uses `pkill -f` o `pgrep -f` con un patrón que también esté en tu propio comando**: mata tu propia shell. Busca por `ps -eo pid,args | grep "^ *[0-9]* node .*pagina.html"` y haz `kill PID`.
- Para trabajos en segundo plano usa marcadores (`echo MOSCA_OK`) en el log.
- Solo para cambiar el audio no hace falta volver a grabar: `mezcla3.py video.mp4 voz.wav salida.mp4 sfx.json` copia el vídeo tal cual.
- Si el vídeo lo pide, mira la plantilla de la escena explicativa: el urinario (`ejemplos/mosca.html`: la mosca, el hombre Open Peeps que entra, el chorro con dasharray, se va, brillos + `ding`).

## Canal de emprendimiento (no PLEA5E)
Usa el mismo motor y las mismas reglas de sonido, pero **cambia la marca** en `:root` de la plantilla (`--oro`, `--fondo`, `--glow1..3`). Así el canal tiene identidad propia y no se confunde con PLEA5E. Las reglas 14 y los colores de PLEA5E no aplican ahí.
