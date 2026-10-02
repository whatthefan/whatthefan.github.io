# «Un toque» — motion graphics puro (estilo lyric/kinetic con cámara continua)

Referencia que pasó Juan: el vídeo de @_mexicat (glifos en plano técnico, curvas de nivel, agujero negro con rejilla, typing en mono, ficha de papel, grano y glow naranja). Aquí va en oro PLEA5E.

- Montaje: copia `brutal.html` + `trazos.js` en una carpeta con `f/` (Archivo 400/600/800/900, Instrument Serif, Inter Tight 300/500 de /tmp/claude-0/fuentes), `marca-plea5e.svg`, `sello-plea5e.svg` y enlaces a `motor/fx.js` y `motor/escena.js`.
- Cámara continua: cada escena vive entre dos transiciones de `TR` (`dive` a un punto, `pan`, `caer`, `giro`, `corte`, `punto`) y `camara(i, t)` mueve la saliente y la entrante como si fuera la misma toma, con desenfoque de movimiento direccional (un feGaussianBlur por escena).
- Técnicas: trazo con dashoffset + nodos de Bézier, curvas de nivel (marching squares sobre ruido con pozo) inclinadas con `rotateX`, texto en `textPath` en espiral y en círculo, rejilla en perspectiva hundida (proyección propia en canvas), túnel de tarjetas con `translateZ`, ficha de papel con muelle, letras que caen con gravedad, polvo dorado con profundidad, grano y viñeta, HUD fijo de visor.
- Palabras que entran con desenfoque y desliz: `frase(id, html, t0, stagger, {t1})` (recorre todos los nodos de texto).
