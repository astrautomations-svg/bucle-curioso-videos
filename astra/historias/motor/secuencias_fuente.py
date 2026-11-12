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
('2026-11-08', 'diciembre se llena: avisa primero a los tuyos', [
 f(9, T('DICIEMBRE SE LLENA:', 260, rot=-2), L('Cenas de empresa', 480, 'blanco', 'busts-in-silhouette', x='l', rot=-2),
   L('Regalos de última hora', 620, 'rojo', 'party-popper', x='r', lado='i', rot=2), L('Citas antes de las fiestas', 760, 'amarillo', 'spiral-calendar', x='l', rot=-1), foco=0.4),
 f(5, T('EL ERROR:', 260, rot=-1), L('Esperar a que te escriban', 480, 'naranja', 'hourglass-done', x='l', rot=-2),
   L('Tus clientes de siempre reservan en otro sitio', 1300, 'rojo', 'cross-mark', rot=1)),
 f(12, T('LA SOLUCIÓN:', 260, rot=-2), CHAT([['out', 'Hola Lucía, diciembre se está llenando. ¿Te guardo hueco antes de Navidad?'], ['in', '¡Sí! Mejor la semana del 15']], 430),
   L('Avisa primero a los tuyos', 1150, 'verde', 'logo-whatsapp', x='l', rot=-2), L('Y les guarda el hueco', 1300, 'azul', 'logo-googlecalendar', x='r', lado='i', rot=2), foco=0.5),
 f(32, T('SIN ESCRIBIR UNO A UNO', 300, rot=-2), L('Cada mensaje con su nombre', 500, 'blanco', 'speech-balloon', x='l', rot=-1),
   L('Y tú, a lo tuyo', 1300, 'amarillo', 'smiling-face-with-sunglasses', x='r', lado='i', rot=2)),
 fc(39, CTA('DICIEMBRE', 1150, '¿Avisamos a tus clientes\nantes que la competencia?'), foco=0.3)]),
('2026-11-09', 'presupuestos que se quedan sin respuesta', [
 f(7, T('TE PIDEN PRESUPUESTO:', 260, rot=-2), L('Se lo mandas', 530, 'blanco', 'envelope', x='l', rot=-2),
   L('Y silencio', 680, 'rojo', 'cross-mark', x='r', lado='i', rot=2), foco=0.55),
 f(36, T('EL ERROR:', 260, rot=-1), L('No volver a escribir', 480, 'naranja', 'hourglass-done', x='l', rot=-2),
   L('Por no parecer pesado', 1300, 'blanco', 'grimacing-face', x='r', lado='i', rot=2)),
 f(20, T('LA SOLUCIÓN:', 260, rot=-2), CHAT([['out', 'Hola Javier, ¿pudiste ver el presupuesto? Si tienes alguna duda, te la resuelvo'], ['in', '¡Sí! ¿Empezamos la semana que viene?']], 430),
   L('Hace el seguimiento solo', 1150, 'verde', 'logo-whatsapp', x='l', rot=-2), L('En el momento justo', 1300, 'azul', 'alarm-clock', x='r', lado='i', rot=2)),
 fc(27, CTA('VENTAS', 320, '¿Cuántos presupuestos tienes\nesperando respuesta?'), foco=0.35)]),
('2026-11-10', 'gana el primero que contesta', [
 f(11, T('PASA CADA DÍA:', 260, rot=-2), L('Un cliente pide precio', 480, 'blanco', 'speech-balloon', x='l', rot=-2),
   L('A varios negocios a la vez', 630, 'amarillo', 'busts-in-silhouette', x='r', lado='i', rot=2),
   L('Gana el primero que contesta', 1300, 'rojo', 'stopwatch', rot=-1)),
 f(3, T('CON UN SISTEMA:', 260, rot=-2), CHAT([['in', 'Hola, ¿cuánto cuesta? ¿Tenéis hueco esta semana?'], ['out', '¡Hola! Ahora te paso los precios. Hay hueco el martes a las 18:00, ¿te lo guardo?'], ['in', 'Perfecto, resérvalo']], 430),
   L('Contesta en segundos', 1150, 'azul', 'high-voltage', x='l', rot=-2), L('Y cierra la cita', 1300, 'verde', 'logo-googlecalendar', x='r', lado='i', rot=2)),
 fc(17, T('LLEGA TÚ PRIMERO', 280, rot=-2), CTA('PRIMERO', 1150, '¿Cuánto tardas tú\nen contestar?'))]),
