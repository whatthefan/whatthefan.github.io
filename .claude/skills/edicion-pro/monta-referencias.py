"""Monta el estilo REFERENCIAS: base.mp4 + tramos con la persona desenfocada (cristal encima) + capa.mov + sonidos.
Cambiar T, los tramos de desenfoque (trim) y la lista sfx. Si el tramo es de pantalla partida, recortar la mitad de abajo y ampliarla (crop/scale) antes del gblur."""
import subprocess
import imageio_ffmpeg, os
F = os.environ.get('FFMPEG') or imageio_ffmpeg.get_ffmpeg_exe()
E = os.environ.get('SFX', 'marketing/instagram/sonidos/edicion')
T=19.833
sfx=[('arrow-swoosh',1.62,.22),('mouse-click',1.8,.28),('arrow-swoosh-2',4.84,.28),('mac-typing',5.55,.2),
     ('camera-shutter',6.25,.22),('arrow-swoosh',7.88,.22),('mouse-click',8.55,.32),('woah-drop',8.97,.5),
     ('arrow-swoosh-2',9.5,.24),('ding',13.25,.28),('arrow-swoosh-2',14.67,.28),('arrow-swoosh',14.78,.18),
     ('arrow-swoosh',16.98,.2),('mouse-click',17.08,.26),('mouse-click',17.87,.26),('mouse-click',19.03,.26)]
ins=['-i','base.mp4','-i','capa.mov']
f=['[0:v]split=3[b][x1][x2]',
   '[x1]trim=1.633:2.767,setpts=PTS-STARTPTS,gblur=sigma=40,eq=brightness=-0.03,format=yuva420p,fade=in:st=0:d=0.2:alpha=1,setpts=PTS+1.633/TB[y1]',
   f'[x2]trim=17:{T},setpts=PTS-STARTPTS,crop=1080:960:0:960,scale=2160:1920,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.03,format=yuva420p,fade=in:st=0:d=0.2:alpha=1,setpts=PTS+17/TB[y2]',
   '[b][y1]overlay=eof_action=pass[b1]','[b1][y2]overlay=eof_action=pass[b2]',
   '[b2][1:v]overlay=format=auto,format=yuv420p[v]']
mix=['[0:a]']
for k,(n,t,v) in enumerate(sfx):
    ins+=['-i',f'{E}/{n}.mp3']; ms=int(t*1000)
    f.append(f'[{k+2}:a]aresample=48000,aformat=channel_layouts=stereo,volume={v},adelay={ms}|{ms}[s{k}]'); mix.append(f'[s{k}]')
f.append(''.join(mix)+f'amix=inputs={len(mix)}:normalize=0:duration=first,alimiter=limit=0.9[a]')
subprocess.run([F,'-loglevel','error','-y',*ins,'-filter_complex',';'.join(f),'-map','[v]','-map','[a]','-c:v','libx264','-preset','slow','-crf','18',
  '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-t',str(T),'demo.mp4'],check=True)
print('ok')
