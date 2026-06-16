
# Gestor Universitario FIUBA — Backend

API REST desarrollada con Flask y MySQL para la gestión de cursos universitarios.
Proyecto final de Introducción al Desarrollo de Software — Curso Lanzillota 2026.

> **💡 Frontend:** El repositorio correspondiente al backend de esta aplicación se encuentra disponible en: `https://github.com/gjoel6055-wq/gestor-universitario-armjsss`
---

## Tecnologías

- **Python 3.12**
- **Flask** — framework web
- **MySQL** — base de datos relacional
- **mysql-connector-python** — conexión a MySQL
- **PyJWT** — autenticación con tokens JWT
- **Werkzeug** — hash de contraseñas
- **python-dotenv** — variables de entorno

# Gestor Universitario FIUBA — Backend

API REST desarrollada con Flask y MySQL para la gestión de cursos universitarios.
Proyecto final de Introducción al Desarrollo de Software — Curso Lanzillota 2026.

> **💡 Frontend:** El repositorio correspondiente al backend de esta aplicación se encuentra disponible en: `https://github.com/gjoel6055-wq/gestor-universitario-armjsss`
---

## Tecnologías

- **Python 3.12**
- **Flask** — framework web
- **MySQL** — base de datos relacional
- **mysql-connector-python** — conexión a MySQL
- **PyJWT** — autenticación con tokens JWT
- **Werkzeug** — hash de contraseñas
- **python-dotenv** — variables de entorno

---

## Estructura del proyecto

```
gestion_curso_fiuba/
├── Backend/
│   ├── app/
│   │   ├── db.py                               # Conexión a MySQL
│   │   ├── constants.py                        # Constantes globales (regex, etc)
│   │   ├── routes/
│   │   │   ├── auth.py                         # POST /login, /registro, /logout
│   │   │   ├── usuarios.py                     # GET /usuarios
│   │   │   ├── alumnos.py                      # CRUD alumnos + abandono + CSV
│   │   │   ├── docentes.py                     # CRUD docentes
│   │   │   ├── cursos.py                       # CRUD cursos
│   │   │   ├── tipos_evaluacion.py             # CRUD tipos de evaluación
│   │   │   ├── evaluaciones.py                 # CRUD evaluaciones
│   │   │   ├── equipos.py                      # CRUD equipos + alumnos + evaluaciones
│   │   │   ├── notas.py                        # CRUD notas
│   │   │   ├── asistencias.py                  # QR + asistencias
│   │   │   ├── materiales.py                   # CRUD materiales
│   │   │   └── log.py                          # Consulta de log de actividad
│   │   ├── services/
│   │   │   ├── auth_service.py                 # Login, registro, decorador JWT
│   │   │   ├── alumno_service.py
│   │   │   ├── docente_service.py
│   │   │   ├── curso_service.py
│   │   │   ├── tipo_evaluacion_service.py
│   │   │   ├── evaluacion_service.py
│   │   │   ├── equipo_service.py
│   │   │   ├── nota_service.py
│   │   │   ├── asistencia_service.py
│   │   │   ├── material_service.py
│   │   │   ├── log_service.py
│   │   │   ├── qr_service.py
│   │   │   ├── mail_service.py
│   │   │   └── pdf_service.py
│   │   └── repositories/
│   │       ├── usuario_repository.py
│   │       ├── alumno_repository.py
│   │       ├── docente_repository.py
│   │       ├── curso_repository.py
│   │       ├── tipo_evaluacion_repository.py
│   │       ├── evaluacion_repository.py
│   │       ├── equipo_repository.py
│   │       ├── nota_repository.py
│   │       ├── asistencia_repository.py
│   │       ├── material_repository.py
│   │       └── log_repository.py
│   ├── database/
│   │   ├── schema.sql                          # Creación de tablas
│   │   └── seed.sql                            # Datos de prueba
│   └── app.py                                  # Punto de entrada
├── README.md
├── requirements.txt
├── setup_virtualenv.sh
├── setup_virtualenv.bat
├── .env
└── .env.example
```

---

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/gjoel6055-wq/gestor-universitario-armjsss
cd gestor-universitario-armjsss
```

### 2. Configurar la Base de Datos con MySQL local

Si ya tenes MySQL corriendo en tu maquina (puerto 3306 por defecto):

Crear la base de datos y cargar el esquema y datos de prueba:

**Linux / macOS / WSL:**
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS gestor_universitario;"
mysql -u root -p gestor_universitario < Backend/database/schema.sql
mysql -u root -p gestor_universitario < Backend/database/seed.sql
```

**Windows PowerShell:**
```powershell
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS gestor_universitario;"
Get-Content Backend\database\schema.sql | mysql -u root -p gestor_universitario
Get-Content Backend\database\seed.sql | mysql -u root -p gestor_universitario
```

Verificar que las tablas se hayan creado:
```bash
mysql -u root -p -e "USE gestor_universitario; SHOW TABLES;"
```
*Si tu usuario, password, puerto o nombre de base no coinciden con los defaults, actualiza el `.env` antes de levantar la API.*

### 3. Configurar las variables de entorno

```bash
cp .env.example .env
```

Editá el archivo `.env` con tus credenciales:

```env
EMAIL_SENDER=gestoruniversitario123@gmail.com
EMAIL_PASSWORD=tu contraseña de negocio
API_BASE_URL = "http://127.0.0.1:8080"
FRONT_BASE_URL = "http://127.0.0.1:5030"
DB_HOST = "127.0.0.1"
DB_PORT="3306"
DB_USER="root"
DB_PASSWORD=""
DB_NAME="gestor_universitario"
SECRET_KEY=tu_clave_secreta_larga_y_segura
```

### 4. Entorno virtual, instalación y ejecución

El proyecto incluye scripts de setup que crean el entorno virtual, instalan las dependencias y levantan la API automáticamente.

**Windows:**
```cmd
setup_virtualenv.bat
```

**Linux / macOS:**
```bash
chmod +x setup_virtualenv.sh
./setup_virtualenv.sh
```

Una vez iniciada, la API estará disponible en `http://localhost:8080`.

---

## Autenticación

La API usa **JWT (JSON Web Tokens)**. El token se obtiene en el login y debe enviarse en el header de cada request:

```
Authorization: Bearer <token>
```

El token expira a las **8 horas**. Hay dos roles:

