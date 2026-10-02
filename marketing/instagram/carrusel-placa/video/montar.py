"""Monta escena-montada.html del video "la placa, destripada": mete en la
plantilla las letras, las capas de la placa (las de ../capas.js), el chip
y a Estrellita. Desde la raiz del repo:
    python3 marketing/instagram/carrusel-placa/video/montar.py
"""
import base64
import json
import re

V = 'marketing/instagram/carrusel-placa/video/'
CAPAS_DIR = 'marketing/instagram/carrusel-placa/capas/'
b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
uri = lambda f: f'data:image/png;base64,{b64(CAPAS_DIR + f + ".png")}'

# el chip: la bobina de cobre que va pegada detras del vinilo, a la altura del icono
CHIP = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600">'
        + ''.join(f'<rect x="{110 + 16 * i}" y="{170 + 16 * i}" width="{230 - 32 * i}" height="{230 - 32 * i}" rx="{18 - 3 * i}" '
                  f'fill="none" stroke="#C98A3A" stroke-width="7"/>' for i in range(4))
        + '<rect x="200" y="260" width="50" height="50" rx="6" fill="#1b1b1b" stroke="#C98A3A" stroke-width="4"/></svg>')
chip_uri = 'data:image/svg+xml;base64,' + base64.b64encode(CHIP.encode()).decode()

# de abajo arriba: [clase, fondo(s), rotulo]
CAPAS = [
    ('vidrio', None, 'Metacrilato de <b>4 mm</b>'),
    ('chip', [chip_uri], 'El <b>chip NFC</b>'),
    ('fondo', [uri('pieza-fondo')], 'Vinilo <b>impreso</b>'),
    ('banda', [uri('pieza-banda')], 'Tus <b>colores</b>'),
    ('titulo', [uri('pieza-titulo')], 'Mensaje <b>+ Google</b>'),
    ('cliente', [uri('pieza-cliente')], 'Tu <b>logo y nombre</b>'),
    ('qr', [uri('pieza-qr')], 'Tu <b>código QR</b>'),
    ('toca', [uri('pieza-nfc'), uri('pieza-instr'), uri('pieza-tel')], '<b>Toca</b> o escanea'),
]
css = '\n'.join(f'.k-{c}{{background-image:{",".join(f"url({u})" for u in f)}}}' for c, f, _ in CAPAS if f)
html = ''.join(f'<div class="capa {"vidrio" if c == "vidrio" else "k-" + c}" id="capa{i}">'
               + ('<i class="lado ab"></i><i class="lado de"></i>' if c == 'vidrio' else '') + '</div>'
               for i, (c, f, _) in enumerate(CAPAS))


def estrellita(pose, pref):
    s = open(f'public/marca/estrellita/{pose}.svg').read()
    s = re.sub(r'<\?xml[^>]*>|<title>.*?</title>|<!--.*?-->', '', s, flags=re.S)
    return re.sub(r'(id="|href="#|url\(#)([\w-]+)', lambda m: f'{m.group(1)}{pref}{m.group(2)}', s)


h = open(V + 'escena.html').read()
for k, v in {'ANTON': b64('fuente/anton-latin.woff2'), 'MONT': b64('fuente/montserrat-latin.woff2'),
             'CAVEAT': b64('fuente/caveat-latin.woff2'), 'CSS_CAPAS': css, 'CAPAS': html,
             'LISTA_CAPAS': json.dumps([[c, r] for c, f, r in CAPAS], ensure_ascii=False),
             'EST_SALUDA': estrellita('saluda', 's-')}.items():
    h = h.replace('{{' + k + '}}', v)
assert '{{' not in h, re.findall(r'\{\{\w+\}\}', h)
open(V + 'escena-montada.html', 'w').write(h)
