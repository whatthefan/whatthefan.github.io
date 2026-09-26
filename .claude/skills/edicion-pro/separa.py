"""separa.py — quita la voz de un vídeo/audio y deja música + efectos (para sacar los sfx de las referencias).

Modelo UVR MDX-Net (ONNX, CPU). Se baja de las releases de GitHub:
  curl -L -o mdx.onnx https://github.com/TRvlvr/model_repo/releases/download/all_public_uvr_models/UVR-MDX-NET-Inst_HQ_3.onnx
Uso:
  python3 separa.py referencia.mp4 sin_voz.wav      (-> sin_voz.wav y sin_voz-voz.wav)
"""
import os
import subprocess
import sys

import numpy as np
import onnxruntime as ort

MODELO = os.environ.get("MDX", "/tmp/claude-0/sfxref/UVR-MDX-NET-Inst_HQ_3.onnx")
N_FFT, HOP, DIM_F, DIM_T, SR = 6144, 1024, 3072, 256, 44100


def ffmpeg():
    import shutil
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def leer(ruta):
    raw = subprocess.run([ffmpeg(), "-loglevel", "error", "-i", ruta, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).T.copy()


def escribir(ruta, x):
    p = subprocess.Popen([ffmpeg(), "-loglevel", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", "-", ruta],
                         stdin=subprocess.PIPE)
    p.stdin.write(np.clip(x.T, -1, 1).astype(np.float32).tobytes())
    p.stdin.close()
    p.wait()


def stft(x):
    ven = np.hanning(N_FFT + 1)[:-1].astype(np.float32)
    x = np.pad(x, ((0, 0), (N_FFT // 2, N_FFT // 2)), mode="reflect")
    n = 1 + (x.shape[1] - N_FFT) // HOP
    idx = np.arange(N_FFT)[None, :] + HOP * np.arange(n)[:, None]
    return np.fft.rfft(x[:, idx] * ven, axis=-1).transpose(0, 2, 1)  # (2, F, T)


def istft(S, largo):
    ven = np.hanning(N_FFT + 1)[:-1].astype(np.float32)
    fr = np.fft.irfft(S.transpose(0, 2, 1), n=N_FFT, axis=-1) * ven
    n = fr.shape[1]
    out = np.zeros((2, N_FFT + HOP * (n - 1)), np.float32)
    w = np.zeros(out.shape[1], np.float32)
    for i in range(n):
        out[:, i * HOP:i * HOP + N_FFT] += fr[:, i]
        w[i * HOP:i * HOP + N_FFT] += ven ** 2
    out /= np.maximum(w, 1e-8)
    return out[:, N_FFT // 2:N_FFT // 2 + largo]


def separar(x):
    s = ort.InferenceSession(MODELO, providers=["CPUExecutionProvider"])
    trozo = HOP * (DIM_T - 1)
    pad = N_FFT // 2
    largo = x.shape[1]
    x2 = np.pad(x, ((0, 0), (pad, pad + trozo)))
    out = np.zeros_like(x2)
    paso = trozo // 2
    peso = np.zeros(x2.shape[1], np.float32)
    ven = np.hanning(trozo).astype(np.float32)
    for i in range(0, x2.shape[1] - trozo, paso):
        seg = x2[:, i:i + trozo]
        S = stft(seg)[:, :DIM_F, :DIM_T]
        if S.shape[2] < DIM_T:
            S = np.pad(S, ((0, 0), (0, 0), (0, DIM_T - S.shape[2])))
        ent = np.concatenate([S.real, S.imag], 0)[None].astype(np.float32)   # (1,4,F,T): L re, R re, L im, R im
        ent = np.stack([S[0].real, S[0].imag, S[1].real, S[1].imag])[None].astype(np.float32)
        y = s.run(None, {"input": ent})[0][0]
        Y = np.stack([y[0] + 1j * y[1], y[2] + 1j * y[3]])
        Y = np.pad(Y, ((0, 0), (0, N_FFT // 2 + 1 - DIM_F), (0, 0)))
        rec = istft(Y, trozo)
        out[:, i:i + trozo] += rec * ven
        peso[i:i + trozo] += ven
    out /= np.maximum(peso, 1e-3)
    return out[:, pad:pad + largo] * 1.022


if __name__ == "__main__":
    ent, sal = sys.argv[1], sys.argv[2]
    x = leer(ent)
    inst = separar(x)
    escribir(sal, inst)
    escribir(sal.rsplit(".", 1)[0] + "-voz.wav", x - inst)
    print("listo:", sal)