('2026-11-11', 'encargos de Navidad que se pierden', [
 f(10, T('EN DICIEMBRE TE LLEGAN:', 260, rot=-2), L('Encargos por WhatsApp', 480, 'blanco', 'logo-whatsapp', x='l', rot=-2),
   L('Por teléfono', 630, 'amarillo', 'telephone-receiver', x='r', lado='i', rot=2), L('Y en una nota de papel', 780, 'verde', 'memo', x='l', rot=-1), foco=0.4),
 f(25, T('EL PROBLEMA:', 260, rot=-1), L('Uno se queda sin apuntar', 480, 'rojo', 'cross-mark', x='l', rot=-2),
   L('Y te enteras el mismo día', 1300, 'naranja', 'grimacing-face', rot=1)),
 f(41, T('LA SOLUCIÓN:', 260, rot=-2), CHAT([['in', 'Hola, quiero hacer un encargo para el 23'], ['out', '¡Hola! Apuntado para el 23. ¿A qué hora pasas a recogerlo?'], ['in', 'Sobre las 12']], 430),
   L('Apunta cada encargo', 1150, 'verde', 'clipboard', x='l', rot=-2), L('Y avisa el día antes', 1300, 'azul', 'bell', x='r', lado='i', rot=2)),
 fc(18, T('NI UN ENCARGO PERDIDO', 300, rot=-2), CTA('ENCARGOS', 1250, '¿Cómo apuntas tú\nlos encargos de Navidad?'), foco=0.45)]),
('2026-11-12', 'horario de Navidad: las mismas preguntas', [
 f(33, T('EN NAVIDAD TE PREGUNTAN:', 260, rot=-2), L('¿Abrís el 24?', 480, 'blanco', 'spiral-calendar', x='l', rot=-2),
   L('¿Y el 31 por la tarde?', 630, 'amarillo', 'alarm-clock', x='r', lado='i', rot=2), L('¿Qué horario tenéis?', 780, 'verde', 'speech-balloon', x='l', rot=-1)),
 f(3, T('EL PROBLEMA:', 260, rot=-1), L('Siempre la misma pregunta', 480, 'naranja', 'repeat-button', x='l', rot=-2),
   L('En plena temporada alta', 1300, 'rojo', 'fire', x='r', lado='i', rot=2)),
 f(29, T('LA SOLUCIÓN:', 260, rot=-2), CHAT([['in', 'Hola, ¿abrís el día 24?'], ['out', '¡Hola! El 24 abrimos por la mañana. ¿Te reservo hora?'], ['in', 'Sí, a primera hora']], 430),
   L('Contesta con tu horario', 1150, 'azul', 'logo-whatsapp', x='l', rot=-2), L('Y reserva la cita', 1300, 'verde', 'logo-googlecalendar', x='r', lado='i', rot=2)),
 f(42, T('MEJOR AÚN:', 260, rot=-2), L('Avisa antes de que pregunten', 480, 'amarillo', 'megaphone', x='l', rot=-2),
   L('A cada cliente, con su nombre', 630, 'blanco', 'busts-in-silhouette', x='r', lado='i', rot=2)),
 fc(27, CTA('FIESTAS', 320, '¿Tienes ya listo tu\nhorario de Navidad?'), foco=0.35)]),
