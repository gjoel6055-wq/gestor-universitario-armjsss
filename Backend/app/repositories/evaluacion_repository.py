from datetime import datetime
from app.db import get_connection
import logging

logger = logging.getLogger(__name__)


def obtener_todas_evaluaciones(curso_id=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if curso_id:
            cursor.execute(
                '''
                SELECT e.evaluacion_id, e.nombre, e.fecha, e.peso, e.descripcion,
                       e.curso_id, e.tipo_id,
                       t.nombre AS tipo_nombre,
                       c.nombre AS curso_nombre
                FROM evaluaciones e
                JOIN tipos_evaluacion t ON t.tipo_id = e.tipo_id
                JOIN cursos c ON c.curso_id = e.curso_id
                WHERE e.deleted_at IS NULL
                AND e.curso_id = %s
                ORDER BY e.fecha
                ''',
                (curso_id,)
            )
        else:
            cursor.execute(
                '''
                SELECT e.evaluacion_id, e.nombre, e.fecha, e.peso, e.descripcion,
                       e.curso_id, e.tipo_id,
                       t.nombre AS tipo_nombre,
                       c.nombre AS curso_nombre
                FROM evaluaciones e
                JOIN tipos_evaluacion t ON t.tipo_id = e.tipo_id
                JOIN cursos c ON c.curso_id = e.curso_id
                WHERE e.deleted_at IS NULL
                ORDER BY e.fecha
                '''
            )
        return cursor.fetchall() or []
    except Exception as e:
        logger.error(f'Error al obtener evaluaciones: {e}')
        return []
    finally:
        cursor.close()
        conn.close()


def obtener_evaluacion_por_id(evaluacion_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            '''
            SELECT e.evaluacion_id, e.nombre, e.fecha, e.peso, e.descripcion,
                   e.curso_id, e.tipo_id,
                   t.nombre AS tipo_nombre,
                   c.nombre AS curso_nombre
            FROM evaluaciones e
            JOIN tipos_evaluacion t ON t.tipo_id = e.tipo_id
            JOIN cursos c ON c.curso_id = e.curso_id
            WHERE e.evaluacion_id = %s AND e.deleted_at IS NULL
            ''',
            (evaluacion_id,)
        )
        return cursor.fetchone()
    except Exception as e:
        logger.error(f'Error al obtener evaluacion {evaluacion_id}: {e}')
        return None
    finally:
        cursor.close()
        conn.close()


def guardar_evaluacion_bd(datos):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''
            INSERT INTO evaluaciones (tipo_id, curso_id, nombre, fecha, peso, descripcion)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''',
            (
                datos.get('tipo_id'),
                datos.get('curso_id'),
                datos.get('nombre'),
                datos.get('fecha'),
                datos.get('peso'),
                datos.get('descripcion')
            )
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        return obtener_evaluacion_por_id(nuevo_id)
    except Exception as e:
        conn.rollback()
        logger.error(f'Error al guardar evaluacion: {e}')
        return None
    finally:
        cursor.close()
        conn.close()


def modificar_evaluacion_bd(evaluacion_id, datos):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''
            UPDATE evaluaciones
            SET tipo_id = %s, curso_id = %s, nombre = %s,
                fecha = %s, peso = %s, descripcion = %s
            WHERE evaluacion_id = %s AND deleted_at IS NULL
            ''',
            (
                datos.get('tipo_id'),
                datos.get('curso_id'),
                datos.get('nombre'),
                datos.get('fecha'),
                datos.get('peso'),
                datos.get('descripcion'),
                evaluacion_id
            )
        )
        conn.commit()
        return obtener_evaluacion_por_id(evaluacion_id)
    except Exception as e:
        conn.rollback()
        logger.error(f'Error al modificar evaluacion {evaluacion_id}: {e}')
        return None
    finally:
        cursor.close()
        conn.close()


def borrar_evaluacion_bd(evaluacion_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE evaluaciones SET deleted_at = %s WHERE evaluacion_id = %s AND deleted_at IS NULL',
            (datetime.now(), evaluacion_id)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f'Error al borrar evaluacion {evaluacion_id}: {e}')
        return False
    finally:
        cursor.close()
        conn.close()
