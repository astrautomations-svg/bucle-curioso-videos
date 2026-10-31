"""Fuente de las secuencias de historias (formato v4). Ejecutar: python3 motor/secuencias_fuente.py -> secuencias.json"""
import json, os
def T(t, y, **k): return dict(tipo='titulo', texto=t, y=y, **k)
def L(t, y, color='azul', icono=None, **k):
    d = dict(tipo='linea', texto=t, y=y, color=color, **k)
    if icono: d['icono'] = icono
    return d
def X(t, y, **k): return dict(tipo='texto', texto=t, y=y, **k)
def NUM(t, y, sub=None): return dict(tipo='numero', texto=t, y=y, **({'sub': sub} if sub else {}))
def CHAT(m, y, titulo='WhatsApp'): return dict(tipo='chat', mensajes=m, y=y, titulo=titulo)
def ICS(ics, y): return dict(tipo='iconos', iconos=ics, y=y)
def CTA(t, y, antes=None): return dict(tipo='cta', texto=t, y=y, **({'antes': antes} if antes else {}))
def f(img, *b, **k): return dict(img='banco/%02d.jpg' % img, bloques=list(b), **k)
CARA = {18: [330, 860, 580, 1140], 27: [200, 850, 560, 1250], 17: [520, 500, 880, 950], 39: [220, 650, 460, 950]}
def fc(img, *b, **k): return f(img, *b, cara=CARA[img], **k)

