from app.db import get_connection

def registrar_log(usuario_id, accion, ip, email=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO log_actividad (usuario_id, email, accion, ip) VALUES (%s,%s,%s,%s)"

    try:
        cursor.execute(query, (usuario_id, email, accion, ip, ))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error al registrar actividad en DB: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def listar_logs(accion=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if accion:
        query = "SELECT * FROM log_actividad WHERE accion LIKE %s"
        parametros = (f"%{accion}%", )
    else:
        query = "SELECT * FROM log_actividad ORDER BY fecha_actividad DESC "
        parametros = ()

    try:
        cursor.execute(query, parametros)
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

