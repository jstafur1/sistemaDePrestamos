# ASSUMPTIONS.md

## S-01 · Tipos de persona solicitante
- **Decisión:** pueden ser docentes o estudiantes.
- **Motivo:** Son las personas que necesitan estos equipos para poder desempeñar su labor.
- **Consecuencia:** el código universitario es opcional para docentes.

## S-02 · Zona horaria 
- **Decisión:** La fecha se toma en zona de Bogotá (UTC-5).
- **Motivo:** Las entregas y devoluciones de los equipos deben tener su hora especifíca, ya que no se conoce la zona horaria del usuario solicitante.
- **Consecuencia:** Se debe tener en cuenta la fecha actual para los cálculos de vencimiento.

## S-03 · Clave para el administrador
- **Decisión:** Se propone una clave compartida en una variable de entorno.
- **Motivo:** Con clave compartida en variable de entorno, se cumple con la regla de que el administrador es quien marca como prestado en el sistema cuando efectivamente entregue el equipo.  
- **Consecuencia:** protección mínima: quien conozca la clave opera como administrador, sin rastro de quién fue.

## S-04 · Correos
- **Decisión:** fuera de alcance, no se envían ni se registran
- **Motivo:** Para esta versión no se requiere envío real de correos.
- **Consecuencia:** No se envían no se registran

## S-05 · Identificación del solicitante
-**Decisión** Identificación del solicitante por número de documento, y rechazo si repite documento con otro nombre.
- **Motivo** Para la integridad de datos y que por error no se crucen prestamos de personas diferentes con el mismo documento.
- **Consecuencia:** Una cédula que no coincida con el nombre debe ser rechazada, esto en el caso de solicitar otro equipo. 

## S-06 Equipo apartado 
- **Decisión:** Una solicitud aparta el equipo, el administrador cancela las solicitudes que nadie reclama (no hay vencimiento automático).
- **Motivo:** El administrador debe velar por los equipos y una solicitud que nadie reclama debe ser cancelada para que el equipo vuelva a estar disponible.
- **Consecuencia** El estudiante o docente debe estar pendiente de sus solicitudes y estar pendiente de reclamar el equipo.





