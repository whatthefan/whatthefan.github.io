# -*- coding: utf-8 -*-
"""Los dibujos de la Estrellita para la web.

Reune lo que ya estaba suelto en tres sitios —el generador de poses, el
de caras y el de la uve— y saca de una vez el juego entero que usa la
pagina: ocho fotogramas de caminata y once poses, cada una en
las dos direcciones.

    python3 gen/estrellita.py

Borra los .svg que haya en public/marca/estrellita y los vuelve a
escribir. Si hay que cambiar algo se cambia AQUI, no en los .svg.

DOS COSAS NUEVAS

1. CADA POSE LLEVA SU CARA. Ella no tiene boca y no se la voy a poner:
   la marca es una estrella con ojos, y una estrella con boca ya es
   otro personaje. Todo pasa por la pupila (donde mira), su tamano (si
   le gusta lo que ve) y el parpado. Es como funcionan los dibujos
   mudos de los anos 30, donde el ojo hace el trabajo entero.

2. PARPADEA SOLA. Dentro del SVG va un parpado con una animacion de
   CSS. Un SVG cargado con <img> no ejecuta guiones, pero SI corre sus
   animaciones declaradas, asi que parpadea sin una sola linea de
   JavaScript en la pagina y sin un archivo por fotograma. Cada pose
   lleva su propio retardo para que no parezca un reloj.

   Y si el sistema pide menos movimiento, el propio dibujo se queda
   quieto: la media consulta va dentro del SVG.
"""
import io, math, os

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(os.path.dirname(AQUI), 'public', 'marca', 'estrellita')

# ── de donde salen los brazos y las piernas ──
CAD_I, CAD_D = (302, 838), (722, 838)
HOM_I, HOM_D = (262, 476), (762, 476)
SUELO = 1000

# ── los ojos, tal como vienen del dibujo original ──
OJO  = [(438, 238), (588, 230)]
OJO_RX, OJO_RY = 80, 94
PUP  = [(456, 254), (606, 246)]
PUP_RX, PUP_RY = 31, 39
LUZ  = [(467, 240), (617, 232)]
LUZ_R = 11


def cara(dx=0, dy=0, escala=1.0, parpado=0.0, guino=None, inclina=0):
    """El bloque de ojos con la expresion pedida.

    dx, dy    hacia donde mira
    escala    pupila grande = le gusta lo que ve. El truco mas viejo
              del dibujo animado y sigue funcionando.
    parpado   cuanto le tapa el parpado. Con medio ojo tapado
              cualquier personaje parece harto.
    guino     'izq' o 'der' para cerrar uno.
    """
    p = ['<g class="borde">']
    for (cx, cy) in OJO:
        p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{OJO_RX}" ry="{OJO_RY}" fill="#F7F4EC"/>')
    p.append('</g>')

    def raya(cx, cy):
        return (f'<path d="M {cx-56} {cy-6} Q {cx} {cy+40} {cx+56} {cy-6}" '
                f'fill="none" stroke="#0A0E16" stroke-width="24" stroke-linecap="round"/>')

    for i, ((cx, cy), (px, py), (lx, ly)) in enumerate(zip(OJO, PUP, LUZ)):
        if guino == ('izq' if i == 0 else 'der'):
            p.append(raya(cx, cy))           # este se queda cerrado siempre
            continue
        # ── EL PARPADEO ──
        # Dos dibujos del mismo ojo, uno encima del otro, y una
        # animacion que los va apagando y encendiendo al reves. Antes
        # esto era un parpado negro que bajaba y tapaba el ojo, y no
        # valia: los ojos se salen de la cabeza, o sea que tapar el
        # ojo con negro sobre fondo oscuro no cierra nada, hace un
        # agujero en la punta de la estrella. Un ojo cerrado en este
        # estilo es una raya curva, la misma del guino.
        p.append(f'<g class="ojo-abre">')
        p.append(f'<ellipse cx="{px+dx:.0f}" cy="{py+dy:.0f}" '
                 f'rx="{PUP_RX*escala:.0f}" ry="{PUP_RY*escala:.0f}" fill="#0A0E16"/>')
        p.append(f'<circle cx="{lx+dx:.0f}" cy="{ly+dy:.0f}" '
                 f'r="{LUZ_R*escala:.0f}" fill="#F7F4EC"/>')
        p.append('</g>')
        p.append(f'<g class="ojo-cierra">{raya(cx, cy)}</g>')

    if parpado > 0:
        for i, (cx, cy) in enumerate(OJO):
            if guino == ('izq' if i == 0 else 'der'):
                continue
            alto = 2 * OJO_RY * parpado
            giro = inclina if i == 0 else -inclina
            p.append(
                f'<g class="ojo-abre" clip-path="url(#ojo{i})">'
                f'<rect x="{cx-OJO_RX-30}" y="{cy-OJO_RY-40}" '
                f'width="{2*OJO_RX+60}" height="{alto+40:.0f}" fill="#0A0E16" '
                f'transform="rotate({giro} {cx} {cy})"/></g>')

    return '\n  '.join(p)


