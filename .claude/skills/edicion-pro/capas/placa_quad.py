import cv2,numpy as np,json
H,W=1080,960; B=12
def mascara(im):
    h=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
    m=((h[:,:,0]>=88)&(h[:,:,0]<=125)&(h[:,:,1]>=15)&(h[:,:,1]<=95)&(h[:,:,2]>=125)).astype(np.uint8)*255
    return cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
def blob(m):
    n,l,st,_=cv2.connectedComponentsWithStats(m)
    if n<2: return None
    k=1+np.argmax(st[1:,4])
    return (l==k).astype(np.uint8)*255 if st[k,4]>=15000 else None
enb=lambda p:p[0]<B or p[1]<B or p[0]>W-1-B or p[1]>H-1-B
def lados(b):
    cs,_=cv2.findContours(b,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); c=max(cs,key=cv2.contourArea)
    hull=cv2.convexHull(c).astype(np.float32)
    ap=cv2.approxPolyDP(hull,0.012*cv2.arcLength(hull,True),True).reshape(-1,2).astype(float)
    cx,cy=ap.mean(0); L={}
    for k in range(len(ap)):
        p,q=ap[k],ap[(k+1)%len(ap)]; n=np.linalg.norm(q-p)
        if n<60 or (enb(p) and enb(q)): continue
        d=(q-p)/n; ang=np.degrees(np.arctan2(d[1],d[0]))%180; m=(p+q)/2
        if ang<35 or ang>145: key='t' if m[1]<cy else 'b'; d=d if d[0]>0 else -d
        elif 55<ang<125: key='l' if m[0]<cx else 'r'; d=d if d[1]>0 else -d
        else: continue
        if key not in L or n>L[key][2]: L[key]=(p,d,n)
    return L
def cruza(a,b):
    (p,d),(q,e)=a[:2],b[:2]; A=np.array([d,-e]).T
    t=np.linalg.solve(A,q-p); return p+d*t[0]
res={}; sw=None
for i in range(829,918):
    im=cv2.imread('capa/cu/%04d.jpg'%i); b=blob(mascara(im))
    if b is None: continue
    L=lados(b); k=set(L)
    try:
        if k>={'t','b','l','r'}: Q=[cruza(L['t'],L['l']),cruza(L['t'],L['r']),cruza(L['b'],L['r']),cruza(L['b'],L['l'])]
        elif k>={'t','l','r'}:
            TL,TR=cruza(L['t'],L['l']),cruza(L['t'],L['r']); w=np.linalg.norm(TR-TL); sw=w; Q=[TL,TR,TR+L['r'][1]*w,TL+L['l'][1]*w]
        elif k>={'b','l','r'}:
            BL,BR=cruza(L['b'],L['l']),cruza(L['b'],L['r']); w=np.linalg.norm(BR-BL); Q=[BL-L['l'][1]*w,BR-L['r'][1]*w,BR,BL]
        elif k>={'t','b','l'}:
            TL,BL=cruza(L['t'],L['l']),cruza(L['b'],L['l']); h=np.linalg.norm(BL-TL); Q=[TL,TL+L['t'][1]*h,BL+L['b'][1]*h,BL]
        elif k>={'t','b','r'}:
            TR,BR=cruza(L['t'],L['r']),cruza(L['b'],L['r']); h=np.linalg.norm(BR-TR); Q=[TR-L['t'][1]*h,TR,BR,BR-L['b'][1]*h]
        elif k>={'t','l'} and sw:
            TL=cruza(L['t'],L['l']); ww=max(sw,L['t'][2]); Q=[TL,TL+L['t'][1]*ww,TL+L['t'][1]*ww+L['l'][1]*ww,TL+L['l'][1]*ww]
        elif k>={'t','r'} and sw:
            TR=cruza(L['t'],L['r']); Q=[TR-L['t'][1]*sw,TR,TR+L['r'][1]*sw,TR-L['t'][1]*sw+L['r'][1]*sw]
        else: continue
    except np.linalg.LinAlgError: continue
    Q=np.array(Q); w=np.linalg.norm(Q[1]-Q[0]); h=np.linalg.norm(Q[3]-Q[0])
    if not (0.6<w/h<1.6) or not cv2.isContourConvex(Q.astype(np.float32)): continue
    res[i]=Q
# filtra saltos y suaviza
ks=sorted(res); A=np.array([cv2.contourArea(res[k].astype(np.float32)) for k in ks])
ok={k:res[k] for j,k in enumerate(ks) if not (0<j<len(ks)-1 and (A[j]>1.5*max(A[j-1],A[j+1]) or A[j]<0.6*min(A[j-1],A[j+1])))}
fin={}
for k in range(829,918):
    vec=[ok[j] for j in (k-1,k,k+1) if j in ok]
    if k in ok: fin[k]=np.mean(vec,0).tolist()
    elif (k-1) in ok and (k+1) in ok: fin[k]=((ok[k-1]+ok[k+1])/2).tolist()
json.dump(fin,open('placa_quad.json','w')); print(len(fin),sorted(fin))
