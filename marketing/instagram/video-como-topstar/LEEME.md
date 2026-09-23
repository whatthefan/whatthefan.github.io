# Reel "Cómo funciona PLEA5E" (al estilo del anuncio de topStar)

`PLEA5E-reel-como-funciona.mp4`: 60 s, vertical 1080×1920, 30 fps, con
música y efectos. `portada.png` es la portada del reel (el gancho).

`PLEA5E-reel-como-funciona-solo-efectos.mp4`: el mismo vídeo sin música,
solo con los efectos. Para ponerle encima una canción de la biblioteca
de Instagram (las canciones de tendencia suelen dar más alcance): en el
editor, añade la canción y deja el volumen del vídeo al 60-70 % para que
se oigan los efectos.

Versión 2. La idea sigue siendo la del anuncio de topStar (dos locales,
gana el de más estrellas, cómo funciona), pero vendido como en el vídeo
de Jurado: pregunta directa al dueño, el error tachado y la forma buena
con su check, y cierre con "Comenta PLACA". Público: dueños de bares,
restaurantes y comercios. Todos los datos técnicos salen de la web.

Cambios frente a la primera versión: fuera el logotipo con las rayas
(ahora va el sello con PLEA5E debajo, como la foto de perfil), fuera
Barvi y Piccola, Estrellita sin el contorno blanco, y los tres modelos
limpios, sin fondo, de cerca y con el grosor del material.

## Escenas

| Segundos | Qué se ve |
|---|---|
| 0 – 5 | "Si tienes un bar, un restaurante o un comercio… esto te está costando clientes." |
| 5 – 12,5 | Dos locales en la misma calle (3,9 ★ y 4,7 ★). El cliente mira Google Maps y entra en el de más estrellas. |
| 12,5 – 20 | ¿Cómo pides las reseñas? «¿Nos dejas una reseña?» se tacha ❌ ("dice que sí y se le olvida"). ✅ Que acerque el móvil a la placa: 10 segundos, antes de irse. |
| 20 – 25 | Aparece PLEA5E: placas NFC para reseñas de Google, con la marca de tu local. |
| 25 – 37,5 | Los tres modelos, de cerca y girando, con sus datos: placa de mesa (90×90 mm, metacrilato 4 mm, adhesivo 3M), expositor (76×118 mm, en L, no se pega) y tarjeta (85×54 mm, PVC). Todos con chip NFC y QR. |
| 37,5 – 45 | Así de fácil: acerca el móvil, se abre tu ficha de Google, cinco estrellas. Sin app, iPhone y Android; sin NFC, el QR. |
| 45 – 52,5 | Cómo trabajamos: WhatsApp → diseño en 48 h → no se imprime hasta que te guste → en tu local en 3-10 días, envío gratis. Las placas: pago único. |
| 52,5 – 60 | "¿Sería una locura probarlo en tu local?" · COMENTA PLACA · WhatsApp · plea5e.es · Desde 25 €. |

El seguimiento de 35 €/mes no sale en el vídeo: el cierre es "Comenta
PLACA" y con la cuota delante se liaba. Aun así el vídeo no dice "sin
cuotas" (el servicio existe en la web): dice "las placas: pago único".

Los modelos llevan negocios inventados (Bar La Plaza, Barbería Norte,
Taller Hermanos Ruiz) y salen del generador con `modelos.js`, que los
guarda a 3600 px; se bajaron a 1400 px con ffmpeg para que la escena
no pese.

**Ojo con "Comenta PLACA":** si lo publicas así, hay que contestar por
privado a cada comentario (a mano o con ManyChat).

## Voz (opcional)

El vídeo va con música y se entiende sin sonido. Si quieres voz, grábala
tú con **Voz en off** en el editor de Reels (se nota que hay una persona
detrás) y baja la música al 30 %.

| Entra en | Frase |
|---|---|
| 0,2 s | Si tienes un bar, un restaurante o un comercio… esto te está costando clientes. |
| 5,2 s | El cliente mira Google Maps… y entra en el de más estrellas. |
| 12,7 s | ¿Cómo pides las reseñas? "¿Nos dejas una reseña?" Te dice que sí… y se le olvida al salir. |
| 16,6 s | Lo que funciona: que acerque el móvil a la placa. Diez segundos, antes de irse. |
| 20,3 s | Eso es PLEA5E. Placas con chip NFC, con la marca de tu local. |
| 25,2 s | Placa de mesa, en metacrilato, con adhesivo 3M. Expositor de pie para la barra. Y tarjeta para el delantal. |
| 37,8 s | Acerca el móvil, se abre tu Google y cinco estrellas. Sin app. |
| 45,3 s | Nos escribes, te diseñamos la placa en 48 horas y no se imprime nada hasta que te guste. Las placas se pagan una vez. |
| 52,7 s | ¿Sería una locura probarlo en tu local? Comenta PLACA y te lo contamos. |

## Texto de la publicación

> ¿Por qué entran en el bar de enfrente y no en el tuyo? ⭐
>
> El cliente mira Google Maps y en 3 segundos elige: gana el que tiene más estrellas.
> Y "¿nos dejas una reseña?" no funciona: te dicen que sí y se les olvida al salir.
>
> Con PLEA5E el cliente acerca el móvil a la placa, en la mesa, y ya está escribiendo tu reseña.
>
> 🔹 Placa de mesa 90×90 mm · metacrilato 4 mm · adhesivo 3M
> 🔹 Expositor de pie para barra o mostrador
> 🔹 Tarjeta para el delantal
> Todas con chip NFC + QR, diseñadas con tu marca.
>
> ✅ Diseño en 48 h, sin coste de diseño
> ✅ No se imprime nada hasta que te guste
> ✅ Las placas se pagan una vez, sin apps
> ✅ Envío gratis a península
>
>
> 👉 Comenta PLACA y te mandamos precios y ejemplos por privado.
> 📍 Córdoba · Envío a toda España · plea5e.es
>
> #reseñasgoogle #googlemaps #hosteleria #bares #restaurantes #comercioslocales #barberia #nfc #cordoba #negocioslocales

## Cómo se rehace

Desde la raíz del repo:

```
node marketing/instagram/video-como-topstar/modelos.js      # los tres modelos, del generador
python3 marketing/instagram/video-como-topstar/montar.py    # mete modelos, letras, sello y Estrellita
python3 marketing/instagram/video-como-topstar/musica.py    # audio.wav y audio-solo-efectos.wav
FFMPEG=ffmpeg node marketing/instagram/video-como-topstar/grabar.js
# la versión solo con efectos: el mismo vídeo con la otra pista
ffmpeg -i PLEA5E-reel-como-funciona.mp4 -i audio-solo-efectos.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest PLEA5E-reel-como-funciona-solo-efectos.mp4
```

La música (`musica.py`) es pop tranquilo a 96 BPM: piano eléctrico,
bajo, batería, pad y una melodía que entra con el golpe de PLEA5E. Está
ecualizada para el altavoz del móvil (menos grave de relleno, más
presencia). Los efectos van cuadrados al segundo con cada animación.

`escena.html` es la animación entera: `render(t)` pinta el segundo `t`.
Los textos se cambian ahí; los segundos de los efectos, en `musica.py`.
`fotogramas.js` saca fotogramas sueltos para revisar sin grabar todo.
