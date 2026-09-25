"""Plan del short: cortes (tiempos del original), encuadre, subtitulos y eventos (graficos y sonidos).
Saca plan.json con todo en tiempo de SALIDA."""
import json, numpy as np

FPS = 30
cara = json.load(open('cara.json'))
ct, cx = np.array(cara['t']), np.array(cara['x'])

# (entra, sale, texto que se oye, layout, zoom)   layout: full = tu cara a pantalla completa
#                                                  split = grafico arriba y tu abajo
S = [
    (1.00, 1.98, '¿Veis esto?', 'split', 1.0),
    (2.60, 5.55, 'Hace que tus clientes te dejen la reseña en menos de 10 segundos.', 'split', 1.0),
    (5.98, 6.88, 'Me llamo Juan', 'full', 1.0),
    (7.18, 7.95, 'y tengo PLEA5E.', 'full', 1.12),
    (8.22, 11.78, 'Hacemos placas para restaurantes, bares y comercios locales.', 'split', 1.0),
    (12.10, 13.72, 'Tus clientes salen contentos…', 'full', 1.0),
    (13.98, 15.10, '…pero nadie te escribe.', 'full', 1.1),
    (15.45, 16.50, 'Y no es que no quieran:', 'full', 1.0),
    (16.70, 18.92, 'es que se les olvida o les da pereza buscarte.', 'full', 1.12),
    (19.38, 20.55, 'Con la placa en la mesa', 'split', 1.0),
    (20.82, 22.42, 'solo tienen que acercar el móvil', 'split', 1.0),
    (22.68, 23.40, 'y… ¡BOOM!', 'full', 1.14),
    (23.92, 24.82, 'Ya se abre.', 'split', 1.0),
    (25.18, 28.85, '¿Qué es lo que se abre? Las ganas de tu cliente de dejarte la reseña.', 'split', 1.0),
    (29.15, 29.75, '¿Por qué?', 'full', 1.1),
    (29.97, 35.10, 'Porque no tienen que descargar nada, ni tener una app, ni tener que buscarte.', 'split', 1.0),
    (35.10, 36.85, 'Y si alguien tiene un móvil antiguo…', 'full', 1.0),
    (37.18, 38.82, 'tenemos el QR también.', 'split', 1.0),
    (38.82, 41.42, '¿Y por qué nosotros? Por tres simples motivos.', 'full', 1.1),
    (41.42, 43.62, 'La diseñamos con tu logo y tus colores.', 'split', 1.0),
    (43.62, 47.12, 'El diseño es gratis y no se imprime nada hasta que te guste.', 'split', 1.0),
    (49.70, 53.62, 'No te mandamos una placa y ya. Te enseñamos a ti y a tu equipo cuándo y', 'split', 1.0),
    (54.30, 54.90, 'cómo pedirla.', 'split', 1.0),
    (55.30, 57.12, 'Y es lo que de verdad marca la diferencia.', 'full', 1.12),
    (57.12, 60.80, 'Las placas: pago único. La pagas una vez y es tuya.', 'split', 1.0),
    (61.40, 63.42, 'Y hablas conmigo directamente por WhatsApp.', 'split', 1.0),
    (63.74, 66.00, 'Somos de Córdoba y enviamos a toda España.', 'full', 1.0),
    (66.52, 67.85, '¿Quieres ver cómo quedaría la tuya?', 'full', 1.12),
    (68.45, 69.35, 'Comenta PLACA', 'split', 1.0),
    (70.25, 72.26, 'y te mandamos tu diseño.', 'split', 1.0),
]

seg, t = [], 0.0
for i, (a, b, txt, lay, z) in enumerate(S):
    a, b = round(a * FPS) / FPS, round(b * FPS) / FPS
    m = (ct >= a - .3) & (ct <= b + .3)
    x = float(np.median(cx[m])) if m.sum() >= 2 else float(np.median(cx))
    d = b - a
    seg.append(dict(i=i, a=a, b=b, t0=round(t, 4), t1=round(t + d, 4), txt=txt, lay=lay, z=z, cx=x))
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
subs[-1]['t1'] = TOTAL

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
    dict(k='final', t0=T(29), t1=TOTAL),
]

# sonidos: (archivo, tiempo, volumen)
V = 'sonidos/virales/'; B = 'sonidos/'
sfx = [
    (V + 'vine-boom.mp3', T(0), .55),
    (B + 'whoosh.mp3', T(1) - .12, .5),
    (B + 'pop.mp3', palabra(1, 'menos'), .6),
    (B + 'whoosh-short.mp3', T(2), .45),
    (B + 'pop.mp3', palabra(4, 'restaurantes'), .5), (B + 'pop.mp3', palabra(4, 'bares'), .5), (B + 'pop.mp3', palabra(4, 'comercios'), .5),
    (B + 'sparkle.mp3', T(5, .2), .45),
    (V + 'grillos.mp3', palabra(6, 'nadie'), .35),
    (V + 'bruh.mp3', palabra(8, 'pereza') + .25, .5),
    (B + 'whoosh.mp3', T(9) - .12, .5),
    (B + 'whoosh-cinematic.mp3', palabra(10, 'acercar'), .4),
    (V + 'vine-boom.mp3', palabra(11, 'BOOM'), .6),
    (V + 'ding.mp3', T(12, .1), .35),
    (B + 'sparkle.mp3', T(13, 2.2), .4),
    (V + 'huh.mp3', T(14), .45),
    (B + 'glitch-1.mp3', palabra(15, 'descargar'), .5), (B + 'glitch-2.mp3', palabra(15, 'app'), .5), (B + 'glitch-3.mp3', palabra(15, 'buscarte'), .5),
    (B + 'ping.mp3', T(17, .2), .5),
    (B + 'riser.mp3', T(18) - .2, .35),
    (B + 'impact-bass-1.mp3', palabra(18, 'tres'), .6),
    (B + 'whoosh.mp3', T(19) - .12, .5),
    (V + 'ding.mp3', palabra(20, 'gratis'), .35),
    (B + 'whoosh.mp3', T(21) - .12, .5),
    (B + 'whoosh.mp3', T(24) - .12, .5),
    (B + 'chime.mp3', palabra(24, 'tuya'), .4),
    (B + 'notification.mp3', T(25, .15), .55),
    (B + 'pop.mp3', palabra(26, 'España'), .5),
    (V + 'wait-a-minute.mp3', T(27), .0),   # reservado, apagado
    (V + 'airhorn.mp3', T(28), .28),
    (B + 'whoosh.mp3', T(29) - .12, .5),
    (B + 'sparkle.mp3', T(29, .8), .45),
]
sfx = [s for s in sfx if s[2] > 0]
json.dump(dict(fps=FPS, total=TOTAL, seg=seg, subs=subs, ev=ev, sfx=sfx), open('plan.json', 'w'), ensure_ascii=False, indent=1)
print('duracion', round(TOTAL, 2), 's ·', len(seg), 'cortes ·', len(subs), 'subtitulos ·', len(ev), 'graficos ·', len(sfx), 'sonidos')