| Rol | Permisos |
|---|---|
| `docente` | Acceso completo a todos los endpoints |
| `alumno` | Solo puede ver sus propias notas y asistencias |

---

## Endpoints

## Autenticación y Autorización

| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| POST | `/login` | Iniciar sesión | No |
| POST | `/registro` | Registrar cuenta | No |
| POST | `/logout` | Cerrar sesión | Sí |

### Iniciar sesión
Autentica al usuario en el sistema y retorna un token JWT válido por 8 horas.

*   **Ruta:** `/login`
*   **Método:** `POST`
*   **Auth requerida:** No

**Ejemplo de Petición:**
```json
{
  "email": "garcia.carlos@fiuba.edu.ar",
  "password": "password123"
}
```

**Respuestas HTTP:**
*   `200 OK`
    ```json
    {
      "mensaje": "Login exitoso",
      "token": "eyJhbGciOiJIUzI1NiIsInR5...",
      "datos": {
        "nombre": "Carlos",
        "email": "garcia.carlos@fiuba.edu.ar",
        "rol": "docente"
      }
    }
    ```
*   `401 Unauthorized`
    ```json
    {"error": "La contraseña ingresada es incorrecta"}
    ```
*   `404 Not Found`
    ```json
    {"error": "El email ingresado no se encuentra registrado."}
    ```

### Registrar cuenta
Permite la creación de un nuevo usuario en la base de datos (con rol alumno por defecto).

*   **Ruta:** `/registro`
*   **Método:** `POST`
*   **Auth requerida:** No

**Ejemplo de Petición:**
```json
{
  "nombre": "Juan",
  "apellido": "Perez",
  "email": "juanperez@fiuba.edu.ar",
  "password": "password123",
  "padron": "105554"
}
```

**Respuestas HTTP:**
*   `201 Created`
    ```json
    {"mensaje": "Se creó el usuario con exito."}
    ```
*   `400 Bad Request`
    ```json
    {"error": "Todos los campos son obligatorios"}
    ```
*   `400 Bad Request` (Si el email es inválido)
    ```json
    {"error": "El formato del email no es válido"}
    ```
*   `409 Conflict`
    ```json
    {"error": "El email ingresado ya se encuentra en uso."}
    ```

### Cerrar Sesión
Invalida el token del lado del cliente.

*   **Ruta:** `/logout`
*   **Método:** `POST`
*   **Auth requerida:** Sí

**Respuestas HTTP:**
*   `200 OK`
    ```json
    {"mensaje": "Se cerró la sesión con exito."}
    ```

---


### Cursos

| Método | Endpoint | Descripción | Rol |
|---|---|---|---|
| GET | `/cursos` | Listar todos los cursos | Cualquiera |
| GET | `/cursos/<curso_id>` | Ver curso por ID | Cualquiera |
| POST | `/cursos` | Crear curso | Docente |
| PUT | `/cursos/<curso_id>` | Actualizar curso completo | Docente |
| PATCH | `/cursos/<curso_id>` | Actualizar campos parciales | Docente |
| DELETE | `/cursos/<curso_id>` | Eliminar curso (lógico) | Docente |

**POST /cursos**
```json
{
  "nombre": "Introducción al Desarrollo de Software",
  "cuatrimestre": "1C",
  "anio": 2026,
  "descripcion": "Curso introductorio con Python y Flask"
}
```
**Éxito (201):** Objeto del curso creado.
**Errores:** 400 `{"error": "El cuerpo de la solicitud no puede estar vacío"}`, 409 `{"error": "el curso ya existe"}`

#### PUT `/cursos/<int:curso_id>` y PATCH `/cursos/<int:curso_id>`
**Request PUT (Completo):**
```json
{
  "nombre": "Intro al Desarrollo (Actualizado)",
  "cuatrimestre": "2C",
  "anio": 2026,
  "descripcion": "Nuevo temario"
}
```
**Request PATCH (Parcial):**
```json
{
  "descripcion": "Solo actualizo descripcion"
}
```
**Errores:** 400 (Cuerpo vacío), 404 (No encontrado), 409 (Nombre duplicado).

#### DELETE `/cursos/<int:curso_id>`
**Éxito (200):** `{"mensaje": "Curso {id} eliminado correctamente"}`
**Errores:** 400 (Error validación), 404 `{"error": "curso no encontrado"}`, 409 `{"error": "el curso tiene dependencias asociadas"}`

---

### Alumnos

| Método | Endpoint | Descripción | Rol |
|---|---|---|---|
| GET | `/alumnos` | Listar alumnos | Docente |
| GET | `/alumnos?estado=activo` | Filtrar por estado | Docente |
| GET | `/alumnos?curso_id=<id>` | Filtrar por curso | Docente |
| GET | `/alumnos/<padron>` | Ver alumno por padrón | Docente |
| POST | `/alumnos` | Crear alumno | Docente |
| PUT | `/alumnos/<padron>` | Actualizar alumno completo | Docente |
| PATCH | `/alumnos/<padron>` | Actualizar campos parciales | Docente |
| PATCH | `/alumnos/<padron>/abandono` | Marcar como abandonó | Docente |
| DELETE | `/alumnos/<padron>` | Eliminar alumno (lógico) | Docente |
| POST | `/alumnos/importar-csv` | Importar masivamente | Docente |

#### GET `/alumnos` y GET `/alumnos/<int:padron>`
**Éxito (200):** Devuelve alumnos. **Errores:** 404 `{"error": "Alumno no encontrado."}`

#### POST `/alumnos`
**Request:**
```json
{
  "padron": "103963",
  "nombre": "Carolina",
  "apellido": "Di Matteo",
  "email": "cdimatteo@fiuba.edu.ar",
  "password": "password123"
}
```
**Éxito (201):** Alumno creado.
**Errores:** 400 `{"error": "Faltan campos obligatorios"}`, 409 `{"error": "El padrón ya está registrado."}` o `"El email ya está registrado."`

#### PUT `/alumnos/<int:padron>` y PATCH `/alumnos/<int:padron>`
**Request PUT/PATCH:**
```json
{
  "nombre": "Carolina Nueva",
  "email": "nuevoemail@fiuba.edu.ar",
  "abandono": 1
}
```
**Errores:** 400 `{"error": "Se requiere al menos un campo para actualizar."}`, 404 (No encontrado), 409 (Email en uso).

#### DELETE `/alumnos/<int:padron>`
**Éxito (200):** `{"message": "Alumno eliminado con éxito.", "status": true}`
**Errores:** 404 `{"error": "Alumno no encontrado."}`