S = [
('2026-10-27', 'preguntas repetidas', [
 fc(18, T('EL PROBLEMA:', 260, rot=-2), L('¿Qué horario tenéis?', 470, 'blanco', 'speech-balloon', x='l', rot=-2),
    L('¿Cuánto cuesta?', 610, 'amarillo', 'euro-banknote', x='r', lado='i', rot=2), L('¿Me cambias la cita?', 750, 'verde', 'spiral-calendar', x='l', rot=-1),
    L('Y tú, contestando a mano', 1360, 'rojo', 'cross-mark', rot=1), foco=0.45),
 f(3, T('EL COSTE REAL:', 260, rot=-1), X('Si se te va 1 hora al día\nen WhatsApp y llamadas…', 470), NUM('22 HORAS', 700, 'al mes contestando lo mismo'),
   L('Casi 3 jornadas enteras', 1330, 'naranja', 'hourglass-done', rot=-2)),
 f(20, T('LA SOLUCIÓN:', 260, rot=-2), CHAT([['in', 'Hola, ¿tenéis hueco el jueves?'], ['out', '¡Hola! Sí, el jueves a las 17:00 está libre. ¿Te lo reservo?']], 430),
   L('Contesta al momento', 1000, 'azul', 'high-voltage', x='l', rot=-2), L('Agenda la cita', 1150, 'amarillo', 'logo-googlecalendar', x='r', lado='i', rot=2),
   L('Hace el seguimiento', 1300, 'verde', 'logo-whatsapp', x='l', rot=-1)),
 fc(39, T('TODO ESTO 24/7', 1060, rot=-2), CTA('SISTEMA', 1220, '¿Tu negocio pierde clientes\npor no contestar a tiempo?'), foco=0.3)]),
('2026-10-28', 'clientes que no vuelven', [
 f(30, T('¿CUÁNTOS NO HAN VUELTO?', 260, rot=-2), L('Vinieron una vez', 520, 'blanco', 'bust-in-silhouette', x='l', rot=-2),
   L('Y nadie les volvió a escribir', 680, 'rojo', 'cross-mark', x='r', lado='i', rot=2)),
 f(25, T('LA SOLUCIÓN:', 260, rot=-1), CHAT([['out', 'Hola Laura, ¡cuánto tiempo! ¿Te guardo hueco esta semana?'], ['in', '¡Sí! El jueves por la tarde']], 430),
   L('Detecta quién lleva tiempo sin venir', 1050, 'verde', 'eyes', x='l', rot=-2), L('Y le escribe en el momento justo', 1200, 'azul', 'logo-whatsapp', x='r', lado='i', rot=1)),
 f(38, T('SIN ACORDARTE DE NADIE', 300, rot=-2), CTA('VOLVER', 1150, '¿Quieres verlo en tu negocio?'), foco=0.4)]),
('2026-10-29', 'llamadas perdidas', [
 fc(27, T('EL PROBLEMA:', 260, rot=-2), L('Estás atendiendo', 470, 'blanco', 'busts-in-silhouette', x='l', rot=-2),
    L('Suena el teléfono', 620, 'amarillo', 'telephone-receiver', x='r', lado='i', rot=2), L('No puedes cogerlo', 1330, 'rojo', 'cross-mark', rot=-1), foco=0.35),
 f(13, T('EL COSTE REAL:', 260, rot=-1), X('Ese cliente no deja mensaje.', 480), L('Llama al siguiente de Google', 1300, 'naranja', 'logo-google', rot=2), foco=0.6),
 f(3, T('LA SOLUCIÓN:', 260, rot=-2), L('Un agente de voz coge la llamada', 480, 'azul', 'telephone-receiver', x='l', rot=-2),
   L('Resuelve la duda', 640, 'verde', 'check-mark-button', x='r', lado='i', rot=2), L('Y agenda la cita', 1300, 'amarillo', 'logo-googlecalendar', x='l', rot=-1)),
 f(16, NUM('24/7', 560, 'aunque tú no estés')),
 fc(39, CTA('LLAMADAS', 1150, '¿Cuántas llamadas pierdes\na la semana?'), foco=0.3)]),
('2026-10-30', 'detrás de cámaras', [
 f(20, T('DETRÁS DE CÁMARAS', 260, rot=-2), X('Así se ve una noche\nmontando un sistema', 480), ICS(['logo-whatsapp', 'logo-n8n', 'logo-googlecalendar'], 1300)),
 f(7, L('1. Entiendo cómo trabaja el negocio', 420, 'blanco', 'magnifying-glass-tilted-left', x='l', rot=-2),
   X('Qué preguntan tus clientes.\nQué se repite.', 600, size=42), foco=0.55),
 fc(18, L('2. Lo construyo para que funcione solo', 380, 'azul', 'gear', x='l', rot=-1),
    L('3. Lo pruebo hasta que no falla', 1300, 'verde', 'check-mark-button', x='r', lado='i', rot=1), foco=0.45),
 f(4, T('¿UNO ASÍ PARA TI?', 300, rot=-2), CTA('SISTEMA', 1150, 'Te digo por dónde empezaría'), foco=0.4)]),
('2026-10-31', 'automatizar no es perder el trato', [
 f(8, T('MITO:', 280, rot=-2), L('«Si automatizo, pierdo el trato personal»', 480, 'blanco', size=58)),
 fc(17, L('Al revés', 300, 'naranja', 'thinking-face', x='l', rot=-2), L('El trato se pierde cuando contestas tarde y con prisa', 1250, 'rojo', rot=1)),
 f(25, T('EL REPARTO:', 260, rot=-1), L('El sistema: lo repetitivo', 480, 'celeste', 'robot', x='l', rot=-2), L('Tú: tus clientes', 640, 'verde', 'handshake', x='r', lado='i', rot=2)),
 f(38, CTA('TRATO', 1050, '¿Qué parte de tu negocio\nse puede automatizar?'), foco=0.4)]),
('2026-11-01', 'haz la cuenta', [
 f(13, T('HAZ ESTA CUENTA:', 260, rot=-2), L('1 hora al día en WhatsApp y llamadas', 480, 'blanco', 'stopwatch', x='l', rot=-1),
   L('× 22 días laborables × 12 meses', 640, 'amarillo', 'calendar', x='r', lado='i', rot=2), foco=0.6),
 f(3, NUM('264 HORAS', 480, 'al año, contestando lo mismo'), L('Son 33 jornadas de 8 horas', 1300, 'naranja', 'hourglass-done', rot=-2)),
 f(14, T('ESE TIEMPO SE RECUPERA', 300, rot=-2), CTA('HORAS', 1100, '¿Te ayudo a calcular el tuyo?'))]),
('2026-11-02', 'citas que no se presentan', [
 f(29, T('EL PROBLEMA:', 260, rot=-2), L('El cliente reserva', 480, 'blanco', 'spiral-calendar', x='l', rot=-2), L('Y no aparece', 640, 'rojo', 'cross-mark', x='r', lado='i', rot=2)),
 f(26, L('Ese hueco ya no lo llenas', 1350, 'naranja', 'hourglass-done', rot=-1)),
 f(20, T('LA SOLUCIÓN:', 260, rot=-1), CHAT([['out', 'Hola Marta, te recuerdo tu cita de mañana a las 10:00. ¿Te viene bien?'], ['in', 'Uf, mejor el viernes'], ['out', 'Hecho, te la cambio al viernes a las 10:00']], 430),
   L('Recuerda y cambia citas solo', 1300, 'verde', 'logo-whatsapp', rot=-2)),
 fc(18, T('MENOS HUECOS VACÍOS', 300, rot=-2), CTA('CITAS', 1250), foco=0.45)]),
('2026-11-03', 'clientes que escriben de noche', [
 f(33, L('23:47', 300, 'blanco', 'crescent-moon', x='l', rot=-2), T('UN CLIENTE TE ESCRIBE', 1020, rot=-1), L('Tú estás durmiendo', 1280, 'rojo', 'sleeping-face', rot=2)),
 f(25, L('Contestas por la mañana', 400, 'amarillo', 'sun', x='l', rot=-2), L('Ya reservó en otro sitio', 1300, 'rojo', 'cross-mark', x='r', lado='i', rot=2)),
 f(3, T('CON UN SISTEMA:', 260, rot=-2), CHAT([['in', 'Hola, ¿mañana tenéis algo libre?'], ['out', '¡Hola! Sí, mañana a las 11:00. ¿Te lo reservo?'], ['in', 'Perfecto']], 430),
   L('Cita hecha mientras duermes', 1300, 'verde', 'check-mark-button', rot=-1)),
 fc(39, CTA('NOCHE', 1150, '¿Lo montamos en tu negocio?'), foco=0.3)]),
('2026-11-04', 'lo que he aprendido', [
 f(1, T('LO QUE HE APRENDIDO:', 280, rot=-2), X('Los negocios que crecen\nno hacen más horas.', 1250)),
 f(19, L('Miden', 420, 'azul', 'bar-chart', x='l', rot=-2), L('Y automatizan lo que se repite', 580, 'verde', 'repeat-button', x='r', lado='i', rot=2)),
 f(9, L('Se rodean de gente que construye sistemas', 360, 'blanco', 'rocket', x='l', rot=-1), L('No de gente que apaga fuegos', 1300, 'rojo', 'fire', x='r', lado='i', rot=2)),
 f(4, T('EL TIEMPO ES PARA CRECER', 300, rot=-2), CTA('SISTEMA', 1050, '¿Te digo por dónde empezaría yo?'), foco=0.4)]),
('2026-11-05', 'reseñas', [
 f(10, T('PREGUNTA:', 260, rot=-2), L('¿Cuántos clientes contentos nunca te dejan reseña?', 450, 'blanco', 'glowing-star', rot=-1), foco=0.4),
 f(31, T('LA SOLUCIÓN:', 260, rot=-1), L('Les escribe después de la visita', 480, 'amarillo', 'logo-whatsapp', x='l', rot=-2),
   L('Y pide la reseña en el momento justo', 640, 'verde', 'star-struck', x='r', lado='i', rot=2)),
 fc(27, CTA('RESEÑAS', 320, '¿Quieres más reseñas\nsin pedirlas tú?'), foco=0.35)]),
('2026-11-06', 'el dueño es el cuello de botella', [
 f(35, T('SÉ SINCERO:', 280, rot=-2), X('Si te vas una semana…', 470)),
 f(28, L('¿Tu negocio sigue funcionando?', 900, 'blanco', 'thinking-face', rot=-1)),
 fc(17, L('Si la respuesta es no', 300, 'rojo', 'warning', x='l', rot=-2), T('EL CUELLO DE BOTELLA ERES TÚ', 1100, rot=-1)),
 f(20, T('LO QUE SE REPITE:', 260, rot=-2), L('Mensajes', 480, 'blanco', 'logo-whatsapp', x='l', rot=-2), L('Citas', 620, 'amarillo', 'logo-googlecalendar', x='r', lado='i', rot=2),
   L('Seguimientos', 760, 'verde', 'repeat-button', x='l', rot=-1), L('Avisos', 900, 'celeste', 'bell', x='r', lado='i', rot=1), X('se puede sistematizar', 1300)),
 f(21, T('Y TÚ VUELVES A DIRIGIR', 300, rot=-2), CTA('SISTEMA', 1200, '¿Te digo qué sacaría\nde tus manos primero?'))]),
('2026-11-07', 'prepárate para Black Friday y Navidad', [
 f(15, T('SE ACERCA:', 260, rot=-2), L('Black Friday', 480, 'naranja', 'shopping-cart', x='l', rot=-2),
   L('Navidad', 630, 'rojo', 'glowing-star', x='r', lado='i', rot=2), X('¿Tu negocio está preparado?', 1250)),
 f(25, T('LO QUE PASA:', 260, rot=-1), L('¿Seguís con la oferta?', 480, 'blanco', 'speech-balloon', x='l', rot=-2),
   L('¿Hay hueco el sábado?', 620, 'amarillo', 'spiral-calendar', x='r', lado='i', rot=2), L('¿Hacéis bonos regalo?', 760, 'verde', 'party-popper', x='l', rot=-1),
   L('Y tú, sin dar abasto', 1330, 'rojo', 'cross-mark', rot=1)),
 f(13, T('CON UN SISTEMA:', 260, rot=-2), CHAT([['in', 'Hola, ¿seguís con la oferta de Black Friday?'], ['out', '¡Hola! Sí, hasta el domingo. ¿Te reservo hora?'], ['in', 'Sí, el sábado por la mañana']], 430),
   L('Contesta al momento', 1150, 'azul', 'high-voltage', x='l', rot=-2), L('Y reserva por ti', 1300, 'verde', 'logo-googlecalendar', x='r', lado='i', rot=2), foco=0.6),
 fc(18, T('MÓNTALO ANTES, NO EN DICIEMBRE', 300, rot=-2), CTA('NAVIDAD', 1250, '¿Lo dejamos listo\nantes del Black Friday?'), foco=0.45)]),
]
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
json.dump([dict(fecha=a, tema=b, frames=c) for a, b, c in S], open('secuencias.json', 'w'), ensure_ascii=False, indent=1)
