"""Junta el video base, la capa de graficos y los sonidos."""
import json, subprocess
FF = '/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2'
S = '/home/user/whatthefan.github.io/marketing/instagram/'
P = json.load(open('plan.json'))
ins = ['-i', 'base.mp4', '-i', 'capa.mov']
f = ['[0:v][1:v]overlay=format=auto,format=yuv420p[v]']
mix = ['[0:a]']
for k, (arch, t, vol) in enumerate(P['sfx']):
    ins += ['-i', S + arch]
    ms = max(0, int(t * 1000))
    f.append(f'[{k + 2}:a]aresample=48000,aformat=channel_layouts=stereo,volume={vol},adelay={ms}|{ms}[s{k}]')
    mix.append(f'[s{k}]')
f.append(''.join(mix) + f'amix=inputs={len(mix)}:normalize=0:duration=first,alimiter=limit=0.9[a]')
subprocess.run([FF, '-loglevel', 'error', '-y', *ins, '-filter_complex', ';'.join(f), '-map', '[v]', '-map', '[a]',
                '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', str(P['total']), 'PLEA5E-short-juan.mp4'], check=True)
print('listo')
