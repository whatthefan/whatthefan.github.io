"""Avatares de Instagram de PLEA5E (1080x1080, pensados para recorte circular).

Salen de los mismos trazos que la web: la estrella y el 5 de public/icono.svg
y la mascota de public/marca/estrellita/. Se ejecuta desde la raiz del repo:
    python3 marketing/instagram/avatar/generar.py
"""
import re

ico = open('public/icono.svg').read()
STAR = re.search(r'<path fill="#E9BC46" d="([^"]+)"', ico).group(1)
FIVE = re.search(r'<path fill="#0A0E16" transform="[^"]+" d="([^"]+)"', ico).group(1)

NOCHE, ORO, CREMA = '#06080E', '#E9BC46', '#F4EFE3'
CAB = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">'


def sello(estrella, cinco):
    # El 5 entero dentro del cuerpo de la estrella: en el icono de la web
    # asoma por arriba y, a 40 px, la estrella parece partida.
    s = 0.46
    return (f'<path fill="{estrella}" d="{STAR}"/>'
            f'<path fill="{cinco}" transform="translate(397.2 735.6) scale({s})" d="{FIVE}"/>')


def en_circulo(contenido, escala=0.86):
    # Centro visual de la estrella ~ (512, 470) en su caja de 1024.
    return f'<g transform="translate(540 565) scale({escala}) translate(-512 -470)">{contenido}</g>'


def guardar(nombre, svg):
    open(f'marketing/instagram/avatar/{nombre}.svg', 'w').write(svg)


guardar('A-sello-noche', CAB + f'<rect width="1080" height="1080" fill="{NOCHE}"/>'
        + en_circulo(sello(ORO, NOCHE)) + '</svg>')

guardar('B-sello-oro', CAB + f'<rect width="1080" height="1080" fill="{ORO}"/>'
        + en_circulo(sello(NOCHE, ORO)) + '</svg>')

# La mascota tiene brazos y piernas en tinta oscura: sobre noche desaparecen,
# por eso va sobre crema con el aro de oro.
m = open('public/marca/estrellita/guino.svg').read()
m = re.sub(r'<svg [^>]*>', '<svg x="150" y="175" width="780" height="700" viewBox="-190 -40 1404 1260">', m, count=1)
m = re.sub(r'<\?xml[^>]*>', '', m)
guardar('C-estrellita', CAB + f'<rect width="1080" height="1080" fill="{CREMA}"/>'
        f'<circle cx="540" cy="540" r="508" fill="none" stroke="{ORO}" stroke-width="16"/>' + m + '</svg>')
