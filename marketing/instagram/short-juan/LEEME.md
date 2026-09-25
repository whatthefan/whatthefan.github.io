# Short «¿Veis esto?» (Juan a cámara, 59 s)

El vídeo original y el montado NO se guardan aquí: salen tu cara y el repo es público.
Aquí quedan los scripts para volver a montarlo si cambia algo (en una carpeta de trabajo con
`original.mov`, `audio16.wav`, `cara.json`):

1. `plan.py`  → cortes, encuadre (full = cara entera, split = gráfico arriba y tú abajo), subtítulos y sonidos
2. `base.py`  → vídeo base 1080x1920 con los cortes y la voz limpia
3. `capa.py` + `node grabar.js todo` → gráficos y subtítulos con transparencia
4. `final.py` → lo junta todo con los sonidos

`fino.json` es la transcripción (Whisper small, en local) con sus tiempos.

**Versión final publicada: la v6** (`plan.py` + `capa.py`). `capa2.py` es la prueba con el estilo
de la skill edicion-pro: a Juan no le convenció para este vídeo; queda para los siguientes.
