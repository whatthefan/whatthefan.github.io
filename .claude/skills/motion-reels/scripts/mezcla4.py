"""mezcla4.py vídeo.mov voz.wav salida.mp4 pagina.html — los SFX salen de la lista FX de la página (cada sonido va con su efecto visual).
Si la lista está escrita en el archivo (/*FX*/[...]/*FX*/) la lee; si se rellena con fx(...) al cargar, la saca con fx-de-pagina.js."""
import sys,json,re,subprocess,os
D=os.path.dirname(os.path.abspath(__file__))
h=open(sys.argv[4]).read(); m=re.search(r'/\*FX\*/(.*?)/\*FX\*/',h,re.S); fx=json.loads(m.group(1)) if m else []
if not fx: fx=json.loads(subprocess.run(['node',os.path.join(D,'fx-de-pagina.js'),sys.argv[4]],capture_output=True,text=True,check=True).stdout.strip().splitlines()[-1])
L=[[f['t'],f['s'],f['db']]+([f['dur']] if 'dur' in f else []) for f in fx if f.get('s')]
print(len(L),'sonidos'); json.dump(L,open('/tmp/sfx-auto.json','w'))
subprocess.run(['python3',os.path.join(D,'mezcla2.py'),sys.argv[1],sys.argv[2],sys.argv[3],'/tmp/sfx-auto.json'],check=True)
