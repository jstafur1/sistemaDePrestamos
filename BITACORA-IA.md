## 2026-10-09 · Sesión 1: contexto del agente y repositorio

**Qué pedí.** Ayuda a un mentor en el chat para dividir la prueba en
partes, redactar AGENTS.md y aprender el flujo con Antigravity.

**Qué decidí yo.**
- Recortar el alcance: sin login, sin imagen del carnet, sin correos
  reales y sin vencimiento automático de solicitudes.
- Definir vencido (fecha de hoy posterior a la de vencimiento) y días
  de atraso, con la fecha de vencimiento calculada y guardada al
  entregar el equipo.
- Cinco estados de equipo (incluyendo Apartado y Bloqueado) y cuatro de
  préstamo (incluyendo Cancelado).
- Identificar a la persona solicitante por su documento y rechazar la
  solicitud si repite el documento con otro nombre.
- Zona horaria de Bogotá para las fechas.

**Qué corregí o rechacé.**
- Mi regla 1 usaba "entrega" donde quería decir "devolución", y rompía
  mi propia convención de vocabulario. La corregí.
- La sugerencia de listar carnet y correos en "Fuera de alcance": la
  rechacé porque ya no estaban en mi AGENTS.md.
- La contradicción sobre qué pasa al devolver (queda disponible vs.
  bloqueado) la resolví con la regla de la novedad.

**Incidente.** Mi primer commit incluyó la carpeta venv/ porque el
.gitignore estaba mal creado: 3800 objetos y casi 19 MiB en el primer
push. Causa: el .gitignore solo evita archivos nuevos, no quita los ya
rastreados. Acción: reescribí el historial con filter-branch y estoy
volviendo a publicar con --force-with-lease. [Estado: actualiza aquí si
ya quedó limpio en GitHub.]

**Qué no he verificado todavía.**
- La revisión de ambigüedades por el agente en Antigravity.
- La tabla de transiciones de estados y ASSUMPTIONS.md.
- La versión de Python (mi requirements.txt trae paquetes que suelen
  instalarse en versiones anteriores a 3.11): correr `python --version`.
- La conexión a Supabase.