---

### Docentes

| Método | Endpoint | Descripción | Rol |
|---|---|---|---|
| GET | `/docentes` | Listar docentes | Cualquiera |
| GET | `/docentes/<legajo>` | Ver docente por legajo | Cualquiera |
| POST | `/docentes` | Crear docente | Docente |
| PUT | `/docentes/<legajo>` | Actualizar completo | Docente |
| PATCH | `/docentes/<legajo>` | Actualizar parcial | Docente |
| DELETE | `/docentes/<legajo>` | Eliminar (lógico) | Docente |

#### POST `/docentes`
**Request:**
```json
{
  "legajo": "9001",
  "nombre": "Martín",
  "apellido": "Sosa",
  "email": "msosa@fiuba.edu.ar",
  "password": "password123"
}
```
**Éxito (201):** Docente creado.
**Errores:** 400 (Campos obligatorios), 409 (Legajo o email en uso).

*(Soporta GET, PUT, PATCH, DELETE con los mismos esquemas de respuesta y errores 404 que alumnos)*

---

### Evaluaciones

| Método | Endpoint | Descripción | Rol |
|---|---|---|---|
| GET | `/tipos-evaluacion` | Listar tipos | Cualquiera |
| POST | `/tipos-evaluacion` | Crear tipo | Docente |
| PUT | `/tipos-evaluacion/<id>` | Actualizar tipo | Docente |
| PATCH | `/tipos-evaluacion/<id>` | Actualizar parcial | Docente |
| DELETE | `/tipos-evaluacion/<id>` | Eliminar tipo | Docente |
| GET | `/evaluaciones` | Listar evaluaciones | Cualquiera |
| GET | `/evaluaciones?curso_id=<id>` | Filtrar por curso | Cualquiera |
| GET | `/evaluaciones/<id>` | Ver evaluación | Cualquiera |
| POST | `/evaluaciones` | Crear evaluación | Docente |
| PUT | `/evaluaciones/<id>` | Actualizar completa | Docente |
| PATCH | `/evaluaciones/<id>` | Actualizar parcial | Docente |
| DELETE | `/evaluaciones/<id>` | Eliminar (lógico) | Docente |

#### POST `/tipos-evaluacion`
**Request:**
```json
{
  "nombre": "Trabajo Práctico Grupal",
  "descripcion": "Evaluación con exposición oral"
}
```
**Éxito (201):** Objeto creado. **Errores:** 400 (Cuerpo vacío).

*(Soporta GET, PUT, PATCH, DELETE con errores 400 y 404 por ID no encontrado)*
---

### Equipos

| Método | Endpoint | Descripción | Rol |
|---|---|---|---|
| GET | `/equipos` | Listar equipos | Cualquiera |
| GET | `/equipos?curso_id=<id>` | Filtrar por curso | Cualquiera |
| GET | `/equipos/<id>` | Ver equipo con integrantes | Cualquiera |
| POST | `/equipos` | Crear equipo | Docente |
| PUT | `/equipos/<id>` | Actualizar equipo | Docente |
| PATCH | `/equipos/<id>` | Actualizar parcial | Docente |
| DELETE | `/equipos/<id>` | Eliminar (lógico) | Docente |
| POST | `/equipos/<id>/alumnos` | Agregar alumno | Docente |
| DELETE | `/equipos/<id>/alumnos/<padron>` | Quitar alumno | Docente |
| POST | `/equipos/<id>/evaluaciones` | Asociar evaluación | Docente |
| DELETE | `/equipos/<id>/evaluaciones/<eval_id>` | Desasociar evaluación | Docente |

#### POST `/equipos`
**Request:**
```json
{
  "curso_id": 1,
  "nombre": "Grupo Antigravity"
}
```
**Errores:** 404 (Curso no existe), 409 (Equipo ya existe en curso).

#### POST `/equipos/<equipo_id>/alumnos`
**Request:**
```json
{
  "padron": "103963"
}
```
**Errores:** 404 (Equipo/Alumno no existe), 409 (Alumno ya en otro equipo).

*(Soporta GET, DELETE, y endpoints similares para `/equipos/<id>/evaluaciones`)*

---

### Notas

| Método | Endpoint | Descripción | Rol |
|---|---|---|---|
| GET | `/notas?padron=<padron>` | Notas de un alumno | Docente |
| GET | `/notas?padron=<padron>&curso_id=<id>` | Notas filtradas por curso | Docente |
| GET | `/notas/mias` | Mis notas (alumno) | Alumno |
| POST | `/notas` | Cargar nota | Docente |
| PUT | `/notas/<nota_id>` | Actualizar nota completa | Docente |
| PATCH | `/notas/<nota_id>` | Actualizar parcial | Docente |
| DELETE | `/notas/<nota_id>` | Eliminar nota (lógico) | Docente |

#### POST `/notas`
**Request (Nota individual):**
```json
{
  "evaluacion_id": 3,
  "padron": "103963",
  "nota": 9.5,
  "observaciones": "Excelente"
}
```
**Errores:** 400 (Faltan campos), 404 (Alumno/Evaluacion no encontrada), 409 (Nota ya cargada).

*(Soporta GET, PUT, PATCH, DELETE para modificar notas existentes)*

---

### Asistencias

| Método | Endpoint | Descripción                    | Rol     |
|---|---|--------------------------------|---------|
| GET | `//asistencias_curso` | Asistencias de un curso        | Docente |
| POST | `/asistencia/validar-qr/<string:token>` | Validar QR escaneado           | Público |
| POST | `//enviar_mails_asistencia` | Enviar QR por email a un curso | Docente |

### Enviar Mails con Códigos QR
*   **Ruta:** `/enviar_mails_asistencia`
*   **Método:** `POST`

**Ejemplo de Petición:**
```json
{
  "curso_id": 1
}
```

**Respuestas HTTP:**
*   `200 OK` (Correos enviados o en cola)
*   `400 Bad Request`: `{"error": "Falta el curso_id o el curso no tiene alumnos"}`

### Validar QR de Asistencia
*   **Ruta:** `/asistencia/validar-qr/<token_qr>`
*   **Método:** `POST`

**Respuestas HTTP:**
*   `201 Created`
    ```json
    {"mensaje": "Se ha registrado su asistencia con exito."}
    ```
