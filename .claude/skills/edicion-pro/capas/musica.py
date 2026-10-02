"""musica.py entrada.mp4 musica.mp3 salida.mp4 [inicio_musica] [dB] — añade música de fondo que baja sola cuando hablas (sidechain)."""
import subprocess,sys
F='/tmp/claude-0/bin/ffmpeg'
e,m,o=sys.argv[1:4]; ini=float(sys.argv[4]) if len(sys.argv)>4 else 0; db=float(sys.argv[5]) if len(sys.argv)>5 else -20
fl=(f"[1:a]atrim={ini},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume={db}dB,afade=t=in:d=0.6[m];"
    "[0:a]asplit[v][k];[m][k]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=400[md];"
    "[v][md]amix=inputs=2:normalize=0:duration=first,afade=t=out:st=%s:d=0.8,alimiter=limit=0.93[a]")
dur=float(subprocess.run([F,'-i',e],capture_output=True,text=True).stderr.split('Duration: ')[1].split(',')[0].split(':')[-1])
subprocess.run([F,'-loglevel','error','-y','-i',e,'-i',m,'-filter_complex',fl%(dur-.8),'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',o],check=True)
