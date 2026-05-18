from app.repositories.material_repository import crear_material_db

def registrar_nuevo_material(titulo, descripcion, url, curso_id):
    return crear_material_db(titulo, descripcion, url, curso_id)