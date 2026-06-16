from app.repositories.docente_repository import (
    obtener_todos_los_docentes,
    buscar_docente_por_legajo,
    crear_docente_en_bd,
    actualizar_docente_en_bd,
    eliminar_docente_en_bd
)


def listar_docentes():
    return obtener_todos_los_docentes()


def obtener_docente(legajo):
    return buscar_docente_por_legajo(legajo)


def registrar_docente(legajo, nombre, apellido, email, password_hash, departamento=''):
    return crear_docente_en_bd(legajo, nombre, apellido, email, password_hash, departamento)


def modificar_docente(legajo, nombre=None, apellido=None, departamento=None):
    return actualizar_docente_en_bd(legajo, nombre, apellido, departamento)


def borrar_docente(legajo):
    return eliminar_docente_en_bd(legajo)