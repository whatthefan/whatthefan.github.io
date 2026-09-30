# Career ROI Lab · concepto para TripleTen

Calculadora de retorno de inversión para los bootcamps de TripleTen, pensada
como pieza de candidatura a AI Growth Marketing Manager. Proyecto independiente:
no es una página oficial de TripleTen.

## Qué hay en esta carpeta

| Archivo | Qué es |
|---|---|
| `index.html` | Toda la experiencia: HTML, CSS y JS en un solo archivo. |
| `demo.mp4` | Vídeo vertical (1080×1920, sin voz) que enseña paso a paso cómo se usa. |
| `demo-poster.jpg` | Portada del vídeo. |
| `og.png` | Imagen de vista previa al compartir el enlace. |
| `video/` | Guion y grabador del vídeo (no hace falta publicarlo). |

## De dónde salen los datos

Todo lo que se dice de TripleTen sale de sus webs públicas (revisadas en
septiembre de 2026) y está en `MARKETS`, dentro del `<script>` de `index.html`:

- **EE. UU.** (tripleten.com, sus páginas de programa y su FAQ): precios por
  adelantado, duración, sueldos de referencia de cada programa, 15–20 h a la
  semana, garantía de 10 meses en los programas de nivel inicial (los
  Accelerator no la tienen), reembolso en los primeros 14 días, financiación con
  Climb Credit y Edly, y resultados del informe de empleo de 2026.
- **México** (tripleten.mx y sus páginas de programa): precio con descuento,
  precio original, mensualidades, sueldo inicial de referencia mensual,
  garantía de 6 meses y el 93% de empleo que publican.

Los precios con descuento cambian a menudo: si alguno varía, se cambia en
`MARKETS` y todo lo demás (calculadora, Nova, tarjeta) se actualiza solo.

Nova no es un modelo de lenguaje: entiende la pregunta por palabras clave y
responde con esos datos (con enlace a la fuente) y con los números de tu plan.
Si no tiene un dato verificado, lo dice y enlaza a TripleTen en vez de
inventarlo.

## Antes de enviarlo

Abre `index.html`, busca `CONFIG` (casi al principio del `<script>`) y rellena
`author`, `linkedin` y `email`. Aparecerán tu firma y los botones de contacto en
la sección «Para el equipo de TripleTen».

## Publicarlo

Sube la carpeta entera (sin `video/` si quieres). Por ejemplo, arrástrala a
<https://app.netlify.com/drop> con tu cuenta abierta: te da una dirección
propia que puedes renombrar en *Site configuration → Change site name*.

Ábrela siempre desde un navegador (Chrome, Safari). La vista previa de archivos
del móvil no ejecuta JavaScript y no funciona nada.

## Volver a grabar el vídeo

```bash
FFMPEG=/ruta/a/ffmpeg node tripleten/video/grabar.js
```

Graba la página real con un reloj virtual, así que cada fotograma sale nítido.
Si cambian los tiempos, copia los de `video/capitulos.json` a `CHAPTERS` en
`index.html`.
