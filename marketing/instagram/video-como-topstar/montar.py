"""Monta escena-montada.html: la plantilla escena.html con todo metido
dentro (letras, modelos, sello, edificios y Estrellita), sin nada que
pedir fuera.

Los modelos salen de modelos.js (el generador de placas); aqui se les da
grosor apilando la misma imagen hacia atras: 4 mm de metacrilato en la
placa y el expositor, la tarjeta casi plana.

Desde la raiz del repo:  python3 marketing/instagram/video-como-topstar/montar.py
"""
import base64
import re

D = 'marketing/instagram/video-como-topstar/'
b64 = lambda f: base64.b64encode(open(f, 'rb').read()).decode()
uri = lambda f, tipo='image/png': f'data:{tipo};base64,{b64(f)}'


def estrellita(pose, pref):
    s = open(f'public/marca/estrellita/{pose}.svg').read()
    s = re.sub(r'<\?xml[^>]*>|<title>.*?</title>', '', s, flags=re.S)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    return re.sub(r'(id="|href="#|url\(#)([\w-]+)', lambda m: f'{m.group(1)}{pref}{m.group(2)}', s)


def sello():
    """La estrella con el 5 entero dentro, como el avatar (escala 0,42)."""
    ico = open('public/icono.svg').read()
    star = re.search(r'<path fill="#E9BC46" d="([^"]+)"', ico).group(1)
    five = re.search(r'<path fill="#0A0E16" transform="[^"]+" d="([^"]+)"', ico).group(1)
    s = .42
    return (f'<path fill="#E9BC46" d="{star}"/>'
            f'<path fill="#06080E" transform="translate({512 - 249.5 * s:.1f} {316 + 860 * s:.1f}) scale({s})" d="{five}"/>')


CSS_MODELOS = []


def capas(nombre, grosor_px, n):
    """La imagen repetida n veces hacia atras: el canto del material.
    La imagen va una sola vez, en una regla de CSS; si fuera en cada capa
    el archivo pesaria diez veces mas."""
    if not any(nombre in c for c in CSS_MODELOS):
        CSS_MODELOS.append(f'.cap-{nombre}{{background:url({uri(D + "modelos/" + nombre + ".png")}) center/100% 100% no-repeat}}')
    atras = ''.join(
        f'<i class="cap-{nombre}" style="transform:translateZ({-grosor_px * (i + 1) / n:.1f}px);'
        f'filter:brightness({.62 + .18 * i / n:.2f}) saturate(.5)"></i>' for i in reversed(range(n)))
    return atras + f'<i class="cap-{nombre}"></i>'


def edificio(id_, x, luz, rotulo):
    ventana = '#F8E1A6' if luz else '#2A3448'
    toldo = '#E9BC46' if luz else '#5D6679'
    raya = '#C99A2E' if luz else '#4A5263'
    rayas = ''.join(f'<rect x="{30 + i * 45}" y="262" width="22" height="68" fill="{raya}"/>' for i in range(8))
    ondas = ' '.join('q22.5 30 45 0' for _ in range(8))
    maceta = lambda cx: (f'<rect x="{cx - 22}" y="505" width="44" height="35" rx="6" fill="#2A3448"/>'
                         f'<circle cx="{cx}" cy="490" r="26" fill="{"#3E6B4F" if luz else "#2C3A33"}"/>')
    return f'''<svg class="abs" id="{id_}" style="left:{x}px;top:870px" width="420" height="540" viewBox="0 0 420 540">
    <rect x="20" y="40" width="380" height="500" fill="#141B2B"/><rect x="0" y="20" width="420" height="40" fill="#1C2536"/>
    <rect x="55" y="95" width="120" height="120" fill="#1C2536"/><rect x="245" y="95" width="120" height="120" fill="#1C2536"/>
    <rect x="63" y="103" width="104" height="104" fill="{ventana}"/><rect x="253" y="103" width="104" height="104" fill="{ventana}"/>
    <rect x="113" y="103" width="4" height="104" fill="#1C2536"/><rect x="303" y="103" width="4" height="104" fill="#1C2536"/>
    <rect x="30" y="260" width="360" height="70" fill="{toldo}"/>{rayas}
    <path d="M30 330 {ondas}" fill="{toldo}"/>
    <rect x="120" y="222" width="180" height="34" rx="6" fill="#06080E"/>
    <text x="210" y="247" text-anchor="middle" font-family="Mont" font-weight="800" font-size="22" letter-spacing="3" fill="{toldo}">{rotulo}</text>
    <rect x="150" y="375" width="120" height="165" fill="#06080E"/><rect x="156" y="381" width="108" height="159" fill="{ventana if luz else '#0F1522'}"/>
    <rect x="240" y="455" width="8" height="26" rx="4" fill="#06080E"/>
    <rect x="45" y="385" width="90" height="100" fill="{ventana}"/><rect x="285" y="385" width="90" height="100" fill="{ventana}"/>
    {maceta(90)}{maceta(330)}
  </svg>'''


h = open(D + 'escena.html').read()
for k, v in {
    'ANTON': b64('fuente/anton-latin.woff2'),
    'MONT': b64('fuente/montserrat-latin.woff2'),
    'SELLO': sello(),
    'EDIFICIOS': edificio('edif1', 90, False, 'TU LOCAL') + edificio('edif2', 570, True, 'ENFRENTE'),
    'CAPAS_PLACA': capas('placa', 30, 12),
    'CAPAS_STAND': capas('stand', 30, 12),
    'CAPAS_TARJETA': capas('tarjeta', 8, 4),
    'EST_SALUDA': estrellita('saluda', 's-'),
}.items():
    h = h.replace('{{' + k + '}}', v)
h = h.replace('/*{{CSS_MODELOS}}*/', '\n'.join(CSS_MODELOS))
assert '{{' not in h, re.findall(r'\{\{\w+\}\}', h)
open(D + 'escena-montada.html', 'w').write(h)
