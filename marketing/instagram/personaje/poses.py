"""Estrellita para Instagram: el juego de poses de la web (gen/estrellita.py) mas
poses nuevas con cosas en la mano, y con los guantes mejorados (se le ven los
dedos: tres nudillos y el pulgar, en vez de una bola con rayas).

No toca los dibujos de la web: usa el mismo generador pero escribe en
marketing/instagram/personaje/svg/. Cada pose sale en las dos direcciones
(NOMBRE.svg y NOMBRE-izq.svg), con el 5 siempre al derecho.

Poses nuevas:
  elegante    chistera, monoculo y baston, con la mano en la cadera (el jefe)
  susurra     la mano junto a la cara, mirando de reojo (el cotilleo)
  palomitas   con un cubo de palomitas, mirando de lado (a ver que dicen)
  megafono    gritando con un megafono (¡COMENTA!)
  lupa        investigando con una lupa
  gota        sentada, con una gota de sudor (cuando no hay resenas)
  monoculo    de pie, solo con el monoculo, mirando por encima

Desde la raiz del repo:  python3 marketing/instagram/personaje/poses.py
"""
import importlib.util
import sys

sys.dont_write_bytecode = True        # que no deje gen/__pycache__ al importar el generador
import os

spec = importlib.util.spec_from_file_location('estrellita', 'gen/estrellita.py')
est = importlib.util.module_from_spec(spec)
spec.loader.exec_module(est)

SALIDA = 'marketing/instagram/personaje/svg'
os.makedirs(SALIDA, exist_ok=True)
est.SALIDA = SALIDA

# ── los guantes, con dedos ──
# Tres nudillos por el lado de fuera y la palma encima: el filo de la palma
# es lo que separa los dedos. El pulgar, donde estaba.
PULGAR = ('<path class="borde" fill="#F7F4EC" '
          'd="M-58 -34 C -92 -66, -126 -62, -138 -34 C -150 -6, -128 22, -92 24"/>')
est.GUANTE = f'''  <g id="guante">
    <circle class="borde" cx="54" cy="-40" r="33" fill="#F7F4EC"/>
    <circle class="borde" cx="74" cy="4" r="34" fill="#F7F4EC"/>
    <circle class="borde" cx="58" cy="48" r="32" fill="#F7F4EC"/>
    <circle class="borde" cx="0" cy="0" r="76" fill="#F7F4EC"/>
    {PULGAR}
    <g class="tinta" stroke-width="11" opacity=".55"><path d="M-6 -46 C 10 -40, 22 -30, 28 -18"/></g>
  </g>'''
est.GUANTE_LIKE = '''  <g id="guante-like">
    <circle class="borde" cx="-60" cy="-8" r="30" fill="#F7F4EC"/>
    <circle class="borde" cx="-64" cy="34" r="30" fill="#F7F4EC"/>
    <circle class="borde" cx="-44" cy="70" r="28" fill="#F7F4EC"/>
    <circle class="borde" cx="0" cy="0" r="76" fill="#F7F4EC"/>
    <path class="borde" fill="#F7F4EC"
          d="M-34 -48 C -76 -94, -68 -156, -30 -174 C 8 -192, 32 -154, 28 -90"/>
  </g>'''

ORO, TINTA, CREMA, ROJO = '#E9BC46', '#0A0E16', '#F7F4EC', '#D9383F'

# ── lo que lleva encima ──
CHISTERA = f'''<g transform="rotate(-12 512 60)">
  <rect class="borde" x="400" y="-170" width="210" height="220" rx="16" fill="{TINTA}"/>
  <rect x="412" y="0" width="186" height="34" fill="{ORO}"/>
  <path class="borde" fill="{TINTA}" d="M330 56 Q 505 20 690 56 Q 700 86 670 92 Q 505 66 350 92 Q 318 86 330 56 Z"/>
  <path d="M430 -150 L430 -10" stroke="#3A4460" stroke-width="16" stroke-linecap="round"/>
</g>'''

MONOCULO = f'''<g>
  <path d="M662 300 C 700 380, 690 470, 648 560" fill="none" stroke="{ORO}" stroke-width="10" stroke-dasharray="4 16" stroke-linecap="round"/>
  <circle cx="588" cy="232" r="104" fill="#BFE6FF" fill-opacity=".18" stroke="{TINTA}" stroke-width="40"/>
  <circle cx="588" cy="232" r="104" fill="none" stroke="{ORO}" stroke-width="16"/>
  <path d="M540 170 Q 560 150 596 150" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" opacity=".8"/>
</g>'''

BASTON = f'''<g>
  <path d="M868 690 L 896 1004" stroke="{TINTA}" stroke-width="40" stroke-linecap="round"/>
  <path d="M868 690 L 896 1004" stroke="#2A3448" stroke-width="16" stroke-linecap="round"/>
  <path d="M868 700 C 860 600, 760 590, 752 660" fill="none" stroke="{TINTA}" stroke-width="44" stroke-linecap="round"/>
  <path d="M868 700 C 860 600, 760 590, 752 660" fill="none" stroke="{ORO}" stroke-width="20" stroke-linecap="round"/>
  <circle cx="896" cy="1004" r="20" fill="{ORO}" stroke="{TINTA}" stroke-width="10"/>
</g>'''

