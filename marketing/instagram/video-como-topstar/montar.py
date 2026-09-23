"""Monta escena-montada.html: la plantilla escena.html con todo metido
dentro (letras, fotos, logotipo y Estrellita), sin nada que pedir fuera.
Desde la raiz del repo:  python3 marketing/instagram/video-como-topstar/montar.py
"""
import base64
import re

D = 'marketing/instagram/video-como-topstar/'
b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
uri = lambda f, tipo: f'data:{tipo};base64,{b64(f)}'


def estrellita(pose, pref):
    s = open(f'public/marca/estrellita/{pose}.svg').read()
    s = re.sub(r'<\?xml[^>]*>|<title>.*?</title>', '', s, flags=re.S)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    # cada copia con sus propios id: van varias en la misma pagina
    return re.sub(r'(id="|href="#|url\(#)([\w-]+)', lambda m: f'{m.group(1)}{pref}{m.group(2)}', s)


marca = re.sub(r'<svg [^>]*>', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4200 -1290 8400 1680" width="1000" height="200">',
               open('public/marca/marca-plea5e.svg').read(), count=1)
marca = re.sub(r'<title>.*?</title>', '', marca)

h = open(D + 'escena.html').read()
for k, v in {
    'ANTON': b64('fuente/anton-latin.woff2'),
    'MONT': b64('fuente/montserrat-latin.woff2'),
    'PLACA': uri('public/producto/placa-recortada.png', 'image/png'),
    'PLACA_CUAD': uri('public/assets/img/53173bd05566.jpg', 'image/jpeg'),
    'EXPOSITOR': uri('public/assets/img/7cc814b5577a.jpg', 'image/jpeg'),
    'TARJETA': uri('public/assets/img/caa45407153b.jpg', 'image/jpeg'),
    'BARVI': uri('public/assets/img/87c348f619be.jpg', 'image/jpeg'),
    'PICCOLA': uri('public/assets/img/bcd3cec2e61f.jpg', 'image/jpeg'),
    'MARCA': marca,
    'EST_ASOMBRO': estrellita('asombro', 'a-'),
    'EST_TACHAN': estrellita('tachan', 't-'),
    'EST_SALUDA': estrellita('saluda', 's-'),
}.items():
    h = h.replace('{{' + k + '}}', v)
assert '{{' not in h
open(D + 'escena-montada.html', 'w').write(h)
