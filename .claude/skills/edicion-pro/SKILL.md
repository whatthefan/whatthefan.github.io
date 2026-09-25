---
name: edicion-pro
description: Editar vídeos cortos (Reels, TikTok, Shorts) con motion design premium estilo SaaS/Apple — fondo casi negro, texto pequeño palabra a palabra con desenfoque, pantallas de app en 3D con borde de luz, cursores que pulsan, campos que se escriben, tarjetas que se apilan, diagramas de círculos, barridos con desenfoque de movimiento y un solo color de acento. Úsala siempre que haya que editar un vídeo de PLEA5E (persona a cámara, anuncio o motion graphics) o cuando Juan pida "edición profesional", "como el vídeo de referencia" o "transiciones así".
---

# Edición pro (motion design premium)

Referencia: el anuncio de «Marz» que pasó Juan (un reaction de un vídeo de 500 $). No se copian sus
diseños: se copia **cómo** está editado. Todo lo de abajo es lo que hace que parezca caro.

## 1. El lenguaje visual

| Regla | Cómo se hace aquí |
|---|---|
| **Fondo casi negro**, nunca negro puro | `#0A0B0F` con un degradado radial apenas más claro en el centro y una viñeta |
| **Un solo acento** | el oro de PLEA5E `#E9BC46` (en la referencia era verde). Rojo `#E5484D` SOLO para lo negativo («imposible», «0 reseñas») |
| **Texto pequeño y fino** | Inter (fuente/inter-latin.woff2), 44-64 px en 1080 de ancho, peso 400-500, blanco al 90 %. Mucho aire alrededor. Nunca rótulos gigantes con borde gordo |
| **Palabra a palabra** | cada palabra entra desde `blur(10px)` + 14 px abajo, con 70 ms de desfase (`M.palabras`) |
| **Una palabra clave en color** | la que importa va en oro (`*palabra*` en `M.palabras`) |
| **Luz, no sombras duras** | brillos suaves (`box-shadow: 0 0 60px rgba(233,188,70,.35)`), bordes de 1 px `rgba(255,255,255,.08)`, un arco de luz en el horizonte |
| **Profundidad** | pantallas de app en perspectiva 3D que se enderezan (`M.tilt`), capas a distintas velocidades |
| **Interfaces de verdad** | la pantalla de Google para escribir la reseña, un campo que se escribe (`M.teclea`), un cursor que pulsa un botón que brilla (`M.cursor`), notificaciones que se apilan |
| **Nada estático** | todo flota un poco (1-2°, 4-6 px) o hace un empuje lento de cámara (escala 1 → 1.04) |

## 2. Transiciones (las que se usan)

1. **Desenfoque cruzado**: sale con `blur(14px)` + escala 0.98, entra con `blur(14px)` + escala 0.96 → 1 (`M.blurIO`). Es la de por defecto.
2. **Barrido (whip)**: el contenido cruza la pantalla en horizontal con desenfoque de movimiento (`M.whip`). Para cambiar de tema.
3. **Empuje hacia la interfaz**: la cámara se mete dentro de una pantalla (escala 1 → 1.6 con desenfoque) y aparece la siguiente.
4. **Apilado**: tarjetas que caen una encima de otra con un poco de giro (tarjetas de pago en la referencia → placas, expositores y tarjetas en PLEA5E).
5. **Diagrama de órbitas**: palabras en círculos con líneas discontinuas que se van conectando hasta el logo.
6. **Corte a negro seco** al final. Sin fundido.

Curvas: entradas `outExpo` (rápidas y suaves al final), salidas `inCubic`. Entradas de 0,4-0,6 s, salidas de 0,25-0,3 s.

## 3. Sonido

Sonidos de edición de `marketing/instagram/sonidos/edicion/`: `arrow-swoosh` en cada barrido,
`woah-drop` en la revelación fuerte (máximo 2-3 por vídeo), `mouse-click` en cada clic de cursor,
`mac-typing` cuando algo se escribe, `camera-shutter` cuando aparece un producto, `metallic-riser` +
`cinematic-impact` antes y en el momento clave, `ding` en un acierto. **Nada de memes** en este estilo.
Volumen de los efectos: 0,3-0,5 frente a la voz; la voz siempre manda.

## 4. Montaje (persona a cámara)

- **Pantalla partida**: la mitad de arriba es el motion design, la de abajo la persona. Es lo que da el look del vídeo de referencia.
- Pantalla completa solo para frases con fuerza emocional, con subtítulo pequeño abajo.
- Subtítulos **discretos**: Inter 600, 56-64 px, blanco con sombra suave, la palabra que se dice en oro. Nada de karaoke gordo con borde negro.
- Quitar silencios y trozos flojos, cortar en los valles de energía de la voz (nunca a mitad de palabra).
- Voz: filtro paso alto 85 Hz, reducción de ruido, compresor suave y `loudnorm` a -14 LUFS.
- Si hay que sustituir una frase, se cambia **solo la voz** (con `atempo` ≤ 1,12 y el volumen igualado al trozo original) y la imagen se queda.

## 5. Cómo se hace (herramientas)

Carpeta de trabajo en `/tmp` (los vídeos de Juan NO van al repo, que es público). Scripts de ejemplo
en `marketing/instagram/short-juan/`:

1. **Transcribir** con Whisper local (sherpa-onnx + `sherpa-onnx-whisper-small`, se descarga de las
   releases de GitHub de k2-fsa) → frases con tiempos.
2. **plan.py**: cortes, layout (`full`/`split`), subtítulos palabra a palabra, escenas y sonidos en tiempo de salida.
3. **base.py**: ffmpeg recorta, voltea si la cámara graba en espejo (Mac/Photo Booth: `hflip`), encuadra siguiendo la cara (OpenCV haar), empuje lento en los planos completos y limpia la voz.
4. **Capa de motion** (HTML 1080×1920, fondo transparente) con `render(t)` usando `motion.js`
   (incrustarlo en el HTML). Se graba con Playwright `omitBackground` a 30 fps → `capa.mov` (png con alfa).
5. **final.py**: superpone la capa y mezcla los sonidos; comprimir a < 30 MB para mandarlo.

Antes del render completo: renderizar 8-10 fotogramas clave, componer sobre la base y mirarlos.

## 6. Lista de control antes de entregar

- [ ] ¿El texto es pequeño, con aire y entra palabra a palabra? ¿Una sola palabra en color?
- [ ] ¿Cada escena tiene profundidad o movimiento (3D, flotar, empuje)?
- [ ] ¿Hay al menos una interfaz «viva» (cursor, tecleo, estrellas que se rellenan)?
- [ ] ¿Las transiciones son desenfoque/barrido, sin cortes secos salvo el final?
- [ ] ¿Los sonidos son de edición (nada de memes) y a volumen por debajo de la voz?
- [ ] ¿Nada importante en los 250 px de abajo (lo tapan los botones de TikTok/Instagram)?
- [ ] ¿Final a negro seco, sin subtítulos ni barra encima?
- [ ] ¿Nada inventado ni promesas de reseñas? («Las placas: pago único», nunca «sin cuotas»)
