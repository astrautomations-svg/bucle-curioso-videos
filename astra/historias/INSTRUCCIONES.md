# Historias diarias de @astra.automations

n8n («Instagram Astra · historias diarias», id IcjSqALD0WCckLJq) publica cada día a las 13:00 (Madrid) la entrada de `cola-historias.json` con la fecha de hoy y `estado: "aprobado"`.

## Cómo se genera una secuencia
1. Añade la secuencia a `motor/secuencias_fuente.py` (lista `S`, formato v4: lee el docstring de `motor/historias.py` y copia el estilo de las secuencias que ya hay) y ejecútalo: escribe `secuencias.json`.
2. Para cada fecha nueva: `python3 motor/historias.py spec.json AAAA-MM-DD` (spec = `{"root": "<esta carpeta>", "seed": "AAAA-MM-DD", "frames": [...]}`).
3. Añade a `cola-historias.json`: `{"fecha", "hora": "13", "estado": "aprobado", "tema", "frames": ["astra/historias/AAAA-MM-DD/01.jpg", ...]}`.
4. Revisa las imágenes a ojo, haz commit y push a `main`.

## Reglas (de Astra)
- Solo para dueños de negocio, con intención de venta. Nada de enseñar herramientas de IA. Llamativo, sin ser cringe. Nunca inventar datos ni cifras.
- De 3 a 6 historias por día. No siempre el mismo número.
- La última siempre lleva el CTA (bloque `cta`).
- Estilo de las historias de Astra (v4): título condensado en caja azul arriba («EL PROBLEMA:», «EL COSTE REAL:», «LA SOLUCIÓN:»…), frases en pastillas de colores repartidas y algo torcidas, cada una con un icono o logo de app al lado, a veces una tarjeta de WhatsApp de ejemplo o un número grande con brillo. La línea de neón con bucles y las flechas ➜➜ las pone el motor solo. Cierre: pregunta en naranja + «RESPONDE: "PALABRA"».
- Las frases de las pastillas, cortas (una línea mejor que dos). Nada por debajo de y≈1500 en historias que no sean la última (ahí van las flechas).
- En fotos donde sale la cara de Astra, pon "cara" en el frame (ver CARA en secuencias_fuente.py) para que la línea no la cruce, y no pongas texto encima.
- Los chats son ejemplos genéricos (nombres de pila inventados, sin datos reales de clientes). Las cifras solo si son cuentas evidentes (1 h/día × 22 días = 22 h), nunca datos inventados.
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
