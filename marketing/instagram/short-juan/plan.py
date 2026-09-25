"""Plan del short: cortes (tiempos del original), encuadre, subtitulos y eventos (graficos y sonidos).
Saca plan.json con todo en tiempo de SALIDA."""
import json, numpy as np

FPS = 30
cara = json.load(open('cara.json'))
ct, cx = np.array(cara['t']), 1620 - np.array(cara['x'])

# (entra, sale, texto que se oye, layout, zoom)   layout: full = tu cara a pantalla completa
#                                                  split = grafico arriba y tu abajo
S = [
    (1.00, 1.98, '¿Veis esto?', 'split', 1.0),
    (2.60, 5.55, 'Hace que tus clientes te dejen la reseña en menos de 10 segundos.', 'split', 1.0),
    (5.98, 6.88, 'Me llamo Juan', 'full', 1.0),
    (7.18, 8.08, 'y tengo PLEA5E.', 'full', 1.12),
    (8.22, 11.78, 'Hacemos placas para restaurantes, bares y comercios locales.', 'split', 1.0),
    (12.10, 13.72, 'Tus clientes salen contentos…', 'full', 1.0),
    (13.98, 15.10, '…pero nadie te escribe.', 'full', 1.1),
    (15.45, 16.50, 'Y no es que no quieran:', 'full', 1.0),
    (16.70, 18.92, 'es que se les olvida o les da pereza buscarte.', 'full', 1.12),
    (19.38, 20.55, 'Con la placa en la mesa', 'split', 1.0),
    (20.82, 22.42, 'solo tienen que acercar el móvil', 'split', 1.0),
    (22.68, 23.40, 'y… ¡BOOM!', 'full', 1.14),
    (23.92, 24.82, 'Ya se abre.', 'split', 1.0),
    (10.52, 14.20, '¿Qué es lo que se abre? Las ganas del cliente para dejarte una reseña.', 'split', 1.0, 'nuevo-589238336.mov'),
    (29.15, 29.75, '¿Por qué?', 'full', 1.1),
    (29.97, 35.10, 'Porque no tienen que descargar nada, ni tener una app, ni tener que buscarte.', 'split', 1.0),
    (35.10, 36.85, 'Y si alguien tiene un móvil antiguo…', 'full', 1.0),
    (37.18, 38.82, 'tenemos el QR también.', 'split', 1.0),
    (38.82, 41.42, '¿Y por qué nosotros? Por tres simples motivos.', 'full', 1.1),
    (41.42, 43.62, 'La diseñamos con tu logo y tus colores.', 'split', 1.0),
    (43.62, 47.12, 'El diseño es gratis y no se imprime nada hasta que te guste.', 'split', 1.0),
    (49.70, 51.22, 'No te mandamos una placa y ya.', 'split', 1.0),
    (8.74, 13.36, 'Y te enseñamos a ti y a tu equipo cuándo y cómo pedir las reseñas,', 'split', 1.0, 'nuevo-589238853.mov'),
    (13.92, 16.16, 'que es lo que de verdad marca la diferencia.', 'full', 1.12, 'nuevo-589238853.mov'),
    (13.74, 18.62, 'Las placas son de pago único: las pagas una vez y son totalmente tuyas.', 'split', 1.0, 'nuevo-589239006.mov'),
    (61.40, 63.42, 'Y hablas conmigo directamente por WhatsApp.', 'split', 1.0),
    (63.74, 66.00, 'Somos de Córdoba y enviamos a toda España.', 'full', 1.0),
    (66.52, 67.85, '¿Quieres ver cómo quedaría la tuya?', 'full', 1.12),
    (68.45, 69.35, 'Comenta PLACA', 'split', 1.0),
    (70.25, 72.85, 'y te mandamos tu diseño.', 'full', 1.0),
]