('2026-11-13', 'cancelaciones de última hora: lista de espera', [
 f(26, T('EN TEMPORADA ALTA:', 260, rot=-2), L('Te cancelan a última hora', 480, 'blanco', 'spiral-calendar', x='l', rot=-2),
   L('Y el hueco se queda vacío', 630, 'rojo', 'cross-mark', x='r', lado='i', rot=2), foco=0.45),
 f(15, T('LO PEOR:', 260, rot=-1), L('Tenías clientes pidiendo hora', 480, 'amarillo', 'busts-in-silhouette', x='l', rot=-2),
   L('Y no te acuerdas de avisarlos', 1300, 'naranja', 'grimacing-face', x='r', lado='i', rot=2)),
 f(20, T('LA SOLUCIÓN:', 260, rot=-2), CHAT([['out', 'Hola Sara, se ha liberado un hueco mañana a las 12:00. ¿Lo quieres?'], ['in', '¡Sí, me lo quedo!'], ['out', 'Hecho, te lo reservo']], 430),
   L('Avisa a tu lista de espera', 1150, 'verde', 'logo-whatsapp', x='l', rot=-2), L('Y llena el hueco solo', 1300, 'azul', 'logo-googlecalendar', x='r', lado='i', rot=2)),
 fc(39, T('NI UN HUECO VACÍO', 1000, rot=-2), CTA('HUECOS', 1170, '¿Cuántas cancelaciones\nte quedan sin llenar?'), foco=0.3)]),
('2026-11-15', 'bonos regalo de Navidad sin estar pendiente', [
 f(8, T('EN NAVIDAD TE PIDEN:', 260, rot=-2), L('¿Hacéis bonos regalo?', 480, 'blanco', 'party-popper', x='l', rot=-2),
   L('¿Me lo mandáis hoy?', 630, 'amarillo', 'speech-balloon', x='r', lado='i', rot=2),
   L('Y tú, con las manos ocupadas', 1300, 'rojo', 'cross-mark', rot=-1), foco=0.45),
 f(25, T('LA SOLUCIÓN:', 260, rot=-1), CHAT([['in', 'Hola, ¿hacéis bonos regalo? Es para mi madre'], ['out', '¡Hola! Sí. ¿Para qué servicio lo quieres?'], ['in', 'El de siempre, gracias']], 430),
   L('Contesta al momento', 1150, 'azul', 'high-voltage', x='l', rot=-2), L('Y apunta cada pedido', 1300, 'verde', 'clipboard', x='r', lado='i', rot=2)),
 fc(18, T('VENDE AUNQUE NO MIRES EL MÓVIL', 300, rot=-2), CTA('REGALO', 1250, '¿Cuántos bonos se te\nescapan en diciembre?'), foco=0.45)]),
('2026-11-16', 'lunes: los mensajes del fin de semana', [
 f(28, T('EL FIN DE SEMANA:', 260, rot=-2), L('Tú, desconectando', 480, 'blanco', 'sun', x='l', rot=-2),
   L('Tu WhatsApp, a tope', 630, 'amarillo', 'logo-whatsapp', x='r', lado='i', rot=2)),
 f(3, T('Y LLEGA EL LUNES:', 260, rot=-1), L('Chats sin leer desde el sábado', 480, 'blanco', 'inbox-tray', x='l', rot=-2),
   L('Ya reservaron en otro sitio', 1300, 'rojo', 'cross-mark', rot=1)),
 f(41, T('LA SOLUCIÓN:', 260, rot=-2), CHAT([['in', 'Hola, ¿tenéis hueco el lunes?'], ['out', '¡Hola! Sí, el lunes a las 10:30. ¿Te lo reservo?'], ['in', 'Perfecto, gracias']], 430),
   L('Contesta también el domingo', 1150, 'azul', 'high-voltage', x='l', rot=-2), L('Y deja la cita hecha', 1300, 'verde', 'logo-googlecalendar', x='r', lado='i', rot=2)),
 fc(17, T('EMPIEZA AL DÍA', 280, rot=-2), CTA('LUNES', 1150, '¿Cuántos mensajes te\nesperan cada lunes?'))]),
