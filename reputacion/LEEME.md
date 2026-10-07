# Reputación IA

Motor que analiza reseñas negativas de Google. Para cada una:

1. **Busca todo lo que incumple las normas de Google**, frase a frase.
   Con una sola frase basta: un insulto, una descripción física, una
   amenaza velada, un dato personal, una queja que no va del negocio...
2. Si encuentra algo, **redacta la apelación** para el formulario de
   Google, citando la norma y el fragmento exacto.
3. Siempre **redacta la respuesta pública** del dueño: empática, con dos
   palabras clave del negocio y llevando la conversación a privado.

## Cómo decide (y cuánto cuesta)

1. **Reglas gratis** (`reglas.mjs`): miran siempre primero. Cazan lo
   evidente: insultos, "la gorda de la barra", amenazas, teléfonos,
   "trabajé aquí", "no he ido pero"...
2. Si encuentran algo claro, ya está: apelación y respuesta salen de
   plantillas. **0 €.**
3. Si no, entra la **IA** (Claude Sonnet 5.5) con lo que vieron las
   reglas como pista. Es la que pilla los matices. **Alrededor de 1
   céntimo** por reseña.
4. Sin clave de la IA funciona solo con las reglas. Lo dudoso sale como
   **"revisar"**: lo mira una persona antes de denunciar.

Con las 9 reseñas de `ejemplos.json`, solo con reglas acierta 8; la
novena (quejarse del aparcamiento) queda en "revisar", que es lo
correcto sin IA.

No tiene nada que ver con la web de PLEA5E: no lo usa nadie de `src/`,
no se sirve desde `public/` y no cambia nada al desplegar.

## La regla que lo hace legal

Cada infracción tiene que llevar la **cita literal** del fragmento en el
que se apoya. `motor.mjs` comprueba que esa cita está de verdad en la
reseña (o en lo que cuenta el dueño, si la infracción sale de ahí). Si
no está, la infracción se descarta, y si no queda ninguna, la apelación
no se entrega.

Denunciar lo que de verdad incumple las normas es un derecho del
negocio. Denunciar inventándose el motivo es lo que la ley de
consumidores castiga, y además Google lo rechaza. Esa comprobación no se
quita.

## Archivos

| | |
|---|---|
| `politicas.mjs` | Las normas de Google y las instrucciones de la IA. **Aquí se afina el criterio.** |
| `reglas.mjs` | El detector gratis y las plantillas de apelación y respuesta. |
| `motor.mjs` | Reparte entre reglas e IA y comprueba las citas. |
| `ejemplos.json` | Reseñas de prueba, cada una con el veredicto que se espera. |
| `analiza.mjs` | Para probarlo desde la terminal. |
| `prueba.mjs` | Pruebas sin red ni clave. |

## Cómo se usa

```
npm install                                  # una vez
npm run prueba-reputacion                    # pruebas gratis, sin clave
npm run reputacion                           # ejemplos, solo con reglas (gratis)
ANTHROPIC_API_KEY=... npm run reputacion     # ejemplos, con IA donde haga falta
ANTHROPIC_API_KEY=... npm run reputacion -- fisico
ANTHROPIC_API_KEY=... npm run reputacion -- "texto de una reseña"
```


Desde código:

```js
import { analiza } from './reputacion/motor.mjs';

const v = await analiza({
  texto: 'La gorda de la barra no paraba de mirar el móvil.',
  estrellas: 1,
  contexto: '',            // lo que sepa el dueño: "es un exempleado"...
  negocio: {
    nombre: 'Bar Manolo', sector: 'bar de tapas', ciudad: 'Valencia',
    palabras_clave: ['tapas caseras', 'terraza en Valencia'],
    contacto: 'hola@barmanolo.es'
  }
});
// v.veredicto, v.fuerza, v.infracciones, v.apelacion, v.respuesta, v.origen
// { modo: 'gratis' } como segundo argumento: nunca usa la IA
```

## En la web

| | |
|---|---|
| `plea5e.es/analiza/` | El analizador gratis, para cualquiera. Solo reglas: no gasta nada. Da el veredicto y la respuesta al momento; la apelación, a cambio de un WhatsApp o correo. Se puede instalar en el móvil como una app. |
| `plea5e.es/taller/resenas.html` | Tu panel. Misma contraseña que Pedidos. Los contactos que deja la gente, con su reseña analizada y un WhatsApp ya escrito para llamarles; y un analizador para ti que puede usar la IA. |
| `src/api/analiza.js` | Lo que atiende al analizador público. |
| `src/api/analisis.js` | Lo que atiende al panel. |

Los contactos se guardan en el mismo almacén que los pedidos
(`ENCARGOS`), con claves que empiezan por `an-`. El panel de pedidos no
las enseña. El correo de aviso usa las mismas variables que los pedidos
(`RESEND_API_KEY`, `CORREO_AVISO`, `CORREO_DE`); la IA del panel, la
misma `ANTHROPIC_API_KEY` de los colores.

## El conector con Google (`plea5e.es/analiza/ficha/`)

