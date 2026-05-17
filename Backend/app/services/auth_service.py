from app.repositories.usuario_repository import buscar_usuario_por_email, ingresar_nuevo_usuario
from werkzeug.security import check_password_hash, generate_password_hash

def procesar_login(email, password):

    datos_usuario = buscar_usuario_por_email(email)

    if datos_usuario == None:
        return None

    if not check_password_hash(datos_usuario['password_hash'], password):
        return 'contrasena_incorrecta'

    return {
        "usuario_id": datos_usuario['usuario_id'],
        "nombre": datos_usuario['nombre'],
        'rol': datos_usuario['rol'],
        'email': datos_usuario['email']
    }


def crear_nuevo_usuario(nombre, apellido, email, password):

    hash_password = generate_password_hash(password)
    rol = 'alumno'
    situacion = ingresar_nuevo_usuario(nombre, apellido, email, hash_password, rol)

    return situacion
