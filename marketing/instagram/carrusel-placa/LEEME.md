# Carrusel "Desliza para agregar" y vídeo "La placa, destripada"

Una placa PLEA5E montada desde cero, capa a capa, al estilo de los
carruseles de "desliza para agregar arroz… toppings…". Negocio y logo
son **inventados** (Bar La Plaza): no existe.

## Carrusel (7 fotos de 1080×1350, `diapositivas/PLEA5E-carrusel-0N.png`)

| | Arriba | Se ve |
|---|---|---|
| 1 | Desliza para agregar **tu nombre** | La placa de metacrilato vacía (4 mm, 90 × 90 mm) |
| 2 | … **tu logo** | Con el nombre y el lema |
| 3 | … **tus colores** | Con el logo, y una lupa que lo amplía |
| 4 | … **el código QR** | Con la banda y los colores de la marca |
| 5 | … **el chip NFC** | Con el mensaje, la G de Google y el QR |
| 6 | Desliza para **probarla** | La placa "en rayos X": el chip de cobre dentro, "Programado con tu ficha de Google" |
| 7 | ¡Lista para tu mesa! **5 ★ en 10 segundos** | La placa terminada con el móvil dejando la reseña · "Comenta PLACA y te hacemos la tuya" |

**Texto de la publicación:**

> Así se hace una placa PLEA5E 👉 desliza
>
> Metacrilato de 4 mm, tu nombre, tu logo, los colores de tu marca, el código QR y un chip NFC programado con tu ficha de Google. El cliente acerca el móvil y en 10 segundos te ha dejado 5 estrellas.
>
> ✅ Diseño con tu marca, sin coste de diseño
> ✅ No se imprime nada hasta que te guste
> ✅ Envío gratis a península
>
> 👉 Comenta PLACA y te mandamos precios y ejemplos por privado.
> 📍 Córdoba · Envío a toda España · plea5e.es
>
> #reseñasgoogle #hosteleria #bares #restaurantes #comercioslocales #nfc #marketingparabares #cordoba

## Vídeo (`video/PLEA5E-placa-destripada.mp4`, 21,7 s, 1080×1920)

La placa entera cae, se inclina y **se abre en sus 8 capas** (metacrilato,
chip NFC, vinilo, colores, mensaje + Google, logo y nombre, QR, "toca o
escanea"); cada una se enciende con su nombre. Se vuelve a juntar de un
golpe (ahí entra la parte fuerte de la música), se programa el chip, un
móvil la toca y salen las cinco estrellas. Cierra con "Comenta PLACA".
Hay versión `-solo-efectos` para ponerle una canción de Instagram.
`video/portada.png` es la portada (la placa abierta).

Súbelo **después** del carrusel, o como segunda publicación el mismo día:
el carrusel enseña las piezas y el vídeo las junta.

## Cómo se rehace

Desde la raíz del repo:

```
python3 marketing/instagram/carrusel-placa/montar-generador.py   # copia del generador con interruptores
node    marketing/instagram/carrusel-placa/capas.js             # la placa por capas (capas/)
python3 marketing/instagram/carrusel-placa/construir.py         # las 7 diapositivas en HTML
node    marketing/instagram/carrusel-placa/hacer-png.js         # y sus fotos
python3 marketing/instagram/carrusel-placa/video/montar.py      # el vídeo
python3 marketing/instagram/carrusel-placa/video/musica.py
FFMPEG=ffmpeg node marketing/instagram/carrusel-placa/video/grabar.js
```

`generador-por-capas.html` es el generador de la web (`public/taller/`)
con cada capa detrás de un interruptor (`window.OC.qr = true` esconde el
QR, etc.). El de la web no se toca. Si el generador cambia, se vuelve a
sacar la copia con `montar-generador.py`.
