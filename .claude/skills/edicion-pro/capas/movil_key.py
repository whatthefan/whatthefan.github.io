import cv2,numpy as np
cap=cv2.VideoCapture('/tmp/claude-0/broll/hd-28300.mp4')
PS=['0','0.5','0.7','0.9','1.1']; pan=[cv2.imread(f'pan/pantalla-{s}.png') for s in PS]
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
        img=pan[min(4,max(0,(i-25)//8))]; H=cv2.getPerspectiveTransform(np.float32([[0,0],[img.shape[1],0],[img.shape[1],img.shape[0]],[0,img.shape[0]]]),dst)
        wp=cv2.warpPerspective(img,H,(w,h)); mm=np.zeros((h,w),np.uint8); cv2.fillConvexPoly(mm,dst.astype(np.int32),1); mm=cv2.dilate(mm,np.ones((3,3)))[:,:,None]
        out[:,:,:3]=np.where(mm>0,wp,out[:,:,:3])
    bg=np.zeros((h,w),np.uint8)
    for k in borde: bg|=(l==k).astype(np.uint8)
    out[:,:,3]=((1-cv2.GaussianBlur(bg.astype(np.float32),(0,0),1.5))*255).astype(np.uint8)
    sp=out[:,:,:3].astype(np.int16); sp[:,:,1]=np.minimum(sp[:,:,1],np.maximum(sp[:,:,0],sp[:,:,2])+10); out[:,:,:3]=sp.astype(np.uint8)
    cv2.imwrite('br/movil/%04d.webp'%i,cv2.resize(out,(1440,810)),[cv2.IMWRITE_WEBP_QUALITY,90])
