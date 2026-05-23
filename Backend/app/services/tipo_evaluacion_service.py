from app.repositories.tipo_evaluacion_repository import (
    guardar_tipo_bd,
    modificar_tipo_bd,
    borrar_tipo_bd
)

def crear_tipo_servicio(datos):
    return guardar_tipo_bd(datos)

def modificar_tipo_servicio(id, datos):
    return modificar_tipo_bd(id, datos)

def borrar_tipo_servicio(id):
    return borrar_tipo_bd(id)