La app del dueño. Se instala en el móvil como una app más.

1. **Busca su negocio** en Google Maps: ve su nota, sus últimas reseñas y
   escribe la respuesta a cualquiera de un toque.
2. **Conecta con Google**: entra con su cuenta y da permiso para
   gestionar las reseñas de su ficha.
3. Desde ahí, **cada dos horas** el vigilante (`src/lib/vigia.mjs`) mira
   sus reseñas nuevas: las de 4 y 5 estrellas las responde solo; las de
   1 a 3 las deja escritas esperando su clic (o las publica solas si lo
   activa), y las denunciables le esperan siempre con la denuncia
   preparada. Si hay algo pendiente, le llega un correo.

Cada ficha tiene su configuración: tono (de tú o de usted), firma,
contacto para las quejas, palabras clave e indicaciones libres ("no
ofrezcas invitaciones"). La IA escribe cada respuesta para esa reseña.

Archivos: `src/api/google.js` (las direcciones), `src/lib/google.mjs`
(lo que se le pide a Google), `src/lib/vigia.mjs` (el vigilante),
`src/lib/cripto.mjs` (cifrado de permisos y sesiones), `src/lib/limite.mjs`
(topes de uso). Pruebas: `src/lib/prueba.mjs`.

### Cómo se activa (una vez, lo haces tú)

Todo en Cloudflare → el Worker → Settings → **Variables and Secrets**.
El panel `/taller/resenas.html` → "Fichas de Google conectadas" te dice
qué falta.

1. **TOKENS_CLAVE**: una frase larga inventada (más de 16 letras), tipo
   `mi-perro-se-llama-tobi-y-come-croquetas-2026`. Ponla como *Secret*.
   No la cambies nunca: si cambia, todos tienen que volver a conectar.
2. **Google Cloud** (console.cloud.google.com), con la cuenta de PLEA5E:
   - Crea un proyecto "PLEA5E".
   - **Para el buscador:** APIs y servicios → Biblioteca → activa
     **Places API (New)**. Credenciales → Crear credencial → Clave de
     API. Restríngela a "Places API (New)". Ponla en Cloudflare como
     **GOOGLE_MAPS_KEY**. Google pide una tarjeta (facturación), pero
     tiene un uso gratis al mes; el Worker no pasa de 300 búsquedas al
     día (`MAPS_TOPE_DIA` para cambiarlo).
   - **Para conectar fichas:** Pantalla de consentimiento de OAuth →
     Externa, nombre "PLEA5E", tu correo, dominio plea5e.es. Credenciales
     → Crear credencial → ID de cliente de OAuth → Aplicación web. En
     "URI de redirección autorizados" pon exactamente
     `https://plea5e.es/api/google/vuelta`. Copia el ID y el secreto a
     Cloudflare: **GOOGLE_CLIENT_ID** y **GOOGLE_CLIENT_SECRET**.
   - **Pide el acceso a la API de Business Profile:** formulario
     "GBP API contact form" → "Application for Basic API Access". Google
     exige una ficha de Google de PLEA5E verificada y activa desde hace
     más de 60 días, con la web en la ficha. Cuando lo aprueben, activa en
     la Biblioteca: **My Business Account Management API**, **My Business
     Business Information API** y **Google My Business API**.
   - Mientras la pantalla de consentimiento esté en modo "Prueba", solo
     pueden conectar las cuentas que añadas como usuarios de prueba (hasta
     100). Para abrirlo a todo el mundo, "Publicar la aplicación": Google
     revisa el permiso de Business Profile y puede pedir un vídeo de cómo
     se usa.
3. **ANTHROPIC_API_KEY**: la misma de los colores. Sin ella, todo
   funciona con plantillas.
4. **RESEND_API_KEY** y **CORREO_DE**: los mismos de los pedidos, para
   los avisos a los dueños.

Hasta que Google apruebe la API, el botón "Conectar con Google" funciona
pero al volver el dueño ve "Google todavía no ha activado la conexión".
El buscador y las respuestas funcionan desde el primer día.

### Topes para que nadie te gaste dinero

| | por persona y día | por día en total | variable |
|---|---|---|---|
| Búsquedas en Maps | 40 | 300 | `MAPS_TOPE_DIA` |
| Respuestas con IA en /analiza/ | 5 | 200 | `IA_TOPE_DIA` |
| Reseñas por vuelta del vigilante | | 12 cada 2 h | `TOPE_VUELTA` en vigia.mjs |

## Lo que falta

- Guardar qué denuncias acepta Google para afinar `politicas.mjs`.
- Que Google apruebe el acceso a la API de Business Profile (arriba).

## Ojo: este repositorio es público

Todo lo que hay aquí se puede ver en GitHub. Si no quieres que te copien
el criterio, haz el repositorio privado (GitHub → Settings → Danger Zone
→ Change visibility). plea5e.es sigue funcionando porque se publica
desde Cloudflare; lo único que dejaría de ir es la dirección vieja
whatthefan.github.io, que en el plan gratis de GitHub necesita que el
repositorio sea público.
