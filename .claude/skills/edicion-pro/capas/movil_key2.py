import cv2,numpy as np
cap=cv2.VideoCapture('/tmp/claude-0/broll/hd-28300.mp4')
A=cv2.imread('pan/pantalla-0.png'); B=cv2.imread('pan/pantalla-1.3.png')
CX=[136,263,390,516,643]; CY=488; R=58
def backout(u): c=1.9; u=u-1; return 1+(c+1)*u**3+c*u**2
def pantalla(i):
    img=A.copy()
    for j,cx in enumerate(CX):
        u=(i-24-j*3.2)/7.0
        if u<=0: continue
        s=backout(min(u,1)); al=min(1,u*2.5)
        pb=B[CY-R:CY+R,cx-R:cx+R].astype(np.float32); pa=A[CY-R:CY+R,cx-R:cx+R].astype(np.float32)
        m=(np.abs(pb-pa).sum(2)>40).astype(np.float32); m=cv2.GaussianBlur(m,(3,3),0)
        M=cv2.getRotationMatrix2D((R,R),(1-min(u,1))*-25,s)
        pw=cv2.warpAffine(pb,M,(2*R,2*R),borderValue=(255,255,255)); mw=cv2.warpAffine(m,M,(2*R,2*R))[:,:,None]*al
        roi=img[CY-R:CY+R,cx-R:cx+R].astype(np.float32); img[CY-R:CY+R,cx-R:cx+R]=(roi*(1-mw)+pw*mw).astype(np.uint8)
    return img
cap.set(cv2.CAP_PROP_POS_MSEC,2500)
for i in range(1,76):
    ok,f=cap.read()
    if not ok: break
    h,w=f.shape[:2]; hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
    g=((hsv[:,:,0]>35)&(hsv[:,:,0]<85)&(hsv[:,:,1]>90)&(hsv[:,:,2]>70)).astype(np.uint8)
    n,l,st,_=cv2.connectedComponentsWithStats(g)
    borde=set(np.unique(np.concatenate([l[0],l[-1],l[:,0],l[:,-1]])))-{0}
    inter=[k for k in range(1,n) if k not in borde and st[k,4]>2000]
    out=np.dstack([f,np.full((h,w),255,np.uint8)])
    if inter:
        k=max(inter,key=lambda k:st[k,4]); m=(l==k).astype(np.uint8)
        cs,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE); c=max(cs,key=cv2.contourArea)
        q=cv2.boxPoints(cv2.minAreaRect(c)); q=q[np.argsort(q[:,1])]; top=q[:2][np.argsort(q[:2,0])]; bot=q[2:][np.argsort(q[2:,0])[::-1]]
        dst=np.float32([top[0],top[1],bot[0],bot[1]])
        img=pantalla(i); H=cv2.getPerspectiveTransform(np.float32([[0,0],[img.shape[1],0],[img.shape[1],img.shape[0]],[0,img.shape[0]]]),dst)
        wp=cv2.warpPerspective(img,H,(w,h)); mm=np.zeros((h,w),np.uint8); cv2.fillConvexPoly(mm,dst.astype(np.int32),1); mm=cv2.dilate(mm,np.ones((3,3)))[:,:,None]
        out[:,:,:3]=np.where(mm>0,wp,out[:,:,:3])
    bg=np.zeros((h,w),np.uint8)
    for k in borde: bg|=(l==k).astype(np.uint8)
    out[:,:,3]=((1-cv2.GaussianBlur(bg.astype(np.float32),(0,0),1.5))*255).astype(np.uint8)
    sp=out[:,:,:3].astype(np.int16); sp[:,:,1]=np.minimum(sp[:,:,1],np.maximum(sp[:,:,0],sp[:,:,2])+10); out[:,:,:3]=sp.astype(np.uint8)
    cv2.imwrite('br/movil/%04d.webp'%i,cv2.resize(out,(1440,810)),[cv2.IMWRITE_WEBP_QUALITY,90])
