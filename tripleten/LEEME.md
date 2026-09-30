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
