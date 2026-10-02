# Estrellita para Instagram

`python3 marketing/instagram/personaje/poses.py` saca en `svg/` todas las poses
de la web (las de `gen/estrellita.py`) más las nuevas con cosas en la mano, y
con los **guantes mejorados**: tres nudillos y el pulgar, para que se le vean
los dedos. No toca los dibujos de la web.

Cada pose sale en las dos direcciones: `NOMBRE.svg` mira a la derecha y
`NOMBRE-izq.svg` a la izquierda. El 5 queda siempre al derecho; no hay que
voltear nunca el dibujo con CSS.

| Pose nueva | Qué hace | Para qué |
|---|---|---|
| `elegante` | chistera, monóculo y bastón, mano en la cadera | "yo me encargo", el jefe |
| `susurra` | mano junto a la cara, mirando de reojo | cotilleos, "oye…" |
| `palomitas` | con un cubo de palomitas, mirando de lado | "a ver qué dicen de ti" |
| `megafono` | gritando con un megáfono | llamadas: "¡COMENTA!" |
| `lupa` | investigando con una lupa | "¿dónde están tus reseñas?" |
| `gota` | sentada con una gota de sudor | cuando algo sale mal |
| `monoculo` | solo con el monóculo, mirando por encima | ironía, "vaya, vaya" |

Y las de siempre: `saluda`, `pulgar`, `tachan`, `salta`, `senala`, `arriba`,
`abajo`, `asombro`, `curiosa`, `guino`, `apunta`, `sentada`, `apoyada` y la
caminata `anda-0…7`.

Para añadir otra pose se escribe en `NUEVAS`, dentro de `poses.py`. Lo que
lleva en la mano va en `lleva=`, entre el cuerpo y los guantes, para que se
vea que lo agarra.
