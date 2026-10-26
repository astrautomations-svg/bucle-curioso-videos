"""Historias Astra: genera una secuencia 1080x1920 desde un JSON.
uso: python3 historias.py spec.json carpeta_salida
spec = {"frames":[{"img":"banco/18.jpg","kicker":"DUEÑOS DE NEGOCIO","text":"¿Cuántas horas pierdes\n**contestando lo mismo?**","foco":0.5}, ... ,
         {"img":"banco/04.jpg","cta":"SISTEMA","text":"..."}]}
**palabra** = resaltado en pastilla azul Astra.
"""
import sys, json, os, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

R = os.path.dirname(os.path.abspath(__file__)) + '/res'
W, H = 1080, 1920
B1, B2 = (2, 158, 252), (2, 20, 235)
def F(w, s): return ImageFont.truetype(f'{R}/Montserrat-{w}.ttf', s)

def autocrop(im):
    a = np.asarray(im.convert('L')).astype(int)
    rows = np.where((a.std(1) > 6))[0]; cols = np.where((a.std(0) > 6))[0]
    if len(rows) and len(cols): im = im.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))
    return im

def cover(im, fy=0.5, fx=0.5):
    s = max(W / im.width, H / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int((im.width - W) * fx); y = int((im.height - H) * fy)
    return im.crop((x, y, x + W, y + H))

def grade(im, bw=False):
    x = np.asarray(im).astype(np.float32) / 255
    x = x + 0.10 * (x - 0.5) * (1 - np.abs(2 * x - 1))
    if not bw: x[..., 0] *= 1.03; x[..., 2] *= 0.96
    yy = np.linspace(0, 1, H)[:, None, None]
    shade = 1.06 - 0.50 * np.clip((yy - 0.42) / 0.5, 0, 1) ** 1.2 - 0.30 * np.clip((0.16 - yy) / 0.16, 0, 1)
    return Image.fromarray((np.clip(x * shade, 0, 1) * 255).astype(np.uint8))

def grad(w, h, r):
    g = np.zeros((h, w, 4), np.uint8); t = np.linspace(0, 1, w)[None, :]
    for i in range(3): g[..., i] = (B1[i] * (1 - t) + B2[i] * t).astype(np.uint8)
    g[..., 3] = 255; im = Image.fromarray(g)
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    im.putalpha(m); return im

def shadow(base, box, r, blur=30, alpha=110, off=10):
    sh = Image.new('RGBA', base.size, (0, 0, 0, 0)); x0, y0, x1, y1 = box
    ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + off, x1, y1 + off), r, fill=(0, 0, 0, alpha))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))

def glass(base, box, r=46):
    x0, y0, x1, y1 = map(int, box); shadow(base, box, r)
    reg = base.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(28))
    reg = Image.blend(reg.convert('RGB'), Image.new('RGB', reg.size, (18, 22, 40)), 0.42).convert('RGBA')
    m = Image.new('L', reg.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, reg.width - 1, reg.height - 1), r, fill=255)
    base.paste(reg, (x0, y0), m)
    ImageDraw.Draw(base).rounded_rectangle(box, r, outline=(255, 255, 255, 70), width=2)

def parse(line):
    return [(p[2:-2], True) if p.startswith('**') else (p, False) for p in re.split(r'(\*\*.+?\*\*)', line) if p]

def lay_text(text, font, maxw):
    """devuelve lineas de tokens [(palabra, hl)] ajustadas a maxw"""
    out = []
    for raw in text.split('\n'):
        toks = []
        for seg, hl in parse(raw):
            toks += [(w, hl) for w in seg.split()]
        line = []
        for tk in toks:
            test = line + [tk]
            if line and width(test, font) > maxw: out.append(line); line = [tk]
            else: line = test
        if line: out.append(line)
    return out

def width(line, font):
    return sum(font.getlength(w) for w, _ in line) + font.getlength(' ') * (len(line) - 1) + 28 * any(h for _, h in line)

