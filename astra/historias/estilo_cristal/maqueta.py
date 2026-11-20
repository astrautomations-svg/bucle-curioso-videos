"""Historias estilo cristal v2: contenedores desordenados y girados, fotos a resolución completa."""
import io, random, numpy as np, cairosvg
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance
S = '/tmp/claude-0/-home-claude/a906aaeb-b6fe-583b-92b9-177d69f08f0d/scratchpad'
OUT = S + '/glass'; LUC = S + '/ico_tool/node_modules/lucide-static/icons'; SI = S + '/ico_tool/node_modules/simple-icons/icons'
A = '/mnt/user-data/attachments/a906aaeb-b6fe-583b-92b9-177d69f08f0d/'
FI = '/usr/share/fonts/opentype/inter/'
def F(w, s): return ImageFont.truetype(FI + {'b': 'InterDisplay-Bold.otf', 'sb': 'InterDisplay-SemiBold.otf', 'm': 'InterDisplay-Medium.otf', 'x': 'InterDisplay-ExtraBold.otf'}[w], s)
W, H = 1080, 1920; BL = (255, 255, 255); NAR = (255, 150, 70); SUB = (228, 234, 246)

def fondo(path, fy=0.5, osc=0.82):
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    im = ImageOps.fit(im, (W, H), Image.LANCZOS, centering=(0.5, fy))
    im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=60, threshold=2))
    im = ImageEnhance.Brightness(im).enhance(osc)
    a = np.array(im).astype(float); y = np.linspace(0, 1, H)[:, None, None]
    a = a * (1 - 0.25 * y)                                      # oscurece solo un poco abajo
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')

def icono(n, s, col=BL, sw=2.0):
    if n.startswith('si:'): svg = open(f'{SI}/{n[3:]}.svg').read().replace('<svg ', '<svg fill="#%02x%02x%02x" ' % col)
    else: svg = open(f'{LUC}/{n}.svg').read().replace('currentColor', '#%02x%02x%02x' % col).replace('stroke-width="2"', f'stroke-width="{sw}"')
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_width=s, output_height=s))).convert('RGBA')

def tarjeta(base, cx, cy, w, h, ang, dibujar, r=42, a=0.16, blur=24):
    """Crea un contenedor de cristal (desenfoca lo de detrás), dibuja el contenido y lo pega girado `ang` grados."""
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

IG = S + '/iconos_glass'
def glass_ico(n, s):
    im = Image.open(f'{IG}/{n}.png').convert('RGBA'); im = im.crop(im.getbbox()); im.thumbnail((s, s), Image.LANCZOS); return im
def cuadro(card, xy, n, col, s=88):
    if '/' in n:
        ic = glass_ico(n, int(s * 1.12)); x, y = xy
        card.alpha_composite(ic, (x + (s - ic.width) // 2, y + (s - ic.height) // 2)); return
def _old_cuadro(card, xy, n, col, s=88):
    x, y = xy; lay = Image.new('RGBA', card.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle((x, y, x + s, y + s), int(s * 0.3), fill=col + (235,)); card.alpha_composite(lay)
    ic = icono(n, int(s * (0.56 if n.startswith('si:') else 0.5))); card.alpha_composite(ic, (x + (s - ic.width) // 2, y + (s - ic.height) // 2))

def lineas(d, xy, t, f, fill, w, lh=1.18):
    x, y = xy; out, cur = [], ''
    for p in t.split():
        z = (cur + ' ' + p).strip()
        if d.textlength(z, font=f) > w and cur: out.append(cur); cur = p
        else: cur = z
    out.append(cur)
    for l in out: d.text((x, y), l, font=f, fill=fill); y += int(f.size * lh)
    return y

def etiqueta(base, x, y, t, ang):
    f = F('b', 30); tw = int(ImageDraw.Draw(base).textlength(t, font=f))
    def dib(c, d): d.ellipse((26, 26, 40, 40), fill=(90, 220, 140)); d.text((56, 14), t, font=f, fill=BL)
    tarjeta(base, x + (tw + 82) / 2, y + 33, tw + 82, 66, ang, dib, r=33, a=0.2, blur=16)

def fila(base, cx, cy, w, ic, col, t, ang, f=None):
    f = f or F('sb', 38)
    def dib(c, d):
        cuadro(c, (22, 14), ic, col, 96)
        lineas(d, (138, 30 if d.textlength(t, font=f) < w - 160 else 16), t, f, BL, w - 160, 1.12)
    tarjeta(base, cx, cy, w, 124, ang, dib, r=34, a=0.13)

# ---------- Historia 1 · EL PROBLEMA (restaurante) ----------
im = fondo(A + 'e8fec547-108653.jpg', fy=0.55)
etiqueta(im, 96, 250, 'EL PROBLEMA', -2.5)
def h1(c, d):
    y = lineas(d, (48, 44), 'Son las 23:40.', F('b', 66), BL, 760)
    lineas(d, (48, y + 4), 'Alguien quiere reservar mesa para mañana. Tu restaurante ya ha cerrado.', F('m', 38), SUB, 740)
tarjeta(im, 520, 500, 850, 300, 1.8, h1)
def wa(c, d):
    cuadro(c, (28, 30), 'canales/whatsapp', None, 112)
    d.text((158, 34), 'Laura', font=F('b', 36), fill=BL); d.text((610, 40), '23:40', font=F('m', 26), fill=(205, 214, 232))
    d.text((158, 84), '¿Mesa para 4 mañana a las 21:30?', font=F('m', 32), fill=SUB)
tarjeta(im, 580, 790, 720, 164, -3.2, wa, r=38, a=0.2)
fila(im, 500, 1010, 780, 'tiempo/luna', None, 'Nadie contesta hasta mañana', 2.4)
fila(im, 590, 1170, 800, 'personas/cliente-perdido', None, 'Reserva donde le respondieron primero', -1.6)
im.convert('RGB').save(f'{OUT}/historia_1.jpg', quality=95)

# ---------- Historia 2 · LA SOLUCIÓN + CTA ----------
im = fondo(A + 'c88f531f-108637.jpg', fy=0.45, osc=0.78)
etiqueta(im, 110, 250, 'LA SOLUCIÓN', 2.2)
def h2(c, d):
    y = lineas(d, (48, 42), 'Un asistente que contesta por ti.', F('b', 60), BL, 760)
    lineas(d, (48, y + 4), 'A cualquier hora. Con tu agenda real.', F('m', 38), SUB, 760)
tarjeta(im, 530, 480, 860, 270, -1.8, h2)
fila(im, 470, 720, 700, 'tiempo/rayo', None, 'Contesta en segundos', 2.6)
fila(im, 600, 870, 740, 'tiempo/calendario-con-check', None, 'Da la cita y la confirma', -2.2)
fila(im, 490, 1020, 760, 'sistema/escudo-con-check', None, 'Lo delicado te lo pasa a ti', 1.4)
def cta(c, d):
    d.text((48, 40), '¿Cuántos mensajes se te quedan', font=F('b', 44), fill=BL)
    d.text((48, 94), 'sin contestar cada noche?', font=F('b', 44), fill=BL)
    lay = Image.new('RGBA', c.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((48, 176, 640, 260), 42, fill=NAR + (245,)); c.alpha_composite(lay)
    ImageDraw.Draw(c).text((86, 192), 'RESPONDE: «NOCHE»', font=F('x', 44), fill=BL)
tarjeta(im, 540, 1290, 880, 300, -1.2, cta, r=48, a=0.17)
im.convert('RGB').save(f'{OUT}/historia_2.jpg', quality=95)
print('ok')