seg, t = [], 0.0
CARAS = {}
for i, (a, b, txt, lay, z, *src) in enumerate(S):
    src = src[0] if src else 'original.mov'
    if src not in CARAS:
        cj = json.load(open('cara.json' if src == 'original.mov' else src.replace('.mov', '') + '-cara.json'))
        CARAS[src] = (np.array(cj['t']), 1620 - np.array(cj['x']))
    ct, cx = CARAS[src]
    a, b = round(a * FPS) / FPS, round(b * FPS) / FPS
    m = (ct >= a - .3) & (ct <= b + .3)
    x = float(np.median(cx[m])) if m.sum() >= 2 else float(np.median(cx))
    d = b - a
    seg.append(dict(i=i, a=a, b=b, t0=round(t, 4), t1=round(t + d, 4), txt=txt, lay=lay, z=z, cx=x, src=src))
    t += d
TOTAL = t

# palabras: repartidas en el trozo segun lo largas que son (con un pelin de adelanto)
pal = []
for s in seg:
    ws = s['txt'].split()
    pesos = [len(w.strip('¿?¡!.,:…')) + 2 for w in ws]
    tot = sum(pesos); acc = 0
    dur = (s['t1'] - s['t0']) * .96
    for w, p in zip(ws, pesos):
        pal.append(dict(w=w, t0=round(s['t0'] + dur * acc / tot - .04, 3), t1=round(s['t0'] + dur * (acc + p) / tot - .04, 3), s=s['i']))
        acc += p

# paginas de subtitulo: 1-3 palabras, sin pasar de ~16 letras, cortando en la puntuacion
paginas, cur = [], []
for p in pal:
    cur.append(p)
    largo = sum(len(q['w']) for q in cur) + len(cur) - 1
    if len(cur) >= 3 or largo >= 14 or p['w'][-1] in '.?!,:…' or (pal.index(p) + 1 < len(pal) and pal[pal.index(p) + 1]['s'] != p['s']):
        paginas.append(cur); cur = []
if cur: paginas.append(cur)
subs = [dict(t0=pg[0]['t0'], t1=pg[-1]['t1'], w=[dict(w=q['w'], t0=q['t0'], t1=q['t1']) for q in pg]) for pg in paginas]
# que cada pagina dure hasta que empiece la siguiente (sin huecos)
for k in range(len(subs) - 1):
    subs[k]['t1'] = subs[k + 1]['t0']
subs[-1]['t1'] = min(TOTAL, subs[-1]['t1'] + .3)

T = lambda i, off=0.0: round(seg[i]['t0'] + off, 3)
def palabra(i, trozo):
    for p in pal:
        if p['s'] == i and trozo.lower() in p['w'].lower():
            return p['t0']
    raise KeyError(trozo)

# graficos (arriba en split; encima en full) y sonidos, en tiempo de salida
ev = [
    dict(k='placa', t0=T(0), t1=seg[1]['t1']),
    dict(k='badge10', t0=palabra(1, 'menos'), t1=seg[1]['t1']),
    dict(k='nombre', t0=T(2, .1), t1=seg[3]['t1']),
    dict(k='negocios', t0=T(4), t1=seg[4]['t1'], pops=[palabra(4, 'restaurantes'), palabra(4, 'bares'), palabra(4, 'comercios')]),
    dict(k='estrellas', t0=T(5, .2), t1=seg[5]['t1']),
    dict(k='cero', t0=palabra(6, 'nadie'), t1=seg[6]['t1']),
    dict(k='bicho', pose='gota', t0=palabra(8, 'pereza'), t1=seg[8]['t1']),
    dict(k='foto', t0=T(9), t1=seg[10]['t1']),
    dict(k='movil', t0=palabra(10, 'acercar'), t1=seg[10]['t1'], fase='llega'),
    dict(k='boom', t0=palabra(11, 'BOOM'), t1=seg[11]['t1']),
    dict(k='movil', t0=T(12), t1=seg[13]['t1'], fase='abre'),
    dict(k='pregunta', t0=T(14), t1=seg[14]['t1']),
    dict(k='lista', t0=T(15), t1=seg[15]['t1'], pops=[palabra(15, 'descargar'), palabra(15, 'app'), palabra(15, 'buscarte')]),
    dict(k='qr', t0=T(17), t1=seg[17]['t1']),
    dict(k='tres', t0=palabra(18, 'tres'), t1=seg[18]['t1']),
    dict(k='motivo1', t0=T(19), t1=seg[20]['t1'], gratis=palabra(20, 'gratis'), guste=palabra(20, 'imprime')),
    dict(k='motivo2', t0=T(21), t1=seg[22]['t1']),
    dict(k='motivo3', t0=T(24), t1=seg[24]['t1'], tuya=palabra(24, 'tuya')),
    dict(k='whatsapp', t0=T(25), t1=seg[25]['t1']),
    dict(k='espana', t0=palabra(26, 'Córdoba'), t1=seg[26]['t1']),
    dict(k='comenta', t0=T(28), t1=seg[28]['t1']),
    dict(k='final', t0=T(29, 2.02), t1=TOTAL),
]
# destellos al cambiar de pantalla completa a partida y al reves
for a_, b_ in zip(seg[:-1], seg[1:]):
    if a_['lay'] != b_['lay']:
        ev.append(dict(k='flash', t0=round(b_['t0'], 3), t1=round(b_['t0'] + .16, 3)))
