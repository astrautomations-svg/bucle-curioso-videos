# Bucle Curioso · vídeos

Vídeos de los reels de @buclecurioso. n8n lee `cola.json` a las 9:00 y a las 19:00 (hora de Madrid) y publica la entrada de ese día y esa hora: el reel (`video`, con `caption`) y su historia (`historia`).

- 9:00: el vídeo de actualidad del día (lo añade la tarea diaria).
- 19:00: los vídeos de reserva, uno al día.

## Astra Automations (@astra.automations)
Carpeta `astra/`: reels de Astra ya aprobados por él. El flujo de n8n «Instagram Astra · publicar reel aprobado» lee `astra/cola-astra.json` a las 19:30 (Madrid) y publica la entrada de ese día con `estado: "aprobado"`. Nada se publica sin el «ok» de Astra.

### Hora de publicación (desde el 5-11-2026)
Astra quiere los reels siempre por la mañana, entre las 9:00 y las 12:00. Dentro de esa franja, la hora con más seguidores conectados es la última (los conectados suben de 9 a 12), así que todos salen a las 11:30 (el flujo de n8n se ejecuta a y media). Los datos de `online_followers` dan el pico real por la noche (21:00-23:00); si algún día se quiere probar, está apuntado aquí.
