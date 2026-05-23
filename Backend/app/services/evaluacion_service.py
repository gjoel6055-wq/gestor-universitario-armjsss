from app.repositories.evaluacion_repository import (
     guardar_evaluacion_bd,
     modificar_evaluacion_bd,
     borrar_evaluacion_bd
)

def crear_evaluacion_servicio(datos):
    return guardar_evaluacion_bd(datos)

def modificar_evaluacion_servicio(id, datos):
    return modificar_evaluacion_bd(id, datos)

def borrar_evaluacion_servicio(id):
    return borrar_evaluacion_bd(id)
