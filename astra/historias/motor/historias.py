"""Historias Astra (v2, estilo nativo de Instagram): texto repartido por la historia, sin contenedor.
uso: python3 historias.py spec.json carpeta_salida
spec = {"root": "...", "frames": [{"img": "banco/18.jpg", "foco": 0.5, "focox": 0.5, "bloques": [ ... ]}]}
bloque = {"tipo": "caja"|"negra"|"azul"|"grande"|"etiqueta"|"cta"|"nota",
          "texto": "líneas\\nseparadas", "y": 380 (borde superior), "x": "c"|"l"|"r", "size": 58, "rot": -3}
  caja     texto negro sobre fondo blanco por línea (clásico de IG)
  negra    texto blanco sobre fondo negro translúcido por línea
  azul     texto blanco sobre degradado azul Astra por línea
  grande   texto blanco grande con sombra, sin fondo
  etiqueta pastilla pequeña con borde (antetítulo)
  nota     texto pequeño con sombra
  cta      botón azul «Escríbeme X» + flechas hacia la barra de respuesta (texto = palabra)
Zonas seguras: no poner nada por encima de y=230 ni por debajo de y=1640 (salvo el cta).
"""
import sys, json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

R = os.path.dirname(os.path.abspath(__file__)) + '/res'
W, H = 1080, 1920
B1, B2 = (2, 158, 252), (2, 20, 235)
def F(w, s): return ImageFont.truetype(f'{R}/Montserrat-{w}.ttf', s)

def autocrop(im):
    a = np.asarray(im.convert('L')).astype(int)
    rows = np.where(a.std(1) > 6)[0]; cols = np.where(a.std(0) > 6)[0]
    if len(rows) and len(cols): im = im.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))
    return im

