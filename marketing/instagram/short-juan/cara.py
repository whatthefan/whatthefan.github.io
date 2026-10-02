import cv2, json, numpy as np
import sys; src=sys.argv[1] if len(sys.argv)>1 else 'original.mov'; cap=cv2.VideoCapture(src); fps=cap.get(5); n=int(cap.get(7))
cas=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
xs=[];ts=[]
for f in range(0,n,6):
    cap.set(1,f); ok,im=cap.read()
    if not ok: break
    g=cv2.cvtColor(cv2.resize(im,(810,540)),cv2.COLOR_BGR2GRAY)
    fa=cas.detectMultiScale(g,1.15,5,minSize=(80,80))
    if len(fa):
        x,y,w,h=max(fa,key=lambda r:r[2]*r[3]); xs.append((x+w/2)*2); ts.append(f/fps)
print(len(xs), 'caras de', n//6, 'min/max', min(xs), max(xs), 'mediana', np.median(xs))
json.dump({'t':ts,'x':xs,'w':im.shape[1],'h':im.shape[0]},open(src.replace('.mov','')+'-cara.json' if src!='original.mov' else 'cara.json','w'))
