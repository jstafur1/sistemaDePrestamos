# ASSUMPTIONS.md

## S-01 · Tipos de persona solicitante  
- **Decisión:** pueden ser docentes o estudiantes.
- **Motivo:** Son las personas que necesitan estos equipos para poder desempeñar su labor.
- **Consecuencia:** el tipo (docente o estudiante) se guarda como dato
  del solicitante. El código universitario es obligatorio para
  estudiantes y opcional para docentes.

## S-02 · Fecha y zona horaria
- **Decisión:** "hoy" es la fecha de calendario en America/Bogota
  (UTC-5), sin hora. La fecha de vencimiento se guarda como fecha
  (DATE) y se calcula al entregar: fecha local de entrega + plazo de
  la categoría.
- **Motivo:** el servidor y la base de datos trabajan en UTC; desde las
  7 p. m. en Colombia ya es el día siguiente en UTC, y sin una zona
  fija un préstamo figuraría vencido horas antes.
- **Consecuencia:** vencido = hoy posterior a la fecha de vencimiento.
  Días de atraso = hoy menos fecha de vencimiento (0 si no está
  vencido). El instante exacto de la entrega se guarda aparte, con
  zona horaria, solo como registro.
  
## S-03 · Clave para el administrador
- **Decisión:** las rutas del administrador exigen una clave compartida,
  leída de la variable de entorno ADMIN_API_KEY.
- **Motivo:** sin login, cualquiera que conozca la dirección podría
  marcar entregas y devoluciones o liberar equipos bloqueados; la clave
  es la protección mínima.
- **Consecuencia:** quien conozca la clave opera como administrador y no
  queda registro de quién fue, salvo el texto declarado al liberar un
  equipo (S-09). La clave no se versiona: va en .env, y .env.example
  documenta solo el nombre.

## S-04 · Correo y notificaciones
- **Decisión:** el correo institucional es un dato obligatorio del
  solicitante y se guarda. No se envía ni se registra ninguna
  notificación por correo.
- **Motivo:** el correo identifica y permite contactar a la persona; el
  envío real queda fuera del alcance de esta versión.
- **Consecuencia:** solo se valida el formato. No hay tabla de
  notificaciones. El correo no es único: la identidad es el documento.

## S-05 · Identificación del solicitante
- **Decisión:** el solicitante es una entidad persistente identificada
  por su número de documento (único). La primera solicitud con un
  documento crea el registro; en las siguientes se valida que el
  nombre coincida y, si no, la solicitud se rechaza.
- **Motivo:** evitar que se crucen préstamos de personas distintas con
  un mismo documento y poder aplicar la regla de bloqueo por documento.
- **Consecuencia:** los nombres se comparan normalizados (sin tildes,
  sin distinguir mayúsculas, sin espacios sobrantes). Si el primer
  registro tuvo un error de escritura, esa persona queda rechazada
  hasta que el administrador lo corrija en la base de datos; no hay
  pantalla de edición en esta versión.

## S-06 · Solicitudes sin reclamar
- **Decisión:** una solicitud aparta el equipo. El administrador cancela
  las solicitudes que nadie reclama; no hay vencimiento automático.
  Cancelar es una operación atómica: el préstamo pasa de Solicitado a
  Cancelado y el equipo de Apartado a Disponible, en la misma
  transacción.
- **Motivo:** un equipo apartado y abandonado no debe quedar fuera de
  circulación para siempre.
- **Consecuencia:** el equipo sigue no disponible hasta que el
  administrador cancele. Como no hay tope de solicitudes (S-08), una
  persona podría apartar muchas unidades; el único control es la
  cancelación manual. Riesgo aceptado.

## S-07 · Asignación del equipo
- **Decisión:** el solicitante elige la categoría y el sistema asigna
  una unidad Disponible de esa categoría. Una solicitud pide un solo
  equipo.
- **Motivo:** el solicitante no conoce el inventario y la solicitud
  queda más simple.
- **Consecuencia:** si no hay unidad Disponible en la categoría, la
  solicitud se rechaza por falta de stock. Para pedir dos equipos se
  hacen dos solicitudes.

## S-08 · Sin tope de préstamos y bloqueo por vencido
- **Decisión:** no hay máximo de préstamos por persona. No puede crear
  solicitudes quien tenga al menos un préstamo Entregado con fecha de
  vencimiento anterior a hoy.
- **Motivo:** el enunciado solo prohíbe pedir a quien tiene un préstamo
  vencido.
- **Consecuencia:** solo cuentan los préstamos Entregado, porque una
  solicitud no tiene fecha de vencimiento. El bloqueo se levanta al
  registrar la devolución de los préstamos vencidos.

## S-09 · Liberación de un equipo bloqueado
- **Decisión:** una devolución con novedad deja el equipo Bloqueado. El
  administrador lo libera con una acción explícita que lo pasa a
  Disponible.
- **Motivo:** el enunciado exige liberación manual.
- **Consecuencia:** se registra cuándo y quién liberó, en la devolución.
  "Quién" es un texto declarado, no verificado, porque no hay login.
  La novedad es de un solo tipo (daño o faltante) más una descripción.

## S-10 · Concurrencia al apartar
- **Decisión:** la base de datos impide dos préstamos activos
  (Solicitado o Entregado) sobre el mismo equipo. Si al apartar la
  inserción falla por esa restricción, el sistema prueba con otra
  unidad, con un máximo de intentos, y si no queda ninguna responde
  que no hay stock.
- **Motivo:** la garantía queda en el motor de base de datos, no en el
  código.
- **Consecuencia:** las pruebas de esta regla necesitan PostgreSQL real.
  La comparación con el bloqueo pesimista va en un ADR.

## S-11 · Mantenimiento
- **Decisión:** el administrador puede poner un equipo en Mantenimiento
  solo si está Disponible, y sacarlo devolviéndolo a Disponible.
- **Motivo:** evitar sacar de circulación una unidad ya apartada o
  prestada.
- **Consecuencia:** para un equipo Apartado o Prestado se cancela o se
  devuelve primero.

## S-12 · Inventario por unidades
- **Decisión:** cada equipo es una unidad física con código de
  inventario único y pertenece a una categoría. El stock de una
  categoría es el número de unidades Disponible y se calcula, no se
  guarda.
- **Motivo:** las reglas de mantenimiento y de novedad aplican a una
  unidad concreta, no a una categoría completa.
- **Consecuencia:** el modelo tiene una fila por unidad y el stock sale
  de una consulta. Los datos iniciales (varias unidades por categoría)
  se cargan con un script, no con las pruebas.

  ## S-13 · Nombre en mayúsculas
- **Decisión:** el nombre completo se guarda en mayúsculas [el sistema
  lo convierte / el sistema rechaza el que llega en minúsculas].
- **Motivo:** [tu razón]
- **Consecuencia:** la comparación de S-05 sigue ignorando tildes y
  espacios sobrantes; la mayúscula solo afecta cómo se guarda y se
  muestra.