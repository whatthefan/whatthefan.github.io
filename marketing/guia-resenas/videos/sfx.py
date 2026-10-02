"""sfx.py vN -> sfx-vN.json para mezcla2 (un sonido por suceso; ninguno repetido salvo las teclas)."""
import json,re,sys
v=sys.argv[1]
V=json.load(open('videos.json'))[v]
TRANS=['packs2/whoosh-b.mp3','packs2/swoosh-a.mp3','packs3/swoosh-suave.mp3','packs2/swish-c.mp3','packs3/swoosh-aire.mp3','packs/arrow-swoosh.mp3','packs3/obturador-swoosh.mp3','packs3/swoosh-corto.mp3']
ALT={'dato':['packs4/toque-bot.mp3','packs4/toque-bot2.mp3','packs2/pop-imagen.mp3'],'si':['packs4/tarea-hecha.mp3','packs4/subida-ok.mp3'],'no':['packs/wrong.mp3','packs4/mareo.mp3'],
     'pasos':['packs3/clic-triple.mp3','packs3/clic-doble.mp3'],'cierre':['packs/ding.mp3']}
usados=set(); fx=[]
def uno(lst):
    for s in lst:
        if s not in usados: usados.add(s); return s
def add(t,s,db,dur=None):
    if s: fx.append([round(t,2),s,db]+([dur] if dur else []))
t0=0; ti=0
for i,e in enumerate(V['escenas']):
    tp=e['tipo']
    if i==0: add(.08,uno(['packs4/notch-abre.mp3']),-6); add(.85,uno(['packs4/bot-saluda.mp3']),-7)
    elif tp!='cierre' and not (tp=='movil' and V['escenas'][i-1]['tipo']=='movil'): add(t0+.06,uno(TRANS[ti:]+TRANS),-8); ti+=1
    if tp=='movil':
        p=e['pant']
        if p=='nfc': add(t0+1.2,uno(['packs/iphone-charging.mp3']),-6)
        if p=='qr': add(t0+1.6,uno(['packs/camera-click.mp3']),-7)
        if p=='ficha': add(t0+.25,uno(['packs4/notch-clic.mp3']),-7)
        if p=='estrellas': add(t0+.9,'packs2/contador.mp3',-11,1.25)
        if p=='publicar': add(t0+.6,'packs2/teclas.mp3',-12,1.9); add(t0+2.95,uno(['packs3/tap.mp3']),-5); add(t0+3.5,uno(['packs4/subida-ok.mp3','packs4/tarea-hecha.mp3']),-6)
    if tp=='lista': add(t0+.65,uno(ALT['si'] if e.get('si') else ALT['no']),-8)
    if tp=='pasos': add(t0+.5,uno(ALT['pasos']),-9)
    if tp=='frases':
        n=len(e['items']); paso=(e['d']-1.2)/n
        for k,it in enumerate(e['items']): add(t0+.5+k*paso+.2,'packs2/teclas.mp3',-12,round(min(len(it['txt'])/34,paso-.2),2))
    if tp=='dato': add(t0+.55,uno(ALT['dato']),-6)
    if tp=='cierre': add(t0+.1,uno(ALT['cierre']),-7)
    t0+=e['d']
json.dump(fx,open(f'sfx-{v}.json','w')); print(v,round(t0,1),'s',len(fx),'sonidos')