PALOMITAS = f'''<g transform="translate(512 690)">
  <g class="borde">
    {''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFF3D1"/>' for x, y, r in
             ((-110, -118, 40), (-60, -150, 44), (0, -134, 46), (60, -154, 42), (112, -120, 40), (-30, -178, 34), (36, -196, 32)))}
  </g>
  <path class="borde" fill="{CREMA}" d="M-150 -100 L150 -100 L112 150 L-112 150 Z"/>
  <clipPath id="cubo"><path d="M-150 -100 L150 -100 L112 150 L-112 150 Z"/></clipPath>
  <g clip-path="url(#cubo)">{''.join(f'<rect x="{-150 + 60 * i}" y="-110" width="30" height="270" fill="{ROJO}"/>' for i in range(6))}</g>
  <path d="M-150 -100 L150 -100 L112 150 L-112 150 Z" fill="none" stroke="{TINTA}" stroke-width="26" stroke-linejoin="round"/>
  <circle cx="186" cy="-230" r="22" fill="#FFF3D1" stroke="{TINTA}" stroke-width="12"/>
</g>'''

MEGAFONO = f'''<g transform="translate(900 470) rotate(-14)">
  <path class="borde" fill="{ROJO}" d="M0 -46 L250 -150 L250 150 L0 46 Z"/>
  <ellipse class="borde" cx="250" cy="0" rx="36" ry="150" fill="{CREMA}"/>
  <rect class="borde" x="-50" y="-46" width="64" height="92" rx="14" fill="{CREMA}"/>
  <g stroke="{TINTA}" stroke-width="16" stroke-linecap="round" fill="none">
    <path d="M320 -120 L380 -170"/><path d="M340 0 L420 0"/><path d="M320 120 L380 170"/></g>
</g>'''

LUPA = f'''<g>
  <path d="M880 600 L 952 470" stroke="{TINTA}" stroke-width="54" stroke-linecap="round"/>
  <path d="M880 600 L 952 470" stroke="#6B3B12" stroke-width="30" stroke-linecap="round"/>
  <circle cx="1010" cy="370" r="118" fill="#BFE6FF" fill-opacity=".35" stroke="{TINTA}" stroke-width="44"/>
  <circle cx="1010" cy="370" r="118" fill="none" stroke="{ORO}" stroke-width="20"/>
  <path d="M950 300 Q 980 270 1024 272" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" opacity=".85"/>
</g>'''

GOTA = f'''<path d="M760 120 C 740 170, 722 196, 722 222 C 722 250, 742 268, 764 268 C 786 268, 806 250, 806 222 C 806 196, 786 170, 760 120 Z"
  fill="#8FD3FF" stroke="{TINTA}" stroke-width="14" stroke-linejoin="round"/>
<path d="M748 212 Q 746 236 764 246" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round"/>'''

q = est.quieta
NUEVAS = {
    'elegante':  ('elegante', dict(dx=10, dy=4, escala=1.0, parpado=.28),
                  lambda: q((236, 640), (868, 700), 60, -10, lleva=BASTON, lean=-3)),
    'susurra':   ('cuchicheando', dict(dx=34, dy=4, escala=1.1, parpado=.22),
                  lambda: q((236, 640), (700, 430), 60, 110, lean=6)),
    'palomitas': ('con palomitas', dict(dx=34, dy=6, escala=1.15, parpado=.12),
                  lambda: q((378, 786), (646, 786), 40, -40, lleva=PALOMITAS)),
    'megafono':  ('con megafono', dict(dx=12, dy=-6, escala=1.35),
                  lambda: q((110, 210), (904, 520), -40, -80, lleva=MEGAFONO)),
    'lupa':      ('con lupa', dict(dx=34, dy=-6, escala=1.25),
                  lambda: q((236, 640), (880, 600), 60, -40, lleva=LUPA, lean=4)),
    'gota':      ('sentada con gota', dict(dy=10, escala=.95, parpado=.3),
                  lambda: q((196, 1002), (828, 1002), -22, 22, bob=150, piernas=est.COLGANDO, lleva=GOTA)),
    'monoculo':  ('con monoculo', dict(dx=-10, dy=8, escala=.95, parpado=.3),
                  lambda: q((236, 640), (788, 640), 60, -60, lleva=MONOCULO)),
}
EXTRA = {'elegante': CHISTERA + MONOCULO}          # lo que va por encima de todo (la cabeza)

total, n = 0, 0
for nombre, (titulo, exp, cuerpo) in {**est.POSES, **NUEVAS}.items():
    dentro = cuerpo()
    if nombre in EXTRA:
        dentro += '\n' + EXTRA[nombre]
    total += est.escribe(nombre, titulo, est.cara(**exp), dentro, .3 + .21 * n)
    n += 1
# la chistera asoma por encima del dibujo: se le da aire arriba a todas
for f in os.listdir(SALIDA):
    p = os.path.join(SALIDA, f)
    s = open(p).read().replace('viewBox="-190 -40 1404 1260"', 'viewBox="-190 -240 1404 1560"')
    # en Instagram, un amarillo mas vivo que el oro de la web (la foto le quita color)
    s = s.replace('fill="#E9BC46"', 'fill="#FFD23A"')
    open(p, 'w').write(s)
print(f'{n} poses (x2 lados) en {SALIDA}, {total / 1024:.0f} KB')
