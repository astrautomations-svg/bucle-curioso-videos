"""Historias Astra · estilo «cristal» (aprobado el 20-11-2026; ver estilo_cristal/maqueta.py).

uso: python3 cristal.py spec.json carpeta_salida
spec = {"root": "...", "seed": "AAAA-MM-DD", "frames": [frame, ...]}
frame = {"img": "banco/41.jpg", "foco": 0.5, "osc": 0.82, "cara": [x0, y0, x1, y1], "bloques": [bloque, ...]}
  "cara": caja de la cara (px sobre 1080x1920): ningún contenedor puede pisarla (el script avisa).
bloques (y = centro vertical en px sobre 1920; cx = centro horizontal; w = ancho; rot = grados, 1-3):
  etiqueta {"texto": "EL PROBLEMA", "x": 96, "y": 283}                        pastilla con punto verde
  titular  {"texto": "Son las 23:40.", "sub": "...", "y": 500, "w": 850}       titular grande + subtítulo
  wa       {"nombre": "Laura", "hora": "23:40", "texto": "...", "y": 790, "w": 720}   mensaje de WhatsApp
  fila     {"icono": "tiempo/luna", "texto": "...", "y": 1010, "w": 780}       icono 3D + frase corta
  cta      {"antes": "¿Cuántos...?", "texto": "NOCHE", "y": 1290, "w": 880}    pregunta + pastilla naranja
Iconos: res/iconos_glass/<carpeta>/<nombre>.png. Sin emojis.
Zona segura: nada por encima de y=230 ni por debajo de y=1640.
"""
import json, os, sys, random, hashlib, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance

AQUI = os.path.dirname(os.path.abspath(__file__))
IG = os.path.join(AQUI, 'res', 'iconos_glass')
FI = '/usr/share/fonts/opentype/inter/'
W, H = 1080, 1920; BL = (255, 255, 255); NAR = (255, 150, 70); SUB = (228, 234, 246)
_CAJAS = []

def F(w, s):
    n = {'b': 'InterDisplay-Bold.otf', 'sb': 'InterDisplay-SemiBold.otf', 'm': 'InterDisplay-Medium.otf', 'x': 'InterDisplay-ExtraBold.otf'}[w]
    try: return ImageFont.truetype(FI + n, s)
    except OSError:
        return ImageFont.truetype(os.path.join(AQUI, 'res', {'b': 'Montserrat-800.ttf', 'sb': 'Montserrat-700.ttf', 'm': 'Montserrat-600.ttf', 'x': 'Montserrat-900.ttf'}[w]), int(s * 0.92))

def fondo(path, fy=0.5, fx=0.5, osc=0.82):
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    im = ImageOps.fit(im, (W, H), Image.LANCZOS, centering=(fx, fy))
    im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=60, threshold=2))
    im = ImageEnhance.Brightness(im).enhance(osc)
    a = np.array(im).astype(float); y = np.linspace(0, 1, H)[:, None, None]
    a = a * (1 - 0.25 * y)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')

def tarjeta(base, cx, cy, w, h, ang, dibujar, r=42, a=0.16, blur=24):
    pad = 60
    x0, y0 = int(cx - w / 2 - pad), int(cy - h / 2 - pad)
    zona = base.crop((x0, y0, x0 + w + 2 * pad, y0 + h + 2 * pad)).convert('RGB').filter(ImageFilter.GaussianBlur(blur))
    z = np.array(zona).astype(float) * (1 - a) + 255 * a
    z = z + (1 - np.linspace(0, 1, z.shape[0])[:, None, None]) * 14
    vid = Image.fromarray(np.clip(z, 0, 255).astype(np.uint8)).crop((pad, pad, pad + w, pad + h)).convert('RGBA')
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    card = Image.new('RGBA', (w, h), (0, 0, 0, 0)); card.paste(vid, (0, 0), m)
    d = ImageDraw.Draw(card)
    d.rounded_rectangle((0, 0, w - 1, h - 1), r, outline=(255, 255, 255, 120), width=2)
    d.rounded_rectangle((3, 3, w - 4, h - 4), r - 3, outline=(255, 255, 255, 26), width=2)
    dibujar(card, d)
    big = Image.new('RGBA', (w + 120, h + 120), (0, 0, 0, 0))
    ImageDraw.Draw(big).rounded_rectangle((60, 76, 60 + w, 76 + h), r, fill=(0, 0, 0, 95))
    big = big.filter(ImageFilter.GaussianBlur(20)); big.alpha_composite(card, (60, 60))
    big = big.rotate(ang, resample=Image.BICUBIC, expand=True)
    base.alpha_composite(big, (int(cx - big.width / 2), int(cy - big.height / 2)))
    _CAJAS.append((int(cx - big.width / 2 + 50), int(cy - big.height / 2 + 50), int(cx + big.width / 2 - 50), int(cy + big.height / 2 - 50)))

def glass_ico(n, s):
    im = Image.open(f'{IG}/{n}.png').convert('RGBA'); im = im.crop(im.getbbox()); im.thumbnail((s, s), Image.LANCZOS); return im

