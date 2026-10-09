# ADR-0001: Herramienta de IA para el desarrollo

## Estado
Aceptada, 2026-10-09

## Contexto
La prueba permite usar IA, pero exige poder explicar cada decisión y
dejar evidencia del proceso. Tengo sesiones cortas de trabajo (por
ejemplo, 1 hora) repartidas en varios días, así que necesito que la
herramienta conserve contexto entre sesiones y que yo pueda revisar
cada cambio antes de aceptarlo.

## Opciones consideradas
A. Antigravity como agente principal en el IDE, con Claude en el chat
   como mentor y segunda opinión de diseño.
B. Solo Claude en el chat. Ve únicamente lo que le pego, no ejecuta
   tests ni lee el repositorio, y yo tendría que copiar todo a mano.
C. Solo Antigravity, sin segunda herramienta. Menos fricción, pero sin
   una revisión externa de mis decisiones de diseño.

## Decisión
Opción A. Antigravity, en modo Planning, escribe y modifica código
siguiendo AGENTS.md. Claude en el chat me guía, discute alternativas y
revisa mis documentos. Yo decido, reviso cada diff y hago todos los
commits y pushes.

## Consecuencias
- A favor: el agente ve el repositorio, puede correr los tests y mostrar
  un plan antes de escribir. El chat me sirve para entender el porqué.
- En contra / riesgos: aceptar código que no entiendo; dos herramientas
  con contexto distinto pueden contradecirse; los modelos y funciones
  cambian entre versiones.
- Controles: AGENTS.md prohíbe commit, push, instalar dependencias sin
  avisar y tocar .env; las reglas de negocio se escriben primero como
  test; reviso cada diff; registro en BITACORA-IA.md qué pedí, qué
  acepté y qué rechacé.

## Evidencia
- Modelo seleccionado en Antigravity al momento de esta decisión:
  Gemini 3.8 Flash Medium.
- Los modos Planning/Fast y el uso de AGENTS.md en la raíz los conocí
  por guías de la comunidad, no por documentación oficial. 