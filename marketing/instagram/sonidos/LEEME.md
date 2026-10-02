# Sonidos para los vídeos

Efectos grabados de verdad, todos con licencia **CC0 1.0** (dominio
público): se pueden usar en vídeos comerciales, anuncios incluidos, sin
pagar ni citar a nadie. Aun así se guarda de dónde sale cada uno.

| Archivos | De dónde | Autor | Licencia |
|---|---|---|---|
| `kenney-*.wav` | [Interface Sounds](https://kenney.nl/assets/interface-sounds) (vía [Calinou/kenney-interface-sounds](https://github.com/Calinou/kenney-interface-sounds)) | Kenney | CC0 1.0 |
| `whoosh*.mp3` | [Swishes Sound Pack](https://opengameart.org/content/swishes-sound-pack) | artisticdude | CC0 1.0 |
| `riser.mp3` | [Riser sound effect short](https://freesound.org/people/syntheffects/sounds/685256/) | syntheffects | CC0 1.0 |
| `impact-bass-*.mp3` | [Impact Sounds](https://kenney.nl/assets/impact-sounds) | Kenney | CC0 1.0 |
| el resto de `*.mp3` (pop, click, ping, chime, sparkle, notification, key-press, error, glitch) | Interface Sounds / UI Audio | Kenney | CC0 1.0 |

Los `.mp3` vienen ya recortados del pack de
[asaf5767/reelkit](https://github.com/asaf5767/reelkit); `procedencia-reelkit.json`
dice el archivo original de cada uno y `licencias/` guarda el texto de
cada licencia tal cual.

Antes de añadir un sonido nuevo: que sea CC0 y SOLO CC0. Un sonido con
varias licencias a la vez (CC0 y además CC-BY-SA, GPL…) no vale.


## `virales/`: los memes de TikTok de siempre

vine boom, bruh, airhorn, ba dum tss, grillos, violín triste, wow, huh, nope, wait a minute,
tubo de metal, oof…, sacados de dos soundboards de GitHub
([Thijzert123/meme-soundboard](https://github.com/Thijzert123/meme-soundboard) y
[imsupercool123qwerty-pixel/soundboard2](https://github.com/imsupercool123qwerty-pixel/soundboard2)),
recortados y al mismo volumen. `MUESTRARIO-virales.mp4` los enseña todos.

OJO: estos NO son CC0. Son los memes que usa todo el mundo en TikTok e Instagram
(nadie reclama por ellos en perfiles normales), pero no tienen licencia comercial:
no usarlos en anuncios pagados. Se han dejado fuera los que son canciones con dueño
(To be continued, Titanic, Shrek, Windows, Inception, «Oh no no no»).

## `edicion/`: los de edición profesional

woah drop, arrow swoosh (x2), camera screenshot, glitch, metallic riser, ding, mouse click,
mac typing, camera shutter, punch riser y cinematic impact. Recortados de dos vídeos de
TikTok de packs de sonidos («Sound Effects for your next video» y el de Dezzy) que pasó Juan.
Tampoco son CC0: para vídeos del perfil sí, para anuncios pagados no.

## referencias/ y ui/ (estilo actual de edición)

- `referencias/`: tics, clics y pops sacados de los 4 vídeos de referencia de Juan (@solazzox, @ruy_r.s,
  @johan.mttz, @milah.edicion) quitando la voz con UVR MDX-Net (`separa.py` de la skill edicion-pro).
  Mismo criterio que los de `edicion/`: bien para el perfil, no para anuncios de pago.
- `ui/`: sintetizados por nosotros (`sintetiza.py`), sin derechos de terceros: `aire-corto` (transición),
  `aire`, `pop`, `tic`, `golpe-suave`, `brillo`, `subida`.
