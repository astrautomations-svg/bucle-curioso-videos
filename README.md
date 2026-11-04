# Bucle Curioso · vídeos

Vídeos de los reels de @buclecurioso. n8n lee `cola.json` a las 9:00 y a las 19:00 (hora de Madrid) y publica la entrada de ese día y esa hora: el reel (`video`, con `caption`) y su historia (`historia`).

- 9:00: el vídeo de actualidad del día (lo añade la tarea diaria).
- 19:00: los vídeos de reserva, uno al día.

## Astra Automations (@astra.automations)
Carpeta `astra/`: reels de Astra ya aprobados por él. El flujo de n8n «Instagram Astra · publicar reel aprobado» lee `astra/cola-astra.json` a las 19:30 (Madrid) y publica la entrada de ese día con `estado: "aprobado"`. Nada se publica sin el «ok» de Astra.

### Hora de publicación (desde el 4-11-2026)
Cada reel sale a la hora en que más seguidores de @astra.automations están conectados ese día de la semana (insight `online_followers`, que Meta da en hora del Pacífico; convertido a Madrid) y que coincide con los reels que más alcance han tenido (publicados de 17:00 a 23:30). El pico está entre las 21:00 y las 23:00; se publica justo antes del pico:
lunes, martes, jueves y viernes 21:30 · miércoles, sábado y domingo 20:30. El flujo de n8n se ejecuta a y media, así que la hora siempre es HH:30. Revisar cada mes con los datos nuevos.