CLIPS = '\n'.join(
    f'  <clipPath id="ojo{i}"><ellipse cx="{cx}" cy="{cy}" '
    f'rx="{OJO_RX}" ry="{OJO_RY}"/></clipPath>'
    for i, (cx, cy) in enumerate(OJO))

GUANTE = '''  <g id="guante">
    <circle class="borde" cx="0" cy="0" r="82" fill="#F7F4EC"/>
    <path class="borde" fill="#F7F4EC"
          d="M-58 -34 C -92 -66, -126 -62, -138 -34 C -150 -6, -128 22, -92 24"/>
    <g class="tinta" stroke-width="14">
      <path d="M22 54 C 34 40, 40 24, 40 8"/>
      <path d="M54 34 C 62 22, 66 10, 66 -2"/>
      <path d="M20 -50 C 34 -40, 42 -26, 44 -12"/>
    </g>
  </g>'''

# El guante de la uve. El de la marca no tiene dedos sueltos —es una
# bola con el pulgar y tres rayas—, asi que los dos dedos se construyen
# igual que todo lo demas: un trazo oscuro de 78 debajo y uno crema de
# 50 encima. Esos 14 por lado son el mismo borde de 26 del cuerpo.
GUANTE_PAZ = '''  <g id="guante-paz">
    <g fill="none" stroke-linecap="round">
      <g stroke="#0A0E16" stroke-width="78">
        <path d="M-24 -30 Q -60 -104, -94 -164"/>
        <path d="M 28 -30 Q  66 -102, 100 -158"/>
      </g>
      <g stroke="#F7F4EC" stroke-width="50">
        <path d="M-24 -30 Q -60 -104, -94 -164"/>
        <path d="M 28 -30 Q  66 -102, 100 -158"/>
      </g>
    </g>
    <circle class="borde" cx="0" cy="0" r="82" fill="#F7F4EC"/>
    <path class="borde" fill="#F7F4EC"
          d="M-58 -34 C -92 -66, -126 -62, -138 -34 C -150 -6, -128 22, -92 24"/>
  </g>'''

ZAPATO = '''  <g id="zapato">
    <path class="borde" fill="#0A0E16"
          d="M0 0 C -86 0, -146 34, -146 84 C -146 120, -92 134, -18 134
             L 52 134 C 80 134, 92 116, 92 90 L 92 22 C 92 6, 76 0, 52 0 Z"/>
    <path fill="#F2EFE6"
          d="M-140 98 C -120 128, -66 134, -18 134 L 52 134 C 76 134, 89 123, 91 100 Z"/>
  </g>'''

ESTRELLA = ('<path class="borde" fill="#E9BC46" d="M512 41L633.8 323.8L962.6 352.3'
            'L709.1 555.6L776.8 856L512 698.8L247.2 856L314.9 555.6L61.4 352.3'
            'L390.2 323.8Z"/>')

