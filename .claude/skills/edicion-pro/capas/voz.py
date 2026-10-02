"""voz.py src segs.json fin salida.wav — misma selección de tramos que base.py, audio SIN procesar (48 kHz)."""
import json,sys,subprocess
F='/tmp/claude-0/bin/ffmpeg'
src,segs,fin,out=sys.argv[1],json.load(open(sys.argv[2])),float(sys.argv[3]),sys.argv[4]
keep=[]
for s in segs:
    a=max(0,s['a']-0.1); b=min(fin,s['b']+0.25)
    if keep and a-keep[-1][1]<0.25: keep[-1][1]=b
    else: keep.append([a,b])
fl=[f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={b-a-0.04}:d=0.04[a{k}]" for k,(a,b) in enumerate(keep)]
fl.append(''.join(f'[a{k}]' for k in range(len(keep)))+f'concat=n={len(keep)}:v=0:a=1,aresample=48000[a]')
subprocess.run([F,'-loglevel','error','-y','-i',src,'-filter_complex',';'.join(fl),'-map','[a]','-ac','1','-c:a','pcm_s16le',out],check=True)
