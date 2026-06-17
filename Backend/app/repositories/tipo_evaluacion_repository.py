from datetime import datetime
from app.db import get_connection, RealDictCursor
import psycopg2
import logging
logger = logging.getLogger(__name__)

def obtener_todos_tipos():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            '''
            SELECT tipo_id, nombre, descripcion, fecha_creacion
            FROM tipos_evaluacion
            WHERE deleted_at IS NULL
            ORDER BY nombre
            '''
        )
        return cursor.fetchall() or []
    except psycopg2.Error as e:
        logger.error(f'Error al obtener tipos de evaluación: {e}')
        return []
    finally:
        cursor.close()
        conn.close()

def obtener_tipo_por_id(tipo_id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute(
            '''
            SELECT tipo_id, nombre, descripcion, fecha_creacion
            FROM tipos_evaluacion
            WHERE tipo_id = %s AND deleted_at IS NULL
            ''',
            (tipo_id,)
        )
        return cursor.fetchone()
    except psycopg2.Error as e:
        logger.error(f'Error al obtener tipo {tipo_id}: {e}')
        return None
    finally:
        cursor.close()
        conn.close()

def guardar_tipo_bd(datos):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''
            INSERT INTO tipos_evaluacion (nombre, descripcion)
            VALUES (%s, %s)
            RETURNING tipo_id
            ''',
            (datos.get('nombre'), datos.get('descripcion'))
        )
        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        return obtener_tipo_por_id(nuevo_id)
    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f'Error al guardar tipo: {e}')
        return None
    finally:
        cursor.close()
        conn.close()

def modificar_tipo_bd(tipo_id, datos):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''
            UPDATE tipos_evaluacion
            SET nombre = %s, descripcion = %s
            WHERE tipo_id = %s AND deleted_at IS NULL
            ''',
            (datos.get('nombre'), datos.get('descripcion'), tipo_id)
        )
        conn.commit()
        return obtener_tipo_por_id(tipo_id)
    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f'Error al modificar tipo {tipo_id}: {e}')
        return None
    finally:
        cursor.close()
        conn.close()

def borrar_tipo_bd(tipo_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE tipos_evaluacion SET deleted_at = %s WHERE tipo_id = %s AND deleted_at IS NULL',
            (datetime.now(), tipo_id)
        )
        conn.commit()
        return True
    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f'Error al borrar tipo {tipo_id}: {e}')
        return False
    finally:
        cursor.close()
        conn.close()