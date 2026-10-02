import subprocess,sys,json
F='/tmp/claude-0/bin/ffmpeg'; S='/home/user/whatthefan.github.io/marketing/instagram/sonidos/'
base,capa,out,sfx=sys.argv[1],sys.argv[2],sys.argv[3],json.loads(open(sys.argv[4]).read())
ins=['-i',base,'-i',capa]; fl=[]; lab=[]
for i,(t,f,v) in enumerate(sfx):
    ins+=['-i',S+f]; n=i+2
    fl.append(f'[{n}:a]aresample=48000,aformat=channel_layouts=stereo,volume={v},adelay={int(t*1000)}|{int(t*1000)}[s{i}]'); lab.append(f'[s{i}]')
fl.append('[0:a]aresample=48000,aformat=channel_layouts=stereo[vz]')
fl.append('[vz]'+''.join(lab)+f'amix=inputs={len(lab)+1}:normalize=0:duration=first,alimiter=limit=0.9[a]')
fl.append('[0:v][1:v]overlay=format=auto,format=yuv420p[v]')
subprocess.run([F,'-loglevel','error','-y',*ins,'-filter_complex',';'.join(fl),'-map','[v]','-map','[a]','-c:v','libx264','-crf','20','-preset','medium','-profile:v','high','-c:a','aac','-b:a','192k','-movflags','+faststart',out],check=True)