CINCO = ('<path fill="#0A0E16" transform="translate(407.3 696.2) scale(0.42)" '
         'd="M247.1 12.2Q147.9 12.2 85.2-36.9Q22.5-85.9 22.5-187.5L22.5-315.4'
         'L201.2-315.4L201.2-241.7Q201.2-218.7 203.9-197.3Q206.5-175.8 216.3-162.1'
         'Q226.1-148.4 247.1-148.4Q274.9-148.4 283.7-167.2Q292.5-186 292.5-215.3'
         'L292.5-384.3Q292.5-405.3 289.8-425.8Q287.1-446.3 277.8-460Q268.6-473.6 248-473.6'
         'Q199.2-473.6 199.2-402.8L41.5-402.8L41.5-859.9L451.2-859.9L451.2-698.7'
         'L204.6-698.7L204.6-577.6Q217.3-593.3 239-605.2Q260.7-617.2 290-617.2'
         'Q348.6-617.2 385.5-594.7Q422.4-572.3 442.1-532.2Q461.9-492.2 469.5-439.5'
         'Q477.1-386.7 477.1-326.2Q477.1-248.5 469-186.3Q460.9-124 437.3-79.6'
         'Q413.6-35.2 367.9-11.5Q322.3 12.2 247.1 12.2"/>')


def cabeza(titulo, retardo):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-190 -40 1404 1260">
<title>Estrellita PLEA5E · {titulo}</title>

<!-- ESTRELLITA — la mascota de PLEA5E.

     No es un dibujo inventado: es el sello. La estrella es la misma y
     el 5 es el mismo trazado; lo unico que se le anade son
     extremidades. Y encaja solo, porque una estrella de cinco puntas
     ya viene con las piernas puestas: las dos puntas de abajo.

     Estilo "rubber hose", el de los dibujos de los anos 30: brazos de
     manguera sin codos, guantes blancos, zapatones y ojos enormes.

     PARPADEA SOLO. Cada ojo esta dibujado dos veces —abierto y
     cerrado, uno sobre otro— y una animacion de CSS los enciende y
     apaga al reves cada seis segundos y pico. Un SVG cargado como imagen no
     ejecuta guiones, pero SI corre sus animaciones declaradas, asi
     que esto funciona sin una linea de JavaScript en la pagina.

     Y EL CUERPO NO VA EN <defs>. Estuvo ahi, puesto con <use>, y el
     parpadeo no se veia: el clon que hace <use> no arrastra las
     animaciones del original. Va escrito tal cual donde se pinta.

     OJO CON LO QUE SE ESCRIBE DENTRO DE <style>: un SVG es XML, no
     HTML, asi que cualquier cosa entre menor y mayor —hasta dentro de
     un comentario de CSS— se lee como etiqueta y parte el archivo.
     Por eso esta explicacion esta aqui arriba y no ahi abajo.

     NO SE EDITA A MANO. Sale de gen/estrellita.py; si hay que cambiar
     algo se cambia alli y se sacan las diecisiete de golpe.                   -->

