# AGENTS.md

## Contexto del proyecto

Es un sistema basado en el seguimiento de equipos de laboratorio los cuales son prestados. 

Este sistema tiene 5 entidades ; Equipo, categoría de equipo, persona solicitante, préstamo, devolución. 

La persona solicitante puede ser un docente o un estudiante, se descarta por completo inicio de sesión mediante un login.  

Cuando se realiza una solicitud el equipo queda apartado.

Para realizar una solicitud de préstamo, debe ingresar unos datos:  

- Nombre completo  (TODO EN MAYÚSCULAS DEBE SER ESCRITO)

- Correo institucional 

- Número de cédula o tarjeta de identidad 

- Código universitario (Opcional si es docente)

Si alguien repite su documento de identidad (Número de cédula o tarjeta de identidad ) con otro nombre debe ser rechazada la solicitud.


Un Equipo es una unidad física con código de inventario único,
perteneciente a una categoría. El stock de una categoría no se guarda:
se calcula contando sus equipos en estado Disponible.

La persona encargada de los equipos (Administrador) tiene una vista aparte donde recibe las solicitudes y este será el que marque como prestado en el sistema cuando efectivamente entregue el equipo. Y cuando el solicitante devuelva el equipo, el equipo queda Disponible, salvo que la devolución tenga novedad: entonces queda Bloqueado.

El administrador tiene una protección minima, el administrador tiene un acceso mediante una clave compartida en una variable de entorno para acessar a su vista.

Los tiempos de prestamo de los equipos son  

Portátiles = 7 días 

Kits de sensores = 10 dias  

Osciloscopios  = 12 dias 

La fecha en el calendario se tomará de la zona horaria America/Bogota (UTC-5)

La fecha de vencimiento = Sería la fecha de entrega en el calendario + plazo por categoría, calculado y guardada al momento de la entrega. 

Vencido = fecha en el calendario posterior a esa fecha. 

Días de atraso = fecha en el calendario menos la fecha de vencimiento. 

El sistema debe tener en cuenta sus fechas de entrega y devolución. En el momento en que se cumpla el plazo de devolución empezará a contar los dias de retraso. Todos los equipos que tengan retraso deben estar en una lista que el administrador puede seleccionar en su vista. 


## Stack 

Python 3.11 

FastAPI 

PostgreSQL en la nube con plan gratuito en supabase. 

Pytest para pruebas 

SQLAlchemy 

Alembic 

La cadena de conexión va en .env como DATABASE_URL 


## Reglas del negocio (No negociables)

Un estudiante o docente con un préstamo vencido sin devolver no puede pedir otro equipo. Tan pronto el administrador registre la devolución de este, ya tiene la opcion disponible. Un solicitante puede tener dos equipos prestados a la vez sin estar vencido. 

Los estados del equipo son = Disponible, Prestado, Mantenimiento, Bloqueado, Apartado.
Los estados del préstamo son = Solicitado, entregado, devuelto, cancelado.

Un equipo marcado en mantenimiento no aparece como disponible aunque esté físicamente en el almacén. 

El plazo de préstamo depende de la categoría del equipo, no del solicitante. Estos plazos ya están escritos en el contexto 

Una devolución puede registrarse con novedad (daño, faltante), y eso bloquea el equipo hasta que el administrador lo libere. Bloquea solo el equipo, pero el solicitante no queda bloqueado 

Consulta obligatoria: Listado de préstamos vencidos a la fecha, con días de atraso. 

  

## Fuera de alcance 

Se descarta un login para los usuarios estudiantes y docentes.
Vencimiento automático de solicitudes.
(riesgo anotado en ASSUMPTIONS.md)

## Convenciones 

- app/models: tablas SQLAlchemy. app/schemas: modelos Pydantic de entrada y salida (clases separadas de los modelos). 

- app/routers: solo recibe la petición y delega. Nunca contiene reglas de negocio. 

- app/services: aquí viven las reglas de negocio. Reciben la fecha actual como parámetro, no la leen del sistema. 

- app/core: configuración y conexión a la base de datos. 

- Las violaciones de reglas lanzan excepciones de dominio propias, y la API las convierte en respuestas HTTP claras (409 o 422). 

- Tests: tests/unit para reglas puras, tests/integration para la API. Nombre: test_<regla>_<escenario>. 

- Vocabulario fijo: "entrega" y "devolución" no se mezclan. 

- Las clases y variables van escritas en español. 


## Comportamiento del agente 

- Antes de escribir código, propone un plan y espera aprobación. 

- Reglas de negocio: primero el test, después la implementación. 

- Ante un vacío del enunciado, pregunta o lo registra en ASSUMPTIONS.md; nunca inventa. 

- No hace commit ni push, no instala dependencias sin avisar, no lee ni escribe .env. 

  

## Historial de correcciones al agente 