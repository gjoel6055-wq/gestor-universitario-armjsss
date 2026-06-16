import logging
import mysql.connector
from app.db import get_connection

logger = logging.getLogger(__name__)


def obtener_todos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            '''
            SELECT * FROM cursos
            WHERE deleted_at IS NULL
            ORDER BY anio DESC, cuatrimestre DESC
            '''
        )
        return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error al obtener cursos: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def obtener_por_id(curso_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            '''
            SELECT * FROM cursos
            WHERE curso_id = %s
            AND deleted_at IS NULL
            ''',
            (curso_id,)
        )
        return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error al obtener curso {curso_id}: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def insertar(datos):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''
            INSERT INTO cursos (nombre, cuatrimestre, anio, descripcion)
            VALUES (%s, %s, %s, %s)
            ''',
            (datos['nombre'], datos['cuatrimestre'], datos['anio'], datos.get('descripcion'))
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        return obtener_por_id(nuevo_id)
    except mysql.connector.errors.IntegrityError as e:
        conn.rollback()
        if e.errno == 1062:
            raise ValueError(
                f"Ya existe un curso '{datos['nombre']}' para el {datos['cuatrimestre']} de {datos['anio']}"
            )
        raise ValueError(f"Error de integridad: {e}")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error al insertar curso: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def actualizar(curso_id, datos):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''
            UPDATE cursos
            SET nombre = %s, cuatrimestre = %s, anio = %s, descripcion = %s
            WHERE curso_id = %s
            AND deleted_at IS NULL
            ''',
            (datos['nombre'], datos['cuatrimestre'], datos['anio'], datos.get('descripcion'), curso_id)
        )
        conn.commit()
        return obtener_por_id(curso_id)
    except mysql.connector.errors.IntegrityError as e:
        conn.rollback()
        if e.errno == 1062:
            raise ValueError(
                f"Ya existe un curso '{datos['nombre']}' para el {datos['cuatrimestre']} de {datos['anio']}"
            )
        raise ValueError(f"Error de integridad: {e}")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error al actualizar curso {curso_id}: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def eliminar(curso_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''
            UPDATE cursos
            SET deleted_at = NOW()
            WHERE curso_id = %s
            AND deleted_at IS NULL
            ''',
            (curso_id,)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"Error al eliminar curso {curso_id}: {e}")
        raise
    finally:
        cursor.close()
        conn.close()