from datetime import datetime
from app.db import get_connection


def obtener_todos_tipos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
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
    except Exception as e:
        print(f'Error al obtener tipos de evaluación: {e}')
        return []
    finally:
        cursor.close()
        conn.close()


def obtener_tipo_por_id(tipo_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
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
    except Exception as e:
        print(f'Error al obtener tipo {tipo_id}: {e}')
        return None
    finally:
        cursor.close()
        conn.close()


def guardar_tipo_bd(datos):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO tipos_evaluacion (nombre, descripcion) VALUES (%s, %s)',
            (datos.get('nombre'), datos.get('descripcion'))
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        return obtener_tipo_por_id(nuevo_id)
    except Exception as e:
        conn.rollback()
        print(f'Error al guardar tipo: {e}')
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
    except Exception as e:
        conn.rollback()
        print(f'Error al modificar tipo {tipo_id}: {e}')
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
    except Exception as e:
        conn.rollback()
        print(f'Error al borrar tipo {tipo_id}: {e}')
        return False
    finally:
        cursor.close()
        conn.close()
