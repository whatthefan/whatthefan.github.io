# Calco del videoclip «I'm upping my P(doom)» para PLEA5E («Subo mi P(toque)»)

Mismo vídeo, escena a escena y en el mismo segundo (2:36, 1920×1080), pero en oro PLEA5E y con texto de PLEA5E. La escaleta completa está en `marketing/instagram/guion-calco-ptoque.md`.

## Montaje
Copia esta carpeta y añade:
- `three.module.js` y `three.core.js` (three r186) y la carpeta `jsm/`, con `postprocessing`, `shaders`, `lines`, `environments`, `geometries` y `utils` (de `node_modules/three/examples/jsm`);
- `trazos.js`, con los trazados del sello (la estrella y el 5), exportados como `export const TRAZOS`;
- `f/` con las fuentes: Archivo 500–900, Archivo Narrow 700, IBM Plex Mono 400/500, EB Garamond 400 (normal y cursiva), Inter Tight 500/600 y Caveat 700 (todas de `@fontsource`).

## Arquitectura
- `core.js`: three.js con bloom, aberración cromática, grano y viñeta (el grano y la viñeta se calculan en espacio de pantalla). Incluye helpers de texto en 3D (`frase`, `pintaKaraoke`: palabras tenues que se encienden), líneas gruesas (`linea` + `trazar`), chispas, `panel` (un canvas 2D dentro del mundo 3D) y `puntosSVG`.
- `secA.js` … `secF.js`: cada sección devuelve `[{t0, t1, frame(t), dom?}]`. `frame` devuelve `{escena, cam, post}` para WebGL, o `null` si la escena es solo DOM. Las escenas DOM (papel, tipografía) tienen su propio grano y viñeta.
- `main.js`: recorre las escenas activas y dibuja. Del 155,3 al 156,3 s hace el flashback: vuelve a pedir tiempos de otras escenas.
- SFX: van en `calco.html`, entre `/*FX*/…/*FX*/`. Caen en los 31 golpes que salen de la pista «other» del original (separada con demucs), más los tecleos de los prompts y del formulario.

## Render (4 núcleos)
Tres procesos en paralelo, con un intermedio h264 (el PNG con alfa no cabe en disco):

```
FFMPEG=/tmp/claude-0/bin/ffmpeg INTER=h264 DESDE=0 HASTA=53 TAM=1920x1080 node motor/grabar.js calco.html todo parte1.mov
```

Luego se concatenan las partes y se pasan por `scripts/mezcla4.py`, con silencio como voz.
