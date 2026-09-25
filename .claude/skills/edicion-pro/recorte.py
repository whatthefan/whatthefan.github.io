"""recorte.py — separa a la persona del fondo (vídeo o foto) con RobustVideoMatting (ONNX, CPU).

Es lo que en CapCut se llama «Eliminar fondo». Con esto se hace: persona delante de un fondo nuevo
(cuadrícula oscura, rayos, imagen de IA), texto DETRÁS de la persona y miniaturas recortadas.

Modelo (15 MB, se baja de las releases de GitHub, Hugging Face suele estar bloqueado):
  curl -L -o rvm.onnx https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3_fp32.onnx

Uso:
  python3 recorte.py foto.png  salida.png            # PNG con transparencia + salida-borde.png (contorno)
  python3 recorte.py video.mp4 mate.mp4 [t0 t1]      # vídeo en grises: blanco = persona
Después, en ffmpeg: [fondo][video][mate]  -> alphamerge + overlay  (ver SKILL.md, «Persona sobre fondo nuevo»)
"""
import os
import subprocess
import sys

import numpy as np
import onnxruntime as ort

MODELO = os.environ.get("RVM", "/tmp/claude-0/modelos/rvm_mobilenetv3_fp32.onnx")
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")


def sesion():
    return ort.InferenceSession(MODELO, providers=["CPUExecutionProvider"])


def estado():
    return [np.zeros((1, 1, 1, 1), np.float32)] * 4


def paso(s, rgb, rec, ratio):
    src = (rgb.astype(np.float32) / 255.0).transpose(2, 0, 1)[None]
    fgr, pha, *rec = s.run(None, {"src": src, "r1i": rec[0], "r2i": rec[1], "r3i": rec[2], "r4i": rec[3],
                                  "downsample_ratio": np.array([ratio], np.float32)})
    return pha[0, 0], rec


def foto(entrada, salida, ratio=0.4):
    import cv2
    bgr = cv2.imread(entrada, cv2.IMREAD_COLOR)
    s, rec = sesion(), estado()
    for _ in range(6):  # el modelo es recurrente: repetir la misma foto estabiliza el mate
        pha, rec = paso(s, bgr[:, :, ::-1], rec, ratio)
    a = np.clip((np.clip(pha, 0, 1) * 255 - 20) * 1.15, 0, 255).astype(np.uint8)
    cv2.imwrite(salida, np.dstack([bgr, a]))
    # contorno blanco tipo pegatina para miniaturas: <salida>-borde.png
    m = cv2.dilate((a > 110).astype(np.uint8) * 255, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25)))
    b = np.zeros((*a.shape, 4), np.uint8)
    b[:, :, :3], b[:, :, 3] = 255, cv2.GaussianBlur(m, (3, 3), 0)
    cv2.imwrite(salida.rsplit('.', 1)[0] + '-borde.png', b)


def video(entrada, salida, t0=None, t1=None, ratio=0.25):
    info = subprocess.run([FFMPEG, "-i", entrada], capture_output=True, text=True).stderr
    import re
    w, h = map(int, re.search(r", (\d{3,5})x(\d{3,5})", info).groups())
    corte = (["-ss", str(t0)] if t0 is not None else []) + (["-to", str(t1)] if t1 is not None else [])
    lee = subprocess.Popen([FFMPEG, "-loglevel", "error", *corte, "-i", entrada, "-f", "rawvideo",
                            "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    esc = subprocess.Popen([FFMPEG, "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray",
                            "-s", f"{w}x{h}", "-r", "30", "-i", "-", "-c:v", "libx264", "-crf", "12",
                            "-pix_fmt", "yuv420p", salida], stdin=subprocess.PIPE)
    s, rec, n = sesion(), estado(), 0
    while True:
        buf = lee.stdout.read(w * h * 3)
        if len(buf) < w * h * 3:
            break
        pha, rec = paso(s, np.frombuffer(buf, np.uint8).reshape(h, w, 3), rec, ratio)
        esc.stdin.write((np.clip(pha, 0, 1) * 255).astype(np.uint8).tobytes())
        n += 1
        if n % 150 == 0:
            print(n, "fotogramas", flush=True)
    esc.stdin.close()
    esc.wait()
    print("listo:", salida, n, "fotogramas")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0].lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        foto(a[0], a[1])
    else:
        video(a[0], a[1], *(float(x) for x in a[2:4]))
