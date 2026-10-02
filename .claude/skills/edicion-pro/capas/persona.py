import cv2,numpy as np,sys,os,subprocess
src,mate,out=sys.argv[1:4]; os.makedirs(out,exist_ok=True)
F='/tmp/claude-0/bin/ffmpeg'
p=subprocess.Popen([F,'-loglevel','error','-i',mate,'-f','rawvideo','-pix_fmt','gray','-'],stdout=subprocess.PIPE)
i=1
while True:
    b=p.stdout.read(960*1080)
    if len(b)<960*1080: break
    a=np.frombuffer(b,np.uint8).reshape(1080,960)
    im=cv2.imread(f'{src}/{i:04d}.jpg')
    if im is None: break
    a=cv2.GaussianBlur(a,(3,3),0)
    cv2.imwrite(f'{out}/{i:04d}.webp',np.dstack([im,a]),[cv2.IMWRITE_WEBP_QUALITY,92]); i+=1
print(i-1)
