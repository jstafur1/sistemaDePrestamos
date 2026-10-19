# AGENTS.md

## Contexto del proyecto

Es un sistema basado en el seguimiento de equipos de laboratorio los cuales son prestados. 

Este sistema tiene 5 entidades ; Equipo, categoría de equipo, persona solicitante, préstamo, devolución. 

La persona solicitante puede ser un docente o un estudiante, se descarta por completo inicio de sesión mediante un login.  

Cuando se realiza una solicitud el equipo queda apartado.

Para realizar una solicitud de préstamo, debe ingresar unos datos:  

- Nombre completo (en mayúsculas, ver S-13)

- Correo institucional 

- Número de cédula o tarjeta de identidad 

- Código universitario (Opcional si es docente)

Si alguien repite su documento de identidad (Número de cédula o tarjeta de identidad ) con otro nombre debe ser rechazada la solicitud.


La persona encargada de los equipos (Administrador) tiene una vista aparte donde recibe las solicitudes y este será el que marque como prestado en el sistema cuando efectivamente entregue el equipo. Y cuando el solicitante devuelva el equipo, el equipo queda Disponible, salvo que la devolución tenga novedad: entonces queda Bloqueado.


Los tiempos de prestamo de los equipos son  

Portátiles = 7 días 

Kits de sensores = 10 dias  

Osciloscopios  = 12 dias 

La fecha en el calendario se tomará de la zona horaria America/Bogota (UTC-5)

La fecha de vencimiento = Sería la fecha de entrega en el calendario + plazo por categoría, calculado y guardada al momento de la entrega. 

Vencido = fecha en el calendario posterior a esa fecha. 

Días de atraso = fecha en el calendario menos la fecha de vencimiento. 

El sistema debe tener en cuenta sus fechas de entrega y devolución. En el momento en que se cumpla el plazo de devolución empezará a contar los dias de retraso. Todos los equipos que tengan retraso deben estar en una lista que el administrador puede seleccionar en su vista. 


## Modelo de dominio
Cinco entidades: CategoriaEquipo (con plazo_dias), Equipo (unidad física
con código de inventario único), Solicitante (identificado por número de
documento único), Prestamo y Devolucion (una por préstamo devuelto; guarda
la novedad si la hay).
El plazo se guarda en la categoría. Al entregar se calcula y se guarda
fecha_vencimiento en el préstamo; cambiar el plazo después no afecta a los
préstamos ya entregados.
El stock de una categoría no se guarda: es el número de equipos Disponible.



## Stack 

Python 3.11 

FastAPI 

PostgreSQL en la nube con plan gratuito en supabase. 

Pytest para pruebas 

SQLAlchemy 

Alembic 

La cadena de conexión va en .env como DATABASE_URL 

Variables de entorno (en .env, no versionado; .env.example lista los
nombres sin valores): DATABASE_URL y ADMIN_API_KEY.
Las rutas del administrador exigen ADMIN_API_KEY en un encabezado.

tzdata (obligatorio en Windows: sin él, zoneinfo no encuentra America/Bogota)

## Reglas del negocio (No negociables)

Los estados del equipo son = Disponible, Prestado, Mantenimiento, Bloqueado, Apartado.
Los estados del préstamo son = Solicitado, Entregado, Devuelto, Cancelado.

Un equipo marcado en mantenimiento no aparece como disponible aunque esté físicamente en el almacén. 

El plazo de préstamo depende de la categoría del equipo, no del solicitante. Estos plazos ya están escritos en el contexto 

Una devolución puede registrarse con novedad (daño, faltante), y eso bloquea el equipo hasta que el administrador lo libere. Bloquea solo el equipo, pero el solicitante no queda bloqueado 

Consulta obligatoria: Listado de préstamos vencidos a la fecha, con días de atraso. 

- No hay tope de préstamos por persona.
- No puede solicitar quien tenga al menos un préstamo Entregado con
  fecha_vencimiento anterior a hoy. Se levanta al registrar la devolución
  de esos préstamos.
- Cada solicitud pide un solo equipo: el solicitante elige categoría y el
  sistema asigna una unidad Disponible.
- El tipo de solicitante (docente o estudiante) se guarda. El código
  universitario es obligatorio para estudiantes y opcional para docentes.
  

## Fuera de alcance
- Login, usuarios, sesiones y roles.
- Envío o registro de notificaciones por correo.
- Vencimiento automático de solicitudes (el administrador las cancela, S-06).


