# Capas sobre vídeo hablado (estilo mezcla)
- `kit.css` / `kit.js`: textos palabra a palabra (K.W reparte tiempos por letras; `*` = oro, `!` = rojo), escenas con cámara y salida en desenfoque vertical, destello, pop, tachado, anillo de toque, estrellas y pantalla de reseña.
- `mosca.html`, `uber.html`: ejemplos reales (vídeos «gancho → giro» 1 y 3). Necesitan junto a ellos escena.js, inter-latin.woff2, cast/, pan/, w-placa.png y sello-oro.svg (sin fondo).
- Proceso: base.mp4 (cortes + audio limpio) → `node grabar.js X.html todo capa.mov` → `python3 mezcla.py base.mp4 capa.mov salida.mp4 sfx.json` (sfx: [segundo, archivo en sonidos/, volumen]).
- La cara y los vídeos de Juan NUNCA van al repo.

## v2 (lo que pidió Juan tras la primera entrega)
- **Cara más lejos**: `base2.py` recorta 960×1080 sin espejo (así lo quiere Juan) → fotogramas JPG → la página los pinta
  dentro de una tarjeta redondeada sobre papel (`K.cara`, `K.caraFrame`, `K.caraPinta`). La página ya es el vídeo entero (opaco).
- **Transiciones**: `K.escenas2` — entrada con zoom y desenfoque, látigo vertical entre escenas seguidas, la tarjeta de cara sale «a través».
- **Motion**: `K.mueve` (desenfoque de movimiento según velocidad), `K.sacude`, `K.chispas` (oro o polvo), palabra grande que golpea y subrayado oro.
- **Placa en la mano**: `placa_quad.py` sigue la placa blanca (máscara azulada, bordes rectos, completa lados fuera de cuadro,
  filtra saltos) y `placa_pinta.py` mete `w-placa.png` con homografía, respeta los dedos (piel) y copia la luz.
- **Sonido**: `mezcla2.py` alinea cada efecto por su golpe y lo iguala a -14 dB (+ dB relativos). Reparto: `edicion/` (swoosh
  en los 2 flashes, woah-drop en el ¡pum!, cinematic-impact en aciertos, mouse-click en toques, ding en estrellas, mac-typing en
  el comentario, camera-shutter al enseñar el producto), `virales/` con cuentagotas (vine-boom en «Nunca»/«nada», nope, grillos 0,6 s),
  `ui/mosca*.mp3` sintetizados.
- **Sin el sello de la estrella**: la marca va en letras (PLEA5E con el 5 en oro).
