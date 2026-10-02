"""sintetiza.py — sonidos de interfaz limpios (sin música debajo), del tipo que usan las referencias.
python3 sintetiza.py carpeta/   ->  aire.mp3, aire-corto.mp3, pop.mp3, tic.mp3, golpe-suave.mp3, subida.mp3, brillo.mp3"""
import os, subprocess, sys
import numpy as np
SR = 44100
rng = np.random.default_rng(5)


def ffmpeg():
    import shutil
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def env(n, ataque, caida):
    t = np.arange(n) / SR
    a = np.clip(t / ataque, 0, 1) ** 2
    d = np.exp(-np.clip(t - ataque, 0, None) / caida)
    return a * d


def pasabanda(x, f_ini, f_fin, q=1.2):
    """filtro de estado variable con frecuencia que barre"""
    n = len(x); f = np.geomspace(f_ini, f_fin, n)
    lo = bp = 0.0; y = np.zeros(n)
    for i in range(n):
        g = 2 * np.sin(np.pi * f[i] / SR)
        hp = x[i] - lo - bp / q
        bp += g * hp; lo += g * bp
        y[i] = bp
    return y


def aire(d=.55, pico=.22, f0=350, f1=2600):
    n = int(d * SR)
    ruido = rng.standard_normal(n)
    y = pasabanda(ruido, f0, f1) * env(n, pico, (d - pico) / 3)
    pan = np.linspace(-.6, .6, n)
    return np.stack([y * (1 - pan) / 2, y * (1 + pan) / 2])


def pop(f0=900, f1=320, d=.09):
    n = int(d * SR); t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / d)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .025)
    y[:40] += rng.standard_normal(40) * .3 * np.linspace(1, 0, 40)
    return np.stack([y, y])


def tic(f=2400, d=.03):
    n = int(d * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * f * t) * np.exp(-t / .006) + rng.standard_normal(n) * np.exp(-t / .0015) * .4
    return np.stack([y, y])


def golpe_suave(d=.45):
    n = int(d * SR); t = np.arange(n) / SR
    f = 95 * (45 / 95) ** (t / d)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .12)
    y += pasabanda(rng.standard_normal(n), 3000, 800) * np.exp(-t / .02) * .5
    return np.stack([y, y])


def subida(d=.7):
    n = int(d * SR); t = np.arange(n) / SR
    y = pasabanda(rng.standard_normal(n), 300, 5000, 2) * (t / d) ** 2.2
    y += np.sin(2 * np.pi * np.cumsum(np.geomspace(220, 880, n)) / SR) * (t / d) ** 3 * .25
    return np.stack([y, y])


def brillo(d=1.1):
    n = int(d * SR); t = np.arange(n) / SR
    y = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t / c) for f, a, c in [(1760, 1, .35), (2637, .6, .25), (3520, .35, .18), (5274, .15, .1)])
    return np.stack([y * .9, y])


def guarda(ruta, x, pico=.8):
    x = x / (np.abs(x).max() + 1e-9) * pico
    f = int(.004 * SR); x[:, -f:] *= np.linspace(1, 0, f)
    p = subprocess.Popen([ffmpeg(), "-loglevel", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", "-",
                          "-c:a", "libmp3lame", "-q:a", "2", ruta], stdin=subprocess.PIPE)
    p.stdin.write(x.T.astype(np.float32).tobytes()); p.stdin.close(); p.wait()


if __name__ == "__main__":
    d = sys.argv[1]; os.makedirs(d, exist_ok=True)
    guarda(f"{d}/aire.mp3", aire(), .6)
    guarda(f"{d}/aire-corto.mp3", aire(.32, .12, 600, 3500), .55)
    guarda(f"{d}/pop.mp3", pop(), .7)
    guarda(f"{d}/tic.mp3", tic(), .6)
    guarda(f"{d}/golpe-suave.mp3", golpe_suave(), .85)
    guarda(f"{d}/subida.mp3", subida(), .6)
    guarda(f"{d}/brillo.mp3", brillo(), .5)
    print("listo")