# confeti
for t_ in [palabra(20, 'gratis'), palabra(24, 'tuya')]:
    ev.append(dict(k='confeti', t0=round(t_, 3), t1=round(t_ + 1.6, 3)))


# sonidos: (archivo, tiempo, volumen)   E = sonidos de edicion (los de los videos de referencia)
V = 'sonidos/virales/'; E_ = 'sonidos/edicion/'
sw = lambda t, v=.45: (E_ + 'arrow-swoosh.mp3', t - .18, v)
sfx = [
    (E_ + 'woah-drop.mp3', T(0) - .05, .8),
    (E_ + 'camera-shutter.mp3', T(0, .05), .5),
    sw(T(1)),
    (E_ + 'ding.mp3', palabra(1, 'menos'), .5),
    sw(T(2), .35),
    (E_ + 'mouse-click.mp3', palabra(4, 'restaurantes'), .7), (E_ + 'mouse-click.mp3', palabra(4, 'bares'), .7), (E_ + 'mouse-click.mp3', palabra(4, 'comercios'), .7),
    (V + 'grillos.mp3', palabra(6, 'nadie'), .3),
    (V + 'bruh.mp3', palabra(8, 'pereza') + .25, .45),
    sw(T(9)),
    (E_ + 'camera-shutter.mp3', T(9, .1), .45),
    (E_ + 'arrow-swoosh-2.mp3', palabra(10, 'acercar') - .1, .4),
    (E_ + 'woah-drop.mp3', palabra(11, 'BOOM') - .08, .85),
    (E_ + 'ding.mp3', T(12, .1), .45),
    (E_ + 'mac-typing.mp3', T(13, 2.3), .35),
    (V + 'huh.mp3', T(14), .4),
    (E_ + 'mouse-click.mp3', palabra(15, 'descargar'), .7), (E_ + 'mouse-click.mp3', palabra(15, 'app'), .7), (E_ + 'mouse-click.mp3', palabra(15, 'buscarte'), .7),
    (E_ + 'camera-screenshot.mp3', T(17, .15), .5),
    (E_ + 'metallic-riser.mp3', palabra(18, 'tres') - 1.3, .4),
    (E_ + 'cinematic-impact.mp3', palabra(18, 'tres'), .55),
    sw(T(19)),
    (E_ + 'ding.mp3', palabra(20, 'gratis'), .5),
    sw(T(21)),
    sw(T(24)),
    (E_ + 'woah-drop.mp3', palabra(24, 'tuya') - .05, .6),
    (E_ + 'mouse-click.mp3', T(25, .15), .7),
    (E_ + 'ding.mp3', palabra(26, 'España'), .4),
    (E_ + 'punch-riser.mp3', T(28) - 1.1, .35),
    (E_ + 'mac-typing.mp3', T(28, .25), .35),
    (V + 'airhorn.mp3', T(28, .05), .2),
]
sfx = [s for s in sfx if s[2] > 0]
json.dump(dict(fps=FPS, total=TOTAL, seg=seg, subs=subs, ev=ev, sfx=sfx), open('plan.json', 'w'), ensure_ascii=False, indent=1)
print('duracion', round(TOTAL, 2), 's ·', len(seg), 'cortes ·', len(subs), 'subtitulos ·', len(ev), 'graficos ·', len(sfx), 'sonidos')
