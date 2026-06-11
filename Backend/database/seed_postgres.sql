-- Nota: Conectarse a la base de datos desde psql o Supabase

-- Nota: PostgreSQL usa TRUNCATE ... CASCADE
TRUNCATE TABLE equipos_evaluaciones CASCADE;
TRUNCATE TABLE equipos_alumnos CASCADE;
TRUNCATE TABLE asistencias CASCADE;
TRUNCATE TABLE notas CASCADE;
TRUNCATE TABLE evaluaciones CASCADE;
TRUNCATE TABLE tipos_evaluacion CASCADE;
TRUNCATE TABLE equipos CASCADE;
TRUNCATE TABLE materiales CASCADE;
TRUNCATE TABLE log_actividad CASCADE;
TRUNCATE TABLE docentes CASCADE;
TRUNCATE TABLE alumnos_cursos CASCADE;
TRUNCATE TABLE alumnos CASCADE;
TRUNCATE TABLE cursos CASCADE;
TRUNCATE TABLE usuarios CASCADE;
-- Nota: PostgreSQL usa TRUNCATE ... CASCADE


-- ══════════════════════════════════════════════════════════════════
-- USUARIOS
-- Contraseña de todos: password123
-- ══════════════════════════════════════════════════════════════════
INSERT INTO usuarios (email, password_hash, nombre, apellido, rol) VALUES
-- Docentes
('garcia.carlos@fiuba.edu.ar',   'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Carlos',    'García',    'docente'),
('martinez.ana@fiuba.edu.ar',    'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Ana',       'Martínez',  'docente'),
('rodriguez.juan@fiuba.edu.ar',  'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Juan',      'Rodríguez', 'docente'),
('lopez.maria@fiuba.edu.ar',     'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'María',     'López',     'docente'),
('fernandez.pedro@fiuba.edu.ar', 'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Pedro',     'Fernández', 'docente'),
-- Alumnos
('perez.lucas@fi.uba.ar',        'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Lucas',     'Pérez',     'alumno'),
('gomez.sofia@fi.uba.ar',        'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Sofía',     'Gómez',     'alumno'),
('diaz.martin@fi.uba.ar',        'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Martín',    'Díaz',      'alumno'),
('sanchez.val@fi.uba.ar',        'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Valentina', 'Sánchez',   'alumno'),
('torres.nico@fi.uba.ar',        'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Nicolás',   'Torres',    'alumno'),
('ramirez.cami@fi.uba.ar',       'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Camila',    'Ramírez',   'alumno'),
('flores.agus@fi.uba.ar',        'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Agustín',   'Flores',    'alumno'),
('rojas.juli@fi.uba.ar',         'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Julieta',   'Rojas',     'alumno'),
('herrera.santi@fi.uba.ar',      'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Santiago',  'Herrera',   'alumno'),
('morales.lucia@fi.uba.ar',      'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Lucía',     'Morales',   'alumno'),
('jimenez.facu@fi.uba.ar',       'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Facundo',   'Jiménez',   'alumno'),
('vargas.flor@fi.uba.ar',        'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Florencia', 'Vargas',    'alumno'),
('castro.tomas@fi.uba.ar',       'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Tomás',     'Castro',    'alumno'),
('ortiz.mica@fi.uba.ar',         'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Micaela',   'Ortiz',     'alumno'),
('ruiz.igna@fi.uba.ar',          'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Ignacio',   'Ruiz',      'alumno'),
('medina.abril@fi.uba.ar',       'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Abril',     'Medina',    'alumno'),
('aguilar.eze@fi.uba.ar',        'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Ezequiel',  'Aguilar',   'alumno'),
('reyes.anto@fi.uba.ar',         'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Antonella', 'Reyes',     'alumno'),
('navarro.mateo@fi.uba.ar',      'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Mateo',     'Navarro',   'alumno'),
('dominguez.pilar@fi.uba.ar',    'pbkdf2:sha256:1000000$ZJorxLRs7LjuWR3N$2a131d0b2bc6e38c7acd234ec6b0ed5d84b1b52ec7ef43217b3b01cd466002b9', 'Pilar',     'Domínguez', 'alumno');


-- ══════════════════════════════════════════════════════════════════
-- DOCENTES
-- usuario_id 1-5 corresponden a los docentes insertados arriba
-- ══════════════════════════════════════════════════════════════════
INSERT INTO docentes (legajo, usuario_id, departamento) VALUES
(10001, 1, 'Informática'),
(10002, 2, 'Informática'),
(10003, 3, 'Matemática'),
(10004, 4, 'Sistemas'),
(10005, 5, 'Informática');


-- ══════════════════════════════════════════════════════════════════
-- ALUMNOS
-- usuario_id 6-25 corresponden a los alumnos insertados arriba
-- padron es PK natural, no AUTO_INCREMENT → se indica explícitamente
-- ══════════════════════════════════════════════════════════════════
INSERT INTO alumnos (padron, usuario_id, abandono) VALUES
(100001, 6,  0),
(100002, 7,  0),
(100003, 8,  0),
(100004, 9,  0),
(100005, 10, 0),
(100006, 11, 0),
(100007, 12, 0),
(100008, 13, 0),
(100009, 14, 0),
(100010, 15, 0),
(100011, 16, 0),
(100012, 17, 0),
(100013, 18, 0),
(100014, 19, 0),
(100015, 20, 0),
(100016, 21, 0),
(100017, 22, 0),
(100018, 23, 0),
(100019, 24, 1),  -- abandonó
(100020, 25, 1);  -- abandonó


-- ══════════════════════════════════════════════════════════════════
-- CURSOS
-- ══════════════════════════════════════════════════════════════════
INSERT INTO cursos (nombre, cuatrimestre, anio, descripcion) VALUES
('Introducción al Desarrollo de Software', '1C', 2026, 'Curso introductorio con Python y Flask'),
('Algoritmos y Programación I',            '1C', 2026, 'Fundamentos de programación y algoritmos'),
('Introducción al Desarrollo de Software', '2C', 2025, 'Edición anterior — archivo histórico');


-- ══════════════════════════════════════════════════════════════════
-- TIPOS DE EVALUACIÓN
-- ══════════════════════════════════════════════════════════════════
INSERT INTO tipos_evaluacion (nombre, descripcion) VALUES
('Parcial',          'Evaluación parcial del cuatrimestre'),
('Parcialito',       'Evaluación corta de un tema específico'),
('Trabajo Práctico', 'Trabajo práctico grupal o individual'),
('Coloquio',         'Evaluación oral integradora');


-- ══════════════════════════════════════════════════════════════════
-- EVALUACIONES
-- curso_id 1 = IDS 2026, curso_id 2 = Algoritmos 2026
-- tipo_id  1 = Parcial, 2 = Parcialito, 3 = TP, 4 = Coloquio
-- ══════════════════════════════════════════════════════════════════
INSERT INTO evaluaciones (tipo_id, curso_id, nombre, fecha, peso, descripcion) VALUES
(1, 1, 'Parcial 1',        '2026-04-15', 2.00, 'Temas: Linux, Git, Agile'),
(1, 1, 'Parcial 2',        '2026-06-10', 2.00, 'Temas: Flask, SQL, Docker'),
(2, 1, 'Parcialito 1',     '2026-03-25', 1.00, 'Evaluación corta de Linux y Bash'),
(3, 1, 'TP Integrador',    '2026-06-17', 3.00, 'Proyecto final integrador'),
(1, 2, 'Parcial 1 - Algo', '2026-04-20', 2.00, 'Algoritmos básicos y estructuras'),
(3, 2, 'TP1 - Algoritmos', '2026-05-15', 2.00, 'Implementación de algoritmos de ordenamiento');


-- ══════════════════════════════════════════════════════════════════
-- EQUIPOS
-- curso_id 1 → 4 equipos, curso_id 2 → 2 equipos
-- ══════════════════════════════════════════════════════════════════
INSERT INTO equipos (curso_id, nombre) VALUES
(1, 'Equipo Alpha'),
(1, 'Equipo Beta'),
(1, 'Equipo Gamma'),
(1, 'Equipo Delta'),
(2, 'Equipo Uno'),
(2, 'Equipo Dos');


-- ══════════════════════════════════════════════════════════════════
-- EQUIPOS_ALUMNOS
-- equipo_id 1-4 → curso 1, equipo_id 5-6 → curso 2
-- alumnos con abandono=1 (padron 100019, 100020) no están en equipos
-- ══════════════════════════════════════════════════════════════════
INSERT INTO equipos_alumnos (equipo_id, padron) VALUES
(1, 100001), (1, 100002), (1, 100003), (1, 100004), (1, 100005),
(2, 100006), (2, 100007), (2, 100008), (2, 100009), (2, 100010),
(3, 100011), (3, 100012), (3, 100013), (3, 100014), (3, 100015),
(4, 100016), (4, 100017), (4, 100018),
(5, 100001), (5, 100002), (5, 100003), (5, 100004), (5, 100005),
(6, 100006), (6, 100007), (6, 100008), (6, 100009), (6, 100010);


-- ══════════════════════════════════════════════════════════════════
-- EQUIPOS_EVALUACIONES
-- evaluacion_id 4 = TP Integrador (curso 1)
-- evaluacion_id 6 = TP1 Algoritmos (curso 2)
-- ══════════════════════════════════════════════════════════════════
INSERT INTO equipos_evaluaciones (equipo_id, evaluacion_id) VALUES
(1, 4), (2, 4), (3, 4), (4, 4),
(5, 6), (6, 6);


-- ══════════════════════════════════════════════════════════════════
-- NOTAS
-- evaluacion_id 1 = Parcial 1, evaluacion_id 3 = Parcialito 1
-- Parcial 2 y TP sin notas para probar carga desde endpoints
-- ══════════════════════════════════════════════════════════════════
INSERT INTO notas (padron, evaluacion_id, nota, observacion) VALUES
-- Parcial 1
(100001, 1,  8.50, NULL),
(100002, 1,  7.00, NULL),
(100003, 1,  9.00, NULL),
(100004, 1,  6.50, NULL),
(100005, 1,  5.00, 'Recuperó'),
(100006, 1,  7.50, NULL),
(100007, 1,  8.00, NULL),
(100008, 1,  4.00, 'Desaprobó'),
(100009, 1,  9.50, NULL),
(100010, 1,  6.00, NULL),
(100011, 1,  7.00, NULL),
(100012, 1,  8.00, NULL),
(100013, 1,  5.50, NULL),
(100014, 1,  9.00, NULL),
(100015, 1,  6.50, NULL),
(100016, 1,  7.50, NULL),
(100017, 1,  8.50, NULL),
(100018, 1,  7.00, NULL),
-- Parcialito 1
(100001, 3, 10.00, NULL),
(100002, 3,  8.00, NULL),
(100003, 3,  9.00, NULL),
(100004, 3,  7.00, NULL),
(100005, 3,  6.00, NULL),
(100006, 3,  8.50, NULL),
(100007, 3,  9.00, NULL),
(100008, 3,  5.00, NULL),
(100009, 3, 10.00, NULL),
(100010, 3,  7.50, NULL);


-- ══════════════════════════════════════════════════════════════════
-- ASISTENCIAS
-- 3 clases con presencias mixtas para probar historial y stats
-- ══════════════════════════════════════════════════════════════════
INSERT INTO asistencias (padron, fecha, presente, qr_token, qr_expiracion, email_enviado_at) VALUES
-- Clase 1 — 07/05
(100001, '2026-05-07', 1, 'tok_a01_0507', '2026-05-07 23:59:59', '2026-05-07 08:00:00'),
(100002, '2026-05-07', 1, 'tok_a02_0507', '2026-05-07 23:59:59', '2026-05-07 08:00:00'),
(100003, '2026-05-07', 0, 'tok_a03_0507', '2026-05-07 23:59:59', '2026-05-07 08:00:00'),
(100004, '2026-05-07', 1, 'tok_a04_0507', '2026-05-07 23:59:59', '2026-05-07 08:00:00'),
(100005, '2026-05-07', 1, 'tok_a05_0507', '2026-05-07 23:59:59', '2026-05-07 08:00:00'),
(100006, '2026-05-07', 0, 'tok_a06_0507', '2026-05-07 23:59:59', '2026-05-07 08:00:00'),
(100007, '2026-05-07', 1, 'tok_a07_0507', '2026-05-07 23:59:59', '2026-05-07 08:00:00'),
(100008, '2026-05-07', 1, 'tok_a08_0507', '2026-05-07 23:59:59', '2026-05-07 08:00:00'),
(100009, '2026-05-07', 0, 'tok_a09_0507', '2026-05-07 23:59:59', '2026-05-07 08:00:00'),
(100010, '2026-05-07', 1, 'tok_a10_0507', '2026-05-07 23:59:59', '2026-05-07 08:00:00'),
-- Clase 2 — 10/05
(100001, '2026-05-10', 1, 'tok_a01_0510', '2026-05-10 23:59:59', '2026-05-10 08:00:00'),
(100002, '2026-05-10', 0, 'tok_a02_0510', '2026-05-10 23:59:59', '2026-05-10 08:00:00'),
(100003, '2026-05-10', 1, 'tok_a03_0510', '2026-05-10 23:59:59', '2026-05-10 08:00:00'),
(100004, '2026-05-10', 1, 'tok_a04_0510', '2026-05-10 23:59:59', '2026-05-10 08:00:00'),
(100005, '2026-05-10', 1, 'tok_a05_0510', '2026-05-10 23:59:59', '2026-05-10 08:00:00'),
(100006, '2026-05-10', 1, 'tok_a06_0510', '2026-05-10 23:59:59', '2026-05-10 08:00:00'),
(100007, '2026-05-10', 0, 'tok_a07_0510', '2026-05-10 23:59:59', '2026-05-10 08:00:00'),
(100008, '2026-05-10', 1, 'tok_a08_0510', '2026-05-10 23:59:59', '2026-05-10 08:00:00'),
(100009, '2026-05-10', 1, 'tok_a09_0510', '2026-05-10 23:59:59', '2026-05-10 08:00:00'),
(100010, '2026-05-10', 0, 'tok_a10_0510', '2026-05-10 23:59:59', '2026-05-10 08:00:00'),
-- Clase 3 — 14/05
(100001, '2026-05-14', 1, 'tok_a01_0514', '2026-05-14 23:59:59', '2026-05-14 08:00:00'),
(100002, '2026-05-14', 1, 'tok_a02_0514', '2026-05-14 23:59:59', '2026-05-14 08:00:00'),
(100003, '2026-05-14', 1, 'tok_a03_0514', '2026-05-14 23:59:59', '2026-05-14 08:00:00'),
(100004, '2026-05-14', 0, 'tok_a04_0514', '2026-05-14 23:59:59', '2026-05-14 08:00:00'),
(100005, '2026-05-14', 1, 'tok_a05_0514', '2026-05-14 23:59:59', '2026-05-14 08:00:00'),
(100006, '2026-05-14', 1, 'tok_a06_0514', '2026-05-14 23:59:59', '2026-05-14 08:00:00'),
(100007, '2026-05-14', 1, 'tok_a07_0514', '2026-05-14 23:59:59', '2026-05-14 08:00:00'),
(100008, '2026-05-14', 0, 'tok_a08_0514', '2026-05-14 23:59:59', '2026-05-14 08:00:00'),
(100009, '2026-05-14', 1, 'tok_a09_0514', '2026-05-14 23:59:59', '2026-05-14 08:00:00'),
(100010, '2026-05-14', 1, 'tok_a10_0514', '2026-05-14 23:59:59', '2026-05-14 08:00:00');


-- ══════════════════════════════════════════════════════════════════
-- MATERIALES
-- ══════════════════════════════════════════════════════════════════
INSERT INTO materiales (curso_id, titulo, descripcion, archivo_url, tipo, publico, subido_por) VALUES
(1, 'Introducción a Linux y Bash',  'Slides de la clase 1',            '/materiales/linux_bash.pdf',  'pdf',   1, 1),
(1, 'Git y Control de Versiones',   'Guía práctica de Git',            '/materiales/git_guia.pdf',    'pdf',   1, 1),
(1, 'Introducción a Flask',         'Tutorial con ejemplos prácticos', '/materiales/flask_intro.pdf', 'pdf',   0, 1),
(1, 'Video: REST APIs',             'Grabación de la clase de APIs',   '/materiales/apis_rest.mp4',   'video', 0, 2),
(2, 'Algoritmos de Ordenamiento',   'Material teórico de algoritmos',  '/materiales/sorting.pdf',     'pdf',   1, 3);


-- ══════════════════════════════════════════════════════════════════
-- LOG_ACTIVIDAD
-- ══════════════════════════════════════════════════════════════════
INSERT INTO log_actividad (usuario_id, email, accion, ip) VALUES
(1, 'garcia.carlos@fiuba.edu.ar', 'Inicio sesion',              '192.168.1.10'),
(1, 'garcia.carlos@fiuba.edu.ar', 'Creó un curso nuevo IDS 2026 1C',    '192.168.1.10'),
(1, 'garcia.carlos@fiuba.edu.ar', 'crear evaluacion Parcial 1', '192.168.1.10'),
(2, 'martinez.ana@fiuba.edu.ar',  'Inicio sesion',              '192.168.1.11'),
(6, 'perez.lucas@fi.uba.ar',      'Inicio sesion',              '192.168.1.20'),
(7, 'gomez.sofia@fi.uba.ar',      'Inicio sesion',              '192.168.1.21'),
(8, 'diaz.martin@fi.uba.ar',      'Inicio sesion',              '192.168.1.22');


-- ══════════════════════════════════════════════════════════════════
-- ALUMNOS_CURSOS
-- ══════════════════════════════════════════════════════════════════
INSERT INTO alumnos_cursos (padron, curso_id) VALUES
(100001, 1),
(100001, 2),
(100002, 1),
(100003, 1),
(100004, 2),
(100005, 1),
(100006, 1),
(100007, 1),
(100008, 1),
(100009, 1),
(100010, 1),
(100011, 1),
(100012, 1),
(100013, 1),
(100014, 1),
(100015, 1),
(100016, 1),
(100017, 1),
(100018, 1);
