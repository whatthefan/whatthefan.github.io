"""Piezas comunes de los PDF de PLEA5E (la guia de resenas y el kit de venta):
fuentes, colores, estilos de pagina, Estrellita con bocadillo, estrellas, iconos y
el movil dibujado para ensenar los pasos."""
import base64
import math

b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
svg = lambda f: 'data:image/svg+xml;base64,' + b64(f)
jpg = lambda f: 'data:image/jpeg;base64,' + b64(f)
png = lambda f: 'data:image/png;base64,' + b64(f)
E = 'marketing/instagram/personaje/svg/'
LOGO = svg('public/marca/marca-plea5e.svg')
LOGO_CLARO = svg('public/marca/marca-plea5e-claro.svg')
QR = svg('public/qr/qr-plea5e-es-plano.svg')
FUENTE = lambda n, f, w='400': f"@font-face{{font-family:{n};font-weight:{w};src:url(data:font/woff2;base64,{b64('fuente/' + f)})}}"

# cada pose se mete una sola vez en el PDF: como clase de CSS con la imagen de fondo
_POSES = {}


def _pose(pose):
    if pose not in _POSES:
        _POSES[pose] = f'p{len(_POSES)}'
    return _POSES[pose]


def css_poses():
    return ''.join(f'.{c}{{background-image:url({svg(E + p + ".svg")})}}' for p, c in _POSES.items())


def estrella(tam, color='#E9BC46', borde=None):
    p = []
    for k in range(10):
        r = 10 if k % 2 == 0 else 4.2
        p.append(f'{10 + r * math.sin(math.pi * k / 5):.2f} {10 - r * math.cos(math.pi * k / 5):.2f}')
    b = f' stroke="{borde}" stroke-width="1.2" stroke-linejoin="round"' if borde else ''
    return f'<svg class="est" width="{tam}" height="{tam}" viewBox="-1 -1 22 22"><path d="M{"L".join(p)}Z" fill="{color}"{b}/></svg>'


CINCO = lambda tam, c='#E9BC46', borde=None: '<span class="cinco">' + ''.join(estrella(tam, c, borde) for _ in range(5)) + '</span>'


def bicho(pose, estilo, dice=None, lado='izq', bestilo=''):
    """Estrellita (en mm). dice: lo que dice, en un bocadillo a mano. lado: de que lado sale el pico."""
    c = _pose(pose)
    b = ''
    if dice:
        b = f'<div class="bocadillo pico-{lado}" style="{bestilo}">{dice}</div>'
    return f'<div class="bicho {c}" style="{estilo}"></div>{b}'


SI = '<svg viewBox="0 0 20 20" class="ico"><circle cx="10" cy="10" r="10" fill="#2F8F5B"/><path d="M5.5 10.5l3 3 6-7" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
NO = '<svg viewBox="0 0 20 20" class="ico"><circle cx="10" cy="10" r="10" fill="#C0392B"/><path d="M6.5 6.5l7 7M13.5 6.5l-7 7" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/></svg>'
CASILLA = '<span class="casilla"></span>'
G_LOGO = ('<svg viewBox="0 0 48 48" class="glogo"><path fill="#4285F4" d="M45.1 24.5c0-1.6-.1-2.8-.4-4.1H24v7.4h12.1c-.2 1.8-1.6 4.6-4.5 6.5l6.9 5.3c4.1-3.8 6.6-9.4 6.6-15.1z"/>'
          '<path fill="#34A853" d="M24 46c5.9 0 10.9-2 14.5-5.3l-6.9-5.3c-1.8 1.3-4.3 2.2-7.6 2.2-5.8 0-10.7-3.8-12.5-9.1l-7.1 5.5C8 41 15.4 46 24 46z"/>'
          '<path fill="#FBBC05" d="M11.5 28.5c-.5-1.4-.8-2.9-.8-4.5s.3-3.1.7-4.5l-7.1-5.5C2.8 17 2 20.4 2 24s.8 7 2.3 10z"/>'
          '<path fill="#EA4335" d="M24 10.2c4.1 0 6.9 1.8 8.5 3.3l6.2-6C34.9 4 29.9 2 24 2 15.4 2 8 7 4.3 14l7.1 5.5c1.8-5.3 6.8-9.3 12.6-9.3z"/></svg>')


def movil(dentro, estilo=''):
    """un movil dibujado (54 x 110 mm) con lo que se le pase en la pantalla"""
    return f'<div class="movil" style="{estilo}"><div class="movil-isla"></div><div class="movil-pant">{dentro}</div></div>'


