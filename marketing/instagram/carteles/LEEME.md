# Carteles PLEA5E, en la calle (estilo "NO CABE EN LA BOCA")

Un carrusel de 3 fotos (1080×1350, sacadas a 2160×2700) con la placa y el
mensaje de las reseñas en cosas del día a día, como en la referencia de
BRUTO.

1. **`fotos/escena-fachada.png`**: una lona gigante en una fachada de
   ladrillo, con sol de tarde y la sombra de la escalera de incendios.
   **QUE HABLEN · [la placa] · PLEA5E® · DE TU BAR**.
   Abajo: *NFC // QR // GOOGLE // 5 ESTRELLAS // 10 SEGUNDOS // SIN APPS* y
   *HECHO PARA QUE TE VALOREN.*
2. **`fotos/escena-mupi.png`**: un mupi de parada al anochecer, encendido,
   con la ciudad desenfocada detrás. **ANTES DE ENTRAR, TE BUSCAN.** ·
   [la placa] · *QUE LO QUE LEAN SEA BUENO.*
3. **`fotos/escena-mesa.png`**: una mesa de bar con un café, la placa y el
   ticket. Al final del ticket pone *"¿Qué tal todo? Si te hemos tratado
   bien, acerca el móvil a la placa de la mesa. Son 10 segundos. ★★★★★"*.

**No son fotos.** Son escenas en 3D hechas con código (three.js, licencia
MIT, en `lib/`): el ladrillo, la madera, la acera, la taza y la escalera
se dibujan aquí. No hay fotos de nadie ni imágenes generadas por IA. El
bar, la dirección y los precios son **inventados** (Bar La Plaza, la
misma placa de ejemplo del otro carrusel).

Los diseños planos, para imprimirlos de verdad o para ponerlos en una
maqueta de Canva o Placeit sobre una foto real, están en `png/`:
`lona-que-hablen.png` (2:3), `mupi-te-buscan.png` (mupi de 120×176) y
`ticket-bar.png` (ticket de 80 mm).

**Texto de la publicación:**

> Que hablen de tu bar. Pero que hablen bien. ⭐⭐⭐⭐⭐
> Antes de entrar, te buscan en Google. La placa PLEA5E hace que tu cliente te deje la reseña en 10 segundos: toca o escanea, sin apps.
>
> 👉 Comenta PLACA y te mandamos precios y ejemplos por privado.
> 📍 Córdoba · Envío a toda España · plea5e.es
>
> #reseñasgoogle #hosteleria #bares #restaurantes #marketingparabares #comercioslocales #nfc #cordoba

## Cómo se rehace

Desde la raíz del repo:

```
python3 marketing/instagram/carteles/carteles.py              # los carteles en HTML
node    marketing/instagram/carteles/hacer-png.js lona-que-hablen mupi-te-buscan ticket-bar
node    marketing/instagram/carteles/hacer-png.js escena-fachada escena-mupi escena-mesa
```
(primero los carteles, y después las escenas, que los usan).
