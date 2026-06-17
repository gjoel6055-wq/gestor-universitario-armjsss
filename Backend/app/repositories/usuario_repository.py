from app.db import get_connection, RealDictCursor
import logging
import psycopg2
logger = logging.getLogger(__name__)

def buscar_usuario_por_email(email):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = "SELECT * FROM usuarios WHERE email = %s"
    try:
        cursor.execute(query, (email,))
        usuario = cursor.fetchone()
        return usuario
    except psycopg2.Error as e:
        logger.error(f"error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def ingresar_nuevo_usuario(nombre, apellido, email, hash, rol, identificador):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query_usuario = '''
        INSERT INTO usuarios (email, password_hash, nombre, apellido, rol)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING usuario_id
    '''
    validation_query = "SELECT * FROM usuarios WHERE email = %s"
    try:
        cursor.execute(validation_query, (email,))
        email_en_uso = cursor.fetchone()
        if email_en_uso:
            return "email en uso"

        cursor.execute(query_usuario, (email, hash, nombre, apellido, rol))
        nuevo_usuario_id = cursor.fetchone()['usuario_id']

        if rol == 'alumno':
            query_alumno = "INSERT INTO alumnos (padron, usuario_id) VALUES (%s, %s)"
            cursor.execute(query_alumno, (identificador, nuevo_usuario_id))
        elif rol == 'docente':
            query_docente = "INSERT INTO docentes (legajo, usuario_id) VALUES (%s, %s)"
            cursor.execute(query_docente, (identificador, nuevo_usuario_id))

        conn.commit()
        return True
    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f'Error al ingresar nuevo usuario: {e}')
        return None
    finally:
        cursor.close()
        conn.close()