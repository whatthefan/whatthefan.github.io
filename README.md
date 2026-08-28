# PLEA5E

Web de PLEA5E: placas, expositores y tarjetas con chip NFC y código QR
para que los clientes de un negocio dejen su reseña en Google.

## Qué hay aquí

| | |
|---|---|
| `public/` | Lo que se sirve. HTML suelto: no hay nada que compilar. |
| `public/taller/generador.html` | El generador de placas. Herramienta interna, no enlazada desde la web y fuera del `robots.txt`. **Se monta**, no se edita: sale de `gen/plantilla.html` con `npm run generador`. |
| `src/` | El Worker: recibe el encargo, pide el diseño a la IA, avisa por correo. `src/lib/` es la parte que no habla con nadie y se puede probar suelta. |
| `gen/` | La plantilla del generador y el guion que lo monta. |
| `public/marca/`, `producto/`, `qr/`, `tarjeta/` | Logotipos, fotos y códigos. |
| `public/r/` | Las páginas de salto de cada cliente. |
| `LEEME.txt` | El manual, en castellano llano. Empieza por ahí. |

## Cómo se publica

Cloudflare Workers, con `npm run deploy` (wrangler). La configuración
está en `wrangler.jsonc`; `public/` se sirve tal cual y `src/` atiende
`/api/`. El `netlify.toml` se queda por si hiciera falta volver.

Las claves (Anthropic, Resend, la del panel) van en las variables de
entorno de Cloudflare, **nunca en el código**: lo que entra en el
historial se queda ahí para siempre.

## Antes de tocar nada

El manual (`LEEME.txt`) explica lo que se puede cambiar sin saber
programar: el número de Bizum, la fianza, la fecha de la oferta, los
enlaces de Google de cada local y los datos del aviso legal.
