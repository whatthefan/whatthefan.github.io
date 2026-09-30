# Career ROI Lab · concepto para TripleTen

Calculadora de retorno de inversión para los bootcamps de TripleTen, pensada
como pieza de candidatura a AI Growth Marketing Manager. Proyecto independiente:
no es una página oficial de TripleTen.

## Qué hay en esta carpeta

| Archivo | Qué es |
|---|---|
| `index.html` | Toda la experiencia, en español e inglés: HTML, CSS y JS en un solo archivo. |
| `demo.mp4` / `demo-en.mp4` | Vídeo vertical (1080×1920, sin voz, con efectos de sonido y música suave) que enseña paso a paso cómo se usa, en español y en inglés. |
| `demo-poster.jpg` / `demo-poster-en.jpg` | Portadas de los vídeos. |
| `og.png` | Imagen de vista previa al compartir el enlace. |
| `video/` | Guion y grabador del vídeo (no hace falta publicarlo). |

## Idiomas

La página está completa en español y en inglés: textos, Nova (entiende
preguntas en los dos idiomas), fechas, tarjeta, calendario, email y vídeo.

- Elige sola el idioma del navegador (español si empieza por `es`, inglés si no).
- El botón **EN / ES** de arriba cambia de idioma y lo recuerda.
- Para mandar un enlace en un idioma concreto: `.../tripleten/?lang=en` o `?lang=es`.

Los textos en inglés están junto a los españoles dentro del `<script>`: los
fijos del HTML en `STATIC_EN` y el resto con `tr("español", "English")`.

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

## Volver a grabar los vídeos

```bash
REC_LANG=es FFMPEG=/ruta/a/ffmpeg node tripleten/video/grabar.js   # demo.mp4
REC_LANG=en FFMPEG=/ruta/a/ffmpeg node tripleten/video/grabar.js   # demo-en.mp4
```

Graba la página real con un reloj virtual, así que cada fotograma sale nítido.
Mientras graba apunta cada toque, tecla, mensaje de Nova y animación; después
`video/sonido.py` (Python 3 + numpy) sintetiza los efectos en su instante
exacto, añade una base musical suave y lo mezcla con el vídeo. Todo el sonido
se genera por código: no hay música ni samples con licencia de terceros.

Si cambian los tiempos, copia los de `video/capitulos.json` y
`video/capitulos-en.json` a `CHAPTERS` en `index.html`.
