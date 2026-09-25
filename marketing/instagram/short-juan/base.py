"""El video de base (1080x1920): cortes, encuadre por trozo y el audio de la voz limpio."""
import json, subprocess
FF = '/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2'
P = json.load(open('plan.json'))
W0, H0 = 1620, 1080
n = len(P['seg'])
SRC = ['original.mov'] + [s['voz'][0] for s in P['seg'] if s['voz']]
ENT = {s['i']: k + 1 for k, s in enumerate([s for s in P['seg'] if s['voz']])}
f = [f'[0:v]split={n}' + ''.join(f'[v{i}]' for i in range(n))]
orig = [s['i'] for s in P['seg'] if not s['voz']]
f.append(f'[0:a]asplit={len(orig)}' + ''.join(f'[a{i}]' for i in orig))

grado = 'eq=contrast=1.06:saturation=1.12:brightness=0.01,colorbalance=rs=.03:gs=.01:bs=-.03,unsharp=5:5:0.6'
for s in P['seg']:
    i, a, b, z, x = s['i'], s['a'], s['b'], s['z'], s['cx']
    if s['lay'] == 'full':
        h = H0 / z; w = h * 9 / 16; y = (H0 - h) * .08
        tam = '1080:1920'
    else:
        h = 780 / z; w = h * 1080 / 960; y = (H0 - h) * .25
        tam = '1080:960'
    x0 = min(max(x - w / 2, 0), W0 - w)
    crop = f'crop={int(w)//2*2}:{int(h)//2*2}:{int(x0)}:{int(y)}'
    pad = ',pad=1080:1920:0:960:black' if s['lay'] == 'split' else ''
    if s['i'] == 11:   # BOOM: temblor
        crop = crop.rsplit(':', 2)[0] + f":'{int(x0)}+14*sin(t*55)':'{int(y)}+10*cos(t*47)'"
        x0 = max(14, min(x0, W0 - w - 14))
    # empuje lento hacia dentro en los planos a pantalla completa
    D = s['t1'] - s['t0']
    emp = (f",scale=w='trunc(1080*(1+0.06*t/{D:.3f})/2)*2':h=-2:eval=frame,crop=1080:1920:'(iw-1080)/2':'(ih-1920)*0.3'" if s['lay'] == 'full' else '')
    D_ = s['t1'] - s['t0']; k_ = D_ / (b - a)
    f.append(f'[v{i}]trim={a}:{b},setpts=(PTS-STARTPTS)*{k_:.5f},hflip,{crop},scale={tam}:flags=lanczos{emp}{pad},{grado},setsar=1,fps=30[V{i}]')
    if s['voz']:
        vf, va, vb = s['voz']
        f.append(f'[{ENT[i]}:a]atrim={va}:{va + D_:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={D_-0.05:.3f}:d=0.05[A{i}]')
    else:
        f.append(f'[a{i}]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={b-a-0.05:.3f}:d=0.05[A{i}]')
f.append(''.join(f'[V{i}][A{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=1[v][ar]')
f.append('[ar]highpass=f=85,lowpass=f=12500,afftdn=nf=-28,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,'
         'equalizer=f=3200:t=q:w=1.2:g=2,loudnorm=I=-14:TP=-1.5:LRA=7,aresample=48000,aformat=channel_layouts=stereo[a]')
subprocess.run([FF, '-loglevel', 'error', '-y', *sum([['-i', x] for x in SRC], []), '-filter_complex', ';'.join(f), '-map', '[v]', '-map', '[a]',
                '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', 'base.mp4'], check=True)
print('base.mp4 hecho')
