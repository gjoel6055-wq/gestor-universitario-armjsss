from app.repositories.nota_repository import (
    guardar_nota_bd,
    modificar_nota_bd,
    borrar_nota_bd
)

def crear_nota_servicio(datos):
    return guardar_nota_bd(datos)

def modificar_nota_servicio(id, datos):
    return modificar_nota_bd(id, datos)

def borrar_nota_servicio(id):
    return borrar_nota_bd(id)
