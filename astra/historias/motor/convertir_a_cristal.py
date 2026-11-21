"""Pasa las secuencias antiguas (titulo/linea/chat/cta) del 22 al 26-11 al estilo cristal."""
import json, random, subprocess, os
R = '/home/claude/bucle-curioso-videos/astra/historias'
IC = {'logo-whatsapp': 'canales/whatsapp', 'logo-instagram': 'canales/instagram', 'speech-balloon': 'canales/mensaje-entrante',
      'spiral-calendar': 'tiempo/calendario', 'pushpin': 'negocio/tienda', 'crescent-moon': 'tiempo/luna', 'cross-mark': 'estados/x-roja',
      'clipboard': 'sistema/documento-con-check', 'hourglass-done': 'tiempo/reloj-de-arena', 'busts-in-silhouette': 'personas/equipo',
      'bell': 'sistema/campana', 'thinking-face': 'estados/alerta', 'repeat-button': 'sistema/engranaje', 'shopping-cart': 'negocio/tienda',
      'memo': 'negocio/ticket-factura', 'bust-in-silhouette': 'personas/cliente', 'high-voltage': 'tiempo/rayo',
      'logo-googlecalendar': 'tiempo/calendario-con-check', 'check-mark-button': 'estados/check-verde'}
NOMBRES = {'in': None}

def convertir(sec):
    rnd = random.Random(sec['fecha'])
    def rot(): return round(rnd.choice([-1, 1]) * rnd.uniform(1.2, 3.0), 1)
    frames = []
    for fr in sec['frames']:
        nb = []; y_sig = 470
        for b in fr['bloques']:
            t = b['tipo']
            if t == 'titulo':
                txt = b['texto'].rstrip(':').strip()
                if b['y'] > 600:   # título a media altura (historia del CTA): titular
                    nb.append(dict(tipo='titular', texto=txt[0] + txt[1:].lower(), y=1110, rot=rot(), w=820))
                else:
                    nb.append(dict(tipo='etiqueta', texto=txt.upper(), y=295, x=rnd.choice([96, 110, 120]), rot=rot()))
            elif t == 'linea':
                y = (1120 if b['y'] < 1250 else 1340) if b['y'] > 900 else y_sig
                w = min(860, 300 + len(b['texto']) * 20)
                cx = rnd.choice([470, 520, 580]) if w < 800 else 540
                nb.append(dict(tipo='fila', icono=IC.get(b.get('icono'), 'sistema/asistente-robot'), texto=b['texto'], y=y, cx=cx, w=w, rot=rot()))
                if b['y'] <= 900: y_sig = y + 190
            elif t == 'chat':
                y = 540
                for d, m in b['mensajes'][:2]:
                    ext = d == 'in'
                    nb.append(dict(tipo='wa', nombre='Cliente' if ext else 'Tu negocio', texto=m, y=y, w=800,
                                   cx=560 if ext else 520, hora='22:%02d' % rnd.randint(5, 55), rot=rot(),
                                   icono='canales/instagram' if b.get('titulo') == 'Instagram' else 'canales/whatsapp'))
                    y += 255
                y_sig = y + 40
            elif t == 'cta':
                nb.append(dict(tipo='cta', texto=b['texto'], antes=b.get('antes', '¿Quieres uno así?'), y=1440, rot=rot()))
            elif t == 'texto':
                nb.append(dict(tipo='titular', texto=b['texto'], y=b['y'], rot=rot(), w=820, size=56))
        if fr.get('cara'):
            for b2 in nb:
                if b2['tipo'] == 'titular' and b2['y'] > 900: b2['y'] = 470
            if fr['cara'][3] > 1200:
                for b2 in nb:
                    if b2['tipo'] == 'cta': b2['y'] = 1458
        nf = {k: v for k, v in fr.items() if k != 'bloques'}; nf['bloques'] = nb
        frames.append(nf)
    return frames

secs = json.load(open(f'{R}/secuencias.json'))
for s in secs:
    if s['fecha'] in ('2026-11-22', '2026-11-23', '2026-11-24', '2026-11-25', '2026-11-26'):
        fr = convertir(s)
        spec = {'root': R, 'seed': s['fecha'], 'frames': fr}
        p = f'/tmp/claude-0/-home-claude/a906aaeb-b6fe-583b-92b9-177d69f08f0d/scratchpad/glass/spec_{s["fecha"]}.json'
        json.dump(spec, open(p, 'w'), ensure_ascii=False, indent=1)
        print(subprocess.run(['python3', f'{R}/motor/cristal.py', p, f'/tmp/claude-0/-home-claude/a906aaeb-b6fe-583b-92b9-177d69f08f0d/scratchpad/glass/out/{s["fecha"]}'], capture_output=True, text=True).stdout)