def cover(im, fy=0.5, fx=0.5):
    s = max(W / im.width, H / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int((im.width - W) * fx); y = int((im.height - H) * fy)
    return im.crop((x, y, x + W, y + H))

def grade(im):
    x = np.asarray(im).astype(np.float32) / 255
    x = x + 0.10 * (x - 0.5) * (1 - np.abs(2 * x - 1))
    x[..., 0] *= 1.03; x[..., 2] *= 0.96
    yy = np.linspace(0, 1, H)[:, None, None]
    shade = 1.04 - 0.22 * np.clip((yy - 0.70) / 0.3, 0, 1) - 0.18 * np.clip((0.12 - yy) / 0.12, 0, 1)
    return Image.fromarray((np.clip(x * shade, 0, 1) * 255).astype(np.uint8))

def grad(w, h):
    g = np.zeros((h, w, 4), np.uint8); t = np.linspace(0, 1, w)[None, :]
    for i in range(3): g[..., i] = (B1[i] * (1 - t) + B2[i] * t).astype(np.uint8)
    g[..., 3] = 255; return Image.fromarray(g)

def wrap(text, font, maxw):
    out = []
    for raw in text.split('\n'):
        line = ''
        for w in raw.split():
            t = (line + ' ' + w).strip()
            if line and font.getlength(t) > maxw: out.append(line); line = w
            else: line = t
        out.append(line)
    return out

def layer_lines(lines, font, estilo, align):
    """capa RGBA con cada línea sobre su propio fondo redondeado (como el texto con fondo de IG)"""
    padx, pady = int(font.size * 0.38), int(font.size * 0.20); lh = int(font.size * 1.18) + 2 * pady - 6
    ws = [int(font.getlength(l)) for l in lines]; mw = max(ws) + 2 * padx
    im = Image.new('RGBA', (mw + 40, lh * len(lines) + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (l, w) in enumerate(zip(lines, ws)):
        bw = w + 2 * padx
        x0 = 20 + {'c': (mw - bw) // 2, 'l': 0, 'r': mw - bw}[align]; y0 = 20 + i * lh
        box = (x0, y0, x0 + bw, y0 + lh + 2)
        if estilo == 'caja': d.rounded_rectangle(box, 16, fill=(255, 255, 255, 255)); col = (12, 12, 16)
        elif estilo == 'negra': d.rounded_rectangle(box, 16, fill=(0, 0, 0, 165)); col = (255, 255, 255)
        else:
            g = grad(bw, lh + 2); m = Image.new('L', g.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, bw - 1, lh + 1), 16, fill=255)
            im.paste(g, (x0, y0), m); col = (255, 255, 255)
        d.text((x0 + padx, y0 + pady - font.size * 0.06), l, font=font, fill=col)
    return im

def layer_shadow_text(lines, font, align, fill=(255, 255, 255)):
    lh = int(font.size * 1.2); ws = [font.getlength(l) for l in lines]; mw = int(max(ws))
    im = Image.new('RGBA', (mw + 60, lh * len(lines) + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (l, w) in enumerate(zip(lines, ws)):
        x = 30 + {'c': (mw - w) / 2, 'l': 0, 'r': mw - w}[align]
        d.text((x, 30 + i * lh), l, font=font, fill=fill)
    a = im.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda v: min(255, int(v * 0.9)))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(a)
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.alpha_composite(sh, (0, 4)); out.alpha_composite(im)
    return out

def place(base, lay, b):
    rot = b.get('rot', 0)
    if rot: lay = lay.rotate(rot, resample=Image.BICUBIC, expand=True)
    al = b.get('x', 'c'); y = int(b['y']) - 25
    x = {'c': (W - lay.width) // 2, 'l': 50, 'r': W - 50 - lay.width}[al]
    if isinstance(b.get('dx'), (int, float)): x += int(b['dx'])
    base.alpha_composite(lay, (x, y))
    return y, y + lay.height

def bloque(base, b):
    t = b.get('tipo', 'caja'); al = b.get('x', 'c')
    if t in ('caja', 'negra', 'azul'):
        f = F(800, b.get('size', 62)); return place(base, layer_lines(wrap(b['texto'], f, 900), f, t, al), b)
    elif t == 'grande':
        f = F(900, b.get('size', 84)); return place(base, layer_shadow_text(wrap(b['texto'], f, 940), f, al), b)
    elif t == 'nota':
        f = F(700, b.get('size', 42)); return place(base, layer_shadow_text(wrap(b['texto'], f, 900), f, al), b)
    elif t == 'etiqueta':
        f = F(800, b.get('size', 32)); s = b['texto']; w = int(f.getlength(s)) + 48
        im = Image.new('RGBA', (w + 8, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((4, 4, w + 3, 59), 28, fill=(0, 0, 0, 120), outline=(255, 255, 255, 230), width=3)
        d.text((28, 13), s, font=f, fill=(255, 255, 255)); return place(base, im, b)
    elif t == 'cta':
        f = F(900, b.get('size', 52)); s = f'Escríbeme «{b["texto"]}»'; bw = int(f.getlength(s)) + 120
        im = Image.new('RGBA', (bw + 80, 200), (0, 0, 0, 0))
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((40, 50, bw + 40, 170), 60, fill=(0, 0, 0, 150))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
        g = grad(bw, 120); m = Image.new('L', g.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, bw - 1, 119), 60, fill=255)
        im.paste(g, (40, 40), m); ImageDraw.Draw(im).text((100, 68), s, font=f, fill=(255, 255, 255))
        r = place(base, im, b)
        d = ImageDraw.Draw(base); ax = W / 2; ay = b['y'] + 175
        for k in range(3):
            yy = ay + k * 34
            d.line([(ax - 34, yy), (ax, yy + 26), (ax + 34, yy)], fill=(255, 255, 255, 230 - 60 * k), width=9, joint='curve')
        return r

def frame(fr, root):
    im = autocrop(ImageOps.exif_transpose(Image.open(os.path.join(root, fr['img']))).convert('RGB'))
    bg = grade(cover(im, fr.get('foco', 0.5), fr.get('focox', 0.5))).convert('RGBA')
    prev = None
    for b in fr['bloques']:
        b = dict(b)
        if prev and prev[0] - 10 <= b['y'] < prev[1] - 30:   # se solapa con el anterior: lo empuja debajo
            b['y'] = prev[1] - 30 + 8
        prev = bloque(bg, b)
    return bg.convert('RGB')

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.endswith('.jpg'): os.remove(os.path.join(out, f))
    root = spec.get('root', os.path.dirname(os.path.abspath(sys.argv[1])))
    for i, fr in enumerate(spec['frames'], 1):
        frame(fr, root).save(f'{out}/{i:02d}.jpg', quality=93)
    print(out, len(spec['frames']))