('2026-11-17', 'Black Friday: los que preguntan y no reservan', [
 f(15, T('TE PREGUNTAN:', 260, rot=-2), L('¿Cuánto es la oferta?', 480, 'blanco', 'speech-balloon', x='l', rot=-2),
   L('¿Hasta cuándo dura?', 630, 'amarillo', 'shopping-cart', x='r', lado='i', rot=2), L('Les contestas… y nada', 1300, 'rojo', 'cross-mark', rot=-1)),
 f(36, T('EL PROBLEMA:', 260, rot=-1), L('Nadie les vuelve a escribir', 480, 'naranja', 'hourglass-done', x='l', rot=-2),
   L('Y la oferta se acaba sin ellos', 1300, 'blanco', 'grimacing-face', x='r', lado='i', rot=2)),
 f(20, T('LA SOLUCIÓN:', 260, rot=-2), CHAT([['out', 'Hola Nuria, la oferta acaba el domingo. ¿Te guardo hora antes?'], ['in', '¡Sí! El viernes por la tarde']], 430),
   L('Les recuerda la oferta', 1150, 'verde', 'logo-whatsapp', x='l', rot=-2), L('Antes de que se acabe', 1300, 'azul', 'alarm-clock', x='r', lado='i', rot=2)),
 fc(39, T('QUE NO SE QUEDEN A MEDIAS', 1000, rot=-2), CTA('OFERTA', 1170, '¿Cuántos te preguntaron\ny no volvieron?'), foco=0.3)]),
('2026-11-18', 'cenas de empresa: reservas de grupo por WhatsApp', [
 f(31, T('CENAS DE EMPRESA:', 260, rot=-2), L('¿Tenéis menú para grupos?', 480, 'blanco', 'speech-balloon', x='l', rot=-2),
   L('Somos 14… o igual 16', 630, 'amarillo', 'busts-in-silhouette', x='r', lado='i', rot=2), L('¿Hay opción vegetariana?', 780, 'verde', 'thinking-face', x='l', rot=-1), foco=0.45),
 f(33, T('EL PROBLEMA:', 260, rot=-1), L('Cada grupo, un chat eterno', 480, 'naranja', 'repeat-button', x='l', rot=-2),
   L('Y tú, contestando de noche', 1300, 'rojo', 'crescent-moon', x='r', lado='i', rot=2)),
 f(25, T('LA SOLUCIÓN:', 260, rot=-2), CHAT([['in', 'Hola, ¿tenéis menú para una cena de empresa el 19?'], ['out', '¡Hola! Sí, ahora te paso el menú. ¿Cuántos seréis?'], ['in', 'Unos 15, te confirmo el viernes']], 430),
   L('Manda el menú al momento', 1150, 'azul', 'logo-whatsapp', x='l', rot=-2), L('Y apunta la reserva', 1300, 'verde', 'logo-googlecalendar', x='r', lado='i', rot=2)),
 f(42, T('Y ADEMÁS:', 260, rot=-2), L('Pide cuántos serán al final', 480, 'blanco', 'clipboard', x='l', rot=-2),
   L('Y recuerda la cena el día antes', 630, 'amarillo', 'bell', x='r', lado='i', rot=2)),
 fc(18, T('TÚ, A LLENAR EL LOCAL', 300, rot=-2), CTA('GRUPOS', 1250, '¿Cuántas reservas de grupo\nllevas a mano?'), foco=0.45)]),
('2026-11-19', 'temporada alta: reseñas que nadie pide', [
 f(30, T('EN TEMPORADA ALTA:', 260, rot=-2), L('El local, lleno', 480, 'blanco', 'fire', x='l', rot=-2),
   L('Clientes que salen contentos', 630, 'amarillo', 'star-struck', x='r', lado='i', rot=2),
   L('Y ni una reseña nueva', 1300, 'rojo', 'cross-mark', rot=-1), foco=0.45),
 f(20, T('LA SOLUCIÓN:', 260, rot=-2), CHAT([['out', 'Hola Marta, gracias por venir hoy. ¿Nos dejas tu opinión en Google? Aquí tienes el enlace'], ['in', '¡Claro! Ahora mismo te la dejo']], 430),
   L('Pide la reseña al salir', 1150, 'verde', 'logo-whatsapp', x='l', rot=-2), L('Sin que tengas que acordarte', 1300, 'azul', 'logo-google', x='r', lado='i', rot=2)),
 fc(39, T('QUE TE ELIJAN EN GOOGLE', 1000, rot=-2), CTA('RESEÑAS', 1170, '¿Cuántos clientes contentos\nse van sin dejar reseña?'), foco=0.3)]),
]
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
json.dump([dict(fecha=a, tema=b, frames=c) for a, b, c in S], open('secuencias.json', 'w'), ensure_ascii=False, indent=1)