*   `200 OK`
    ```json
    {"mensaje": "Tu asistencia ya fue registrada previamente."}
    ```
*   `404 Not Found`
    ```json
    {"error": "El qr escaneado es invalido"}
    ```
*   `410 Gone`
    ```json
    {"error": "El codigo escaneado ya expiró, pruebe con un codigo vigente"}
    ```
*   `500 Internal Server Error`
    ```json
    {"error": "Ha ocurrido un error al registrar su asistencia, intentelo otra vez."}
    ```

### Obtener lista de asistencias
* **Ruta:** `/asistencias_curso?fecha=YYYY-MM-DD`
* **Método:** `GET`
* **Respuestas:**
  * **200 OK**:
    ```json
    {
      "mensaje": "se a devuelto la lista de asistencia con exito",
      "lista_alumnos": [
        {"padron": 103963, "presente": true}
      ]
    }
    ```


---

### Log y Dashboard

| Método | Endpoint | Descripción | Rol |
|---|---|---|---|
| GET | `/historial_logs` | Ver log de actividad | Docente |
| GET | `/dashboard/stats` | Estadísticas generales | Docente |
| GET | `/dashboard/stats?curso_id=<id>` | Stats por curso | Docente |
| GET | `/dashboard/alumnos` | Listado con filtros | Docente |

### Obtener historial inmutable
* **Ruta:** `/historial_logs`
* **Método:** `GET`
* **Respuestas:**
  * **200 OK**:
    ```json
    {
      "historial": [
        {
          "log_id": 15,
          "email": "garcia.carlos@fiuba.edu.ar",
          "accion": "Creó un curso nuevo",
          "fecha_actividad": "2026-06-15 15:30:00",
          "ip": "127.0.0.1"
        }
      ]
    }
    ```
  * **500 Internal Server Error**: `{"error": "No se pudo acceder al historial de actividad."}`

## Base de datos

El sistema tiene **13 tablas** con borrado lógico via `deleted_at`:

```
usuarios → docentes / alumnos (1:1)
usuarios → log_actividad (1:N)
alumnos  → alumnos_cursos ↔ cursos (N:M)
cursos   → evaluaciones, equipos, materiales (1:N)
tipos_evaluacion → evaluaciones (1:N)
evaluaciones → notas (1:N)
alumnos  → notas, asistencias (1:N)
equipos  → equipos_alumnos ↔ alumnos (N:M)
equipos  → equipos_evaluaciones ↔ evaluaciones (N:M)
```
## Diagrama Entidad-Relación
```mermaid
erDiagram
    usuarios {
        int usuario_id PK
        string email
        string password_hash
        string nombre
        string apellido
        string rol
        string fecha_registro
        string deleted_at
    }
    cursos {
        int curso_id PK
        string nombre
        string cuatrimestre
        int anio
        string descripcion
        string fecha_creacion
        string deleted_at
    }
    tipos_evaluacion {
        int tipo_id PK
        string nombre
        string descripcion
        string fecha_creacion
        string deleted_at
    }
    docentes {
        int legajo PK
        int usuario_id FK
        string departamento
        string deleted_at
    }
    alumnos {
        int padron PK
        int usuario_id FK
        boolean abandono
        string deleted_at
    }
    alumnos_cursos {
        int padron PK
        int curso_id PK
        string fecha_inscripcion
    }
    log_actividad {
        int log_id PK
        int usuario_id FK
        string email
        string accion
        string fecha_actividad
        string ip
    }
    evaluaciones {
        int evaluacion_id PK
        int tipo_id FK
        int curso_id FK
        string nombre
        string fecha
        float peso
        string descripcion
        string deleted_at
    }
    equipos {
        int equipo_id PK
        int curso_id FK
        string nombre
        string fecha_creacion
        string deleted_at
    }
    materiales {
        int material_id PK
        int curso_id FK
        string titulo
        string descripcion
        string archivo_url
        string tipo
        boolean publico
        string fecha_subida
        int subido_por FK
        string deleted_at
    }
    notas {
        int nota_id PK
        int padron FK
        int evaluacion_id FK
        float nota
        string fecha_carga
        string observacion
        string deleted_at
    }
    asistencias {
        int asistencia_id PK
        int padron FK
        string fecha
        boolean presente
        string qr_token
        string qr_expiracion
        string email_enviado_at
    }
    equipos_alumnos {
        int equipo_alumnos_id PK
        int equipo_id FK
        int padron FK
        string fecha_alta
        string deleted_at
    }
    equipos_evaluaciones {
        int equipo_evaluacion_id PK
        int equipo_id FK
        int evaluacion_id FK
        string deleted_at
    }
    usuarios ||--o| docentes : "es"
    usuarios ||--o| alumnos : "es"
    usuarios ||--o{ log_actividad : "genera"
    usuarios ||--o{ materiales : "sube"
    tipos_evaluacion ||--o{ evaluaciones : "clasifica"
    cursos ||--o{ evaluaciones : "tiene"
    cursos ||--o{ equipos : "tiene"
    cursos ||--o{ materiales : "contiene"
    cursos ||--o{ alumnos_cursos : "ofrece"
    alumnos ||--o{ alumnos_cursos : "se_inscribe"
    evaluaciones ||--o{ notas : "tiene"
    alumnos ||--o{ notas : "recibe"
    alumnos ||--o{ asistencias : "registra"
    equipos ||--o{ equipos_alumnos : "incluye"
    alumnos ||--o{ equipos_alumnos : "integra"
    equipos ||--o{ equipos_evaluaciones : "asociado_a"
    evaluaciones ||--o{ equipos_evaluaciones : "vinculada_a"
```

Para ver el esquema completo ver `database/schema.sql`.

---

## Datos de prueba

El `seed.sql` incluye:
- 5 docentes y 20 alumnos (18 activos, 2 con abandono)
- 3 cursos (2 del 2026, 1 del 2025)
- 4 tipos de evaluación, 6 evaluaciones
- 6 equipos con alumnos asignados
- Notas y asistencias de ejemplo

**Contraseña de todos los usuarios del seed:** `password123`

---

## Convenciones del código

**Arquitectura de tres capas:**
```
Route → Service → Repository → DB
```

- `routes/` — recibe HTTP, valida body, llama al service, devuelve JSON
- `services/` — lógica de negocio, validaciones, retorna strings descriptivos en caso de error
- `repositories/` — solo SQL con `try/except/finally`, borrado lógico con `deleted_at`

