# Instagram de PLEA5E (@plea5e.es)

Todo lo de redes va aquí, fuera de `public/`: no se sirve en la web.

## avatar/

Foto de perfil. 1080×1080, pensada para el recorte en círculo.

| | |
|---|---|
| `B-sello-oro.png` | **La recomendada.** Estrella negra con el 5 en oro sobre fondo oro. Un círculo amarillo liso destaca entre las historias (casi todas son fotos) y se sigue leyendo a 24 px en los comentarios. |
| `A-sello-noche.png` | La misma en negro. Elegante, pero en Instagram en modo oscuro el borde desaparece. |
| `C-estrellita.png` | La mascota. La más simpática, pero a tamaño de comentario ya no se distingue: mejor como protagonista de reels e historias que como foto de perfil. |
| `comparativa-perfil.png` | Las tres puestas en un perfil, en la barra de historias y en un comentario. |

El 5 va entero dentro de la estrella (en `public/icono.svg` asoma por
arriba y, en pequeño, la estrella parece partida).

Se regeneran los SVG con `python3 marketing/instagram/avatar/generar.py`
desde la raíz del repo.
