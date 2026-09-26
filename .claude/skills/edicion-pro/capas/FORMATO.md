# FORMATO PLEA5E v5 — «como las referencias» (POR DEFECTO desde el 26-9 noche)

Juan rechazó la v4 (collage de pegatinas, Montserrat, oro sobre oscuro, recorte de su cara): «se ve IA, tipografía fea,
poco profesional». Lo que hacen de verdad las referencias (estudiado fotograma a fotograma):
- **Cara real a pantalla completa**, SIN recortar (nada de «green screen»). Subtítulos pequeños blancos a la altura del
  pecho (Inter Display 600, ~50 px), 1-4 palabras; «punch-in» (zoom seco 1,08-1,13) en la palabra fuerte.
- **Escenas en gris claro** (degradado suave + textura de papel muy leve). Texto **gris oscuro**, Inter Display
  (500 pequeño / 700 grande), centrado, sin cursivas ni colores. Letra a letra con desenfoque (@solazzox).
- **Objetos en blanco y negro** sin borde (como los recortes de @johan.mttz). **Solo la placa real va en color.**
- **Tipografía cinética 3D**: número o palabra gigante que gira en perspectiva (el «01» de @solazzox): `K.gira`.
- **Transiciones de editor** (`K.escenas5` + `K.efectos`): tinta (manchas que crecen), látigo lateral con desenfoque,
  estrobo blanco/negro + iris, zoom a través, corte con fuga de luz naranja. Una distinta en cada corte.
- Nada de fondo oscuro con oro, nada de pegatinas de colores, nada de chispas/brillos: huele a IA.
- Sonido: látigo = `whoosh-short`, estrobo = `edicion/glitch`, tinta/zoom = `ui/aire`, ¡pum! = `woah-drop`.
Ejemplos: `mosca5.html`, `uber5.html`; kit: `kit5.css` + `kit5.js` (sobre kit + kit2 + kit3).

---
(Formato v4 anterior, descartado:)
# FORMATO PLEA5E (v4) — la plantilla de todos los vídeos hablados

Hoja visual: `identidad.html` (se renderiza con `grabar.js identidad.html prueba id 0`).
Base de código: `kit4.css` + `kit4.js` (sobre kit/kit2/kit3). Ejemplos completos: `mosca4.html`, `uber4.html`.

## Estructura (30 s)
1. **Gancho con cara** (1-3 s): Juan recortado como pegatina (borde blanco), abajo; frase pequeña delante y la palabra
   grande DETRÁS de la cabeza. Un detalle vivo (la mosca volando alrededor).
2. **Historia en collage** (4-7 escenas): papel con fibra, titular arriba a la izquierda, UNA idea por escena,
   máx. 3 elementos (pegatina real/3D, cinta, papel rasgado, sello, garabato).
3. **¡Pum!**: destello + woah drop + la placa REAL (foto recortada) se pega con cinta.
4. **Demo**: el móvil toca la placa → pantalla de reseña con etiqueta «Demostración».
5. **Marca** (1 s, fondo noche): PLEA5E en Montserrat 900 con el 5 en oro. Nunca el sello de la estrella.
6. **CTA con cara**: «comenta PLACA» detrás de la cabeza + comentario que se escribe solo.
La cara no sale en medio: solo gancho y CTA.

## Tipografía (obligatoria)
Montserrat. Frase pequeña 700 / 52 px; palabra grande 900 / 128 px, interletra −5 %, interlínea 0,9;
palabra clave 900 **cursiva** en oro con subrayado. Alineado a la izquierda (margen 90). Detrás de la cabeza: 200-280 px.

## Ritmo
Entrada ≤ 0,45 s (muelle); cada elemento **quieto ≥ 1 s** antes de salir; nada entra mientras otro está a medias.
Si la frase va rápida, menos elementos, no más rápido.

## Zonas
Arriba 0-200 libre · titular 250-600 · contenido 700-1500 · abajo 1650+ libre (texto de Instagram) · derecha abajo libre (botones).

## Sonido
Voz: `voz.py` + cadena de `cadena-voz.txt` (RNNoise `arnndn` modelo std de github.com/richardpl/arnndn-models, puerta suave,
−3 dB a 250 Hz, +2,5 dB a 4 kHz, de-esser, compresor, −14 LUFS). La cadena antigua (afftdn) se comía los agudos: NO usar.
Efectos (`mezcla2.py`, alineados al golpe, base −14 dB): pegar = `ui/pega*.mp3`, cinta = `ui/cinta.mp3`, tachar =
`ui/rotulador.mp3`, cortes = `ui/aire-corto.mp3`, ¡pum! = `edicion/woah-drop.mp3`, toque = `edicion/mouse-click.mp3`,
estrellas = `tic-b` + `ding`, acierto = `cinematic-impact`, viral puntual = `vine-boom` / `nope` / `grillos` (0,6 s).
