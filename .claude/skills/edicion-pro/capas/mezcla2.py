"""mezcla2.py vídeo.mov audio.mp4 salida.mp4 sfx.json
sfx: [[segundo_del_golpe, archivo en sonidos/, dB_relativos(0 = nivel base -24 dB), duración_opcional]]
Cada sonido se adelanta lo que tarda en llegar a su golpe y se iguala de volumen."""
import subprocess,sys,json,numpy as np,functools
F='/tmp/claude-0/bin/ffmpeg'; S='/home/user/whatthefan.github.io/marketing/instagram/sonidos/'
@functools.lru_cache(None)
def mide(f):
    a=np.frombuffer(subprocess.run([F,'-loglevel','error','-i',S+f,'-ac','1','-ar','8000','-f','s16le','-'],capture_output=True).stdout,np.int16).astype(float)
    e=np.sqrt(np.convolve(a*a,np.ones(160)/160,'same')); return e.argmax()/8000, 20*np.log10(e.max()/32768+1e-9)
vid,aud,out,sfx=sys.argv[1],sys.argv[2],sys.argv[3],json.load(open(sys.argv[4]))
ins=['-i',vid,'-i',aud]; fl=[]; lab=[]
for i,x in enumerate(sfx):
    t,f,rel=x[:3]; dur=x[3] if len(x)>3 else None
    pk,db=mide(f); st=max(0,t-pk); g=10**((-24+rel-db)/20)
    ins+=['-i',S+f]; n=i+2
    tr=f'atrim=0:{dur},afade=t=out:st={max(0,dur-.25)}:d=.25,' if dur else ''
    fl.append(f'[{n}:a]{tr}aresample=48000,aformat=channel_layouts=stereo,volume={g:.3f},adelay={int(st*1000)}|{int(st*1000)}[s{i}]'); lab.append(f'[s{i}]')
fl.append('[1:a]aresample=48000,aformat=channel_layouts=stereo[vz]')
fl.append('[vz]'+''.join(lab)+f'amix=inputs={len(lab)+1}:normalize=0:duration=first,alimiter=limit=0.93[a]')
subprocess.run([F,'-loglevel','error','-y',*ins,'-filter_complex',';'.join(fl),'-map','0:v','-map','[a]','-c:v','libx264','-crf','19','-preset','medium','-pix_fmt','yuv420p','-profile:v','high','-c:a','aac','-b:a','192k','-movflags','+faststart','-shortest',out],check=True)
