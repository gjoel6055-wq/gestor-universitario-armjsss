from app.db import get_connection
from datetime import datetime

def crear_nueva_asistencia(padron, fecha, qr_token, fecha_expiraicon):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO asistencias (padron, fecha, qr_token, qr_expiracion) VALUES (%s,%s,%s,%s)"

    try:
        cursor.execute(query, (padron, fecha, qr_token, fecha_expiraicon, ))
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
