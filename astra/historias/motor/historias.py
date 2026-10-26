"""Historias Astra v3: el estilo de las historias de Astra (garabatos de neón, pastillas de colores,
iconos y logos de apps, tarjetas de chat, títulos condensados), con la marca de ahora (azul Astra).

uso: python3 historias.py spec.json carpeta_salida
spec = {"root": "...", "seed": "2026-10-27", "frames": [frame, ...]}
frame = {"img": "banco/18.jpg", "foco": 0.5, "focox": 0.5, "garabato": true, "bloques": [bloque, ...]}
Las flechas ➡➡ de «sigue» se ponen solas en todas menos la última.

bloques (y = borde superior en px sobre 1920; x = "c" | "l" | "r"; rot = grados):
  titulo  {"texto": "EL PROBLEMA:"}                      condensado grande sobre caja azul
  linea   {"texto": "...", "color": "azul|blanco|amarillo|verde|rojo|naranja|negro",
           "icono": "nombre", "lado": "d|i", "size": 62}  pastilla de color (Oswald) con icono opcional al lado
  texto   {"texto": "...", "size": 50, "color": "blanco|azul|amarillo"}   Montserrat con sombra
  numero  {"texto": "+22 h", "sub": "al mes", "size": 190}               número grande con brillo de neón
  chat    {"mensajes": [["in", "¿Hay hueco el jueves?"], ["out", "Sí, a las 17:00 ✅"]], "titulo": "WhatsApp"}
  iconos  {"iconos": ["logo-whatsapp", "logo-gmail", ...], "size": 130}   fila de iconos en pastillas
  cta     {"texto": "SISTEMA", "antes": "¿Quieres uno así?"}             «RESPONDE: "SISTEMA"» + icono buzón
Iconos disponibles: los .png de res/iconos (sin extensión). Logos: logo-whatsapp, logo-gmail,
logo-googlecalendar, logo-n8n, logo-claude, logo-instagram, logo-calendly, logo-google.
Zona segura: nada por encima de y=240 ni por debajo de y=1600 (salvo cta/flechas).
"""
import sys, json, os, math, random, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageChops

R = os.path.dirname(os.path.abspath(__file__)) + '/res'
W, H = 1080, 1920
AZUL = (30, 123, 255); B1, B2 = (2, 158, 252), (2, 20, 235)
COL = {  # fondo, texto
    'azul': ((38, 132, 255), (255, 255, 255)), 'blanco': ((255, 255, 255), (15, 15, 20)),
    'amarillo': ((255, 214, 64), (214, 80, 0)), 'verde': ((196, 245, 150), (24, 140, 40)),
    'rojo': ((232, 48, 72), (255, 255, 255)), 'naranja': ((255, 112, 40), (255, 255, 255)),
    'negro': ((10, 10, 14), (255, 255, 255)), 'celeste': ((120, 205, 255), (8, 40, 120)),
}
def MF(w, s): return ImageFont.truetype(f'{R}/Montserrat-{w}.ttf', s)
def OF(s, wght=650):
    f = ImageFont.truetype(f'{R}/Oswald.ttf', s)
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f
def icono(n, s): return Image.open(f'{R}/iconos/{n}.png').convert('RGBA').resize((s, s), Image.LANCZOS)

# ---------- fondo ----------
def autocrop(im):
    a = np.asarray(im.convert('L')).astype(int)
    rows = np.where(a.std(1) > 6)[0]; cols = np.where(a.std(0) > 6)[0]
    if len(rows) and len(cols): im = im.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))
    return im

