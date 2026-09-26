# Capas sobre vídeo hablado (estilo mezcla)
- `kit.css` / `kit.js`: textos palabra a palabra (K.W reparte tiempos por letras; `*` = oro, `!` = rojo), escenas con cámara y salida en desenfoque vertical, destello, pop, tachado, anillo de toque, estrellas y pantalla de reseña.
- `mosca.html`, `uber.html`: ejemplos reales (vídeos «gancho → giro» 1 y 3). Necesitan junto a ellos escena.js, inter-latin.woff2, cast/, pan/, w-placa.png y sello-oro.svg (sin fondo).
- Proceso: base.mp4 (cortes + audio limpio) → `node grabar.js X.html todo capa.mov` → `python3 mezcla.py base.mp4 capa.mov salida.mp4 sfx.json` (sfx: [segundo, archivo en sonidos/, volumen]).
- La cara y los vídeos de Juan NUNCA van al repo.
