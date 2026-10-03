# Reputación IA

Motor que analiza reseñas negativas de Google. Para cada una:

1. **Busca todo lo que incumple las normas de Google**, frase a frase.
   Con una sola frase basta: un insulto, una descripción física, una
   amenaza velada, un dato personal, una queja que no va del negocio...
2. Si encuentra algo, **redacta la apelación** para el formulario de
   Google, citando la norma y el fragmento exacto.
3. Siempre **redacta la respuesta pública** del dueño: empática, con dos
   palabras clave del negocio y llevando la conversación a privado.

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
| `motor.mjs` | Llama a la IA y comprueba las citas. |
| `ejemplos.json` | Reseñas de prueba, cada una con el veredicto que se espera. |
| `analiza.mjs` | Para probarlo desde la terminal. |
| `prueba.mjs` | Pruebas sin red ni clave. |

## Cómo se usa

```
npm install                                  # una vez
npm run prueba-reputacion                    # pruebas gratis, sin clave
ANTHROPIC_API_KEY=... npm run reputacion     # las reseñas de ejemplo
ANTHROPIC_API_KEY=... npm run reputacion -- fisico
ANTHROPIC_API_KEY=... npm run reputacion -- "texto de una reseña"
```

Cada reseña analizada es una llamada a la IA y cuesta unos céntimos.

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
// v.veredicto, v.fuerza, v.infracciones, v.apelacion, v.respuesta
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