def pantalla_resena(estrellas=0, texto='', boton=False, negocio='Tu negocio'):
    est = ''.join(estrella(22, '#FBBC04' if i < estrellas else '#DADCE0') for i in range(5))
    return (f'<div class="pr-cab">{G_LOGO}<div><b>{negocio}</b><small>Escribe una reseña</small></div></div>'
            f'<div class="pr-cuerpo"><div class="pr-q">¿Qué te ha parecido?</div><div class="pr-est">{est}</div>'
            f'<div class="pr-caja">{texto}<span class="pr-cursor"></span></div>'
            f'<div class="pr-btn{" on" if boton else ""}">Publicar</div></div>')


CSS_BASE = FUENTE('Anton', 'anton-latin.woff2') + FUENTE('Mont', 'montserrat-latin.woff2', '100 900') + FUENTE('Caveat', 'caveat-latin.woff2', '400 700') + '''
@page{size:A4;margin:0}
*{margin:0;padding:0;box-sizing:border-box}
:root{--noche:#06080E;--noche2:#10141F;--oro:#E9BC46;--oro-os:#A47A12;--crema:#FBF7EE;--crema2:#F3EBDB;--tinta:#161A24;--gris:#5A5F6B;--linea:#E3D8C2;
  --verde:#2F8F5B;--verde-cl:#D5EBDD;--rojo:#C0392B;--rojo-cl:#F2D6D2}
html,body{background:#888}
body{font-family:Mont;color:var(--tinta);font-size:10.5pt;line-height:1.5}
.pag{width:210mm;height:297mm;position:relative;overflow:hidden;background:var(--crema);page-break-after:always;padding:25mm 18mm 20mm}
.pag:last-child{page-break-after:auto}
.pag::before{content:"";position:absolute;inset:0;pointer-events:none;opacity:.35;mix-blend-mode:multiply;
  background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='260' height='260'><filter id='r'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .55  0 0 0 0 .5  0 0 0 0 .42  0 0 0 .22 0'/></filter><rect width='260' height='260' filter='url(%23r)'/></svg>")}
.oscura{background:radial-gradient(ellipse 90% 60% at 70% 20%,#1A2136 0%,#0B0F1A 55%,var(--noche) 100%);color:#fff}
.oscura::before{mix-blend-mode:overlay;opacity:.5}
.cab{position:absolute;top:9mm;left:18mm;right:18mm;display:flex;align-items:center;gap:4mm;font-size:7.5pt;letter-spacing:.18em;text-transform:uppercase;color:var(--gris);font-weight:600}
.cab-logo{height:4.2mm}
.cab::after{content:"";flex:1;height:.3mm;background:var(--linea)}
.pie{position:absolute;bottom:9mm;left:18mm;right:18mm;display:flex;align-items:baseline;gap:1.5mm;font-size:7.5pt;color:var(--gris)}
.pie span{flex:1}
.pie b{font-family:Anton;font-size:12pt;color:var(--oro-os);font-weight:400}
.etq{display:inline-block;font-weight:800;font-size:8pt;letter-spacing:.22em;text-transform:uppercase;color:var(--oro-os);margin-bottom:3mm}
.etq::before{content:"";display:inline-block;width:9mm;height:.5mm;background:currentColor;vertical-align:middle;margin-right:3mm}
h1,h2,h3{font-family:Anton;font-weight:400;text-transform:uppercase;line-height:1.12;letter-spacing:.005em}
h2{font-size:33pt;margin-bottom:5mm}
h2 em{font-style:normal;color:var(--oro-os)}
h3{font-size:13.5pt;margin-bottom:1.5mm}
.intro{font-size:11.5pt;color:#383D49;max-width:150mm;margin-bottom:8mm}
.intro b{color:var(--tinta)}
.mano{font-family:Caveat;font-weight:700}
.bicho{position:absolute;background-size:contain;background-repeat:no-repeat;background-position:center bottom;filter:drop-shadow(0 2.5mm 2.5mm rgba(0,0,0,.2))}
.bocadillo{position:absolute;background:#fff;border:.6mm solid var(--tinta);border-radius:6mm;padding:2.5mm 4.5mm;font-family:Caveat;font-weight:700;font-size:15pt;line-height:1.1;color:var(--tinta);box-shadow:1.2mm 1.4mm 0 var(--tinta);z-index:2}
.bocadillo::after{content:"";position:absolute;width:5mm;height:5mm;background:#fff;border:.6mm solid var(--tinta);border-top:0;border-left:0;bottom:-3.1mm;transform:rotate(45deg)}
.pico-izq::after{left:7mm}.pico-der::after{right:7mm}
.est{display:inline-block;vertical-align:middle}
.cinco{display:inline-flex;gap:1mm}
.ico{width:5.5mm;height:5.5mm;flex:none;margin-top:.3mm}
.casilla{display:inline-block;width:4.4mm;height:4.4mm;border:.45mm solid var(--oro-os);border-radius:1mm;flex:none;margin-top:.7mm;background:#fff}
.caja{background:#fff;border:.3mm solid var(--linea);border-radius:3mm;padding:6mm;box-shadow:0 1mm 0 var(--linea)}
.caja-os{background:var(--noche);color:#fff;border-radius:3mm;padding:6mm 7mm}
.caja-os h3{color:var(--oro)}
.caja-os p,.caja-os li{color:#D5DAE5}
.num{font-family:Anton;color:var(--oro-os);font-size:40pt;line-height:.9}
.fila{display:grid;gap:5mm}
.lista{list-style:none;display:flex;flex-direction:column;gap:3mm}
.lista li{display:flex;gap:3mm;align-items:flex-start}
.linea-rell{border-bottom:.35mm dashed #B9AE98;height:9mm}
.cita{font-family:Caveat;font-weight:700;font-size:16pt;line-height:1.15;color:var(--tinta)}
.cita::before{content:"«";color:var(--oro-os)}.cita::after{content:"»";color:var(--oro-os)}
.chip{display:inline-block;font-weight:800;font-size:7.5pt;letter-spacing:.16em;text-transform:uppercase;background:var(--oro);color:var(--noche);padding:1mm 2.5mm;border-radius:1mm;margin-bottom:2mm}
.chip.verde{background:var(--verde-cl);color:#1F6B42}.chip.rojo{background:var(--rojo-cl);color:#8A2A1E}.chip.gris{background:var(--crema2);color:var(--gris)}
.foto{border-radius:3mm;overflow:hidden;box-shadow:0 2mm 5mm rgba(0,0,0,.18)}
.foto img{display:block;width:100%;height:100%;object-fit:cover}
.nota{font-size:8.8pt;color:var(--gris)}
table{border-collapse:collapse;width:100%;font-size:9.5pt}
td,th{border:.3mm solid var(--linea);padding:2.6mm 3mm;text-align:left;background:#fff;vertical-align:top}
th{background:var(--crema2);font-weight:800;font-size:7.8pt;letter-spacing:.08em;text-transform:uppercase}
.paso-n{display:inline-grid;place-items:center;width:9mm;height:9mm;border-radius:50%;background:var(--noche);color:var(--oro);font-family:Anton;font-size:13pt;flex:none}
/* el movil */
.movil{position:absolute;width:54mm;height:110mm;border-radius:8mm;background:#111;padding:2.2mm;box-shadow:0 4mm 10mm rgba(0,0,0,.28),inset 0 0 0 .5mm #333}
.movil-isla{position:absolute;top:3.6mm;left:50%;transform:translateX(-50%);width:15mm;height:3.6mm;border-radius:2mm;background:#000;z-index:2}
.movil-pant{width:100%;height:100%;border-radius:6.2mm;background:#fff;overflow:hidden;position:relative;font-size:7.6pt;color:#202124}
.pr-cab{display:flex;gap:2.5mm;align-items:center;padding:10mm 4mm 3mm;border-bottom:.3mm solid #e8eaed}
.glogo{width:7mm;height:7mm;flex:none}
.pr-cab b{display:block;font-size:8.6pt}.pr-cab small{color:#5f6368;font-size:7pt}
.pr-cuerpo{padding:5mm 4mm;text-align:center}
.pr-q{font-weight:700;font-size:9pt;margin-bottom:3mm}
.pr-est{display:flex;justify-content:center;gap:1mm;margin-bottom:4mm}
.pr-caja{border:.3mm solid #dadce0;border-radius:2mm;min-height:24mm;text-align:left;padding:2.5mm;font-size:7.6pt;line-height:1.35}
.pr-cursor{display:inline-block;width:.3mm;height:3mm;background:#1a73e8;vertical-align:middle;margin-left:.3mm}
.pr-btn{margin:4mm auto 0;width:22mm;padding:1.8mm 0;border-radius:4mm;background:#e8eaed;color:#9aa0a6;font-weight:700;font-size:7.6pt}
.pr-btn.on{background:#1a73e8;color:#fff}
'''


def html(titulo, css_extra, paginas):
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{titulo}</title>'
            f'<style>{CSS_BASE}{css_poses()}{css_extra}</style></head><body>{"".join(paginas)}</body></html>')
