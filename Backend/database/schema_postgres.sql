-- Nota: La base de datos debe crearse manualmente en PostgreSQL/Supabase

-- Nota: Conectarse a la base de datos desde psql o Supabase

-- =========================================================================
-- 1. TABLAS INDEPENDIENTES (Nivel 1)
-- =========================================================================

CREATE TABLE usuarios (
    usuario_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    rol VARCHAR(20) CHECK (rol IN ('alumno', 'docente')) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS cursos (
    curso_id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    cuatrimestre VARCHAR(10) CHECK (cuatrimestre IN ('1C', '2C')) NOT NULL,
    anio INT NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS tipos_evaluacion (
    tipo_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

-- =========================================================================
-- 2. ENTIDADES ESPECÍFICAS Y LOGS (Dependen de Usuarios o Cursos)
-- =========================================================================

CREATE TABLE IF NOT EXISTS docentes (
    legajo INT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    departamento VARCHAR(100),
    deleted_at TIMESTAMP DEFAULT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS alumnos (
    padron INT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    abandono BOOLEAN DEFAULT 0,
    deleted_at TIMESTAMP DEFAULT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS alumnos_cursos (
    padron INT NOT NULL,
    curso_id INT NOT NULL,
    fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (padron, curso_id),
    FOREIGN KEY (padron) REFERENCES alumnos(padron) ON DELETE CASCADE,
    FOREIGN KEY (curso_id) REFERENCES cursos(curso_id) ON DELETE CASCADE
);

-- log_actividad no lleva deleted_at: es un registro de auditoría inmutable
CREATE TABLE IF NOT EXISTS log_actividad (
    log_id SERIAL PRIMARY KEY,
    usuario_id INT,
    email VARCHAR(255),
    accion VARCHAR(255) NOT NULL,
    fecha_actividad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip VARCHAR(45),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE SET NULL
);

-- =========================================================================
-- 3. PLANIFICACIÓN ACADÉMICA Y GRUPOS
-- =========================================================================

CREATE TABLE IF NOT EXISTS evaluaciones (
    evaluacion_id SERIAL PRIMARY KEY,
    tipo_id INT NOT NULL,
    curso_id INT NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    fecha DATE NOT NULL,
    peso DECIMAL(5,2) NOT NULL,
    descripcion TEXT,
    deleted_at TIMESTAMP DEFAULT NULL,
    FOREIGN KEY (tipo_id) REFERENCES tipos_evaluacion(tipo_id),
    FOREIGN KEY (curso_id) REFERENCES cursos(curso_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS equipos (
    equipo_id SERIAL PRIMARY KEY,
    curso_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL,
    FOREIGN KEY (curso_id) REFERENCES cursos(curso_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS materiales (
    material_id SERIAL PRIMARY KEY,
    curso_id INT NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT,
    archivo_url VARCHAR(255) NOT NULL,
    tipo VARCHAR(50),
    publico BOOLEAN DEFAULT 1,
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subido_por INT,
    deleted_at TIMESTAMP DEFAULT NULL,
    FOREIGN KEY (curso_id) REFERENCES cursos(curso_id) ON DELETE CASCADE,
    FOREIGN KEY (subido_por) REFERENCES usuarios(usuario_id) ON DELETE SET NULL
);

-- =========================================================================
-- 4. SEGUIMIENTO ALUMNOS (Notas, Asistencias e Intermedias de Equipos)
-- =========================================================================

CREATE TABLE IF NOT EXISTS notas (
    nota_id SERIAL PRIMARY KEY,
    padron INT NOT NULL,
    evaluacion_id INT NOT NULL,
    nota DECIMAL(4,2) NOT NULL,
    fecha_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observacion TEXT,
    deleted_at TIMESTAMP DEFAULT NULL,
    FOREIGN KEY (padron) REFERENCES alumnos(padron) ON DELETE CASCADE,
    FOREIGN KEY (evaluacion_id) REFERENCES evaluaciones(evaluacion_id) ON DELETE CASCADE
);

-- asistencias no lleva deleted_at: son registros históricos inmutables
CREATE TABLE IF NOT EXISTS asistencias (
    asistencia_id SERIAL PRIMARY KEY,
    padron INT NOT NULL,
    fecha DATE NOT NULL,
    presente BOOLEAN NOT NULL DEFAULT 0,
    qr_token VARCHAR(255),
    qr_expiracion TIMESTAMP,
    email_enviado_at TIMESTAMP,
    FOREIGN KEY (padron) REFERENCES alumnos(padron) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS equipos_alumnos (
    equipo_alumnos_id SERIAL PRIMARY KEY,
    equipo_id INT NOT NULL,
    padron INT NOT NULL,
    fecha_alta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL,
    FOREIGN KEY (equipo_id) REFERENCES equipos(equipo_id) ON DELETE CASCADE,
    FOREIGN KEY (padron) REFERENCES alumnos(padron) ON DELETE CASCADE,
    UNIQUE(equipo_id, padron)
);

CREATE TABLE IF NOT EXISTS equipos_evaluaciones (
    equipo_evaluacion_id SERIAL PRIMARY KEY,
    equipo_id INT NOT NULL,
    evaluacion_id INT NOT NULL,
    deleted_at TIMESTAMP DEFAULT NULL,
    FOREIGN KEY (equipo_id) REFERENCES equipos(equipo_id) ON DELETE CASCADE,
    FOREIGN KEY (evaluacion_id) REFERENCES evaluaciones(evaluacion_id) ON DELETE CASCADE,
    UNIQUE(equipo_id, evaluacion_id)
);
