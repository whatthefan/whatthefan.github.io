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

## avatar/ronda2/

Segunda tanda, tras "no me convence": la estrella con el 5 más el nombre,
y otros fondos y colores (noche, azul, crema, oro, verde, blanco, oro
metálico) y dos ideas nuevas: la estrella dentro de un bocadillo (una
reseña) y con las ondas de "acerca el móvil".

`tablero.png` las enseña todas juntas, en grande y en pequeño. Cada una
tiene su PNG de 1080×1080 con el número delante.

Las letras son Anton (el nombre, de la misma familia que el 5 del sello)
y Montserrat (los textos del aro), metidas en base64 desde `fuente/`.
Se regenera con `python3 marketing/instagram/avatar/ronda2/generar.py`;
los PNG se sacan haciendo captura de los `.html` sueltos que monta.

## avatar/final/

Las elegidas: la 3 y la 5, las dos con el aro de oro metálico de la 8.

| | |
|---|---|
| `PLEA5E-avatar-3-estrella-y-nombre.png` | La estrella arriba y PLEA5E debajo. |
| `PLEA5E-avatar-5-plea-estrella-e.png` | PLEA★E: la estrella hace de 5, con las cinco estrellitas debajo. |
| `perfil.png` | Las dos puestas en un perfil de Instagram en modo oscuro. |

El 5 va más pequeño dentro de la estrella (escala 0,42 en vez de 0,46):
antes la base del 5 se salía por la muesca entre las dos patas y se
fundía con el fondo. Ahora queda entero, con oro alrededor.

Se regenera con `python3 marketing/instagram/avatar/final/generar.py`;
los PNG salen de la captura de los `.html` que monta.
