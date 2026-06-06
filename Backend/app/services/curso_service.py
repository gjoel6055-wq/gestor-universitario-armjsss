from app.repositories import curso_repository


def obtener_todos():
    return curso_repository.obtener_todos()


def obtener_por_id(curso_id):
    curso = curso_repository.obtener_por_id(curso_id)
    if not curso:
        raise ValueError(f'Curso {curso_id} no encontrado')
    return curso


def crear(datos):
    if not datos.get('nombre'):
        raise ValueError('El nombre es obligatorio')
    if not datos.get('cuatrimestre'):
        raise ValueError('El cuatrimestre es obligatorio')
    if not datos.get('anio'):
        raise ValueError('El año es obligatorio')
    if datos['cuatrimestre'] not in ('1C', '2C'):
        raise ValueError('El cuatrimestre debe ser 1C o 2C')

    # Acepta tanto int como string numérico
    try:
        anio = int(datos['anio'])
    except (ValueError, TypeError):
        raise ValueError('El año debe ser un número válido entre 2000 y 2100')
    if anio < 2000 or anio > 2100:
        raise ValueError('El año debe ser un número válido entre 2000 y 2100')
    datos['anio'] = anio  # Normalizar siempre a int

    return curso_repository.insertar(datos)


def actualizar(curso_id, datos):
    obtener_por_id(curso_id)
    if not datos.get('nombre'):
        raise ValueError('El nombre es obligatorio')
    if not datos.get('cuatrimestre'):
        raise ValueError('El cuatrimestre es obligatorio')
    if not datos.get('anio'):
        raise ValueError('El año es obligatorio')
    if datos['cuatrimestre'] not in ('1C', '2C'):
        raise ValueError('El cuatrimestre debe ser 1C o 2C')

    try:
        anio = int(datos['anio'])
    except (ValueError, TypeError):
        raise ValueError('El año debe ser un número válido entre 2000 y 2100')
    if anio < 2000 or anio > 2100:
        raise ValueError('El año debe ser un número válido entre 2000 y 2100')
    datos['anio'] = anio

    return curso_repository.actualizar(curso_id, datos)


def actualizar_parcial(curso_id, datos):
    curso_actual = obtener_por_id(curso_id)
    if 'cuatrimestre' in datos and datos['cuatrimestre'] not in ('1C', '2C'):
        raise ValueError('El cuatrimestre debe ser 1C o 2C')
    if 'anio' in datos:
        try:
            anio = int(datos['anio'])
        except (ValueError, TypeError):
            raise ValueError('El año debe ser un número válido entre 2000 y 2100')
        if anio < 2000 or anio > 2100:
            raise ValueError('El año debe ser un número válido entre 2000 y 2100')
        datos['anio'] = anio

    datos_actualizados = {
        'nombre':       datos.get('nombre',       curso_actual['nombre']),
        'cuatrimestre': datos.get('cuatrimestre', curso_actual['cuatrimestre']),
        'anio':         datos.get('anio',         curso_actual['anio']),
        'descripcion':  datos.get('descripcion',  curso_actual['descripcion'])
    }
    return curso_repository.actualizar(curso_id, datos_actualizados)


def eliminar(curso_id):
    obtener_por_id(curso_id)
    curso_repository.eliminar(curso_id)