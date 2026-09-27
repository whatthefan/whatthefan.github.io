"""extraer-sfx.py vídeo.mp4 destino/ nombre:inicio:dur_aprox [nombre:inicio:dur ...] [--sin-voz]
Saca SFX de un vídeo de referencia SIN cortarlos:
  1) --sin-voz: separa la voz con Demucs (pip install demucs; usa torch) y trabaja sobre no_vocals.wav
  2) desde `inicio`, alarga el final hasta que el sonido cae 40 dB bajo su pico o empieza otro sonido
  3) si la fuente lo corta (cola > -32 dB), añade una cola de reverb suave para que se apague natural
  4) normaliza a -1 dBFS y guarda mp3 192k
Ejemplo: python3 extraer-sfx.py guia.mp4 sonidos/packs2 whoosh:26.65:.35 riser:6.3:3.4 --sin-voz"""
import sys,os,subprocess,shutil,numpy as np,soundfile as sf
from scipy.signal import fftconvolve
F=os.environ.get('FFMPEG') or ('/tmp/claude-0/bin/ffmpeg' if os.path.exists('/tmp/claude-0/bin/ffmpeg') else shutil.which('ffmpeg'))
args=[a for a in sys.argv[1:] if not a.startswith('--')]; sinvoz='--sin-voz' in sys.argv
src,dst,items=args[0],args[1],args[2:]; os.makedirs(dst,exist_ok=True)
tmp='/tmp/extraer-sfx'; os.makedirs(tmp,exist_ok=True); w=f'{tmp}/src.wav'
subprocess.run([F,'-v','error','-y','-i',src,'-ac','2','-ar','44100',w],check=True)
if sinvoz:
    subprocess.run([sys.executable,'-m','demucs','--two-stems=vocals','-n','htdemucs','-o',tmp,w],check=True)
    w=f'{tmp}/htdemucs/src/no_vocals.wav'
x,sr=sf.read(w)
rng=np.random.default_rng(1)
def fin(a,ln,maxs=4.0):
    m=x.mean(1); h=int(.02*sr); db=20*np.log10(np.array([np.sqrt((m[i:i+h]**2).mean())+1e-9 for i in range(0,len(m)-h,h)]))
    i0=int(a/.02); pk=db[i0:i0+max(1,int(ln/.02))].max(); j=i0+int(ln/.02)
    while j<len(db)-3 and j<i0+int(maxs/.02):
        if db[j]<pk-40: return j*h, db[j]-pk
        if db[j+2]-db[j]>9 and db[j+2]>pk-25: return (j+1)*h, db[j]-pk      # arranca otro sonido
        j+=1
    return j*h, db[j-1]-pk
def cola(y,resto):
    if resto<-32: fo=min(int(.08*sr),len(y)//4); y[-fo:]*=np.linspace(1,0,fo)[:,None]; return y
    T=1.4; t=np.arange(int(T*sr))/sr; ir=rng.standard_normal((len(t),2))*np.exp(-t/.32)[:,None]
    z=np.vstack([y,np.zeros((len(t),2))]); wet=np.stack([fftconvolve(z[:,c],ir[:,c])[:len(z)] for c in range(2)],1)
    wet=wet/np.abs(wet).max()*np.abs(y[-int(.15*sr):]).max()*.9; fo=int(.12*sr)
    e=np.ones(len(z)); e[len(y)-fo:len(y)]=np.linspace(1,0,fo); e[len(y):]=0
    out=z*e[:,None]+wet*(1-e)[:,None]*(np.arange(len(z))>=len(y)-fo)[:,None]
    out[-int(.3*sr):]*=np.linspace(1,0,int(.3*sr))[:,None]; return out
for it in items:
    n,a,ln=it.split(':'); a,ln=float(a),float(ln); b,resto=fin(a,ln)
    y=x[int(a*sr):b].copy(); fi=int(.004*sr); y[:fi]*=np.linspace(0,1,fi)[:,None]; y=cola(y,resto); y=y/np.abs(y).max()*.89
    sf.write(f'{tmp}/o.wav',y,sr); subprocess.run([F,'-v','error','-y','-i',f'{tmp}/o.wav','-b:a','192k',f'{dst}/{n}.mp3'],check=True)
    print(f'{n}: {len(y)/sr:.2f} s, pico a {np.argmax(np.abs(y).mean(1))/sr:.2f} s')
