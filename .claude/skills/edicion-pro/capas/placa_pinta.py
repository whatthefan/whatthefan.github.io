import cv2,numpy as np,json,os
q={int(k):np.array(v) for k,v in json.load(open('placa_quad.json')).items()}
ks=sorted(q)
for a,b in zip(ks,ks[1:]):
    if 1<b-a<=6:
        for k in range(a+1,b): q[k]=q[a]+(q[b]-q[a])*(k-a)/(b-a)
dis=cv2.imread('capa/w-placa.png',cv2.IMREAD_UNCHANGED); S=dis.shape[0]
D=dis[:,:,:3].astype(np.float32); DA=dis[:,:,3].astype(np.float32)/255
src=np.float32([[0,0],[S,0],[S,S],[0,S]])
os.makedirs('capa/cu2',exist_ok=True)
for k in range(1,918):
    f='capa/cu/%04d.jpg'%k; im=cv2.imread(f)
    if k in q:
        Hm=cv2.getPerspectiveTransform(src,np.float32(q[k]))
        wd=cv2.warpPerspective(D,Hm,(960,1080),flags=cv2.INTER_LINEAR)
        wa=cv2.warpPerspective(DA,Hm,(960,1080),flags=cv2.INTER_LINEAR)
        hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV).astype(np.float32)
        piel=((hsv[:,:,0]<30)|(hsv[:,:,0]>165))&(hsv[:,:,1]>40)
        m=(~piel).astype(np.float32); m=cv2.GaussianBlur(cv2.erode(m,np.ones((3,3))),(0,0),1.5)
        a=(wa*m)[:,:,None]
        luz=cv2.GaussianBlur(hsv[:,:,2],(0,0),12)/225.0; luz=np.clip(luz,.55,1.1)[:,:,None]
        out=im.astype(np.float32)*(1-a)+wd*luz*a
        im=np.clip(out,0,255).astype(np.uint8)
    cv2.imwrite('capa/cu2/%04d.jpg'%k,im,[cv2.IMWRITE_JPEG_QUALITY,93])
print('ok',len(q))
