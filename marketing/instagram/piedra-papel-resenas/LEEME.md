# "Piedra, papel y… reseñas"

La broma: es piedra, papel o tijera, pero la tercera jugada no es la
tijera, es **la mano con el móvil tocando una placa PLEA5E**. Y esa gana
siempre. Estilo de la referencia: fondo beige liso, una palabra grande y
la mano en el centro.

## Carrusel (3 fotos de 1080×1350, `diapositivas/`)

1. **Piedra**: el puño.
2. **Papel**: la mano abierta.
3. **Reseñas**: la mano con el móvil toca la placa, salen cinco estrellas · "…y esta gana siempre".

## Vídeo (`video/PLEA5E-piedra-papel-resenas.mp4`, 9,5 s, 1080×1920)

"¿Jugamos?" · Piedra (golpe) · Papel (golpe) · ¿Tijera? (golpe, y se
tacha con una ❌ y un "error") · **¡Reseñas!** (entra la placa, el móvil
la toca, salen las cinco estrellas con su "ding") · "…y esta gana
siempre" · Comenta PLACA. Hay versión `-solo-efectos` para ponerle una
canción de Instagram; `video/portada.png` es la portada.

**Texto de la publicación:**

> Piedra, papel o… ¿reseñas? 🤔
> Hay una jugada que gana siempre: que tu cliente acerque el móvil y te deje 5 ⭐ en 10 segundos.
>
> 👉 Comenta PLACA y te mandamos precios y ejemplos por privado.
> 📍 Córdoba · Envío a toda España · plea5e.es
>
> #piedrapapeltijera #reseñasgoogle #hosteleria #bares #restaurantes #comercioslocales #nfc #cordoba

## Las manos

Son de [Fluent Emoji](https://github.com/microsoft/fluentui-emoji)
(Microsoft, **licencia MIT**: uso comercial libre; el texto va en
`manos/LICENSE-fluentui-emoji.txt`), en vector. A la del móvil se le
cambia la manga rosa por los azules de PLEA5E.

**Con una mano de verdad queda más cercano.** Haz 3 fotos con el móvil
(en vertical, 4:5 o más alta), de tu mano sobre una pared o cartulina
beige, con luz de ventana y sin sombras duras:

- `fotos/piedra.jpg`: el puño, de lado, como en la referencia.
- `fotos/papel.jpg`: la mano abierta.
- `fotos/resenas.jpg`: la mano acercando el móvil a una placa PLEA5E.

Déjalas en `fotos/` (o pásamelas) y vuelve a sacar el carrusel: si están,
se usan en vez de las dibujadas y la palabra va encima.

## Cómo se rehace

Desde la raíz del repo:

```
python3 marketing/instagram/piedra-papel-resenas/construir.py     # las 3 diapositivas en HTML
node    marketing/instagram/piedra-papel-resenas/hacer-png.js     # y sus fotos
python3 marketing/instagram/piedra-papel-resenas/video.py         # el vídeo
python3 marketing/instagram/piedra-papel-resenas/video/musica.py
FFMPEG=ffmpeg node marketing/instagram/piedra-papel-resenas/video/grabar.js
```
