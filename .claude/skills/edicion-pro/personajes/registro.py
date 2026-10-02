"""registro.py — prepara peeps.mjs (registro estático de Open Peeps + compositor Effigy sin require dinámico).
Pasos (una vez, en una carpeta de trabajo):
  npm init -y && npm i react@18 react-dom@18 @opeepsfun/open-peeps esbuild
  python3 registro.py            # crea peeps.mjs
  cp <skill>/personajes/genera.mjs . && npx esbuild genera.mjs --bundle --platform=node --format=cjs --outfile=genera.cjs
  node genera.cjs reparto.json salida/
Open Peeps: ilustraciones de Pablo Stanley (CC0); paquete npm @opeepsfun/open-peeps (MIT)."""
import os, re
B = 'node_modules/@opeepsfun/open-peeps/build'
imp, reg = [], {}
for cat, d in [('head', 'head'), ('face', 'face'), ('body', 'body/effigy'), ('beard', 'beard'), ('accessory', 'accessory'),
               ('standing', 'body/standing'), ('sitting', 'body/sitting')]:
    reg[cat] = []
    for f in sorted(os.listdir(f'{B}/{d}')):
        if f.endswith('.js') and f != 'index.js':
            n = f[:-3]; v = f'{cat}_{n}'
            imp.append(f"import {v} from '@opeepsfun/open-peeps/build/{d}/{n}.js';"); reg[cat].append((n, v))
src = open(f'{B}/Effigy.js').read()
for cat, pat in [('head', './head/'), ('face', './face/'), ('body', './body/effigy/'), ('beard', './beard/'), ('accessory', './accessory/')]:
    src = re.sub(r'require\("' + re.escape(pat) + r'"\.concat\((\w+)\.type\)\)', lambda m: f'{{default: R.{cat}[{m.group(1)}.type]}}', src)
src = src.replace('import React from "react";', '')
out = ['import React from "react";', 'import { renderToStaticMarkup } from "react-dom/server";'] + imp
out.append('const R={' + ','.join(f'{c}:{{' + ','.join(f'"{n}":{v}' for n, v in L) + '}' for c, L in reg.items()) + '};')
out.append(src)
out.append('export { R, renderToStaticMarkup, React, createHair, createFace, createBeard, createAccessory, createHead };')
open('peeps.mjs', 'w').write('\n'.join(out))
print({k: len(v) for k, v in reg.items()})
