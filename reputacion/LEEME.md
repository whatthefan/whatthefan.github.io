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

## Lo que falta

- Conectar con la API de Google Business Profile para leer las reseñas
  nuevas y publicar las respuestas solas.
- El panel donde el dueño ve el análisis y pulsa "Denunciar".
- Guardar qué denuncias acepta Google para afinar `politicas.mjs`.

## Ojo: este repositorio es público

Todo lo que hay aquí se puede ver en GitHub. Si no quieres que te copien
el criterio, haz el repositorio privado (GitHub → Settings → Danger Zone
→ Change visibility). plea5e.es sigue funcionando porque se publica
desde Cloudflare; lo único que dejaría de ir es la dirección vieja
whatthefan.github.io, que en el plan gratis de GitHub necesita que el
repositorio sea público.
