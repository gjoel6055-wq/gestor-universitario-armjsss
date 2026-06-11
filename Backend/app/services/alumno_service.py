import logging
from app.repositories.alumno_repository import (
    obtener_todos_los_alumnos,
    buscar_alumno_por_padron,
    crear_alumno_en_bd,
    actualizar_alumno_en_bd,
    eliminar_alumno_en_bd,
    obtener_cursos_del_alumno
)
from werkzeug.security import generate_password_hash

logger = logging.getLogger(__name__)


def obtener_todos_alumnos():
    """
    Obtiene la lista de todos los alumnos registrados.
    
    Returns:
        list: Lista de alumnos con su información básica
    """
    try:
        alumnos = obtener_todos_los_alumnos()
        for a in alumnos:
            a['cursos'] = obtener_cursos_del_alumno(a['padron'])
        return alumnos
    except Exception as e:
        logger.error(f"Error al obtener alumnos: {e}")
        return None


def obtener_alumno(padron):
    """
    Obtiene los detalles de un alumno por su número de padrón.
    
    Args:
        padron (str): Número de padrón del alumno
        
    Returns:
        dict: Información del alumno o None si no existe
    """
    try:
        if not padron:
            return None
            
        alumno = buscar_alumno_por_padron(padron)
        if alumno:
            alumno['cursos'] = obtener_cursos_del_alumno(padron)
        return alumno
    except Exception as e:
        logger.error(f"Error al obtener alumno por padron: {e}")
        return None


def crear_alumno(datos):
    """
    Crea un nuevo alumno en el sistema.
    
    Args:
        datos (dict): Diccionario con los datos del alumno
                     - nombre (str): Nombre del alumno
                     - apellidos (str): Apellidos del alumno
                     - matricula (str): Número de matrícula/padrón
                     - fechaNacimiento (str, opcional): Fecha de nacimiento (YYYY-MM-DD)
                     - email (str): Email del alumno
                     - password (str): Contraseña del alumno
        
    Returns:
        dict: Información del alumno creado o error si algo falla
              Returns 'padron en uso' si el padrón ya existe
              Returns 'email en uso' si el email ya existe
    """
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
        logger.error(f"Error al crear alumno: {e}")
        return {'error': str(e)}


def actualizar_alumno(padron, datos):
    """
    Actualiza los datos de un alumno existente.
    
    Args:
        padron (str): Número de padrón del alumno
        datos (dict): Diccionario con los datos a actualizar
                     - nombre (str, opcional): Nuevo nombre
                     - apellidos (str, opcional): Nuevos apellidos
                     - email (str, opcional): Nuevo email
                     - password (str, opcional): Nueva contraseña
                     - abandono (bool, opcional): Estado abandono
                     - cursos (list, opcional): Cursos
        
    Returns:
        dict: Información del alumno actualizado o error si algo falla
    """
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
        logger.error(f"Error al actualizar alumno: {e}")
        return {'error': str(e)}


def eliminar_alumno(padron):
    """
    Elimina un alumno del sistema.
    
    Args:
        padron (str): Número de padrón del alumno
        
    Returns:
        dict: Confirmación de eliminación o error si algo falla
    """
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
        logger.error(f"Error al eliminar alumno: {e}")
        return {'error': str(e)}
