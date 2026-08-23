# -*- coding: utf-8 -*-
"""Monta el generador en un solo archivo.

Mete dentro la librería de QR y el logotipo de PLEA5E, para que el archivo
funcione sin pedirle nada a ningún servidor: se puede abrir con doble clic
desde el escritorio, sin internet (salvo la tipografía, que si no carga se
sustituye por la del sistema).
"""
import io, json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SALIDA = os.path.join(RAIZ, 'zip', 'taller', 'generador.html')

h = io.open(os.path.join(AQUI, 'plantilla.html'), encoding='utf-8').read()

# ── la librería de QR (MIT, de Kazuhiko Arase) ──
qr = io.open(os.path.join(RAIZ, 'node_modules', 'qrcode-generator', 'dist', 'qrcode.js'),
             encoding='utf-8').read()
assert 'var qrcode = function()' in qr, 'la libreria de QR no es la que espero'
assert h.count('/*__QR__*/') == 1
h = h.replace('/*__QR__*/', '\n' + qr + '\n')

# ── el logotipo ──
# OJO: va el de LETRAS OSCURAS. El de la web las lleva blancas, porque allí
# se apoya sobre el fondo negro; sobre la placa, que es blanca, esas letras
# desaparecen y solo queda la estrella. Se ve raro y cuesta darse cuenta.
FUENTE = os.path.join(RAIZ, 'zip', 'marca', 'marca-plea5e-claro.svg')
web = io.open(FUENTE, encoding='utf-8').read()
assert '#FFFFFF' not in web, 'este logotipo lleva letras blancas: sobre la placa no se verían'
# Nos quedamos SOLO con lo de dentro. Si arrastramos también los atributos
# del <svg> original y luego les ponemos los nuestros delante, el archivo
# acaba con xmlns, width y height repetidos: eso ya no es XML válido, el
# navegador se niega a pintarlo y el logotipo desaparece del pie sin decir
# nada. Pasó, y por eso hay un test que lo vigila.
m = re.search(r'<svg[^>]*>(.*?)</svg>', web, re.S)
assert m, 'no encuentro el logotipo en ' + FUENTE
# como imagen suelta necesita el xmlns y una medida propia; dentro del HTML
# de la web no hacían falta, porque los ponía el propio documento
cuerpo = m.group(1)
# Las dos barras de los lados son la banda que cruza la cabecera de la web,
# no parte del logotipo. En la placa sobran: la raya del pie ya la dibuja el
# propio generador, y así el dibujo ocupa solo lo que ocupa la marca.
antes = cuerpo
cuerpo = re.sub(r'<rect x="-4200\.0"[^>]*/>', '', cuerpo, count=1)
cuerpo = re.sub(r'<rect x="3201\.8"[^>]*/>', '', cuerpo, count=1)
assert cuerpo != antes and cuerpo.count('<rect') == antes.count('<rect') - 2, 'no he quitado las dos barras'
# la caja se recorta a lo que de verdad ocupa la marca, medido con getBBox
svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="1281" height="288" '
       'viewBox="-3202 -1259 6404 1438">' + cuerpo + '</svg>')
assert svg.count('<svg') == 1 and svg.count('xmlns') == 1, 'atributos repetidos'
assert svg.count('viewBox') == 1, 'mas de un viewBox'
assert '<path' in svg, 'el logotipo se ha quedado sin trazos'
assert h.count("'__LOGO__'") == 1
h = h.replace("'__LOGO__'", json.dumps(svg, ensure_ascii=False))

# ── la tipografia, dentro del archivo ──
# Montserrat (SIL Open Font License 1.1), el subconjunto latino de Google
# Fonts. Es la letra de la plantilla de verdad. Va metida en base64 y no
# enlazada a Google: si un dia no hay red, o Google cambia la direccion, o
# el navegador tarda, la placa NO se puede dibujar con otra letra. Una
# placa impresa con la tipografia equivocada es papel tirado.
import base64
CRUDA = os.path.join(AQUI, '..', 'fuente', 'montserrat-latin.woff2')
b = open(CRUDA, 'rb').read()
assert b[:4] == b'wOF2', 'eso no es un woff2'
assert 30000 < len(b) < 90000, 'la fuente pesa lo que no debe: %d' % len(b)
assert h.count('__FUENTE__') == 1
h = h.replace('__FUENTE__', base64.b64encode(b).decode('ascii'))

# ── comprobaciones de que no queda nada a medio pegar ──
for resto in ('__QR__', '__LOGO__', '__FUENTE__'):
    assert resto not in h, resto
assert 'Rubik' not in h, 'ha quedado alguna referencia a la letra vieja'
assert h.count('@font-face') == 1

os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
io.open(SALIDA, 'w', encoding='utf-8').write(h)
print('generador montado ·', len(h) // 1024, 'KB ·', SALIDA)
