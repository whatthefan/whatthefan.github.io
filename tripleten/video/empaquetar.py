"""Versión de un solo archivo de la web, con los dos vídeos dentro.

    python3 tripleten/video/empaquetar.py salida.html [ffmpeg]

Recomprime demo.mp4 y demo-en.mp4 a 720p (con sonido), los mete en la página
junto con sus portadas y deja un index.html que funciona subido solo, sin
ningún archivo al lado.
"""
import base64
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[1]
ffmpeg = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("FFMPEG", "ffmpeg")

html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()


def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode("ascii")


blocks = []
with tempfile.TemporaryDirectory() as tmp:
    for lang, name in (("es", "demo"), ("en", "demo-en")):
        small = os.path.join(tmp, name + ".mp4")
        subprocess.run([ffmpeg, "-y", "-v", "error", "-i", os.path.join(ROOT, name + ".mp4"),
                        "-vf", "scale=720:1280:flags=lanczos", "-c:v", "libx264", "-preset", "slow", "-crf", "30",
                        "-profile:v", "high", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "80k",
                        "-movflags", "+faststart", small], check=True)
        print(lang, "vídeo:", round(os.path.getsize(small) / 1e6, 1), "MB")
        blocks.append('<script type="application/octet-stream" id="pack-video-%s">%s</script>' % (lang, b64(small)))
        poster = os.path.join(ROOT, name.replace("demo", "demo-poster") + ".jpg")
        blocks.append('<script type="text/plain" id="pack-poster-%s">data:image/jpeg;base64,%s</script>' % (lang, b64(poster)))


def swap(a, b):
    global html
    assert html.count(a) == 1, a
    html = html.replace(a, b)


# Sin rutas a archivos externos: el JS pone el vídeo y la portada.
swap('<video id="demo" controls playsinline preload="metadata" poster="demo-poster.jpg"><source src="demo.mp4" type="video/mp4"></video>',
     '<video id="demo" controls playsinline preload="metadata"></video>')
swap('<meta charset="UTF-8">', '<meta charset="UTF-8">\n<meta name="croi-packed" content="1">')
# Los vídeos van al final, después del script: la página funciona antes de que terminen de llegar.
assert html.rstrip().endswith("</html>")
i = html.rindex("</body>")
html = html[:i] + "\n".join(blocks) + "\n" + html[i:]
open(out, "w", encoding="utf-8").write(html)
print("listo:", out, round(os.path.getsize(out) / 1e6, 1), "MB")
