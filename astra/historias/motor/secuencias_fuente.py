import json
def E(t,y,**k): return dict(tipo='etiqueta',texto=t,y=y,**k)
def G(t,y,**k): return dict(tipo='grande',texto=t,y=y,**k)
def C(t,y,**k): return dict(tipo='caja',texto=t,y=y,**k)
def N(t,y,**k): return dict(tipo='negra',texto=t,y=y,**k)
def A(t,y,**k): return dict(tipo='azul',texto=t,y=y,**k)
def T(t,y,**k): return dict(tipo='nota',texto=t,y=y,**k)
def CTA(t,y=1430): return dict(tipo='cta',texto=t,y=y)
def f(img,*b,**k): return dict(img='banco/%02d.jpg'%img,bloques=list(b),**k)
S=[
('2026-10-27','preguntas repetidas',[
 f(18,E('SI TIENES UN NEGOCIO',270),G('¿Cuántas horas pierdes\na la semana…',360),A('contestando lo mismo?',1420,rot=-2),foco=0.45),
 f(3,C('¿Qué horario tenéis?',400,x='l',rot=-3),C('¿Cuánto cuesta?',560,x='r',rot=2),C('¿Me cambias la cita?',1300,x='l',rot=1),G('Siempre lo mismo.',1490)),
 f(17,N('Mientras tú conduces…',330),A('tu negocio sigue contestando',1420,rot=-1),T('Con tu tono. Las 24 horas.',1540)),
 f(39,G('¿Te digo qué\nautomatizaría primero\nen tu negocio?',1040,size=70),CTA('SISTEMA',1440),foco=0.3)]),
('2026-10-28','clientes que no vuelven',[
 f(30,G('¿Cuántos clientes\nvinieron una vez…',400),A('y no volvieron?',560,rot=-2)),
 f(25,N('No es que no les gustara.',360),C('Es que nadie les\nvolvió a escribir.',1290,rot=1),T('Un sistema lo hace por ti:\nen el momento justo y con tu tono.',1530)),
 f(38,G('Te enseño cómo\nfuncionaría en\ntu negocio',430),CTA('VOLVER'),foco=0.4)]),
('2026-10-29','llamadas perdidas',[
 f(27,E('DUEÑOS DE NEGOCIO',270),G('Estás atendiendo.',360),C('Suena el teléfono.',1330,rot=-2),A('No puedes cogerlo.',1460,rot=1),foco=0.35),
 f(13,G('Ese cliente\nno deja mensaje.',420),N('Llama al siguiente.',1420),foco=0.6),
 f(3,C('Un agente de voz\ncoge la llamada,',400,x='l',rot=-2),A('resuelve la duda',1320,x='r',rot=2),C('y agenda la cita.',1440,x='r')),
 f(16,G('Tú sigues con lo tuyo.',420),T('Ninguna llamada se pierde.',1500)),
 f(2,G('¿Lo vemos en\ntu negocio?',420),CTA('LLAMADAS'))]),
('2026-10-30','detrás de cámaras',[
 f(20,E('DETRÁS DE CÁMARAS',270),G('Así se ve una noche\nmontando un sistema',360)),
 f(7,C('1. Entiendo cómo\ntrabaja el negocio',380,x='l',rot=-2),T('Qué preguntan tus clientes.\nQué se repite.',540,x='l'),foco=0.55),
 f(18,C('2. Lo construyo para\nque funcione solo',380,x='l',rot=-1),A('3. Lo pruebo hasta\nque no falla',1430,x='r',rot=1),foco=0.45),
 f(4,G('¿Quieres uno así\npara tu negocio?',400),CTA('SISTEMA'),foco=0.4)]),
('2026-10-31','automatizar no es perder el trato',[
 f(8,E('MITO',270),G('«Si automatizo,\npierdo el trato\npersonal»',360)),
 f(17,N('Al revés.',330),C('El trato se pierde\ncuando contestas\ntarde y con prisa.',1360,rot=-1)),
 f(25,C('El sistema: lo repetitivo.',400,x='l',rot=-2),A('Tú: tus clientes.',1400,x='r',rot=2)),
 f(38,G('Te digo qué parte\nde tu negocio se\npuede automatizar',430),CTA('TRATO'),foco=0.4)]),
('2026-11-01','haz la cuenta',[
 f(13,E('HAZ ESTA CUENTA',270),G('1 hora al día\nen WhatsApp\ny llamadas',360),foco=0.6),
 f(3,C('× 22 días laborables',420,rot=-2),A('= 22 horas al mes',560,rot=1),T('Casi tres jornadas enteras\ncontestando lo mismo.',1480)),
 f(14,G('Ese tiempo se\npuede recuperar.',420),CTA('HORAS'))]),
('2026-11-02','citas que no se presentan',[
 f(29,G('El cliente reserva.',420),A('Y no aparece.',560,rot=-2)),
 f(26,C('Ese hueco\nya no lo llenas.',1450,rot=1)),
 f(20,N('El sistema le recuerda la cita…',380,x='l'),C('y si no puede venir,\nla cambia solo.',1400,x='r',rot=1)),
 f(18,G('Te enseño cómo\nfunciona con\ntu agenda',430),CTA('CITAS'),foco=0.45)]),
('2026-11-03','clientes que escriben de noche',[
 f(33,E('23:47',270),G('Un cliente te escribe.',1300,size=76),N('Tú estás durmiendo.',1470)),
 f(25,C('Por la mañana contestas.',400,x='l',rot=-2),A('Ya reservó en otro sitio.',1420,x='r',rot=1)),
 f(3,G('Con un sistema,\nle contestan\nal momento.',450),T('Le resuelve la duda y le deja la cita hecha.',1500)),
 f(16,G('Y tú te levantas con\nla agenda más llena.',420)),
 f(39,G('¿Lo montamos\nen tu negocio?',1180),CTA('NOCHE',1440),foco=0.3)]),
('2026-11-04','lo que he aprendido',[
 f(1,E('LO QUE HE APRENDIDO',270),G('Los negocios que crecen\nno hacen más horas.',1380)),
 f(9,C('Se rodean de gente que\nconstruye sistemas,',400,x='l',rot=-1),A('no de gente que\napaga fuegos.',1440,x='r',rot=2)),
 f(12,G('El tiempo que\nrecuperas es\npara crecer.',430)),
 f(4,G('Te digo por dónde\nempezaría yo',420),CTA('SISTEMA'),foco=0.4)]),
('2026-11-05','reseñas',[
 f(10,E('PREGUNTA',270),G('¿Cuántos clientes\ncontentos nunca te\ndejan una reseña?',360),foco=0.4),
 f(31,C('No es que no quieran.',380,x='l',rot=-2),A('Es que nadie se lo pide.',1440,x='r',rot=1),T('El sistema escribe tras la visita\ny pide la reseña en el momento justo.',1570)),
 f(27,G('Te enseño cómo lo\nharía en tu negocio',430),CTA('RESEÑAS'),foco=0.35)]),
('2026-11-06','el dueño es el cuello de botella',[
 f(35,E('SÉ SINCERO',270),G('Si te vas una semana…',360)),
 f(28,G('¿tu negocio sigue\nfuncionando?',1000)),
 f(17,N('Si la respuesta es no,',330),A('el cuello de botella\neres tú.',1440,rot=-1)),
 f(20,C('Mensajes.',380,x='l',rot=-3),C('Citas.',500,x='l',rot=2),C('Seguimientos.',620,x='l',rot=-1),A('Lo que se repite\nse puede sistematizar.',1420)),
 f(21,G('¿Te digo qué sacaría\nde tus manos primero?',420),CTA('SISTEMA'))]),
]
json.dump([dict(fecha=a,tema=b,frames=c) for a,b,c in S],open('secuencias.json','w'),ensure_ascii=False,indent=1)