def cuadro(card, xy, n, s=88):
    ic = glass_ico(n, int(s * 1.12)); x, y = xy
    card.alpha_composite(ic, (x + (s - ic.width) // 2, y + (s - ic.height) // 2))

def partir(d, t, f, w):
    if '\n' in t: return [l for par in t.split('\n') for l in partir(d, par, f, w)]
    out, cur = [], ''
    for p in t.split():
        z = (cur + ' ' + p).strip()
        if d.textlength(z, font=f) > w and cur: out.append(cur); cur = p
        else: cur = z
    out.append(cur)
    return out

def lineas(d, xy, t, f, fill, w, lh=1.18):
    x, y = xy
    for l in partir(d, t, f, w): d.text((x, y), l, font=f, fill=fill); y += int(f.size * lh)
    return y

_D = ImageDraw.Draw(Image.new('RGB', (10, 10)))
def alto(t, f, w, lh=1.18): return len(partir(_D, t, f, w)) * int(f.size * lh)

def etiqueta(base, b):
    t = b['texto']; f = F('b', 30); tw = int(_D.textlength(t, font=f))
    def dib(c, d): d.ellipse((26, 26, 40, 40), fill=(90, 220, 140)); d.text((56, 14), t, font=f, fill=BL)
    x = b.get('x', 96)
    tarjeta(base, x + (tw + 82) / 2, b['y'], tw + 82, 66, b.get('rot', -2), dib, r=33, a=0.2, blur=16)

def titular(base, b):
    w = b.get('w', 850); ft, fs = F('b', b.get('size', 64)), F('m', 38)
    h = 44 + alto(b['texto'], ft, w - 96) + (4 + alto(b['sub'], fs, w - 110) if b.get('sub') else 0) + 34
    def dib(c, d):
        y = lineas(d, (48, 44), b['texto'], ft, BL, w - 96)
        if b.get('sub'): lineas(d, (48, y + 4), b['sub'], fs, SUB, w - 110)
    tarjeta(base, b.get('cx', 530), b['y'], w, h, b.get('rot', 1.8), dib)

def wa(base, b):
    w = b.get('w', 720); fn, fm, fh = F('b', 36), F('m', 32), F('m', 26)
    h = 84 + alto(b['texto'], fm, w - 200, 1.2) + 32
    def dib(c, d):
        cuadro(c, (28, 30), b.get('icono', 'canales/whatsapp'), 112)
        d.text((158, 34), b['nombre'], font=fn, fill=BL)
        if b.get('hora'): d.text((w - 40 - d.textlength(b['hora'], font=fh), 40), b['hora'], font=fh, fill=(205, 214, 232))
        lineas(d, (158, 84), b['texto'], fm, SUB, w - 200, 1.2)
    tarjeta(base, b.get('cx', 580), b['y'], w, max(h, 164), b.get('rot', -3), dib, r=38, a=0.2)

def fila(base, b):
    w = b.get('w', 780); f = F('sb', 38); t = b['texto']
    def dib(c, d):
        cuadro(c, (22, 14), b['icono'], 96)
        lineas(d, (138, 30 if d.textlength(t, font=f) < w - 160 else 16), t, f, BL, w - 160, 1.12)
    tarjeta(base, b.get('cx', 540), b['y'], w, 124, b.get('rot', 2), dib, r=34, a=0.13)

def cta(base, b):
    w = b.get('w', 880); fa = F('b', 44); fp = F('x', 44)
    antes = b.get('antes', '¿Quieres uno así?')
    la = partir(_D, antes, fa, w - 96); ya = 40 + len(la) * 54
    pill = 'RESPONDE: «%s»' % b['texto']; pw = int(_D.textlength(pill, font=fp)) + 76
    h = ya + 30 + 84 + 40
    def dib(c, d):
        y = 40
        for l in la: d.text((48, y), l, font=fa, fill=BL); y += 54
        lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((48, ya + 30, 48 + pw, ya + 114), 42, fill=NAR + (245,)); c.alpha_composite(lay)
        ImageDraw.Draw(c).text((86, ya + 46), pill, font=fp, fill=BL)
    tarjeta(base, b.get('cx', 540), b['y'], w, h, b.get('rot', -1.2), dib, r=48, a=0.17)

TIPOS = dict(etiqueta=etiqueta, titular=titular, wa=wa, fila=fila, cta=cta)

def choca(a, b): return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]

def frame(fr, root, n):
    im = fondo(os.path.join(root, fr['img']), fr.get('foco', 0.5), fr.get('focox', 0.5), fr.get('osc', 0.82))
    _CAJAS.clear(); avisos = []
    for b in fr['bloques']:
        TIPOS[b['tipo']](im, b)
        c = _CAJAS[-1]
        if c[1] < 230 or c[3] > 1640 or c[0] < 20 or c[2] > W - 20: avisos.append(f'{n}: {b["tipo"]} fuera de zona {c}')
        if fr.get('cara') and choca(c, fr['cara']): avisos.append(f'{n}: {b["tipo"]} pisa la cara {c}')
        for o in _CAJAS[:-1]:
            if choca(c, o): avisos.append(f'{n}: {b["tipo"]} se solapa con {o}')
    return im.convert('RGB'), avisos

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.endswith('.jpg'): os.remove(os.path.join(out, f))
    root = spec.get('root', os.path.dirname(os.path.abspath(sys.argv[1])))
    todos = []
    for i, fr in enumerate(spec['frames'], 1):
        im, av = frame(fr, root, i); todos += av
        im.save(f'{out}/{i:02d}.jpg', quality=93)
    for a in todos: print('AVISO', a)
    print(out, len(spec['frames']))
