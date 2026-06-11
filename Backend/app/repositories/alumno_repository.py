import logging
from app.db import ejecutar_consulta, ejecutar_mutacion

logger = logging.getLogger(__name__)


SQL_BASE_ALUMNOS = """
    SELECT a.padron,
           a.abandono,
           u.usuario_id,
           u.nombre,
           u.apellido,
           u.email,
           u.fecha_registro
    FROM alumnos a
    JOIN usuarios u ON a.usuario_id = u.usuario_id
"""


def obtener_todos_los_alumnos():
    """
    Obtiene la lista de todos los alumnos registrados.
    """
    try:
        sql = SQL_BASE_ALUMNOS + ' ORDER BY a.padron'
        return ejecutar_consulta(sql)
    except Exception as e:
        logger.error(f'Error al obtener alumnos: {e}')
        return []


def buscar_alumno_por_padron(padron):
    """
    Obtiene los detalles de un alumno por su numero de padron.
    """
    try:
        sql = SQL_BASE_ALUMNOS + ' WHERE a.padron = :padron'
        filas = ejecutar_consulta(sql, {'padron': padron})
        return filas[0] if filas else None
    except Exception as e:
        logger.error(f'Error al buscar alumno por padron: {e}')
        return None


def crear_alumno_en_bd(padron, nombre, apellido, email, password_hash, abandono=False):
    """
    Crea un nuevo alumno en la base de datos.
    Retorna True si se creo correctamente, o un string con el error.
    """
    try:
        # Verificar si el padron ya existe
        existe = ejecutar_consulta(
            'SELECT padron FROM alumnos WHERE padron = :padron',
            {'padron': padron}
        )
        if existe:
            return 'padron en uso'

        # Verificar si el email ya existe
        existe_email = ejecutar_consulta(
            'SELECT usuario_id FROM usuarios WHERE email = :email',
            {'email': email}
        )
        if existe_email:
            return 'email en uso'

        # Insertar usuario y obtener el id
        sql_usuario = """
            INSERT INTO usuarios (email, password_hash, nombre, apellido, rol)
            VALUES (:email, :password_hash, :nombre, :apellido, 'alumno')
            RETURNING usuario_id
        """
        usuario_id = ejecutar_mutacion(sql_usuario, {
            'email': email,
            'password_hash': password_hash,
            'nombre': nombre,
            'apellido': apellido
        })

        # Insertar alumno
        sql_alumno = """
            INSERT INTO alumnos (padron, usuario_id, abandono)
            VALUES (:padron, :usuario_id, :abandono)
        """
        ejecutar_mutacion(sql_alumno, {
            'padron': padron,
            'usuario_id': usuario_id,
            'abandono': int(bool(abandono))
        })

        return True
    except Exception as e:
        logger.error(f'Error al crear alumno: {e}')
        return None


def actualizar_alumno_en_bd(padron, nombre=None, apellido=None, email=None, password_hash=None, abandono=None, cursos=None):
    """
    Actualiza los datos de un alumno existente.
    """
    alumno = buscar_alumno_por_padron(padron)
    if alumno is None:
        return 'alumno no encontrado'

    try:
        # Verificar si el email ya esta en uso por otro usuario
        if email is not None and email != alumno['email']:
            existe = ejecutar_consulta(
                'SELECT usuario_id FROM usuarios WHERE email = :email AND usuario_id <> :usuario_id',
                {'email': email, 'usuario_id': alumno['usuario_id']}
            )
            if existe:
                return 'email en uso'

        # Construir actualizacion dinamica de usuarios
        updates = []
        params = {'usuario_id': alumno['usuario_id']}

        if nombre is not None:
            updates.append('nombre = :nombre')
            params['nombre'] = nombre
        if apellido is not None:
            updates.append('apellido = :apellido')
            params['apellido'] = apellido
        if email is not None:
            updates.append('email = :email')
            params['email'] = email
        if password_hash is not None:
            updates.append('password_hash = :password_hash')
            params['password_hash'] = password_hash

        if updates:
            sql = f"UPDATE usuarios SET {', '.join(updates)} WHERE usuario_id = :usuario_id"
            ejecutar_mutacion(sql, params)

        # Actualizar estado de abandono
        if abandono is not None:
            ejecutar_mutacion(
                'UPDATE alumnos SET abandono = :abandono WHERE padron = :padron',
                {'abandono': int(bool(abandono)), 'padron': padron}
            )

        # Sincronizar cursos si se paso la lista
        if cursos is not None:
            # Primero eliminamos las relaciones anteriores
            ejecutar_mutacion('DELETE FROM alumnos_cursos WHERE padron = :padron', {'padron': padron})
            # Insertamos las nuevas
            for curso_id in cursos:
                if curso_id:
                    ejecutar_mutacion(
                        'INSERT INTO alumnos_cursos (padron, curso_id) VALUES (:padron, :curso_id)',
                        {'padron': padron, 'curso_id': int(curso_id)}
                    )

        return True
    except Exception as e:
        logger.error(f'Error al actualizar alumno: {e}')
        return None


def eliminar_alumno_en_bd(padron):
    """
    Elimina un alumno del sistema.
    """
    alumno = buscar_alumno_por_padron(padron)
    if alumno is None:
        return 'alumno no encontrado'

    try:
        ejecutar_mutacion(
            'DELETE FROM usuarios WHERE usuario_id = :usuario_id',
            {'usuario_id': alumno['usuario_id']}
        )
        return True
    except Exception as e:
        logger.error(f'Error al eliminar alumno: {e}')
        return None


def obtener_cursos_del_alumno(padron):
    """
    Obtiene los cursos asociados a un alumno.
    """
    try:
        sql = """
            SELECT c.curso_id, c.nombre, c.cuatrimestre, c.anio, c.descripcion
            FROM alumnos_cursos ac
            JOIN cursos c ON ac.curso_id = c.curso_id
            WHERE ac.padron = :padron AND c.deleted_at IS NULL
            ORDER BY c.anio DESC, c.cuatrimestre DESC
        """
        return ejecutar_consulta(sql, {'padron': padron})
    except Exception as e:
        logger.error(f'Error al obtener cursos del alumno {padron}: {e}')
        return []
