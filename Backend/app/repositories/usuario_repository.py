from app.db import get_connection


def buscar_usuario_por_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM usuarios WHERE email= %s"
    try:
        cursor.execute(query, (email,))
        usuario = cursor.fetchone()
        return usuario
    except Exception as e:
        print(f"error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def ingresar_nuevo_usuario(nombre, apellido, email, hash, rol, identificador):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query_usuario = 'INSERT INTO usuarios (email, password_hash, nombre, apellido, rol) VALUES (%s,%s,%s,%s,%s)'
    validation_query = "SELECT * FROM usuarios WHERE email = %s"

    try:
        cursor.execute(validation_query, (email,))
        email_en_uso = cursor.fetchone()

        if email_en_uso:
            return "email en uso"

        cursor.execute(query_usuario, (email, hash, nombre, apellido, rol))
        nuevo_usuario_id = cursor.lastrowid

        if rol == 'alumno':
            query_alumno = "INSERT INTO alumnos (padron, usuario_id) VALUES (%s, %s)"
            cursor.execute(query_alumno, (identificador, nuevo_usuario_id))

        elif rol == 'docente':
            query_docente = "INSERT INTO docentes (legajo, usuario_id) VALUES (%s, %s)"
            cursor.execute(query_docente, (identificador, nuevo_usuario_id))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f'Error al ingresar nuevo usuario: {e}')
        return None
    finally:
        cursor.close()
        conn.close()