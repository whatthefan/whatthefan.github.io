# PLEA5E

Web de PLEA5E: placas, expositores y tarjetas con chip NFC y código QR
para que los clientes de un negocio dejen su reseña en Google.

## Qué hay aquí

| | |
|---|---|
| `index.html` + `assets/` | La web. HTML suelto: no hay nada que compilar. |
| `taller/generador.html` | El generador de placas. Herramienta interna, no enlazada desde la web y fuera del `robots.txt`. |
| `netlify/functions/` | El servidor: recibe el encargo, pide el diseño a la IA, avisa por correo. |
| `marca/`, `producto/`, `qr/`, `tarjeta/` | Logotipos, fotos y códigos. |
| `r/` | Las páginas de salto de cada cliente. |
| `LEEME.txt` | El manual, en castellano llano. Empieza por ahí. |

## Cómo se publica

Netlify lee este repositorio y publica solo. No hay comando de
construcción: la carpeta se sirve tal cual.

Las claves (Anthropic, Resend, la del panel) van en las variables de
entorno de Netlify, **nunca en el código**: lo que entra en el
historial se queda ahí para siempre.

## Antes de tocar nada

El manual (`LEEME.txt`) explica lo que se puede cambiar sin saber
programar: el número de Bizum, la fianza, la fecha de la oferta, los
enlaces de Google de cada local y los datos del aviso legal.
