import base64,re,json
ico=open('public/icono.svg').read()
STAR=re.search(r'<path fill="#E9BC46" d="([^"]+)"',ico).group(1)
FIVE=re.search(r'<path fill="#0A0E16" transform="[^"]+" d="([^"]+)"',ico).group(1)
NOCHE,ORO,BLANCO='#06080E','#E9BC46','#FFFFFF'
CE,CA=0.42,316; CT=f'translate({512-249.5*CE:.1f} {CA+860*CE:.1f}) scale({CE})'
ANCHO={'P':967,'L':814,'E':843,'A':994}; AM=1760/2048
D='font-family:Anton'
def tr(c,w): return f'<path d="{STAR}" fill="{c}" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"/>'
def sello(cx,cy,esc,contorno=True,cinco=NOCHE,estrella=ORO):
    b=(tr(ORO,110)+tr(NOCHE,74)) if contorno else ''
    return f'<g transform="translate({cx:.1f} {cy:.1f}) scale({esc:.4f}) translate(-512 -470)">{b}<path fill="{estrella}" d="{STAR}"/><path fill="{cinco}" transform="{CT}" d="{FIVE}"/></g>'
def minis(cx,y,tam,paso): return ''.join(sello(cx+(i-2)*paso,y,tam/1000,False,ORO,ORO) for i in range(5))
def plea_estrella(cx,y,tam,letra,esp=.03,crece=1.5):
    k,gap=tam/2048,tam*esp; plea=sum(ANCHO[c] for c in 'PLEA')*k+3*gap; e=ANCHO['E']*k
    esc=AM*tam*crece/815; ae=902*esc*1.08; tot=plea+gap+ae+gap+e; x0=cx-tot/2
    t=f'style="{D};font-size:{tam}px;letter-spacing:{gap:.1f}px" fill="{letra}"'
    return f'<text x="{x0:.1f}" y="{y}" {t}>PLEA</text><text x="{x0+tot-e:.1f}" y="{y}" {t}>E</text>'+sello(x0+plea+gap+ae/2,y-AM*tam/2-tam*.03,esc)
def nombre(cx,y,tam,letra,ls=4): return f'<text x="{cx}" y="{y}" text-anchor="middle" style="{D};font-size:{tam}px;letter-spacing:{ls}px" fill="{letra}">PLEA5E</text>'
# (nombre, ancho, alto, cuerpo(letra))
P={
 'logo':            (1080,1080,lambda L: sello(540,403.4,.478)+nombre(540,794,169,L)+minis(540,870.5,71.2,80)),
 'logo-horizontal': (1400,560, lambda L: plea_estrella(700,340,230,L)+minis(700,470,50,92)),
 'nombre':          (1080,420, lambda L: nombre(540,250,200,L,5)+minis(540,340,60,90)),
 'estrella-5':      (1080,1080,lambda L: sello(540,560,.98)),
}
b64=base64.b64encode(open('fuente/anton-latin.woff2','rb').read()).decode()
out=[]
for n,(w,h,f) in P.items():
    vars_=[('fondo-negro',BLANCO,True),('transparente',BLANCO,False)]
    if n!='estrella-5': vars_.append(('transparente-fondo-claro',NOCHE,False))
    for v,L,fondo in vars_:
        bg=f'<rect width="{w}" height="{h}" fill="{NOCHE}"/>' if fondo else ''
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w*2}" height="{h*2}">{bg}{f(L)}</svg>'
        out.append((f'PLEA5E-{n}-{v}',w*2,h*2,f'<html><head><meta charset="utf-8"><style>@font-face{{font-family:Anton;src:url(data:font/woff2;base64,{b64})}}body{{margin:0;background:transparent}}</style></head><body>{svg}</body></html>'))
json.dump(out,open('/tmp/logotipos-paginas.json','w'))
print(len(out))