**Manejo de errores en services:**
```python
'campos_incompletos' → 400
'email_en_uso'       → 409
'no_encontrado'      → 404
None                 → 500
True / objeto        → éxito
```

**Borrado lógico:**
Ninguna tabla se elimina físicamente. Se usa `UPDATE SET deleted_at = NOW()`.
Las tablas `log_actividad` y `asistencias` son inmutables y no tienen `deleted_at`.

---

## Equipo

| Integrante | Módulos |
|---|---|
| Ariana | Tipos evaluación, Evaluaciones, Notas |
| Joel | Auth (JWT), Asistencias, Log |
| Rafael | Alumnos, Dashboard |
| Shirley | Docentes, Cursos, Equipos |
---

## Estructura del proyecto

```
gestion_curso_fiuba/
├── Backend/
│   ├── app/
│   │   ├── db.py                               # Conexión a MySQL
│   │   ├── constants.py                        # Constantes globales (regex, etc)
│   │   ├── routes/
│   │   │   ├── auth.py                         # POST /login, /registro, /logout
│   │   │   ├── usuarios.py                     # GET /usuarios
│   │   │   ├── alumnos.py                      # CRUD alumnos + abandono + CSV
│   │   │   ├── docentes.py                     # CRUD docentes
│   │   │   ├── cursos.py                       # CRUD cursos
│   │   │   ├── tipos_evaluacion.py             # CRUD tipos de evaluación
│   │   │   ├── evaluaciones.py                 # CRUD evaluaciones
│   │   │   ├── equipos.py                      # CRUD equipos + alumnos + evaluaciones
│   │   │   ├── notas.py                        # CRUD notas
│   │   │   ├── asistencias.py                  # QR + asistencias
│   │   │   ├── materiales.py                   # CRUD materiales
│   │   │   └── log.py                          # Consulta de log de actividad
│   │   ├── services/
│   │   │   ├── auth_service.py                 # Login, registro, decorador JWT
│   │   │   ├── alumno_service.py
│   │   │   ├── docente_service.py
│   │   │   ├── curso_service.py
│   │   │   ├── tipo_evaluacion_service.py
│   │   │   ├── evaluacion_service.py
│   │   │   ├── equipo_service.py
│   │   │   ├── nota_service.py
│   │   │   ├── asistencia_service.py
│   │   │   ├── material_service.py
│   │   │   ├── log_service.py
│   │   │   ├── qr_service.py
│   │   │   ├── mail_service.py
│   │   │   └── pdf_service.py
│   │   └── repositories/
│   │       ├── usuario_repository.py
│   │       ├── alumno_repository.py
│   │       ├── docente_repository.py
│   │       ├── curso_repository.py
│   │       ├── tipo_evaluacion_repository.py
│   │       ├── evaluacion_repository.py
│   │       ├── equipo_repository.py
│   │       ├── nota_repository.py
│   │       ├── asistencia_repository.py
│   │       ├── material_repository.py
│   │       └── log_repository.py
│   ├── database/
│   │   ├── schema.sql                          # Creación de tablas
│   │   └── seed.sql                            # Datos de prueba
│   └── app.py                                  # Punto de entrada
├── README.md
├── requirements.txt
├── setup_virtualenv.sh
├── setup_virtualenv.bat
├── .env
└── .env.example
```

---

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/gjoel6055-wq/gestor-universitario-armjsss
cd gestor-universitario-armjsss
```

### 2. Configurar la Base de Datos con MySQL local

Si ya tenes MySQL corriendo en tu maquina (puerto 3306 por defecto):

Crear la base de datos y cargar el esquema y datos de prueba:

**Linux / macOS / WSL:**
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS gestor_universitario;"
mysql -u root -p gestor_universitario < Backend/database/schema.sql
mysql -u root -p gestor_universitario < Backend/database/seed.sql
```

**Windows PowerShell:**
```powershell
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS gestor_universitario;"
Get-Content Backend\database\schema.sql | mysql -u root -p gestor_universitario
Get-Content Backend\database\seed.sql | mysql -u root -p gestor_universitario
```

Verificar que las tablas se hayan creado:
```bash
mysql -u root -p -e "USE gestor_universitario; SHOW TABLES;"
```
*Si tu usuario, password, puerto o nombre de base no coinciden con los defaults, actualiza el `.env` antes de levantar la API.*

### 3. Configurar las variables de entorno

```bash
cp .env.example .env
```

Editá el archivo `.env` con tus credenciales:

```env
EMAIL_SENDER=gestoruniversitario123@gmail.com
EMAIL_PASSWORD=tu contraseña de negocio
API_BASE_URL = "http://127.0.0.1:8080"
FRONT_BASE_URL = "http://127.0.0.1:5030"
DB_HOST = "127.0.0.1"
DB_PORT="3306"
DB_USER="root"
DB_PASSWORD=""
DB_NAME="gestor_universitario"
SECRET_KEY=tu_clave_secreta_larga_y_segura
```

### 4. Entorno virtual, instalación y ejecución

El proyecto incluye scripts de setup que crean el entorno virtual, instalan las dependencias y levantan la API automáticamente.

**Windows:**
```cmd
setup_virtualenv.bat
```

**Linux / macOS:**
```bash
chmod +x setup_virtualenv.sh
./setup_virtualenv.sh
```

Una vez iniciada, la API estará disponible en `http://localhost:8080`.

---

## Autenticación

La API usa **JWT (JSON Web Tokens)**. El token se obtiene en el login y debe enviarse en el header de cada request:

```
Authorization: Bearer <token>
```

El token expira a las **8 horas**. Hay dos roles:

| Rol | Permisos |
|---|---|
| `docente` | Acceso completo a todos los endpoints |
| `alumno` | Solo puede ver sus propias notas y asistencias |

---

## Endpoints

## Autenticación y Autorización

| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| POST | `/login` | Iniciar sesión | No |
| POST | `/registro` | Registrar cuenta | No |
| POST | `/logout` | Cerrar sesión | Sí |

### Iniciar sesión
Autentica al usuario en el sistema y retorna un token JWT válido por 8 horas.

*   **Ruta:** `/login`
*   **Método:** `POST`
*   **Auth requerida:** No

**Ejemplo de Petición:**
```json
{
  "email": "garcia.carlos@fiuba.edu.ar",
  "password": "password123"
}
```

