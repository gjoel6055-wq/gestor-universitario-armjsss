from app.db import get_connection
from datetime import datetime
import logging
import mysql.connector

logger = logging.getLogger(__name__)


def crear_nueva_asistencia(padron, fecha, qr_token, fecha_expiraicon):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO asistencias (padron, fecha, qr_token, qr_expiracion, email_enviado_at) VALUES (%s,%s,%s,%s,%s)"
    fecha_de_envio = datetime.now()

    try:
        cursor.execute(query, (padron, fecha, qr_token, fecha_expiraicon, fecha_de_envio, ))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        conn.rollback()
        logger.error(f"error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def registrar_asistencia(qr_token):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True, buffered=True)
    query_validation = "SELECT qr_expiracion, presente FROM asistencias WHERE qr_token = %s"
    query_registro_asistencia = "UPDATE asistencias SET presente = 1 WHERE qr_token = %s"

    try:
        cursor.execute(query_validation, (qr_token, ))
        resultado = cursor.fetchone()

        if not resultado:
            return "QR invalido"

        if resultado['presente'] == 1:
            return "ya presente"

        fecha_expiracion = resultado['qr_expiracion']
        fecha_actual = datetime.now()

        if fecha_actual > fecha_expiracion:
            return "token expirado"

        cursor.execute(query_registro_asistencia, (qr_token, ))
        conn.commit()
        return True
    except mysql.connector.Error as e:
        conn.rollback()
        logger.error(f"error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def obtener_alumnos_curso(curso_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
                SELECT a.padron, u.nombre, u.email
                FROM usuarios u
                JOIN alumnos a ON u.usuario_id = a.usuario_id
                JOIN alumnos_cursos ac ON a.padron = ac.padron
                WHERE a.abandono = 0 
                  AND u.rol = 'alumno' 
                  AND ac.curso_id = %s
                """

        cursor.execute(query, (curso_id,))
        alumnos = cursor.fetchall()
        return alumnos

    except mysql.connector.Error as e:
        logger.error(f"error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def obtener_asistencias_por_fecha(fecha_consulta):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
                SELECT a.padron, u.nombre, u.apellido, u.email, asis.presente
                FROM usuarios u JOIN alumnos a ON u.usuario_id = a.usuario_id INNER JOIN asistencias asis 
                ON a.padron = asis.padron AND asis.fecha = %s WHERE a.abandono = 0 AND u.rol = 'alumno'
                ORDER BY u.apellido, u.nombre 
                """

        cursor.execute(query, (fecha_consulta,))
        alumnos = cursor.fetchall()

        return alumnos

    except mysql.connector.Error as e:
        logger.error(f"Error en BD al obtener asistencias por fecha: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def obtener_asistencia_por_token(token):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT a.asistencia_id, a.presente, a.qr_expiracion, u.nombre, u.apellido
            FROM asistencias a
            JOIN alumnos al ON a.padron = al.padron
            JOIN usuarios u ON al.usuario_id = u.usuario_id
            WHERE a.qr_token = %s
        """
        cursor.execute(query, (token,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        logger.error(f"Error al buscar token: {e}")
        return None
    finally:
        cursor.close()
        conn.close()