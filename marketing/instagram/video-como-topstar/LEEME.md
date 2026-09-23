# Reel "Cómo funciona PLEA5E" (al estilo del anuncio de topStar)

`PLEA5E-reel-como-funciona.mp4`: 45 s, vertical 1080×1920, 30 fps, con
música y efectos. `portada.png` es la portada del reel.

La idea es la del anuncio de topStar (dos locales en la misma calle,
gana el que tiene más estrellas, cómo funciona, resultado, llamada a la
acción), pero con lo nuestro: noche y oro, Estrellita, nuestras placas
y diseños reales de clientes.

## Escenas

| Segundos | Qué se ve |
|---|---|
| 0 – 7,5 | Dos locales en la misma calle: el tuyo 3,9 ★ y el de enfrente 4,7 ★. El cliente entra en el de enfrente. |
| 7,5 – 12,5 | Tus clientes contentos se van sin dejar reseña: "Reseñas nuevas esta semana: 0". Estrellita, asombrada. |
| 12,5 – 17,5 | Golpe de música y aparece PLEA5E: placas NFC para reseñas de Google, diseñadas con tu marca. |
| 17,5 – 22,5 | La placa, con el chip NFC y el código QR señalados, y dos diseños reales (Barvi y Piccola). |
| 22,5 – 30 | Así de fácil: 1) acerca el móvil, 2) se abre tu Google, 3) 5 estrellas en 10 segundos. |
| 30 – 35 | Las reseñas llegan y la nota sube de 3,9 a 4,8 (con "Ejemplo ilustrativo" abajo). |
| 35 – 40 | Sin cuotas, sin apps: placa, expositor y tarjeta; pago único, diseño gratis, envío gratis a península, no se imprime hasta que te guste. |
| 40 – 45,5 | ¿Hablamos? Estrellita saluda · PLEA5E.ES · WhatsApp · Desde 25 € · Córdoba · envío a toda España. |

Todo lo que dice sale de la web (precios, envío, diseño, pago único).
Las reseñas y la subida de nota son un ejemplo, y así lo pone.

## Voz (opcional)

El vídeo va con música y se entiende sin sonido, igual que el de
topStar. Si quieres voz, en el editor de Reels: **Texto → escribe la
frase → Texto a voz**, o grábala tú con **Voz en off**. Tu propia voz
funciona mejor: se nota que hay una persona detrás.

| Entra en | Frase |
|---|---|
| 0,3 s | Dos locales. La misma calle. |
| 3,3 s | ¿A cuál entra el cliente? |
| 5,4 s | Al que tiene más estrellas en Google. |
| 7,7 s | Y lo peor: tus clientes contentos… se van sin dejar reseña. |
| 12,6 s | Con PLEA5E, eso se acaba. |
| 14,0 s | Placas con chip NFC, diseñadas con tu marca. |
| 22,8 s | El cliente acerca el móvil, se abre tu Google, y en diez segundos te ha dejado cinco estrellas. |
| 30,4 s | Reseñas que llegan solas. |
| 35,2 s | Pago único. Sin cuotas, sin apps. |
| 40,1 s | ¿Hablamos? Escríbenos: plea5e.es |

Si le pones voz, baja la música al 30 % en el editor.

## Texto de la publicación

> ¿Por qué entran en el bar de enfrente y no en el tuyo? ⭐
>
> El cliente mira Google Maps y elige en 3 segundos: gana el que tiene más estrellas.
> Y tus clientes contentos se van sin dejar reseña… porque nadie se lo pone fácil.
>
> Con PLEA5E el cliente acerca el móvil a la placa y ya está escribiendo tu reseña. 10 segundos.
>
> ✅ Diseñada con tu marca (gratis)
> ✅ Pago único, sin cuotas ni apps
> ✅ Envío gratis a península
> ✅ No se imprime nada hasta que te guste
>
> 📍 Córdoba · Envío a toda España
> 👉 Escríbenos por WhatsApp o entra en plea5e.es
>
> #reseñasgoogle #googlemaps #hosteleria #bares #restaurantes #marketingparabares #nfc #cordoba #negocioslocales #emprendedores

Música en Instagram: el vídeo ya lleva la suya. No le añadas otra
encima; si quieres una canción de tendencia, quita el audio del vídeo
en el editor y pon esa.

## Cómo se rehace

Desde la raíz del repo:

```
python3 marketing/instagram/video-como-topstar/montar.py    # mete fotos, letras y Estrellita
python3 marketing/instagram/video-como-topstar/musica.py    # música y efectos (audio.wav)
FFMPEG=ffmpeg node marketing/instagram/video-como-topstar/grabar.js
```

`escena.html` es la animación entera: `render(t)` pinta el segundo `t`.
Los textos se cambian ahí; los segundos de los efectos, en `musica.py`.
`fotogramas.js` saca fotogramas sueltos para revisar sin grabar todo.
