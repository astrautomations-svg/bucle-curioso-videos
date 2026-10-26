# Historias diarias de @astra.automations

n8n («Instagram Astra · historias diarias», id IcjSqALD0WCckLJq) publica cada día a las 13:00 (Madrid) la entrada de `cola-historias.json` con la fecha de hoy y `estado: "aprobado"`.

## Cómo se genera una secuencia
1. Añade la secuencia a `motor/secuencias_fuente.py` (lista `S`) y ejecútalo: escribe `secuencias.json`.
2. Para cada fecha nueva: `python3 motor/historias.py spec.json AAAA-MM-DD` (spec = `{"root": "<esta carpeta>", "frames": [...]}`).
3. Añade a `cola-historias.json`: `{"fecha", "hora": "13", "estado": "aprobado", "tema", "frames": ["astra/historias/AAAA-MM-DD/01.jpg", ...]}`.
4. Revisa las imágenes a ojo, haz commit y push a `main`.

## Reglas (de Astra)
- Solo para dueños de negocio, con intención de venta. Nada de enseñar herramientas de IA. Llamativo, sin ser cringe. Nunca inventar datos ni cifras.
- De 3 a 6 historias por día. No siempre el mismo número.
- La última siempre lleva el CTA escrito (bloque `cta`): «Escríbeme PALABRA».
- Texto repartido por la historia, como en Instagram: antetítulo arriba, frase grande, líneas con fondo en distintas alturas. Nunca todo en una caja.
- Nunca texto sobre la cara. Nada por encima de y=230 ni por debajo de y=1640 (salvo el CTA).
- La foto acompaña lo que dice esa historia.
- No juntes fotos parecidas en la misma secuencia. Grupos de parecidas en `banco/`:
  - escritorio de noche: 03, 20, 25
  - él con el portátil: 02, 18, 27, 38, 39
  - terraza: 04, 05, 07, 29
  - cenas y restaurante: 06, 08, 09, 10, 26, 30, 31
  - coches: 11, 21, 22, 23, 24
  - costa: 16, 34, 35, 36, 37
  - paisajes y carretera: 12, 13, 14, 40
  - ciudad de noche: 15, 33
  - escenario y charla: 01, 19
  - sueltas: 17 (conduciendo), 28 (paseo con perros), 32 (gimnasio)
- No repitas la misma foto dos días seguidos ni el mismo tema en la misma semana. Rota palabras del CTA (SISTEMA, VOLVER, LLAMADAS, CITAS, HORAS, NOCHE, RESEÑAS, TRATO…).
