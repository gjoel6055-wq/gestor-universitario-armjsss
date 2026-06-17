from app.db import get_connection, RealDictCursor
import psycopg2

def obtener_todos_los_alumnos():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = '''
            SELECT a.padron,
                   a.abandono,
                   u.usuario_id,
                   u.nombre,
                   u.apellido,
                   u.email,
                   u.fecha_registro
            FROM alumnos a
            JOIN usuarios u ON a.usuario_id = u.usuario_id
            ORDER BY a.padron
        '''
        cursor.execute(query)
        return cursor.fetchall() or []
    except psycopg2.Error as e:
        print(f'Error al obtener alumnos: {e}')
        return []
    finally:
        cursor.close()
        conn.close()

def buscar_alumno_por_padron(padron):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = '''
            SELECT a.padron,
                   a.abandono,
                   u.usuario_id,
                   u.nombre,
                   u.apellido,
                   u.email,
                   u.fecha_registro
            FROM alumnos a
            JOIN usuarios u ON a.usuario_id = u.usuario_id
            WHERE a.padron = %s
        '''
        cursor.execute(query, (padron,))
        return cursor.fetchone()
    except psycopg2.Error as e:
        print(f'Error al buscar alumno por padrón: {e}')
        return None
    finally:
        cursor.close()
        conn.close()

def crear_alumno_en_bd(padron, nombre, apellido, email, password_hash, abandono=False):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT padron FROM alumnos WHERE padron = %s', (padron,))
        if cursor.fetchone():
            return 'padron en uso'

        cursor.execute('SELECT usuario_id FROM usuarios WHERE email = %s', (email,))
        if cursor.fetchone():
            return 'email en uso'

        cursor.execute(
            '''
            INSERT INTO usuarios (email, password_hash, nombre, apellido, rol)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING usuario_id
            ''',
            (email, password_hash, nombre, apellido, 'alumno')
        )
        usuario_id = cursor.fetchone()[0]
        cursor.execute(
            'INSERT INTO alumnos (padron, usuario_id, abandono) VALUES (%s, %s, %s)',
            (padron, usuario_id, bool(abandono))
        )
        conn.commit()
        return True
    except psycopg2.Error as e:
        conn.rollback()
        print(f'Error al crear alumno: {e}')
        return None
    finally:
        cursor.close()
        conn.close()

def actualizar_alumno_en_bd(padron, nombre=None, apellido=None, email=None, password_hash=None, abandono=None, cursos=None):
    alumno = buscar_alumno_por_padron(padron)
    if alumno is None:
        return 'alumno no encontrado'

    conn = get_connection()
    cursor = conn.cursor()
    try:
        if email is not None and email != alumno['email']:
            cursor.execute('SELECT usuario_id FROM usuarios WHERE email = %s AND usuario_id <> %s', (email, alumno['usuario_id']))
            if cursor.fetchone():
                return 'email en uso'

        updates = []
        params = []

        if nombre is not None:
            updates.append('nombre = %s')
            params.append(nombre)
        if apellido is not None:
            updates.append('apellido = %s')
            params.append(apellido)
        if email is not None:
            updates.append('email = %s')
            params.append(email)
        if password_hash is not None:
            updates.append('password_hash = %s')
            params.append(password_hash)

        if updates:
            query = f"UPDATE usuarios SET {', '.join(updates)} WHERE usuario_id = %s"
            params.append(alumno['usuario_id'])
            cursor.execute(query, tuple(params))

        if abandono is not None:
            cursor.execute('UPDATE alumnos SET abandono = %s WHERE padron = %s', (bool(abandono), padron))

        if cursos is not None:
            cursor.execute('DELETE FROM alumnos_cursos WHERE padron = %s', (padron,))
            for curso_id in cursos:
                if curso_id:
                    cursor.execute('INSERT INTO alumnos_cursos (padron, curso_id) VALUES (%s, %s)', (padron, int(curso_id)))

        conn.commit()
        return True
    except psycopg2.Error as e:
        conn.rollback()
        print(f'Error al actualizar alumno: {e}')
        return None
    finally:
        cursor.close()
        conn.close()

def eliminar_alumno_en_bd(padron):
    alumno = buscar_alumno_por_padron(padron)
    if alumno is None:
        return 'alumno no encontrado'

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM usuarios WHERE usuario_id = %s', (alumno['usuario_id'],))
        conn.commit()
        return True
    except psycopg2.Error as e:
        conn.rollback()
        print(f'Error al eliminar alumno: {e}')
        return None
    finally:
        cursor.close()
        conn.close()

def obtener_cursos_del_alumno(padron):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = '''
            SELECT c.curso_id, c.nombre, c.cuatrimestre, c.anio, c.descripcion
            FROM alumnos_cursos ac
            JOIN cursos c ON ac.curso_id = c.curso_id
            WHERE ac.padron = %s AND c.deleted_at IS NULL
            ORDER BY c.anio DESC, c.cuatrimestre DESC
        '''
        cursor.execute(query, (padron,))
        return cursor.fetchall() or []
    except psycopg2.Error as e:
        print(f'Error al obtener cursos del alumno {padron}: {e}')
        return []
    finally:
        cursor.close()
        conn.close()