## Transiciones permitidas (cualquier otra se rechaza con 409)
| Evento | Quién | Préstamo | Equipo | Condición |
|---|---|---|---|---|
| Solicitar | Solicitante | nuevo → Solicitado | Disponible → Apartado | Hay unidad Disponible en la categoría; sin préstamo Entregado vencido; documento y nombre coherentes |
| Entregar | Administrador | Solicitado → Entregado ¿| Apartado → Prestado | Guarda entregado_en y fecha_vencimiento |
| Devolver sin novedad | Administrador | Entregado → Devuelto | Prestado → Disponible | |
| Devolver con novedad | Administrador | Entregado → Devuelto | Prestado → Bloqueado | Tipo y descripción de la novedad obligatorios |
| Liberar bloqueo | Administrador | sin cambio | Bloqueado → Disponible | Registra liberado_en y liberado_por |
| Cancelar solicitud | Administrador | Solicitado → Cancelado | Apartado → Disponible | Atómico |
| Enviar a mantenimiento | Administrador | sin cambio | Disponible → Mantenimiento | Solo desde Disponible |
| Sacar de mantenimiento | Administrador | sin cambio | Mantenimiento → Disponible | |


## Convenciones 

- app/models: tablas SQLAlchemy. app/schemas: modelos Pydantic de entrada y salida (clases separadas de los modelos). 

- app/routers: solo recibe la petición y delega. Nunca contiene reglas de negocio. 

- app/services: aquí viven las reglas de negocio. Reciben la fecha actual como parámetro, no la leen del sistema. 

- app/core: configuración y conexión a la base de datos. 

- Las violaciones de reglas lanzan excepciones de dominio propias, y la API las convierte en respuestas HTTP claras (409 o 422). 

- Tests: tests/unit para reglas puras, tests/integration para la API. Nombre: test_<regla>_<escenario>. 

- Vocabulario fijo: "entrega" y "devolución" no se mezclan. 

- Las clases y variables van escritas en español. 

- app/services/reglas.py: funciones puras, sin SQLAlchemy ni FastAPI y sin
  leer el reloj (¿está vencido?, días de atraso, ¿puede solicitar?,
  nombres equivalentes).
- app/services/<recurso>.py: casos de uso. Reciben la Session y la fecha
  de hoy, cargan datos, llaman a reglas.py y guardan. Una operación es
  una transacción.
- Los tests se separan por dependencia externa, no por capa:
  - tests/unit: no usan base de datos ni red. Incluye reglas.py y las
    pruebas de la API con TestClient que no abren sesión de base de datos
    (por ejemplo /health, validación de entrada y clave de administrador).
  - tests/integration: usan PostgreSQL real (casos de uso y endpoints que
    persisten datos).
- La integridad crítica vive también en la base de datos (restricciones
  únicas y CHECK), no solo en el código.

- Al apartar, la garantía es el índice único parcial de la base de datos; si la inserción falla, se reintenta con otra unidad (máximo [N] intentos) y no se usan bloqueos de fila (S-10).

## Comportamiento del agente 

- Antes de escribir código, propone un plan y espera aprobación. 

- Reglas de negocio: primero el test, después la implementación. 

- Ante un vacío del enunciado, pregunta o lo registra en ASSUMPTIONS.md; nunca inventa. 

- No hace commit ni push, no instala dependencias sin avisar, no lee ni escribe .env. 

- Antes de ejecutar comandos de Python, verifica el intérprete con
  `python -c "import sys; print(sys.executable)"`; debe apuntar a
  venv\Scripts\python.exe. Usa `python -m pip` y `python -m pytest`, y
  ejecuta siempre desde la raíz del proyecto.
  

## Historial de correcciones al agente 
- 2026-10-16: el agente leyó "puede tener dos equipos prestados a la vez"
  como un tope de dos. La regla correcta es que no hay tope. Se reescribió
  la frase y se agregó S-08.

  - 2026-10-19: el agente ubicó test_health.py en tests/integration y solo lo
  escaló como duda al revisarlo contra mi lista de revisión. La causa era una
  definición ambigua en AGENTS.md (unit = solo reglas.py; integration = API
  contra PostgreSQL real), que dejaba sin lugar a las pruebas de API sin base
  de datos. Se redefinió la separación por dependencia externa.