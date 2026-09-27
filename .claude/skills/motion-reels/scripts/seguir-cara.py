import subprocess,json,os,sys,numpy as np,cv2
sys.path.insert(0,'/home/user/whatthefan.github.io/.claude/skills/edicion-pro'); import recorte as R
F='/tmp/claude-0/bin/ffmpeg'; C='/tmp/claude-0/ego/crudos/'; D='/tmp/claude-0/ego/capa/cara/'
TM='zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,'
info=json.load(open('/tmp/claude-0/ego/segs.json')); ses=R.sesion()
def frames(f,a,d,vf,W,H):
    p=subprocess.Popen([F,'-v','error','-ss',str(a),'-i',C+f,'-t',str(d),'-vf',vf,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        yield np.frombuffer(b,np.uint8).reshape(H,W,3)
SEG={'v1952.mov':.95,'v1954.mov':.75,'v2005.mov':.55,'IMG_3068.MOV':.1}
for s in info:
    if s['m']=='-': continue
    a=SEG[s['f']]; d=s['t1']-s['t0']; n=s['n0']
    if s['m']=='L': W,H=1620,1080; vf='fps=30,hflip'
    else: W,H=1080,1920; vf=TM+'fps=30,hflip,scale=1080:1920'
    rec=R.estado(); ims=[]; als=[]; cx=[]
    for rgb in frames(s['f'],a,d,vf,W,H):
        pha,rec=R.paso(ses,rgb,rec,.35 if s['m']=='L' else .25)
        al=np.clip((np.clip(pha,0,1)*255-20)*1.15,0,255).astype(np.uint8)
        top=al[:int(H*.55)].astype(np.float32); cols=top.sum(0)
        cx.append((cols*np.arange(W)).sum()/max(cols.sum(),1) if cols.sum()>1e4 else (cx[-1] if cx else W/2))
        ims.append(rgb); als.append(al)
    cx=np.array(cx)
    if s['m']=='L':  # suavizado fuerte (ida y vuelta) para que el encuadre no tiemble
        k=np.ones(21)/21; sm=np.convolve(np.pad(cx,10,mode='edge'),k,'valid'); x0=np.clip(sm-480,0,W-960).astype(int)
    for j,(im,al) in enumerate(zip(ims,als)):
        if s['m']=='L': im=im[:,x0[j]:x0[j]+960]; al=al[:,x0[j]:x0[j]+960]
        bgr=im[:,:,::-1]
        if s['m']=='L':
            bgr=cv2.resize(bgr,(1080,1215),interpolation=cv2.INTER_LANCZOS4); al=cv2.resize(al,(1080,1215),interpolation=cv2.INTER_LANCZOS4)
        bgr=cv2.addWeighted(bgr,1.4,cv2.GaussianBlur(bgr,(0,0),1.2),-.4,0)
        cv2.imwrite(f'{D}fondo/{n+j:04d}.jpg',bgr,[cv2.IMWRITE_JPEG_QUALITY,93])
        cv2.imwrite(f'{D}persona/{n+j:04d}.webp',np.dstack([bgr,cv2.GaussianBlur(al,(3,3),0)]),[cv2.IMWRITE_WEBP_QUALITY,92])
    print(s['f'],len(ims),flush=True)
