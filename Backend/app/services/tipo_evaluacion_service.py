from app.repositories.tipo_evaluacion_repository import (
    obtener_todos_tipos,
    obtener_tipo_por_id,
    guardar_tipo_bd,
    modificar_tipo_bd,
    borrar_tipo_bd
)


def obtener_tipos():
    return obtener_todos_tipos()


def obtener_tipo(tipo_id):
    return obtener_tipo_por_id(tipo_id)


def crear_tipo(datos):
    if not datos.get('nombre'):
        return 'campos_incompletos'
    return guardar_tipo_bd(datos)


def actualizar_tipo(tipo_id, datos):
    tipo = obtener_tipo_por_id(tipo_id)
    if not tipo:
        return 'no_encontrado'
    if not datos.get('nombre'):
        return 'campos_incompletos'
    return modificar_tipo_bd(tipo_id, datos)


def actualizar_tipo_parcial(tipo_id, datos):
    tipo = obtener_tipo_por_id(tipo_id)
    if not tipo:
        return 'no_encontrado'
    datos_actualizados = {
        'nombre':      datos.get('nombre',      tipo['nombre']),
        'descripcion': datos.get('descripcion', tipo['descripcion'])
    }
    return modificar_tipo_bd(tipo_id, datos_actualizados)


def eliminar_tipo(tipo_id):
    tipo = obtener_tipo_por_id(tipo_id)
    if not tipo:
        return 'no_encontrado'
    borrar_tipo_bd(tipo_id)
    return True
