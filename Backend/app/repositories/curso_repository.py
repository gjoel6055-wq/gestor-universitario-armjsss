from app.db import get_db_connection

def obtener_todos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            'SELECT * FROM cursos ORDER BY anio DESC, cuatrimestre DESC'
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener cursos: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def obtener_por_id(curso_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            'SELECT * FROM cursos WHERE curso_id = %s',
            (curso_id,)
        )
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al obtener curso {curso_id}: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def buscar_duplicado(nombre, cuatrimestre, anio, excluir_id=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if excluir_id:
            cursor.execute(
                '''
                SELECT * FROM cursos
                WHERE nombre = %s AND cuatrimestre = %s AND anio = %s
                AND curso_id != %s
                ''',
                (nombre, cuatrimestre, anio, excluir_id)
            )
        else:
            cursor.execute(
                '''
                SELECT * FROM cursos
                WHERE nombre = %s AND cuatrimestre = %s AND anio = %s
                ''',
                (nombre, cuatrimestre, anio)
            )
        return cursor.fetchone()
    except Exception as e:
        print(f"Error al buscar duplicado: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def insertar(datos):
    conn = get_db_connection()
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
    except Exception as e:
        conn.rollback()
        print(f"Error al insertar curso: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def actualizar(curso_id, datos):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            '''
            UPDATE cursos
            SET nombre = %s, cuatrimestre = %s, anio = %s, descripcion = %s
            WHERE curso_id = %s
            ''',
            (datos['nombre'], datos['cuatrimestre'], datos['anio'], datos.get('descripcion'), curso_id)
        )
        conn.commit()
        return obtener_por_id(curso_id)
    except Exception as e:
        conn.rollback()
        print(f"Error al actualizar curso {curso_id}: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def eliminar(curso_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'DELETE FROM cursos WHERE curso_id = %s',
            (curso_id,)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error al eliminar curso {curso_id}: {e}")
        return False
    finally:
        cursor.close()
        conn.close()