def cover(im, fy=0.5, fx=0.5):
    s = max(W / im.width, H / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = int((im.width - W) * fx); y = int((im.height - H) * fy)
    return im.crop((x, y, x + W, y + H))

def grade(im, osc=0.62):
    x = np.asarray(im).astype(np.float32) / 255
    x = x + 0.12 * (x - 0.5) * (1 - np.abs(2 * x - 1))
    x = x * osc; x[..., 2] = x[..., 2] * 1.06 + 0.015; x[..., 0] *= 0.97
    return Image.fromarray((np.clip(x, 0, 1) * 255).astype(np.uint8))

# ---------- efectos ----------
def glow(lay, color=AZUL, r=22, k=1.6):
    """halo de neón alrededor de una capa"""
    pad = r * 2; big = Image.new('RGBA', (lay.width + 2 * pad, lay.height + 2 * pad), (0, 0, 0, 0))
    big.alpha_composite(lay, (pad, pad))
    a = big.split()[3].filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(r)).point(lambda v: min(255, int(v * k)))
    g = Image.new('RGBA', big.size, color + (0,)); g.putalpha(a)
    out = Image.new('RGBA', big.size, (0, 0, 0, 0)); out.alpha_composite(g); out.alpha_composite(big)
    return out, pad

def catmull(pts, n=24):
    out = []
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = map(np.array, P[i - 1:i + 3])
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(np.array(pts[-1])); return [tuple(p) for p in out]

def garabato(base, rnd):
    """línea de neón a mano alzada que serpentea por la historia, con uno o dos bucles"""
    pts = []; y = rnd.uniform(200, 420); x = rnd.choice([-60, W + 60]); pts.append((x, y))
    side = 1 if x < 0 else -1; nloops = rnd.choice([1, 2, 2])
    for i in range(rnd.randint(3, 5)):
        y += rnd.uniform(220, 380); x = W / 2 + side * rnd.uniform(220, 470); side = -side
        pts.append((x, min(y, 1700)))
        if nloops and rnd.random() < 0.5:
            nloops -= 1; r = rnd.uniform(40, 75); cx, cy = x, y
            for a in np.linspace(0, 2 * math.pi, 7)[1:]:
                pts.append((cx + r * math.sin(a) * (-side), cy - r + r * math.cos(a)))
    pts.append((rnd.choice([-60, W + 60]), min(y + 200, 1880)))
    line = catmull(pts)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.line(line, fill=AZUL + (255,), width=46, joint='curve')
    g = lay.filter(ImageFilter.GaussianBlur(26))
    core = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dc = ImageDraw.Draw(core)
    dc.line(line, fill=(140, 200, 255, 255), width=16, joint='curve')
    core = core.filter(ImageFilter.GaussianBlur(5))
    dc2 = ImageDraw.Draw(core); dc2.line(line, fill=(255, 255, 255, 255), width=7, joint='curve')
    base.alpha_composite(g); base.alpha_composite(g); base.alpha_composite(core)

# ---------- piezas ----------
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

