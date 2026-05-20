import mysql.connector
from app.db import get_db_connection

# EQUIPOS
def obtener_todos(curso_id=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if curso_id:
            cursor.execute(
                '''
                SELECT * FROM equipos
                WHERE curso_id = %s
                AND deleted_at IS NULL
                ORDER BY nombre
                ''',
                (curso_id,)
            )
        else:
            cursor.execute(
                '''
                SELECT * FROM equipos
                WHERE deleted_at IS NULL
                ORDER BY nombre
                '''
            )
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener equipos: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def obtener_por_id(equipo_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            '''
            SELECT e.*, c.nombre AS curso_nombre
            FROM equipos e
            JOIN cursos c ON c.curso_id = e.curso_id
            WHERE e.equipo_id = %s
            AND e.deleted_at IS NULL
            ''',
            (equipo_id,)
        )
        equipo = cursor.fetchone()
        if equipo:
            equipo['alumnos']      = obtener_alumnos_del_equipo(equipo_id)
            equipo['evaluaciones'] = obtener_evaluaciones_del_equipo(equipo_id)
        return equipo
    except Exception as e:
        print(f"Error al obtener equipo {equipo_id}: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def insertar(datos):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO equipos (curso_id, nombre) VALUES (%s, %s)',
            (datos['curso_id'], datos['nombre'])
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        return obtener_por_id(nuevo_id)
    except mysql.connector.errors.IntegrityError as e:
        conn.rollback()
        if e.errno == 1062:
            raise ValueError(
                f"Ya existe un equipo con el nombre '{datos['nombre']}' en ese curso"
            )
        if e.errno == 1452:
            raise ValueError(f"El curso {datos['curso_id']} no existe")
        raise ValueError(f"Error de integridad: {e}")
    except Exception as e:
        conn.rollback()
        print(f"Error al insertar equipo: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def actualizar(equipo_id, datos):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''
            UPDATE equipos
            SET nombre = %s
            WHERE equipo_id = %s
            AND deleted_at IS NULL
            ''',
            (datos['nombre'], equipo_id)
        )
        conn.commit()
        return obtener_por_id(equipo_id)
    except mysql.connector.errors.IntegrityError as e:
        conn.rollback()
        if e.errno == 1062:
            raise ValueError(
                f"Ya existe un equipo con el nombre '{datos['nombre']}' en ese curso"
            )
        raise ValueError(f"Error de integridad: {e}")
    except Exception as e:
        conn.rollback()
        print(f"Error al actualizar equipo {equipo_id}: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def eliminar(equipo_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Marca el equipo como eliminado
        cursor.execute(
            '''
            UPDATE equipos
            SET deleted_at = NOW()
            WHERE equipo_id = %s
            AND deleted_at IS NULL
            ''',
            (equipo_id,)
        )
        # Marca las relaciones pivot como eliminadas también
        cursor.execute(
            '''
            UPDATE equipos_alumnos
            SET deleted_at = NOW()
            WHERE equipo_id = %s
            AND deleted_at IS NULL
            ''',
            (equipo_id,)
        )
        cursor.execute(
            '''
            UPDATE equipos_evaluaciones
            SET deleted_at = NOW()
            WHERE equipo_id = %s
            AND deleted_at IS NULL
            ''',
            (equipo_id,)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error al eliminar equipo {equipo_id}: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


# PIVOT EQUIPOS_ALUMNOS
def obtener_alumnos_del_equipo(equipo_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            '''
            SELECT
                a.padron,
                u.nombre,
                u.apellido,
                u.email,
                ea.fecha_alta
            FROM equipos_alumnos ea
            JOIN alumnos  a ON a.padron     = ea.padron
            JOIN usuarios u ON u.usuario_id = a.usuario_id
            WHERE ea.equipo_id = %s
            AND ea.deleted_at IS NULL
            ORDER BY u.apellido, u.nombre
            ''',
            (equipo_id,)
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener alumnos del equipo {equipo_id}: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def alumno_en_equipo(equipo_id, padron):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            '''
            SELECT 1 FROM equipos_alumnos
            WHERE equipo_id = %s
            AND padron = %s
            AND deleted_at IS NULL
            ''',
            (equipo_id, padron)
        )
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Error al verificar alumno en equipo: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def insertar_alumno(equipo_id, padron):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO equipos_alumnos (equipo_id, padron) VALUES (%s, %s)',
            (equipo_id, padron)
        )
        conn.commit()
        return {'equipo_id': equipo_id, 'padron': padron}
    except mysql.connector.errors.IntegrityError as e:
        conn.rollback()
        if e.errno == 1062:
            raise ValueError(f"El alumno {padron} ya pertenece a este equipo")
        if e.errno == 1452:
            raise ValueError(f"El alumno con padrón {padron} no existe")
        raise ValueError(f"Error de integridad: {e}")
    except Exception as e:
        conn.rollback()
        print(f"Error al agregar alumno al equipo: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def eliminar_alumno(equipo_id, padron):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''
            UPDATE equipos_alumnos
            SET deleted_at = NOW()
            WHERE equipo_id = %s
            AND padron = %s
            AND deleted_at IS NULL
            ''',
            (equipo_id, padron)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error al eliminar alumno del equipo: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


# PIVOT EQUIPOS_EVALUACIONES
def obtener_evaluaciones_del_equipo(equipo_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            '''
            SELECT
                ev.evaluacion_id,
                ev.nombre,
                ev.fecha,
                ev.peso,
                te.nombre AS tipo
            FROM equipos_evaluaciones ee
            JOIN evaluaciones     ev ON ev.evaluacion_id = ee.evaluacion_id
            JOIN tipos_evaluacion te ON te.tipo_id       = ev.tipo_id
            WHERE ee.equipo_id = %s
            AND ee.deleted_at IS NULL
            AND ev.deleted_at IS NULL
            ORDER BY ev.fecha
            ''',
            (equipo_id,)
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener evaluaciones del equipo {equipo_id}: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def evaluacion_en_equipo(equipo_id, evaluacion_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            '''
            SELECT 1 FROM equipos_evaluaciones
            WHERE equipo_id = %s
            AND evaluacion_id = %s
            AND deleted_at IS NULL
            ''',
            (equipo_id, evaluacion_id)
        )
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Error al verificar evaluacion en equipo: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def insertar_evaluacion(equipo_id, evaluacion_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO equipos_evaluaciones (equipo_id, evaluacion_id) VALUES (%s, %s)',
            (equipo_id, evaluacion_id)
        )
        conn.commit()
        return {'equipo_id': equipo_id, 'evaluacion_id': evaluacion_id}
    except mysql.connector.errors.IntegrityError as e:
        conn.rollback()
        if e.errno == 1062:
            raise ValueError(
                f"La evaluación {evaluacion_id} ya está asociada a este equipo"
            )
        if e.errno == 1452:
            raise ValueError(f"La evaluación {evaluacion_id} no existe")
        raise ValueError(f"Error de integridad: {e}")
    except Exception as e:
        conn.rollback()
        print(f"Error al agregar evaluacion al equipo: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def eliminar_evaluacion(equipo_id, evaluacion_id):
    # Borrado lógico en la pivot
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''
            UPDATE equipos_evaluaciones
            SET deleted_at = NOW()
            WHERE equipo_id = %s
            AND evaluacion_id = %s
            AND deleted_at IS NULL
            ''',
            (equipo_id, evaluacion_id)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error al eliminar evaluacion del equipo: {e}")
        return False
    finally:
        cursor.close()
        conn.close()