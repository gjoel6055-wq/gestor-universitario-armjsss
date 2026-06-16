from app.repositories import equipo_repository


# EQUIPOS

def obtener_todos(curso_id=None):
    return equipo_repository.obtener_todos(curso_id)


def obtener_por_id(equipo_id):
    equipo = equipo_repository.obtener_por_id(equipo_id)
    if not equipo:
        raise ValueError(f'Equipo {equipo_id} no encontrado')
    return equipo


def crear(datos):
    if not datos.get('nombre'):
        raise ValueError('El nombre del equipo es obligatorio')
    if not datos.get('curso_id'):
        raise ValueError('El curso_id es obligatorio')
    return equipo_repository.insertar(datos)


def actualizar(equipo_id, datos):
    obtener_por_id(equipo_id)
    if not datos.get('nombre'):
        raise ValueError('El nombre del equipo es obligatorio')
    return equipo_repository.actualizar(equipo_id, datos)


def actualizar_parcial(equipo_id, datos):
    equipo_actual = obtener_por_id(equipo_id)
    datos_actualizados = {
        'nombre': datos.get('nombre', equipo_actual['nombre'])
    }
    return equipo_repository.actualizar(equipo_id, datos_actualizados)


def eliminar(equipo_id):
    obtener_por_id(equipo_id)
    equipo_repository.eliminar(equipo_id)


# ALUMNOS DEL EQUIPO

def agregar_alumno(equipo_id, datos):
    obtener_por_id(equipo_id)
    padron = datos.get('padron')
    if not padron:
        raise ValueError('El padron es obligatorio')
    return equipo_repository.insertar_alumno(equipo_id, padron)


def quitar_alumno(equipo_id, padron):
    obtener_por_id(equipo_id)
    if not equipo_repository.alumno_en_equipo(equipo_id, padron):
        raise ValueError(f'El alumno {padron} no pertenece a este equipo')
    equipo_repository.eliminar_alumno(equipo_id, padron)


# EVALUACIONES DEL EQUIPO

def agregar_evaluacion(equipo_id, datos):
    obtener_por_id(equipo_id)
    evaluacion_id = datos.get('evaluacion_id')
    if not evaluacion_id:
        raise ValueError('El evaluacion_id es obligatorio')
    return equipo_repository.insertar_evaluacion(equipo_id, evaluacion_id)


def quitar_evaluacion(equipo_id, evaluacion_id):
    obtener_por_id(equipo_id)
    if not equipo_repository.evaluacion_en_equipo(equipo_id, evaluacion_id):
        raise ValueError(f'La evaluación {evaluacion_id} no está asociada a este equipo')
    equipo_repository.eliminar_evaluacion(equipo_id, evaluacion_id)