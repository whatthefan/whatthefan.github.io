import onnxruntime as ort,numpy as np,cv2,sys
s=ort.InferenceSession('/tmp/claude-0/modelos/isnet-general-use.onnx',providers=['CPUExecutionProvider'])
for src,dst in zip(sys.argv[1::2],sys.argv[2::2]):
    im=cv2.imread(src); h,w=im.shape[:2]
    x=cv2.resize(cv2.cvtColor(im,cv2.COLOR_BGR2RGB),(1024,1024)).astype(np.float32)/255
    x=(x-np.array([.485,.456,.406]))/np.array([1.,1.,1.]); x=x.transpose(2,0,1)[None].astype(np.float32)
    o=s.run(None,{s.get_inputs()[0].name:x})[0][0,0]; o=(o-o.min())/(o.max()-o.min())
    a=cv2.resize(o,(w,h)); a=(np.clip((a-.15)/.7,0,1)*255).astype(np.uint8)
    ys,xs=np.where(a>20); y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max()
    out=np.dstack([im,a])[y0:y1+1,x0:x1+1]
    sc=min(1,1100/max(out.shape[:2])); out=cv2.resize(out,None,fx=sc,fy=sc,interpolation=cv2.INTER_AREA)
    cv2.imwrite(dst,out); print(dst,out.shape)
