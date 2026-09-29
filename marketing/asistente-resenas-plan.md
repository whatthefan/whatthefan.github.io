# Asistente de reseñas con IA (plan acordado con Juan)

## Planes
- **Básico 20 €/mes:** informe mensual de toques + cambiar a dónde lleva la placa.
- **Completo 35 €/mes:** lo anterior + asistente IA de reseñas + cambio de imagen a mitad de precio.
- **Oferta de fundador:** los 20 primeros negocios, plan Completo a 25 €/mes para siempre.
- Opcional: anual (≈290 €/año).
- Herramienta gratis en plea5e.es con límite diario, como imán de clientes.

## Regla de oro: la IA propone, el negocio decide
- Por defecto, **manual**: 2–3 borradores; el dueño elige, edita o escribe la suya.
- **Automático solo si el dueño lo activa**, y solo para 4–5★ si no las toca en X horas.
- 1–3★ y delicadas (salud, empleados, temas legales): **nunca** automáticas; aviso al dueño.
- Si el dueño ya respondió en Google, el asistente no hace nada.
- Mensaje de venta: «te ayuda a responder», nunca «te consigue reseñas».

## Panel «Mi PLEA5E» (plea5e.es/panel, acceso por enlace al correo)
1. Toques (métricas existentes de /r/).
2. Reseñas con borradores: Publicar · Editar · Más corta · Más cálida.
3. Mi asistente: ficha del local (nombre, tono, firma, platos, horario, reservas, alérgenos, qué hacer ante quejas, palabras prohibidas).
4. Destino de la placa (existente).

## Cómo responde el asistente
- Detecta estrellas, idioma (responde en el mismo), temas y si nombra a alguien.
- Usa la ficha del local para sonar al bar.
- Límites: no inventa, no discute, no da datos personales, no promete compensaciones sin permiso, no repite frases.
- Aprende de las correcciones del dueño (ejemplos guardados).
- Claude por API: modelo rápido para positivas, más potente para quejas.

## Fases
1. **Fase 1 (sin permisos de Google):** panel + «pega tu reseña». Comprobar si el correo de aviso de Google trae el texto completo; si lo trae, reenvío automático a una dirección de PLEA5E y respuesta de vuelta con enlace para publicar.
2. **Fase 2:** «Conectar con Google» (OAuth del propio dueño, revocable) con la API oficial de Business Profile; solicitar acceso a Google. Cron cada 15–30 min en el Worker; publicar con un clic.
3. **Fase 3:** resumen mensual de temas de las reseñas en el informe.

## Técnica
- Cloudflare Worker actual (`src/index.js`) + rutas nuevas `/api/panel/*`, `/api/resenas/*`, `/api/google/*`.
- Datos: D1 (clientes, locales, reseñas, borradores) o el KV actual para empezar.
- Secretos del Worker: `ANTHROPIC_API_KEY`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`. Tokens de Google cifrados.

## Legal (revisar con un asesor antes de lanzar)
- Condiciones del servicio: las respuestas son sugerencias; publica el negocio; lo automático es opcional.
- RGPD: el nombre del autor de la reseña es dato personal → actualizar la política de privacidad y firmar un contrato de encargado del tratamiento con cada cliente; guardar lo mínimo.
- Nunca incentivar reseñas ni pedirlas solo a clientes contentos (lo prohíbe Google).

## Pendiente de Juan
- Clave de la API de Anthropic, guardada por él como secreto en Cloudflare.
- Un bar de prueba para ajustar el tono.
- Revisión legal de las condiciones y la política de privacidad.