def draw_lines(base, lines, font, cx, y, lh):
    d = ImageDraw.Draw(base); sp = font.getlength(' ')
    for line in lines:
        x = cx - width(line, font) / 2
        # agrupa tramos resaltados contiguos en una sola pastilla
        i = 0
        while i < len(line):
            w, hl = line[i]
            if hl:
                j = i; grp = []
                while j < len(line) and line[j][1]: grp.append(line[j][0]); j += 1
                s = ' '.join(grp); gw = font.getlength(s)
                p = grad(int(gw + 28), int(lh * 0.98), 18); base.alpha_composite(p, (int(x), int(y - lh * 0.06)))
                d.text((x + 14, y), s, font=font, fill=(255, 255, 255)); x += gw + 28 + sp; i = j
            else:
                d.text((x, y), w, font=font, fill=(255, 255, 255)); x += font.getlength(w) + sp; i += 1
        y += lh
    return y

def brand(base):
    logo = Image.open(f'{R}/astra_logo.png').convert('RGBA'); logo.thumbnail((54, 54))
    f = F(800, 30); t = 'ASTRA AUTOMATIONS'; w = int(f.getlength(t)) + logo.width + 64
    box = (W / 2 - w / 2, 250, W / 2 + w / 2, 250 + 76); glass(base, box, 38)
    base.alpha_composite(logo, (int(box[0] + 22), int(box[1] + 11)))
    ImageDraw.Draw(base).text((box[0] + 34 + logo.width, box[1] + 20), t, font=F(800, 30), fill=(255, 255, 255))

def frame(fr, root):
    im = autocrop(ImageOps.exif_transpose(Image.open(os.path.join(root, fr['img']))).convert('RGB'))
    bg = grade(cover(im, fr.get('foco', 0.5), fr.get('focox', 0.5))).convert('RGBA')
    if fr.get('marca', True): brand(bg)
    font = F(900, fr.get('size', 66)); lh = int(font.size * 1.28)
    lines = lay_text(fr['text'], font, 860)
    kick = fr.get('kicker'); cta = fr.get('cta')
    th = len(lines) * lh + (70 if kick else 0) + (190 if cta else 0) + (lh * 0.9 if fr.get('sub') else 0)
    top = fr.get('y', 1560 - th) - 60
    box = (60, top, W - 60, top + th + 110); glass(bg, box)
    y = top + 55; d = ImageDraw.Draw(bg)
    if kick:
        fk = F(800, 32); kw = fk.getlength(kick) + 40
        d.rounded_rectangle((W / 2 - kw / 2, y, W / 2 + kw / 2, y + 50), 25, outline=(120, 200, 255), width=3)
        d.text((W / 2 - kw / 2 + 20, y + 7), kick, font=fk, fill=(170, 225, 255)); y += 80
    y = draw_lines(bg, lines, font, W / 2, y, lh)
    if fr.get('sub'):
        fs = F(600, 38); s = fr['sub']; d.text((W / 2 - fs.getlength(s) / 2, y + 8), s, font=fs, fill=(225, 232, 245)); y += lh * 0.9
    if cta:
        fb = F(900, 52); t = f'Escríbeme «{cta}»'; bw = int(fb.getlength(t)) + 120
        bx = int(W / 2 - bw / 2); by = int(y + 40); shadow(bg, (bx, by, bx + bw, by + 120), 60, alpha=150)
        bg.alpha_composite(grad(bw, 120, 60), (bx, by))
        ImageDraw.Draw(bg).text((bx + 60, by + 28), t, font=fb, fill=(255, 255, 255))
        # flecha hacia la barra de respuesta
        ax = W / 2; ay = 1700
        d = ImageDraw.Draw(bg)
        for k in range(3):
            yy = ay + k * 34
            d.line([(ax - 34, yy), (ax, yy + 26), (ax + 34, yy)], fill=(255, 255, 255, 230 - 60 * k), width=9, joint='curve')
    return bg.convert('RGB')

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    root = spec.get('root', os.path.dirname(os.path.abspath(sys.argv[1])))
    for i, fr in enumerate(spec['frames'], 1):
        frame(fr, root).save(f'{out}/{i:02d}.jpg', quality=93); print(out, i)
