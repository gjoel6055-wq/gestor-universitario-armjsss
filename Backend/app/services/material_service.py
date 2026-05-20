from app.repositories.material_repository import (
    crear_material_db, 
    obtener_materiales_db, 
    actualizar_material_db, 
    eliminar_material_db
)

def registrar_nuevo_material(titulo, descripcion, url, curso_id):
    return crear_material_db(titulo, descripcion, url, curso_id)

def listar_materiales():
    return obtener_materiales_db()

def modificar_material(id, titulo, descripcion, url, curso_id):
    return actualizar_material_db(id, titulo, descripcion, url, curso_id)

def eliminar_material(id):
    return eliminar_material_db(id)