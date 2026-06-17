from app.repositories.alumno_repository import (
    obtener_todos_los_alumnos,
    buscar_alumno_por_padron,
    crear_alumno_en_bd,
    actualizar_alumno_en_bd,
    eliminar_alumno_en_bd,
    obtener_cursos_del_alumno,
    obtener_cursos_de_varios_alumnos
)
from werkzeug.security import generate_password_hash


def obtener_todos_alumnos():
    """
    Obtiene la lista de todos los alumnos registrados.

    Returns:
        list: Lista de alumnos con su información básica
    """
    try:
        alumnos = obtener_todos_los_alumnos()
        padrones = [a['padron'] for a in alumnos]
        cursos_por_padron = obtener_cursos_de_varios_alumnos(padrones)
        for a in alumnos:
            a['cursos'] = cursos_por_padron.get(a['padron'], [])
        return alumnos
    except Exception as e:
        print(f"Error al obtener alumnos: {e}")
        return None


def obtener_alumno(padron):
    try:
        if not padron:
            return None

        alumno = buscar_alumno_por_padron(padron)
        if alumno:
            alumno['cursos'] = obtener_cursos_del_alumno(padron)
        return alumno
    except Exception as e:
        print(f"Error al obtener alumno por padrón: {e}")
        return None


def crear_alumno(datos):
    try:
        if not all(key in datos for key in ['nombre', 'apellidos', 'matricula', 'email', 'password']):
            return {'error': 'Faltan datos requeridos'}

        padron = datos.get('matricula')
        nombre = datos.get('nombre')
        apellidos = datos.get('apellidos')
        email = datos.get('email')
        password = datos.get('password')

        password_hash = generate_password_hash(password)

        resultado = crear_alumno_en_bd(padron, nombre, apellidos, email, password_hash)

        if resultado is True:
            alumno = buscar_alumno_por_padron(padron)
            return {
                'mensaje': 'Alumno creado exitosamente',
                'alumno': alumno
            }
        else:
            return {'error': resultado}

    except Exception as e:
        print(f"Error al crear alumno: {e}")
        return {'error': str(e)}


def actualizar_alumno(padron, datos):
    try:
        if not padron:
            return {'error': 'Padrón no especificado'}

        nombre = datos.get('nombre')
        apellidos = datos.get('apellido') if datos.get('apellido') is not None else datos.get('apellidos')
        email = datos.get('email')
        password = datos.get('password')
        abandono = datos.get('abandono')
        cursos = datos.get('cursos')

        password_hash = None
        if password:
            password_hash = generate_password_hash(password)

        resultado = actualizar_alumno_en_bd(
            padron,
            nombre=nombre,
            apellido=apellidos,
            email=email,
            password_hash=password_hash,
            abandono=abandono,
            cursos=cursos
        )

        if resultado is True:
            alumno = buscar_alumno_por_padron(padron)
            return {
                'mensaje': 'Alumno actualizado exitosamente',
                'alumno': alumno
            }
        else:
            return {'error': resultado}

    except Exception as e:
        print(f"Error al actualizar alumno: {e}")
        return {'error': str(e)}


def eliminar_alumno(padron):
    try:
        if not padron:
            return {'error': 'Padrón no especificado'}

        resultado = eliminar_alumno_en_bd(padron)

        if resultado is True:
            return {
                'mensaje': 'Alumno eliminado exitosamente',
                'padron': padron
            }
        else:
            return {'error': resultado}

    except Exception as e:
        print(f"Error al eliminar alumno: {e}")
        return {'error': str(e)}