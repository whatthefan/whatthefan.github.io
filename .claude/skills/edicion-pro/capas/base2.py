import json,sys,subprocess,numpy as np,cv2
F='/tmp/claude-0/bin/ffmpeg'
src,segs,salida,fin=sys.argv[1],json.load(open(sys.argv[2])),sys.argv[3],float(sys.argv[4])
# rangos a conservar
keep=[]
for s in segs:
    a=max(0,s['a']-0.1); b=min(fin,s['b']+0.25)
    if keep and a-keep[-1][1]<0.25: keep[-1][1]=b
    else: keep.append([a,b])
# cara: x del centro (espejado) muestreado a 4 fps
cap=cv2.VideoCapture(src); fps=cap.get(5); cas=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
xs=[];i=0
while True:
    ok,fr=cap.read()
    if not ok: break
    if i%8==0:
        g=cv2.cvtColor(cv2.resize(fr,(540,360)),cv2.COLOR_BGR2GRAY); f=cas.detectMultiScale(g,1.1,5,minSize=(60,60))
        if len(f): x,y,w,h=max(f,key=lambda r:r[2]); xs.append((i/fps,(x+w/2)*3))
    i+=1
xs=np.array(xs); W=960
filt=[];t=0;mapa=[]
for k,(a,b) in enumerate(keep):
    m=(xs[:,0]>=a)&(xs[:,0]<=b); cx=np.median(xs[m,1]) if m.sum()>1 else np.median(xs[:,1])
    x0=int(np.clip(cx-W/2,0,1620-W))
    filt.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,crop={W}:1080:{x0}:0,setsar=1[v{k}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={b-a-0.04}:d=0.04[a{k}]")
    mapa.append({'a':a,'b':b,'t0':round(t,3)}); t+=b-a
n=len(keep)
filt.append(''.join(f'[v{k}][a{k}]' for k in range(n))+f'concat=n={n}:v=1:a=1[v][a0]')
filt.append('[a0]highpass=f=85,afftdn=nf=-25,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,equalizer=f=3000:t=q:w=1:g=2,loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[a]')
subprocess.run([F,'-loglevel','error','-y','-i',src,'-filter_complex',';'.join(filt),'-map','[v]','-map','[a]','-c:v','libx264','-crf','14','-preset','medium','-r','30','-c:a','aac','-b:a','192k',salida],check=True)
# frases en tiempo de salida
def ot(x):
    for m in mapa:
        if m['a']<=x<=m['b']: return m['t0']+x-m['a']
    return None
fr=[]
for s in segs:
    a,b=ot(max(0,s['a'])),ot(min(fin,s['b']))
    if a is None: continue
    ws=s['txt'].split(); L=sum(len(w)+1 for w in ws); c=0; pal=[]
    for w in ws: pal.append([w,round(a+(b-a)*c/L,2)]); c+=len(w)+1
    fr.append({'t0':round(a,2),'t1':round(b,2),'txt':s['txt'],'w':pal})
if 0: json.dump({'total':round(t,2),'frases':fr},open(salida.replace('.mp4','.json'),'w'),ensure_ascii=False,indent=0)
print('total',round(t,2),'cortes',n)
for f in fr: print(f['t0'],f['t1'],f['txt'])
