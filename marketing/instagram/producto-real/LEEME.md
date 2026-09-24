# Carrusel "producto real" (3 fotos, 1080×1350)

Con **fotos de verdad** (`fotos/`, hechas en persona con las piezas en blanco)
y el diseño de PLEA5E pegado encima para que parezca impreso. Estilo de la
referencia de la hamburguesa (`fotos/referencia-hamburguesa.jpg`).

1. **La placa de mesa en la mano**, con un anillo de letras finas alrededor (*5 estrellas •*) en círculo, que pasa por detrás del pulgar y de la mano
2. y 3. **Panorámica:** el expositor de pie en la cornisa, partido justo por la
   mitad entre las dos fotos. Al deslizar, la placa "sigue".
   *Tu bar, / en 5 estrellas.* · Comenta PLACA · PLEA5E.ES

## Cómo se edita la foto (`pegar.py`)

- **Perspectiva:** una homografía lleva el diseño plano a las 4 esquinas de la
  pieza en la foto, medidas a mano (`ESQUINAS` en la llamada a `pegar`).
- **Luz:** el diseño se multiplica por la luz que tiene la pieza en la foto,
  así el sol, las sombras y el degradado siguen ahí.
- **Acabado:** un poco de desenfoque y el mismo grano que la foto.
- **Tapar:** la tarjeta de otra marca que asomaba abajo en la foto de la mano
  se rellena con el fondo desenfocado de alrededor.

Los diseños (`disenos/placa.png` y `disenos/stand.png`) salen del generador de
la web con la placa de ejemplo (Bar La Plaza, **inventado**):
`node marketing/instagram/producto-real/disenos.js`.

Para rehacerlo:
```
node    marketing/instagram/producto-real/disenos.js
python3 marketing/instagram/producto-real/pegar.py
python3 marketing/instagram/producto-real/construir.py
node    marketing/instagram/producto-real/hacer-png.js
```

**Texto de la publicación:**

> Así queda en la mano. Y así, en tu barra. ⭐⭐⭐⭐⭐
> Tu placa PLEA5E, con tu marca y tus colores: tus clientes acercan el móvil o escanean el QR y te dejan la reseña en 10 segundos. Sin apps.
>
> 👉 Comenta PLACA y te mandamos precios y ejemplos por privado.
> 📍 Córdoba · Envío a toda España · plea5e.es
>
> #reseñasgoogle #hosteleria #bares #restaurantes #comercioslocales #nfc #cordoba
