# -*- coding: utf-8 -*-
"""Pone al día la fecha del mapa del sitio.

Google usa la fecha de <lastmod> solo mientras le parece de fiar. Si ve que
siempre dice "hoy" pero al entrar la página es la misma de hace meses, deja
de hacerle caso para todo el dominio. O sea que la fecha tiene que ser la
del último cambio DE CONTENIDO, no la del último despliegue.

Por eso la saca de git: la fecha del último commit que tocó
public/index.html, que es la única página del sitio. Se ejecuta con

    npm run sitemap

después de cambiar la página y antes de subirla. Si no ha cambiado nada,
no toca el archivo y lo dice.
"""
import io, os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
MAPA = os.path.join(RAIZ, 'public', 'sitemap.xml')
PAGINA = 'public/index.html'


def fecha_del_ultimo_cambio():
    """La fecha (AAAA-MM-DD) del último commit que tocó la página."""
    salida = subprocess.check_output(
        ['git', 'log', '-1', '--format=%cs', '--', PAGINA],
        cwd=RAIZ).decode('utf-8').strip()
    # En un clon superficial puede no haber historia del archivo. Antes de
    # inventarse una fecha, mejor pararse: una fecha falsa hace mas daño
    # que una vieja.
    assert re.match(r'^\d{4}-\d{2}-\d{2}$', salida), (
        'git no me da la fecha del ultimo cambio de ' + PAGINA + '. '
        'Me ha devuelto: ' + repr(salida) + '. Pon la fecha a mano en '
        'public/sitemap.xml antes que dejar una inventada.')
    return salida


h = io.open(MAPA, encoding='utf-8').read()
assert h.count('<lastmod>') == 1, (
    'esperaba una sola <lastmod> en el mapa. Si ya hay varias paginas, '
    'este script se ha quedado corto y hay que ampliarlo.')

nueva = fecha_del_ultimo_cambio()
vieja = re.search(r'<lastmod>(.*?)</lastmod>', h).group(1)

if vieja == nueva:
    print('El mapa ya esta al dia (' + vieja + '). No toco nada.')
    sys.exit(0)

h = h.replace('<lastmod>' + vieja + '</lastmod>',
              '<lastmod>' + nueva + '</lastmod>')
io.open(MAPA, 'w', encoding='utf-8').write(h)
print('Fecha del mapa: ' + vieja + '  ->  ' + nueva)
