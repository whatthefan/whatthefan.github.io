"""Hace generador-por-capas.html: una copia del generador de la web
(public/taller/generador.html) con interruptores para esconder cada capa
de la placa. window.OC = {banda: true, qr: true, ...} esconde las que se
digan. Solo para marketing: el generador de verdad no se toca.

Desde la raiz del repo:  python3 marketing/instagram/carrusel-placa/montar-generador.py
"""
import re

C = 'marketing/instagram/carrusel-placa/'
s = open('public/taller/generador.html').read()
O = "(window.OC||{})"
CAPAS = [  # (lo que se pinta, la capa que lo esconde)
    ('banda(bx, by, bw, bh, radio, altoBanda', 'banda'), ('rayasYEstrellas(', 'adornos'),
    ('bloque(t, ', 'titulo'), ('insignia(', 'g'), ('dibujaNfc(icoX', 'nfc'),
    ('dibujaQR(enlaceQR()', 'qr'), ('esquinas(', 'marco'), ('bloque(tIns,', 'instr'),
    ('zonaCliente(', 'cliente'), ('pie(bx, by, bw, bh, radio,', 'pie'),
    ('minisEstrellas(', 'pie'), ('adornoAbajo(', 'adornos'),
]
for trozo, capa in CAPAS:
    # la llamada, no la definicion ("function trozo(") ni otra palabra que acabe igual
    patron = r'(?<![\w.])(?<!function )' + re.escape(trozo)
    s, n = re.subn(patron, f'{O}.{capa} || ' + trozo.replace('\\', '\\\\'), s)
    print(f'{capa:8} {n}  {trozo}')
fondo = "cx.fillStyle = est.fondo;\n    if (sang)"
assert fondo in s
s = s.replace(fondo, f"cx.fillStyle = {O}.fondo ? 'rgba(0,0,0,0)' : est.fondo;\n    if (sang)")
for a, b in (("if (est.conTel && TELEFONO)", f"if (est.conTel && TELEFONO && !{O}.tel)"),
             ("if (conLema) {\n      espaciado(", f"if (conLema && !{O}.lema) {{\n      espaciado(")):
    assert a in s, a
    s = s.replace(a, b)
open(C + 'generador-por-capas.html', 'w').write(s)
