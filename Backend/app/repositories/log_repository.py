from app.db import get_connection, RealDictCursor
import logging
import psycopg2
logger = logging.getLogger(__name__)

def registrar_log(usuario_id, accion, ip, email=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO log_actividad (usuario_id, email, accion, ip) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(query, (usuario_id, email, accion, ip))
        conn.commit()
        return True
    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f"Error al registrar actividad en DB: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def listar_logs(accion=None):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    if accion:
        query = "SELECT * FROM log_actividad WHERE accion LIKE %s"
        parametros = (f"%{accion}%",)
    else:
        query = "SELECT * FROM log_actividad ORDER BY fecha_actividad DESC"
        parametros = ()
    try:
        cursor.execute(query, parametros)
        logs = cursor.fetchall()
        return logs
    except psycopg2.Error as e:
        logger.error(f"Error al listar logs: {e}")
        return False
    finally:
        cursor.close()
        conn.close()