<defs>
  <style>
    .tinta  {{ fill:none; stroke:#0A0E16; stroke-linecap:round; stroke-linejoin:round }}
    .brazo  {{ stroke-width:40 }}
    .pierna {{ stroke-width:52 }}
    .borde  {{ stroke:#0A0E16; stroke-width:26; stroke-linejoin:round }}

    @keyframes abre   {{ 0%, 95.4%, 100% {{ opacity:1 }} 96.6%, 98.2% {{ opacity:0 }} }}
    @keyframes cierra {{ 0%, 95.4%, 100% {{ opacity:0 }} 96.6%, 98.2% {{ opacity:1 }} }}
    .ojo-abre   {{ animation: abre   6.4s steps(1,end) {retardo}s infinite }}
    .ojo-cierra {{ animation: cierra 6.4s steps(1,end) {retardo}s infinite; opacity:0 }}
    @media (prefers-reduced-motion: reduce) {{
      .ojo-abre {{ animation: none }} .ojo-cierra {{ animation: none; opacity:0 }} }}
  </style>
{CLIPS}
{GUANTE}
{GUANTE_PAZ}
{ZAPATO}
</defs>
'''


def pierna(cad, pie, bob):
    cx, cy = cad[0], cad[1] + bob
    px, py = pie
    mx, my = (cx + px) / 2 + (px - cx) * 0.16, (cy + py) / 2 + 14
    return f'<path class="tinta pierna" d="M{cx:.0f} {cy:.0f} Q {mx:.0f} {my:.0f} {px:.0f} {py:.0f}"/>'


def brazo(hom, mano, bob):
    hx, hy = hom[0], hom[1] + bob
    mx, my = mano
    cx, cy = (hx + mx) / 2 + (mx - hx) * 0.1, (hy + my) / 2 - 26
    return f'<path class="tinta brazo" d="M{hx:.0f} {hy:.0f} Q {cx:.0f} {cy:.0f} {mx:.0f} {my:.0f}"/>'


# El centro de la estrella. Espejar alrededor de este punto deja la
# figura mirando al otro lado sin moverla de sitio.
EJE = 512


def escribe(nombre, titulo, expresion, cuerpo, retardo):
    """Saca el dibujo en las DOS direcciones.

    EL 5 NO SE ESPEJA. Esto antes lo hacía la hoja de estilos con un
    scaleX(-1) sobre la imagen entera, y el 5 salía del revés: la
    mascota es el sello de la marca y el 5 es el 5, no se puede leer
    al revés ni un segundo. Así que el espejo se hace aquí, en el
    dibujo, y dentro del espejo se le da la vuelta OTRA VEZ al 5
    —alrededor del mismo eje— para dejarlo como estaba.

    Sale el doble de archivos, treinta y cuatro. Pesan 6 KB cada uno y
    el navegador solo se baja los que usa.
    """
    total = 0
    for lado in ('', '-izq'):
        cinco = (f'<g transform="translate({2*EJE} 0) scale(-1 1)">{CINCO}</g>'
                 if lado else CINCO)
        dentro = cuerpo.replace('@CUERPO@', f'{ESTRELLA}\n{cinco}\n  {expresion}')
        if lado:
            dentro = (f'<g transform="translate({2*EJE} 0) scale(-1 1)">\n'
                      + dentro + '\n</g>')
        svg = cabeza(titulo + (' (al revés)' if lado else ''), retardo) + dentro + '\n</svg>\n'
        io.open(f'{SALIDA}/{nombre}{lado}.svg', 'w', encoding='utf-8').write(svg)
        total += len(svg)
    return total


# ══════════════════════════════════════════════════════════════════
#  EL CICLO DE CAMINATA
#  No son ocho dibujos a mano: es una formula. Cada pie pasa medio
#  ciclo en el suelo (yendo hacia atras, que es lo que empuja al
#  personaje) y medio en el aire volviendo, con un arco. Los brazos van
#  al reves que las piernas, que es como anda cualquiera. Y el cuerpo
#  sube y baja dos veces por ciclo.
# ══════════════════════════════════════════════════════════════════
def paso(p, cad_x):
    ZANCADA, ALTURA = 150.0, 95.0
    if p < 0.5:
        q = p / 0.5
        return cad_x + ZANCADA * (1 - 2 * q), SUELO, -14 * (1 - 2 * q)
    q = (p - 0.5) / 0.5
    return (cad_x - ZANCADA * (1 - 2 * q),
            SUELO - ALTURA * math.sin(math.pi * q),
            -14 * (2 * q - 1))


def fotograma(p):
    bob = -16 * abs(math.sin(2 * math.pi * p)) + 8
    lean = 2.5 * math.sin(2 * math.pi * p)
    pi_x, pi_y, pi_r = paso(p, CAD_I[0])
    pd_x, pd_y, pd_r = paso((p + 0.5) % 1.0, CAD_D[0])
    mi_x = HOM_I[0] - 210 - 120 * math.sin(2 * math.pi * ((p + 0.5) % 1.0))
    md_x = HOM_D[0] + 210 + 120 * math.sin(2 * math.pi * p)
    mi_y = 660 + bob + 30 * math.cos(2 * math.pi * p)
    md_y = 660 + bob - 30 * math.cos(2 * math.pi * p)
    return '\n'.join([
        pierna(CAD_I, (pi_x, pi_y), bob),
        pierna(CAD_D, (pd_x, pd_y), bob),
        f'<use href="#zapato" transform="translate({pi_x:.0f} {pi_y:.0f}) rotate({pi_r:.1f})"/>',
        f'<use href="#zapato" transform="translate({pd_x:.0f} {pd_y:.0f}) rotate({pd_r:.1f}) scale(-1 1)"/>',
        brazo(HOM_I, (mi_x, mi_y), bob),
        brazo(HOM_D, (md_x, md_y), bob),
        f'<g transform="translate(0 {bob:.0f}) rotate({lean:.1f} 512 600)">@CUERPO@</g>',
        f'<use href="#guante" transform="translate({mi_x:.0f} {mi_y:.0f}) rotate(20)"/>',
        f'<use href="#guante" transform="translate({md_x:.0f} {md_y:.0f}) rotate(-20) scale(-1 1)"/>',
    ])


def quieta(mi, md, gi, gd, bob=0, lean=0, piernas=None, paz=False):
    """Una pose de pie: se dan las dos manos y el giro de cada guante."""
    pz = piernas or [
        (pierna(CAD_I, (288, SUELO), bob), f'<use href="#zapato" transform="translate(288 {SUELO})"/>'),
        (pierna(CAD_D, (736, SUELO), bob), f'<use href="#zapato" transform="translate(736 {SUELO}) scale(-1 1)"/>'),
    ]
    mano_d = 'guante-paz' if paz else 'guante'
    esp = '' if paz else ' scale(-1 1)'
    giro = gd if paz else gd
    return '\n'.join(
        [p[0] for p in pz] + [p[1] for p in pz] + [
            brazo(HOM_I, mi, bob), brazo(HOM_D, md, bob),
            f'<g transform="translate(0 {bob}) rotate({lean} 512 600)">@CUERPO@</g>',
            f'<use href="#guante" transform="translate({mi[0]} {mi[1]}) rotate({gi})"/>',
            f'<use href="#{mano_d}" transform="translate({md[0]} {md[1]}) rotate({giro}){esp}"/>',
        ])


# ── SENTADA ──
# En el borde de algo: el culo en la línea, las piernas colgando por
# delante y una mano apoyada atrás. El cuerpo baja 150 para que lo que
# se apoya sea la punta de abajo de la estrella y no los pies.
COLGANDO = [
    ('<path class="tinta pierna" d="M302 988 Q 330 1062 356 1126"/>',
     '<use href="#zapato" transform="translate(356 1126) rotate(74)"/>'),
    ('<path class="tinta pierna" d="M722 988 Q 694 1062 668 1126"/>',
     '<use href="#zapato" transform="translate(668 1126) rotate(-74) scale(-1 1)"/>'),
]

# ── APOYADA ──
# De medio lado contra algo que tiene a su derecha: el cuerpo
# inclinado, el brazo de ese lado estirado haciendo de puntal y los
# pies cruzados.
CRUZADAS = [
    ('<path class="tinta pierna" d="M302 838 Q 340 920 402 1000"/>',
     '<use href="#zapato" transform="translate(402 1000) rotate(-8)"/>'),
    ('<path class="tinta pierna" d="M722 838 Q 680 920 610 1004"/>',
     '<use href="#zapato" transform="translate(610 1004) rotate(10) scale(-1 1)"/>'),
]

SALTO = [
    ('<path class="tinta pierna" d="M302 838 Q 250 900 232 946"/>',
     '<use href="#zapato" transform="translate(232 946) rotate(-24)"/>'),
    ('<path class="tinta pierna" d="M722 838 Q 774 900 792 946"/>',
     '<use href="#zapato" transform="translate(792 946) rotate(24) scale(-1 1)"/>'),
]

# ══════════════════════════════════════════════════════════════════
#  LAS POSES
#  Las nueve que usa la pagina. La mano derecha es la que trabaja
#  siempre: cuando tiene que enseñar algo que esta a su izquierda, el
#  dibujo entero se voltea con scaleX(-1) desde la hoja de estilos.
# ══════════════════════════════════════════════════════════════════
POSES = {
    # señala al frente, horizontal: para lo que tiene al lado
    'senala':  ('senalando', dict(dx=22, dy=2),
                lambda: quieta((6, 612), (1064, 452), 14, -4)),
    # señala hacia arriba en diagonal: para lo que tiene encima
    'arriba':  ('mirando arriba', dict(dy=-10, escala=1.15),
                lambda: quieta((6, 612), (1016, 266), 14, -34)),
    # señala hacia abajo: para lo que tiene a los pies
    'abajo':   ('senalando abajo', dict(dy=14),
                lambda: quieta((110, 700), (900, 792), 30, -66)),
    # las dos manos arriba y las pupilas como platos: «¡anda!».
    # Van ABIERTAS y por encima de los ojos: a la altura de la cara le
    # tapaban medio ojo y parecia que le habian dado un golpe.
    'asombro': ('asombrada', dict(dy=-6, escala=1.45),
                lambda: quieta((130, 150), (894, 150), -34, 34)),
    # saluda con la mano: la primera vez que la ves
    'saluda':  ('saludando', dict(dy=-4, escala=1.1),
                lambda: quieta((6, 612), (952, 176), 14, 46)),
    # asomandose: el cuerpo inclinado hacia delante, las manos juntas
    # por delante y las pupilas del todo hacia el lado. Aqui estuvo la
    # mano de visera sobre los ojos y no valia: unos ojos que se salen
    # de la cabeza no admiten nada encima, se los tapa.
    'curiosa': ('asomandose', dict(dx=30, dy=2, escala=1.15, parpado=0.16),
                lambda: quieta((372, 742), (742, 786), 52, -34, lean=9)),
    # la uve y un guiño
    'guino':   ('la uve', dict(dy=-6, escala=1.15, guino='der'),
                lambda: quieta((72, 176), (952, 152), -46, 9, paz=True)),
    # los dos brazos arriba: el ta-chan
    'tachan':  ('ta-chan', dict(dy=-8, escala=1.35),
                lambda: quieta((72, 176), (952, 176), -46, 46)),
    # de un salto, con las piernas encogidas
    'salta':   ('saltando', dict(dy=-10, escala=1.3),
                lambda: quieta((96, 246), (928, 246), -40, 40, bob=-70, piernas=SALTO)),
    # sentada en el borde de algo, con las piernas colgando
    'sentada': ('sentada', dict(dy=6, escala=1.05),
                lambda: quieta((196, 1002), (828, 1002), -22, 22,
                               bob=150, piernas=COLGANDO)),
    # apoyada de medio lado, con el brazo derecho de puntal
    'apoyada': ('apoyada', dict(dx=18, dy=2, escala=1.08, parpado=0.2),
                lambda: quieta((250, 760), (1004, 900), 34, -4,
                               lean=-11, piernas=CRUZADAS)),
}

if __name__ == '__main__':
    # los viejos, fuera: si queda uno suelto con otro nombre, alguien
    # acabara tirando de el sin saber que ya no se genera
    for f in os.listdir(SALIDA):
        if f.endswith('.svg'):
            os.remove(os.path.join(SALIDA, f))

    total, n = 0, 0
    # andando: la cara normal, que va a lo suyo
    for i in range(8):
        total += escribe(f'anda-{i}', f'andando {i+1}/8', cara(),
                         fotograma(i / 8), 0.3 + 0.21 * i)
        n += 1
    for nombre, (titulo, exp, cuerpo) in POSES.items():
        total += escribe(nombre, titulo, cara(**exp), cuerpo(), 0.3 + 0.21 * n)
        n += 1
    print(f'{n} dibujos, {total/1024:.1f} KB en total')