**Respuestas HTTP:**
*   `200 OK`
    ```json
    {
      "mensaje": "Login exitoso",
      "token": "eyJhbGciOiJIUzI1NiIsInR5...",
      "datos": {
        "nombre": "Carlos",
        "email": "garcia.carlos@fiuba.edu.ar",
        "rol": "docente"
      }
    }
    ```
*   `401 Unauthorized`
    ```json
    {"error": "La contraseña ingresada es incorrecta"}
    ```
*   `404 Not Found`
    ```json
    {"error": "El email ingresado no se encuentra registrado."}
    ```

### Registrar cuenta
Permite la creación de un nuevo usuario en la base de datos (con rol alumno por defecto).

*   **Ruta:** `/registro`
*   **Método:** `POST`
*   **Auth requerida:** No

**Ejemplo de Petición:**
```json
{
  "nombre": "Juan",
  "apellido": "Perez",
  "email": "juanperez@fiuba.edu.ar",
  "password": "password123",
  "padron": "105554"
}
```

**Respuestas HTTP:**
*   `201 Created`
    ```json
    {"mensaje": "Se creó el usuario con exito."}
    ```
*   `400 Bad Request`
    ```json
    {"error": "Todos los campos son obligatorios"}
    ```
*   `400 Bad Request` (Si el email es inválido)
    ```json
    {"error": "El formato del email no es válido"}
    ```
*   `409 Conflict`
    ```json
    {"error": "El email ingresado ya se encuentra en uso."}
    ```

### Cerrar Sesión
Invalida el token del lado del cliente.

*   **Ruta:** `/logout`
*   **Método:** `POST`
*   **Auth requerida:** Sí

**Respuestas HTTP:**
*   `200 OK`
    ```json
    {"mensaje": "Se cerró la sesión con exito."}
    ```

---


### Cursos

| Método | Endpoint | Descripción | Rol |
|---|---|---|---|
| GET | `/cursos` | Listar todos los cursos | Cualquiera |
| GET | `/cursos/<curso_id>` | Ver curso por ID | Cualquiera |
| POST | `/cursos` | Crear curso | Docente |
| PUT | `/cursos/<curso_id>` | Actualizar curso completo | Docente |
| PATCH | `/cursos/<curso_id>` | Actualizar campos parciales | Docente |
| DELETE | `/cursos/<curso_id>` | Eliminar curso (lógico) | Docente |

**POST /cursos**
```json
{
  "nombre": "Introducción al Desarrollo de Software",
  "cuatrimestre": "1C",
  "anio": 2026,
  "descripcion": "Curso introductorio con Python y Flask"
}
```
**Éxito (201):** Objeto del curso creado.
**Errores:** 400 `{"error": "El cuerpo de la solicitud no puede estar vacío"}`, 409 `{"error": "el curso ya existe"}`

#### PUT `/cursos/<int:curso_id>` y PATCH `/cursos/<int:curso_id>`
**Request PUT (Completo):**
```json
{
  "nombre": "Intro al Desarrollo (Actualizado)",
  "cuatrimestre": "2C",
  "anio": 2026,
  "descripcion": "Nuevo temario"
}
```
**Request PATCH (Parcial):**
```json
{
  "descripcion": "Solo actualizo descripcion"
}
```
**Errores:** 400 (Cuerpo vacío), 404 (No encontrado), 409 (Nombre duplicado).

#### DELETE `/cursos/<int:curso_id>`
**Éxito (200):** `{"mensaje": "Curso {id} eliminado correctamente"}`
**Errores:** 400 (Error validación), 404 `{"error": "curso no encontrado"}`, 409 `{"error": "el curso tiene dependencias asociadas"}`

---

### Alumnos

| Método | Endpoint | Descripción | Rol |
|---|---|---|---|
| GET | `/alumnos` | Listar alumnos | Docente |
| GET | `/alumnos?estado=activo` | Filtrar por estado | Docente |
| GET | `/alumnos?curso_id=<id>` | Filtrar por curso | Docente |
| GET | `/alumnos/<padron>` | Ver alumno por padrón | Docente |
| POST | `/alumnos` | Crear alumno | Docente |
| PUT | `/alumnos/<padron>` | Actualizar alumno completo | Docente |
| PATCH | `/alumnos/<padron>` | Actualizar campos parciales | Docente |
| PATCH | `/alumnos/<padron>/abandono` | Marcar como abandonó | Docente |
| DELETE | `/alumnos/<padron>` | Eliminar alumno (lógico) | Docente |
| POST | `/alumnos/importar-csv` | Importar masivamente | Docente |

#### GET `/alumnos` y GET `/alumnos/<int:padron>`
**Éxito (200):** Devuelve alumnos. **Errores:** 404 `{"error": "Alumno no encontrado."}`

#### POST `/alumnos`
**Request:**
```json
{
  "padron": "103963",
  "nombre": "Carolina",
  "apellido": "Di Matteo",
  "email": "cdimatteo@fiuba.edu.ar",
  "password": "password123"
}
```
**Éxito (201):** Alumno creado.
**Errores:** 400 `{"error": "Faltan campos obligatorios"}`, 409 `{"error": "El padrón ya está registrado."}` o `"El email ya está registrado."`

#### PUT `/alumnos/<int:padron>` y PATCH `/alumnos/<int:padron>`
**Request PUT/PATCH:**
```json
{
  "nombre": "Carolina Nueva",
  "email": "nuevoemail@fiuba.edu.ar",
  "abandono": 1
}
```
**Errores:** 400 `{"error": "Se requiere al menos un campo para actualizar."}`, 404 (No encontrado), 409 (Email en uso).

#### DELETE `/alumnos/<int:padron>`
**Éxito (200):** `{"message": "Alumno eliminado con éxito.", "status": true}`
**Errores:** 404 `{"error": "Alumno no encontrado."}`

---

### Docentes

| Método | Endpoint | Descripción | Rol |
|---|---|---|---|
| GET | `/docentes` | Listar docentes | Cualquiera |
| GET | `/docentes/<legajo>` | Ver docente por legajo | Cualquiera |
| POST | `/docentes` | Crear docente | Docente |
| PUT | `/docentes/<legajo>` | Actualizar completo | Docente |
| PATCH | `/docentes/<legajo>` | Actualizar parcial | Docente |
| DELETE | `/docentes/<legajo>` | Eliminar (lógico) | Docente |

