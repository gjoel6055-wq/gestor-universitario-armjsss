from app.db import get_connection
from datetime import datetime


def crear_nueva_asistencia(padron, fecha, qr_token, fecha_expiraicon):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO asistencias (padron, fecha, qr_token, qr_expiracion, email_enviado_at) VALUES (%s,%s,%s,%s,%s)"
    fecha_de_envio = datetime.now()

    try:
        cursor.execute(query, (padron, fecha, qr_token, fecha_expiraicon, fecha_de_envio, ))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print (f"error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def registrar_asistencia(qr_token):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query_validation = "SELECT qr_expiracion FROM asistencias WHERE qr_token = %s"
    query_registro_asistencia = "UPDATE asistencias SET presente = 1 WHERE qr_token = %s"

    try:
        cursor.execute(query_validation, (qr_token, ))
        resultado = cursor.fetchone()

        if not resultado:
            return "QR invalido"

        fecha_expiracion = resultado['qr_expiracion']
        fecha_actual = datetime.now()

        if fecha_actual > fecha_expiracion:
            return "token expirado"

        cursor.execute(query_registro_asistencia, (qr_token, ))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def obtener_alumnos_curso():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
                SELECT a.padron, u.nombre, u.email
                FROM usuarios u
                JOIN alumnos a ON u.usuario_id = a.usuario_id
                WHERE a.abandono = 0 
                  AND u.rol = 'alumno' 
                """

        cursor.execute(query, )
        alumnos = cursor.fetchall()
        print(f"DEBUG: Se encontraron {len(alumnos)} alumnos")
        return alumnos

    except Exception as e:
        print(f"error: {e}")
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

    except Exception as e:
        print(f"Error en BD al obtener asistencias por fecha: {e}")
        return None
    finally:
        cursor.close()
        conn.close()