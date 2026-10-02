"""compone.py — monta el vídeo por capas, de atrás hacia delante:

    1. base.mp4        vídeo de la persona (1080x1920, con su voz)
    2. detras.mov      capa transparente: fondos nuevos (cuadrícula, rayos, imagen IA) y texto DETRÁS de la persona
    3. persona         base + mate.mp4 (de recorte.py) → la persona recortada, encima de lo anterior
                       · en las ventanas «pequeno» se dibuja reducida y abajo (como en la referencia)
    4. delante.mov     capa transparente: iconos, subtítulos, flashes, palabras que golpean
    5. sonidos         efectos con su tiempo y volumen

Uso:  python3 compone.py montaje.json
montaje.json:
{ "base": "base.mp4", "mate": "mate.mp4", "detras": "detras.mov", "delante": "delante.mov",
  "pequeno": [[1.6, 2.77]], "escala": 0.62, "total": 6.0, "salida": "demo.mp4",
  "sfx": [["/ruta/woah-drop.mp3", 0.0, 0.5]] }
"""
import json
import os
import subprocess
import sys

def _ffmpeg():
    import shutil
    if os.environ.get("FFMPEG"):
        return os.environ["FFMPEG"]
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    import imageio_ffmpeg  # pip install imageio-ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


FF = _ffmpeg()
C = json.load(open(sys.argv[1]))
peq = C.get("pequeno", [])
en_peq = "+".join(f"between(t,{a},{b - 0.001})" for a, b in peq) or "0"
s = C.get("escala", 0.62)

ins = ["-i", C["base"], "-i", C["mate"], "-i", C["detras"], "-i", C["delante"]]
f = [
    "[1:v]format=gray,scale=1080:1920,split=2[m][mp]",
    # versión pequeña: los laterales se difuminan (si la toma es cerrada, la persona está cortada en recto)
    f"[mp]geq=lum='p(X,Y)*clip(min(X,W-1-X)/(W*{C.get('borde', 0.12)}),0,1)'[mps]",
    "[0:v]split=3[b0][b1][b2]",
    "[b1][m]alphamerge[pg]",
    f"[b2][mps]alphamerge,scale=iw*{s}:-2[pps]",
    "[b0][2:v]overlay=format=auto[v1]",
    f"[v1][pg]overlay=format=auto:enable='not({en_peq})'[v2]",
    f"[v2][pps]overlay=x=(W-w)/2:y=H-h:format=auto:enable='{en_peq}'[v3]",
    "[v3][3:v]overlay=format=auto,format=yuv420p[v]",
]
mix = ["[0:a]"]
for k, (arch, t, vol) in enumerate(C.get("sfx", [])):
    ins += ["-i", arch]
    ms = max(0, int(t * 1000))
    f.append(f"[{k + 4}:a]aresample=48000,aformat=channel_layouts=stereo,volume={vol},adelay={ms}|{ms}[s{k}]")
    mix.append(f"[s{k}]")
f.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,alimiter=limit=0.9[a]")
subprocess.run([FF, "-loglevel", "error", "-y", *ins, "-filter_complex", ";".join(f), "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", str(C["total"]), C["salida"]], check=True)
print("listo:", C["salida"])
