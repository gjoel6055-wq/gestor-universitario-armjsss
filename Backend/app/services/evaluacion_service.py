from app.repositories.evaluacion_repository import (
    obtener_todas_evaluaciones,
    obtener_evaluacion_por_id,
    guardar_evaluacion_bd,
    modificar_evaluacion_bd,
    borrar_evaluacion_bd
)


def obtener_evaluaciones(curso_id=None):
    return obtener_todas_evaluaciones(curso_id=curso_id)


def obtener_evaluacion(evaluacion_id):
    return obtener_evaluacion_por_id(evaluacion_id)


def crear_evaluacion(datos):
    if not datos.get('nombre'):
        return 'campos_incompletos'
    if not datos.get('tipo_id'):
        return 'campos_incompletos'
    if not datos.get('curso_id'):
        return 'campos_incompletos'
    if not datos.get('fecha'):
        return 'campos_incompletos'
    if not datos.get('peso'):
        return 'campos_incompletos'
    return guardar_evaluacion_bd(datos)


def actualizar_evaluacion(evaluacion_id, datos):
    evaluacion = obtener_evaluacion_por_id(evaluacion_id)
    if not evaluacion:
        return 'no_encontrado'
    if not datos.get('nombre'):
        return 'campos_incompletos'
    if not datos.get('tipo_id'):
        return 'campos_incompletos'
    if not datos.get('curso_id'):
        return 'campos_incompletos'
    if not datos.get('fecha'):
        return 'campos_incompletos'
    if not datos.get('peso'):
        return 'campos_incompletos'
    return modificar_evaluacion_bd(evaluacion_id, datos)


def actualizar_evaluacion_parcial(evaluacion_id, datos):
    evaluacion = obtener_evaluacion_por_id(evaluacion_id)
    if not evaluacion:
        return 'no_encontrado'
    datos_actualizados = {
        'tipo_id':     datos.get('tipo_id',     evaluacion['tipo_id']),
        'curso_id':    datos.get('curso_id',    evaluacion['curso_id']),
        'nombre':      datos.get('nombre',      evaluacion['nombre']),
        'fecha':       datos.get('fecha',       evaluacion['evaluacion_fecha']),
        'peso':        datos.get('peso',        evaluacion['peso']),
        'descripcion': datos.get('descripcion', evaluacion['descripcion'])
    }
    return modificar_evaluacion_bd(evaluacion_id, datos_actualizados)


def eliminar_evaluacion(evaluacion_id):
    evaluacion = obtener_evaluacion_por_id(evaluacion_id)
    if not evaluacion:
        return 'no_encontrado'
    borrar_evaluacion_bd(evaluacion_id)
    return True
