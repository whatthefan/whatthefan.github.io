import subprocess,json,os
F='/tmp/claude-0/bin/ffmpeg'; C='/tmp/claude-0/ego/crudos/'; O='/tmp/claude-0/ego/capa/cara/fondo/'
SEG=[('v1952.mov',.95,8.3,'L'),('v1954.mov',.75,11.2,'L'),('v1957.mov',.3,5.4,'-'),('v2005.mov',.55,14.2,'L'),('IMG_3068.MOV',.1,6.6,'V')]
TM='zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,'
t=0; info=[]; auds=[]
for i,(f,a,b,m) in enumerate(SEG):
    n0=round(t*30)+1; d=b-a
    if m=='L': vf='fps=30,hflip,crop=960:1080:(iw-960)/2:0'
    elif m=='V': vf=TM+'fps=30,hflip,scale=1080:1920'
    if m!='-':
        subprocess.run([F,'-v','error','-y','-ss',str(a),'-i',C+f,'-t',str(d),'-vf',vf,'-q:v','2','-start_number',str(n0),O+'%04d.jpg'],check=True)
    subprocess.run([F,'-v','error','-y','-ss',str(a),'-i',C+f,'-t',str(d),'-vn','-ac','1','-ar','48000',f'/tmp/claude-0/ego/a{i}.wav'],check=True)
    auds.append(f'/tmp/claude-0/ego/a{i}.wav'); info.append({'f':f,'t0':round(t,3),'t1':round(t+d,3),'m':m,'n0':n0}); t+=d
open('/tmp/claude-0/ego/lista.txt','w').write(''.join(f"file '{x}'\n" for x in auds))
subprocess.run([F,'-v','error','-y','-f','concat','-safe','0','-i','/tmp/claude-0/ego/lista.txt','-c','copy','/tmp/claude-0/ego/voz-cruda.wav'],check=True)
ch=open('/home/user/whatthefan.github.io/.claude/skills/motion-reels/scripts/cadena-voz.txt').read().strip().replace('m=std.rnnn','m=/tmp/claude-0/v3/std.rnnn')
subprocess.run([F,'-v','error','-y','-i','/tmp/claude-0/ego/voz-cruda.wav','-af',ch,'-ar','48000','/tmp/claude-0/ego/voz.wav'],check=True)
json.dump(info,open('/tmp/claude-0/ego/segs.json','w'),indent=1); print(info, 'TOTAL', round(t,3))