def pill_icon(n, s=96):
    im = Image.new('RGBA', (int(s * 1.7), s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, im.width - 1, s - 1), s // 2, fill=(255, 255, 255, 250))
    ic = icono(n, int(s * 0.66)); im.alpha_composite(ic, ((im.width - ic.width) // 2, (s - ic.height) // 2))
    return im

def caja_lineas(lines, font, bg, fg, align='c', pad=(22, 6), radius=8):
    lh = int(font.size * 1.22); ws = [int(font.getlength(l)) for l in lines]; mw = max(ws) + 2 * pad[0]
    im = Image.new('RGBA', (mw, lh * len(lines) + 2 * pad[1]), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pos = []
    for i, (l, w) in enumerate(zip(lines, ws)):
        bw = w + 2 * pad[0]; x0 = {'c': (mw - bw) // 2, 'l': 0, 'r': mw - bw}[align]; y0 = i * lh
        d.rectangle((x0, y0, x0 + bw, y0 + lh + 2 * pad[1]), fill=bg + (255,)); pos.append((x0, y0, l))
    for x0, y0, l in pos:
        d.text((x0 + pad[0], y0 + pad[1] + lh * 0.02), l, font=font, fill=fg)
    return im

def sombra_texto(lines, font, align, fill):
    lh = int(font.size * 1.22); ws = [font.getlength(l) for l in lines]; mw = int(max(ws))
    im = Image.new('RGBA', (mw + 60, lh * len(lines) + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (l, w) in enumerate(zip(lines, ws)):
        d.text((30 + {'c': (mw - w) / 2, 'l': 0, 'r': mw - w}[align], 30 + i * lh), l, font=font, fill=fill)
    a = im.split()[3].filter(ImageFilter.GaussianBlur(9))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(a)
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.alpha_composite(sh, (0, 4)); out.alpha_composite(sh, (0, 4)); out.alpha_composite(im)
    return out

def hjoin(a, b, gap=18):
    h = max(a.height, b.height); im = Image.new('RGBA', (a.width + gap + b.width, h), (0, 0, 0, 0))
    im.alpha_composite(a, (0, (h - a.height) // 2)); im.alpha_composite(b, (a.width + gap, (h - b.height) // 2)); return im

def chat_card(msgs, titulo=None):
    f = MF(600, 34); maxw = 600; padding = 26; rows = []
    for who, t in msgs:
        ls = wrap(t, f, maxw); w = int(max(f.getlength(l) for l in ls)) + 44; h = len(ls) * 44 + 30
        rows.append((who, ls, w, h))
    top = 70 if titulo else 26
    Hc = top + sum(r[3] + 16 for r in rows) + 20; Wc = 820
    im = Image.new('RGBA', (Wc, Hc), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, Wc - 1, Hc - 1), 36, fill=(11, 20, 26, 245))
    if titulo:
        im.alpha_composite(icono('logo-whatsapp', 40), (28, 16)); d.text((80, 18), titulo, font=MF(700, 30), fill=(230, 235, 240))
        d.line((24, 64, Wc - 24, 64), fill=(255, 255, 255, 40), width=2)
    y = top
    for who, ls, w, h in rows:
        x = padding if who == 'in' else Wc - padding - w
        d.rounded_rectangle((x, y, x + w, y + h), 18, fill=(32, 44, 51) if who == 'in' else (0, 92, 75))
        for i, l in enumerate(ls): d.text((x + 22, y + 14 + i * 44), l, font=f, fill=(240, 244, 246))
        y += h + 16
    return im

def flechas():
    s = 78; im = Image.new('RGBA', (2 * s + 14, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(2):
        x = k * (s + 14); d.rounded_rectangle((x, 0, x + s - 1, s - 1), 14, fill=(150, 150, 158, 235))
        f = MF(900, 54); d.text((x + s / 2, s / 2 - 2), '➜', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 56), fill=(255, 255, 255), anchor='mm')
    return im

# ---------- colocación ----------
def place(base, lay, b, halo=True):
    rot = b.get('rot', 0)
    if halo and b.get('brillo', True): lay, pad = glow(lay, r=b.get('halo', 18), k=1.3)
    else: pad = 0
    if rot: lay = lay.rotate(rot, resample=Image.BICUBIC, expand=True)
    al = b.get('x', 'c'); y = int(b['y']) - pad
    x = {'c': (W - lay.width) // 2, 'l': 40 - pad, 'r': W - 40 - lay.width + pad}[al] + int(b.get('dx', 0))
    base.alpha_composite(lay, (x, y))
    return y + pad, y + lay.height - pad

def bloque(base, b):
    t = b['tipo']; al = b.get('x', 'c')
    if t == 'titulo':
        f = OF(b.get('size', 104), 700); lay = caja_lineas(wrap(b['texto'], f, 940), f, COL[b.get('color', 'azul')][0], (255, 255, 255), al, pad=(26, 4))
        return place(base, lay, b)
    if t == 'linea':
        f = OF(b.get('size', 62), 600); bg, fg = COL[b.get('color', 'azul')]
        lay = caja_lineas(wrap(b['texto'], f, 760 if b.get('icono') else 940), f, bg, fg, al)
        if b.get('icono'):
            ic = pill_icon(b['icono'], 92); lay = hjoin(ic, lay) if b.get('lado', 'd') == 'i' else hjoin(lay, ic)
        return place(base, lay, b)
    if t == 'texto':
        f = MF(800, b.get('size', 50)); fill = {'blanco': (255, 255, 255), 'azul': (90, 170, 255), 'amarillo': (255, 214, 64)}[b.get('color', 'blanco')]
        return place(base, sombra_texto(wrap(b['texto'], f, 920), f, al, fill), b, halo=False)
    if t == 'numero':
        f = OF(b.get('size', 190), 700); txt = b['texto']
        im = Image.new('RGBA', (int(f.getlength(txt)) + 40, int(f.size * 1.35)), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((20, 0), txt, font=f, fill=(170, 255, 240))
        lay, pad = glow(im, color=(0, 220, 200), r=30, k=2.0)
        if b.get('sub'):
            fs = MF(800, 52); s = sombra_texto([b['sub']], fs, 'c', (255, 255, 255))
            j = Image.new('RGBA', (max(lay.width, s.width), lay.height + s.height - 70), (0, 0, 0, 0))
            j.alpha_composite(lay, ((j.width - lay.width) // 2, 0)); j.alpha_composite(s, ((j.width - s.width) // 2, lay.height - 70)); lay = j
        bb = dict(b, brillo=False); bb['y'] = b['y'] - pad
        return place(base, lay, bb, halo=False)
    if t == 'chat':
        return place(base, chat_card(b['mensajes'], b.get('titulo')), dict(b, halo=26))
    if t == 'iconos':
        s = b.get('size', 120); ics = [pill_icon(n, s) for n in b['iconos']]
        lay = ics[0]
        for ic in ics[1:]: lay = hjoin(lay, ic, 26)
        return place(base, lay, b)
    if t == 'cta':
        r = None
        if b.get('antes'):
            f = OF(64, 600); r = place(base, caja_lineas(wrap(b['antes'], f, 900), f, *COL['naranja']), {'y': b['y'], 'rot': -2})
        y = (r[1] + 40) if r else b['y']
        f = OF(80, 700); lay = caja_lineas(['RESPONDE: "' + b['texto'] + '"'], f, (255, 255, 255), (10, 10, 12), pad=(28, 4))
        lay = hjoin(lay, pill_icon('inbox-tray', 104), 22)
        return place(base, lay, {'y': y})
    raise ValueError(t)

def frame(fr, root, rnd, ultima):
    im = autocrop(ImageOps.exif_transpose(Image.open(os.path.join(root, fr['img']))).convert('RGB'))
    bg = grade(cover(im, fr.get('foco', 0.5), fr.get('focox', 0.5)), fr.get('oscuro', 0.70)).convert('RGBA')
    if fr.get('garabato', True): garabato(bg, rnd)
    prev = None
    for b in fr['bloques']:
        b = dict(b)
        if prev and prev[0] - 10 <= b['y'] < prev[1] + 14:
            b['y'] = prev[1] + 18
        prev = bloque(bg, b)
    if not ultima:
        fl = flechas(); bg.alpha_composite(fl, ((W - fl.width) // 2, 1590))
    return bg.convert('RGB')

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.endswith('.jpg'): os.remove(os.path.join(out, f))
    root = spec.get('root', os.path.dirname(os.path.abspath(sys.argv[1])))
    rnd = random.Random(int(hashlib.md5(str(spec.get('seed', out)).encode()).hexdigest()[:8], 16))
    n = len(spec['frames'])
    for i, fr in enumerate(spec['frames'], 1):
        frame(fr, root, rnd, i == n).save(f'{out}/{i:02d}.jpg', quality=93)
    print(out, n)
