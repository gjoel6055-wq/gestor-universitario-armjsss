from app.db import get_connection

def registrar_log(usuario_id, ip, accion):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO log_actividad (usuario_id, accion, ip) VALUES (%s,%s,%s)"

    try:
        cursor.execute(query, (usuario_id, ip, accion))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error al registrar actividad en DB: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def listar_logs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM log_actividad"

    try:
        cursor.execute(query)
        logs = cursor.fetchall()

        return logs

    except Exception as e:
        print(f"Error al listar logs: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def buscar_log_especifico(id_log):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM log_actividad WHERE log_id = %s"

    try:
        cursor.execute(query, (id_log, ))
        log_buscado = cursor.fetchone()

        if log_buscado:
            return log_buscado

        return 'no existe log con ese id'

    except Exception as e:
        print(f"Error al listar logs: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

