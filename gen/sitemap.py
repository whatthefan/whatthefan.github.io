# -*- coding: utf-8 -*-
"""Pone al día la fecha del mapa del sitio.

Google usa la fecha de <lastmod> solo mientras le parece de fiar. Si ve que
siempre dice "hoy" pero al entrar la página es la misma de hace meses, deja
de hacerle caso para todo el dominio. O sea que la fecha tiene que ser la
del último cambio DE CONTENIDO, no la del último despliegue.

Por eso la saca de git: la fecha del último commit que tocó cada
página (están en PAGINAS, más abajo). Se ejecuta con

    npm run sitemap

después de cambiar la página y antes de subirla. Si no ha cambiado nada,
no toca el archivo y lo dice.
"""
import io, os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
MAPA = os.path.join(RAIZ, 'public', 'sitemap.xml')
# Cada direccion del mapa y el archivo del que sale.
PAGINAS = {
    'https://plea5e.es/': 'public/index.html',
    'https://plea5e.es/analiza/': 'public/analiza/index.html',
}


def fecha_del_ultimo_cambio(pagina):
    """La fecha (AAAA-MM-DD) del último commit que tocó la página."""
    salida = subprocess.check_output(
        ['git', 'log', '-1', '--format=%cs', '--', pagina],
        cwd=RAIZ).decode('utf-8').strip()
    # En un clon superficial puede no haber historia del archivo. Antes de
    # inventarse una fecha, mejor pararse: una fecha falsa hace mas daño
    # que una vieja.
    assert re.match(r'^\d{4}-\d{2}-\d{2}$', salida), (
        'git no me da la fecha del ultimo cambio de ' + pagina + '. '
        'Me ha devuelto: ' + repr(salida) + '. Pon la fecha a mano en '
        'public/sitemap.xml antes que dejar una inventada.')
    return salida


h = io.open(MAPA, encoding='utf-8').read()
cambios = []
for loc, pagina in PAGINAS.items():
    patron = re.compile(r'(<loc>' + re.escape(loc) + r'</loc>\s*<lastmod>)(.*?)(</lastmod>)')
    m = patron.search(h)
    assert m, 'no encuentro ' + loc + ' con su <lastmod> en el mapa.'
    nueva = fecha_del_ultimo_cambio(pagina)
    if m.group(2) != nueva:
        cambios.append(loc + ': ' + m.group(2) + '  ->  ' + nueva)
        h = h[:m.start(2)] + nueva + h[m.end(2):]

if not cambios:
    print('El mapa ya esta al dia. No toco nada.')
    sys.exit(0)

io.open(MAPA, 'w', encoding='utf-8').write(h)
print('\n'.join(cambios))
