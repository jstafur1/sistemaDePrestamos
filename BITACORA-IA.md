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

## 2026-10-18 · Sesión: revisión de requisitos y modelo de datos

**Qué pedí.** Al agente de Antigravity (Claude Sonnet 4.6 Thinking), una
revisión de AGENTS.md y ASSUMPTIONS.md sin escribir código ni modificar
archivos. Devolvió 10 hallazgos con dos opciones cada uno. Al mentor en el
chat le pedí que convirtiera mis decisiones en texto para los documentos y
que propusiera el modelo de datos para que yo lo estudiara.

**Qué decidí yo.** H-01 a H-06 y H-08 a H-10: opción A, salvo H-03: opción B
(concurrencia optimista). En H-07 decidí que no hay tope de préstamos y que
solo bloquea tener un préstamo Entregado vencido. El solicitante elige la
categoría y el sistema asigna la unidad; una solicitud pide un solo equipo.

**Qué reformulé o rechacé del agente.**
- H-01: era un falso dilema; el problema real era que S-04 estaba mal
  redactado y parecía decir que el correo no se guardaba.
- H-03: su consecuencia era incorrecta. Con una restricción única en la base
  de datos, la segunda solicitud falla, no duplica el apartado.
- H-07: interpretó "dos equipos prestados a la vez" como un tope de dos.
  Quise decir que puede tener más de uno. Reescribí la frase y lo dejé en el
  historial de correcciones de AGENTS.md.

**Qué no detectó el agente.** Si el solicitante elige categoría o unidad
concreta, si una solicitud pide uno o varios equipos, cómo se comparan los
nombres en S-05 y las transiciones de Mantenimiento. Los identifiqué yo
antes de leer su respuesta.

**Modelo de datos.** Lo propuso Claude en el chat (cinco tablas, índice
único parcial para impedir dos préstamos activos sobre un equipo, fecha de
vencimiento guardada). Yo lo revisé y contesté tres preguntas de
comprensión; en la de concurrencia corregí mi idea inicial de "azar":
la base de datos garantiza que no ganen las dos solicitudes, y cuál gana
depende del orden de llegada.

**Qué no he verificado todavía.** La conexión a Supabase, la estrategia de
pruebas de integración contra PostgreSQL real y que las migraciones
reproduzcan el modelo.

## 2026-10-18 · Incidentes de entorno

**Incidente 2: tzdata.** Al probar `ZoneInfo('America/Bogota')` obtuve
`ModuleNotFoundError: No module named 'tzdata'` y luego
`ZoneInfoNotFoundError`. Causa: Windows no trae base de datos de zonas
horarias, y `zoneinfo` necesita el paquete `tzdata`. Esto afecta a S-02
(la fecha de vencimiento se calcula en zona de Bogotá). Solución: instalar
tzdata y declararlo en requirements.txt para que no dependa de mi máquina.
[Resultado: confirma que la prueba imprimió "zona ok".]

**Incidente 3: el venv desapareció.** Al activar el entorno,
`venv/Scripts/activate` no existía y `which python` apuntaba al Python
global. Causa probable: al limpiar el historial con filter-branch, Git
sincronizó la carpeta de trabajo y eliminó venv/, que ya no estaba en el
historial. El mentor me había dicho que la carpeta no se borraba y se
equivocó. [Confirma con `ls venv` que realmente no existía o estaba
incompleta.] Solución: recrear el entorno con Python 3.11 y reinstalar con
`pip install -r requirements.txt`.

**Verificación del entorno.** `venv/pyvenv.cfg` indica Python 3.11.0 y el
comando de creación apunta a la carpeta del proyecto. `pip list` mostró
alembic, fastapi, psycopg2-binary y SQLAlchemy, pero no tzdata ni pytest.
`which python` devolvió una ruta mezclada (`/c/Users/.../\Users\...\venv/
Scripts/python`) que Bash interpreta como relativa a la carpeta actual; la
comprobación fiable es `python -c "import sys; print(sys.executable)"`.
`python -c "import sys; print(sys.executable)"` devolvió
`C:\Users\Lenovo\prestamo-equipos-lab\venv\Scripts\python.exe`. Tras
`pip install tzdata`, la prueba de ZoneInfo('America/Bogota') imprimió
"zona ok". El diff de requirements.txt agregó únicamente tzdata==2026.5.
exceptiongroup y tomli siguen en el archivo porque `pip install -r`
los reinstaló; no estorban en Python 3.11. No pude comprobar con qué versión
de Python se creó el entorno original, así que no lo afirmo.
Hallazgo: el primer requirements.txt incluía exceptiongroup y tomli, que
normalmente solo se instalan en Python anterior a 3.11; [confirma con el
diff de requirements.txt que ya no aparecen].


**Hallazgo.** requirements.txt incluía exceptiongroup y tomli, que
normalmente solo se instalan en Python anterior a 3.11, así que el venv
original probablemente se creó con otra versión distinta de la que dice
AGENTS.md. [Confirma con el diff de requirements.txt tras regenerarlo.]

**Lección.** El venv es desechable y se reconstruye desde requirements.txt.
Antes de reescribir el historial, hacer una copia de seguridad del
repositorio.

**Incidente 5: falló la autenticación contra Supabase.** La prueba de
conexión devolvió `FATAL: password authentication failed for user "postgres"`
contra el host del Session pooler. El mentor sugirió primero que el usuario
estaba mal escrito, pero la verificación con make_url (sin imprimir la
contraseña) mostró usuario `postgres.<referencia-del-proyecto>`, host
`aws-0-us-east-1.pooler.supabase.com`, puerto 5432 y base `postgres`: todo
correcto. Eso descartó el usuario, el host y la red, y dejó la contraseña
como causa más probable. [Resultado de la inspección de la contraseña: ...]
[Solución: restablecí la contraseña de la base de datos con una que solo
tiene letras y números y actualicé .env.] [Resultado: `select 1` imprimió 1.]
**Lección.** Diagnosticar por descarte: verificar cada pieza (usuario, host,
puerto, base, contraseña) antes de cambiar nada, y no documentar una causa
que la evidencia no respalda.

## 2026-10-19 · Plan de la base de pruebas (Parte 2.2)

**Qué pedí.** Al agente, en modo Planning y sin código, un plan para la
configuración tipada, un endpoint /health y las primeras pruebas, con
SecretStr y carga perezosa. [Modelo usado: ...]

**Qué hizo bien.** Tests antes de la implementación, sin tocar .env, sin
instalar dependencias ni hacer commit, y sin añadir cosas fuera del alcance.

**Qué corregí.**
- Ubicó test_health.py en tests/integration y solo lo escaló como duda
  cuando lo revisé. La causa estaba en AGENTS.md, que definía mal unit e
  integration; lo reescribí por dependencia externa.
- Su supuesto de que el .env "nunca se lee" en los tests era incorrecto;
  la prueba de ello es que un test de "sin variables" debe fallar y solo
  falla si el archivo real no se lee.
- La comprobación de carga perezosa no podía fallar; la cambié por
  cache_info().currsize == 0.
- Faltaba el test de variables ausentes y el manejo de variables extra.

**Observación.** El agente se autoevaluó con una tabla de ✅ que declaraba
cumplido un punto que no lo estaba; mi revisión tiene que ser la fuente de
verdad, no su resumen.