#### POST `/docentes`
**Request:**
```json
{
  "legajo": "9001",
  "nombre": "Martín",
  "apellido": "Sosa",
  "email": "msosa@fiuba.edu.ar",
  "password": "password123"
}
```
**Éxito (201):** Docente creado.
**Errores:** 400 (Campos obligatorios), 409 (Legajo o email en uso).

*(Soporta GET, PUT, PATCH, DELETE con los mismos esquemas de respuesta y errores 404 que alumnos)*

---

### Evaluaciones

| Método | Endpoint | Descripción | Rol |
|---|---|---|---|
| GET | `/tipos-evaluacion` | Listar tipos | Cualquiera |
| POST | `/tipos-evaluacion` | Crear tipo | Docente |
| PUT | `/tipos-evaluacion/<id>` | Actualizar tipo | Docente |
| PATCH | `/tipos-evaluacion/<id>` | Actualizar parcial | Docente |
| DELETE | `/tipos-evaluacion/<id>` | Eliminar tipo | Docente |
| GET | `/evaluaciones` | Listar evaluaciones | Cualquiera |
| GET | `/evaluaciones?curso_id=<id>` | Filtrar por curso | Cualquiera |
| GET | `/evaluaciones/<id>` | Ver evaluación | Cualquiera |
| POST | `/evaluaciones` | Crear evaluación | Docente |
| PUT | `/evaluaciones/<id>` | Actualizar completa | Docente |
| PATCH | `/evaluaciones/<id>` | Actualizar parcial | Docente |
| DELETE | `/evaluaciones/<id>` | Eliminar (lógico) | Docente |

#### POST `/tipos-evaluacion`
**Request:**
```json
{
  "nombre": "Trabajo Práctico Grupal",
  "descripcion": "Evaluación con exposición oral"
}
```
**Éxito (201):** Objeto creado. **Errores:** 400 (Cuerpo vacío).

*(Soporta GET, PUT, PATCH, DELETE con errores 400 y 404 por ID no encontrado)*
---

### Equipos

| Método | Endpoint | Descripción | Rol |
|---|---|---|---|
| GET | `/equipos` | Listar equipos | Cualquiera |
| GET | `/equipos?curso_id=<id>` | Filtrar por curso | Cualquiera |
| GET | `/equipos/<id>` | Ver equipo con integrantes | Cualquiera |
| POST | `/equipos` | Crear equipo | Docente |
| PUT | `/equipos/<id>` | Actualizar equipo | Docente |
| PATCH | `/equipos/<id>` | Actualizar parcial | Docente |
| DELETE | `/equipos/<id>` | Eliminar (lógico) | Docente |
| POST | `/equipos/<id>/alumnos` | Agregar alumno | Docente |
| DELETE | `/equipos/<id>/alumnos/<padron>` | Quitar alumno | Docente |
| POST | `/equipos/<id>/evaluaciones` | Asociar evaluación | Docente |
| DELETE | `/equipos/<id>/evaluaciones/<eval_id>` | Desasociar evaluación | Docente |

#### POST `/equipos`
**Request:**
```json
{
  "curso_id": 1,
  "nombre": "Grupo Antigravity"
}
```
**Errores:** 404 (Curso no existe), 409 (Equipo ya existe en curso).

#### POST `/equipos/<equipo_id>/alumnos`
**Request:**
```json
{
  "padron": "103963"
}
```
**Errores:** 404 (Equipo/Alumno no existe), 409 (Alumno ya en otro equipo).

*(Soporta GET, DELETE, y endpoints similares para `/equipos/<id>/evaluaciones`)*

---

### Notas

| Método | Endpoint | Descripción | Rol |
|---|---|---|---|
| GET | `/notas?padron=<padron>` | Notas de un alumno | Docente |
| GET | `/notas?padron=<padron>&curso_id=<id>` | Notas filtradas por curso | Docente |
| GET | `/notas/mias` | Mis notas (alumno) | Alumno |
| POST | `/notas` | Cargar nota | Docente |
| PUT | `/notas/<nota_id>` | Actualizar nota completa | Docente |
| PATCH | `/notas/<nota_id>` | Actualizar parcial | Docente |
| DELETE | `/notas/<nota_id>` | Eliminar nota (lógico) | Docente |

#### POST `/notas`
**Request (Nota individual):**
```json
{
  "evaluacion_id": 3,
  "padron": "103963",
  "nota": 9.5,
  "observaciones": "Excelente"
}
```
**Errores:** 400 (Faltan campos), 404 (Alumno/Evaluacion no encontrada), 409 (Nota ya cargada).

*(Soporta GET, PUT, PATCH, DELETE para modificar notas existentes)*

---

### Asistencias

| Método | Endpoint | Descripción                    | Rol     |
|---|---|--------------------------------|---------|
| GET | `//asistencias_curso` | Asistencias de un curso        | Docente |
| POST | `/asistencia/validar-qr/<string:token>` | Validar QR escaneado           | Público |
| POST | `//enviar_mails_asistencia` | Enviar QR por email a un curso | Docente |

### Enviar Mails con Códigos QR
*   **Ruta:** `/enviar_mails_asistencia`
*   **Método:** `POST`

**Ejemplo de Petición:**
```json
{
  "curso_id": 1
}
```

**Respuestas HTTP:**
*   `200 OK` (Correos enviados o en cola)
*   `400 Bad Request`: `{"error": "Falta el curso_id o el curso no tiene alumnos"}`

### Validar QR de Asistencia
*   **Ruta:** `/asistencia/validar-qr/<token_qr>`
*   **Método:** `POST`

**Respuestas HTTP:**
*   `201 Created`
    ```json
    {"mensaje": "Se ha registrado su asistencia con exito."}
    ```
*   `200 OK`
    ```json
    {"mensaje": "Tu asistencia ya fue registrada previamente."}
    ```
*   `404 Not Found`
    ```json
    {"error": "El qr escaneado es invalido"}
    ```
*   `410 Gone`
    ```json
    {"error": "El codigo escaneado ya expiró, pruebe con un codigo vigente"}
    ```
*   `500 Internal Server Error`
    ```json
    {"error": "Ha ocurrido un error al registrar su asistencia, intentelo otra vez."}
    ```

### Obtener lista de asistencias
* **Ruta:** `/asistencias_curso?fecha=YYYY-MM-DD`
* **Método:** `GET`
* **Respuestas:**
  * **200 OK**:
    ```json
    {
      "mensaje": "se a devuelto la lista de asistencia con exito",
      "lista_alumnos": [
        {"padron": 103963, "presente": true}
      ]
    }
    ```


