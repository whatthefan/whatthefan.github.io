"""mezcla4.py vídeo.mov voz.wav salida.mp4 pagina.html — los SFX salen de la lista FX de la página (cada sonido va con su efecto visual)."""
import sys,json,re,subprocess
h=open(sys.argv[4]).read(); fx=json.loads(re.search(r'/\*FX\*/(.*?)/\*FX\*/',h,re.S).group(1))
L=[[f['t'],f['s'],f['db']]+([f['dur']] if 'dur' in f else []) for f in fx if f.get('s')]
json.dump(L,open('/tmp/sfx-auto.json','w'))
subprocess.run(['python3','/tmp/claude-0/v3/mezcla2.py',sys.argv[1],sys.argv[2],sys.argv[3],'/tmp/sfx-auto.json'],check=True)
