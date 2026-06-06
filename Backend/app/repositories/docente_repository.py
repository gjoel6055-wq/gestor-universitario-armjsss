from app.db import get_connection


def obtener_todos_los_docentes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT d.legajo,
                   d.departamento,
                   u.usuario_id,
                   u.nombre,
                   u.apellido,
                   u.email,
                   u.fecha_registro
            FROM docentes d
            JOIN usuarios u ON d.usuario_id = u.usuario_id
            WHERE d.deleted_at IS NULL
            AND u.deleted_at IS NULL
            ORDER BY d.legajo
        '''
        cursor.execute(query)
        return cursor.fetchall() or []
    except Exception as e:
        print(f'Error al obtener docentes: {e}')
        return []
    finally:
        cursor.close()
        conn.close()


def buscar_docente_por_legajo(legajo):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT d.legajo,
                   d.departamento,
                   u.usuario_id,
                   u.nombre,
                   u.apellido,
                   u.email,
                   u.fecha_registro
            FROM docentes d
            JOIN usuarios u ON d.usuario_id = u.usuario_id
            WHERE d.legajo = %s
            AND d.deleted_at IS NULL
            AND u.deleted_at IS NULL
        '''
        cursor.execute(query, (legajo,))
        return cursor.fetchone()
    except Exception as e:
        print(f'Error al buscar docente por legajo: {e}')
        return None
    finally:
        cursor.close()
        conn.close()


def crear_docente_en_bd(legajo, nombre, apellido, email, password_hash, departamento=''):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'SELECT legajo FROM docentes WHERE legajo = %s AND deleted_at IS NULL',
            (legajo,)
        )
        if cursor.fetchone():
            return 'legajo en uso'

        cursor.execute(
            'SELECT usuario_id FROM usuarios WHERE email = %s AND deleted_at IS NULL',
            (email,)
        )
        if cursor.fetchone():
            return 'email en uso'

        # Crear usuario
        cursor.execute(
            'INSERT INTO usuarios (email, password_hash, nombre, apellido, rol) VALUES (%s, %s, %s, %s, %s)',
            (email, password_hash, nombre, apellido, 'docente')
        )
        nuevo_usuario_id = cursor.lastrowid

        # Crear docente asociado
        cursor.execute(
            'INSERT INTO docentes (legajo, usuario_id, departamento) VALUES (%s, %s, %s)',
            (legajo, nuevo_usuario_id, departamento)
        )
        conn.commit()
        return legajo
    except Exception as e:
        conn.rollback()
        print(f'Error al crear docente: {e}')
        return None
    finally:
        cursor.close()
        conn.close()


def actualizar_docente_en_bd(legajo, nombre=None, apellido=None, departamento=None):
    docente = buscar_docente_por_legajo(legajo)
    if docente is None:
        return 'docente no encontrado'

    conn = get_connection()
    cursor = conn.cursor()
    try:
        campos_usuario = []
        params_usuario = []

        if nombre is not None:
            campos_usuario.append('nombre = %s')
            params_usuario.append(nombre)
        if apellido is not None:
            campos_usuario.append('apellido = %s')
            params_usuario.append(apellido)

        if campos_usuario:
            query_usuario = f"UPDATE usuarios SET {', '.join(campos_usuario)} WHERE usuario_id = %s AND deleted_at IS NULL"
            params_usuario.append(docente['usuario_id'])
            cursor.execute(query_usuario, tuple(params_usuario))

        if departamento is not None:
            cursor.execute(
                'UPDATE docentes SET departamento = %s WHERE legajo = %s AND deleted_at IS NULL',
                (departamento, legajo)
            )

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f'Error al actualizar docente {legajo}: {e}')
        return None
    finally:
        cursor.close()
        conn.close()


def eliminar_docente_en_bd(legajo):
    docente = buscar_docente_por_legajo(legajo)
    if docente is None:
        return 'docente no encontrado'

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE docentes SET deleted_at = NOW() WHERE legajo = %s AND deleted_at IS NULL',
            (legajo,)
        )
        cursor.execute(
            'UPDATE usuarios SET deleted_at = NOW() WHERE usuario_id = %s AND deleted_at IS NULL',
            (docente['usuario_id'],)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f'Error al eliminar docente: {e}')
        return None
    finally:
        cursor.close()
        conn.close()