---

### Log y Dashboard

| Método | Endpoint | Descripción | Rol |
|---|---|---|---|
| GET | `/historial_logs` | Ver log de actividad | Docente |
| GET | `/dashboard/stats` | Estadísticas generales | Docente |
| GET | `/dashboard/stats?curso_id=<id>` | Stats por curso | Docente |
| GET | `/dashboard/alumnos` | Listado con filtros | Docente |

### Obtener historial inmutable
* **Ruta:** `/historial_logs`
* **Método:** `GET`
* **Respuestas:**
  * **200 OK**:
    ```json
    {
      "historial": [
        {
          "log_id": 15,
          "email": "garcia.carlos@fiuba.edu.ar",
          "accion": "Creó un curso nuevo",
          "fecha_actividad": "2026-06-15 15:30:00",
          "ip": "127.0.0.1"
        }
      ]
    }
    ```
  * **500 Internal Server Error**: `{"error": "No se pudo acceder al historial de actividad."}`

## Base de datos

El sistema tiene **13 tablas** con borrado lógico via `deleted_at`:

```
usuarios → docentes / alumnos (1:1)
usuarios → log_actividad (1:N)
alumnos  → alumnos_cursos ↔ cursos (N:M)
cursos   → evaluaciones, equipos, materiales (1:N)
tipos_evaluacion → evaluaciones (1:N)
evaluaciones → notas (1:N)
alumnos  → notas, asistencias (1:N)
equipos  → equipos_alumnos ↔ alumnos (N:M)
equipos  → equipos_evaluaciones ↔ evaluaciones (N:M)
```
## Diagrama Entidad-Relación
```mermaid
erDiagram
    usuarios {
        int usuario_id PK
        string email
        string password_hash
        string nombre
        string apellido
        string rol
        string fecha_registro
        string deleted_at
    }
    cursos {
        int curso_id PK
        string nombre
        string cuatrimestre
        int anio
        string descripcion
        string fecha_creacion
        string deleted_at
    }
    tipos_evaluacion {
        int tipo_id PK
        string nombre
        string descripcion
        string fecha_creacion
        string deleted_at
    }
    docentes {
        int legajo PK
        int usuario_id FK
        string departamento
        string deleted_at
    }
    alumnos {
        int padron PK
        int usuario_id FK
        boolean abandono
        string deleted_at
    }
    alumnos_cursos {
        int padron PK
        int curso_id PK
        string fecha_inscripcion
    }
    log_actividad {
        int log_id PK
        int usuario_id FK
        string email
        string accion
        string fecha_actividad
        string ip
    }
    evaluaciones {
        int evaluacion_id PK
        int tipo_id FK
        int curso_id FK
        string nombre
        string fecha
        float peso
        string descripcion
        string deleted_at
    }
    equipos {
        int equipo_id PK
        int curso_id FK
        string nombre
        string fecha_creacion
        string deleted_at
    }
    materiales {
        int material_id PK
        int curso_id FK
        string titulo
        string descripcion
        string archivo_url
        string tipo
        boolean publico
        string fecha_subida
        int subido_por FK
        string deleted_at
    }
    notas {
        int nota_id PK
        int padron FK
        int evaluacion_id FK
        float nota
        string fecha_carga
        string observacion
        string deleted_at
    }
    asistencias {
        int asistencia_id PK
        int padron FK
        string fecha
        boolean presente
        string qr_token
        string qr_expiracion
        string email_enviado_at
    }
    equipos_alumnos {
        int equipo_alumnos_id PK
        int equipo_id FK
        int padron FK
        string fecha_alta
        string deleted_at
    }
    equipos_evaluaciones {
        int equipo_evaluacion_id PK
        int equipo_id FK
        int evaluacion_id FK
        string deleted_at
    }
    usuarios ||--o| docentes : "es"
    usuarios ||--o| alumnos : "es"
    usuarios ||--o{ log_actividad : "genera"
    usuarios ||--o{ materiales : "sube"
    tipos_evaluacion ||--o{ evaluaciones : "clasifica"
    cursos ||--o{ evaluaciones : "tiene"
    cursos ||--o{ equipos : "tiene"
    cursos ||--o{ materiales : "contiene"
    cursos ||--o{ alumnos_cursos : "ofrece"
    alumnos ||--o{ alumnos_cursos : "se_inscribe"
    evaluaciones ||--o{ notas : "tiene"
    alumnos ||--o{ notas : "recibe"
    alumnos ||--o{ asistencias : "registra"
    equipos ||--o{ equipos_alumnos : "incluye"
    alumnos ||--o{ equipos_alumnos : "integra"
    equipos ||--o{ equipos_evaluaciones : "asociado_a"
    evaluaciones ||--o{ equipos_evaluaciones : "vinculada_a"
```

Para ver el esquema completo ver `database/schema.sql`.

---

## Datos de prueba

El `seed.sql` incluye:
- 5 docentes y 20 alumnos (18 activos, 2 con abandono)
- 3 cursos (2 del 2026, 1 del 2025)
- 4 tipos de evaluación, 6 evaluaciones
- 6 equipos con alumnos asignados
- Notas y asistencias de ejemplo

**Contraseña de todos los usuarios del seed:** `password123`

---

## Convenciones del código

**Arquitectura de tres capas:**
```
Route → Service → Repository → DB
```

- `routes/` — recibe HTTP, valida body, llama al service, devuelve JSON
- `services/` — lógica de negocio, validaciones, retorna strings descriptivos en caso de error
- `repositories/` — solo SQL con `try/except/finally`, borrado lógico con `deleted_at`

**Manejo de errores en services:**
```python
'campos_incompletos' → 400
'email_en_uso'       → 409
'no_encontrado'      → 404
None                 → 500
True / objeto        → éxito
```

**Borrado lógico:**
Ninguna tabla se elimina físicamente. Se usa `UPDATE SET deleted_at = NOW()`.
Las tablas `log_actividad` y `asistencias` son inmutables y no tienen `deleted_at`.

---

## Equipo

| Integrante | Módulos |
|---|---|
| Ariana | Tipos evaluación, Evaluaciones, Notas |
| Joel | Auth (JWT), Asistencias, Log |
| Rafael | Alumnos, Dashboard |
| Shirley | Docentes, Cursos, Equipos |