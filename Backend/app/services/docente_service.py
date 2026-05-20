from app.repositories.docente_repository import (
    obtener_docentes_db,
    crear_docente_db,
    eliminar_docente_db
)

def listar_docentes():
    return obtener_docentes_db()

def registrar_docente(legajo, usuario_id, departamento):
    return crear_docente_db(legajo, usuario_id, departamento)

def borrar_docente(legajo):
    return eliminar_docente_db(legajo)