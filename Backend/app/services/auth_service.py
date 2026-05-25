import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify

from app.repositories.usuario_repository import buscar_usuario_por_email, ingresar_nuevo_usuario
from werkzeug.security import check_password_hash, generate_password_hash

SECRET_KEY = "la_clave_super_secreta_secretisima_y_segura"

def generar_token(usuario_id, rol):
    payload = {
        'id': usuario_id,
        'rol': rol,
        'exp': datetime.now(timezone.utc) + timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def procesar_login(email, password):
    datos_usuario = buscar_usuario_por_email(email)

    if datos_usuario == None:
        return None

    if not check_password_hash(datos_usuario['password_hash'], password):
        return 'contrasena_incorrecta'

    token_jwt = generar_token(datos_usuario['usuario_id'], datos_usuario['rol'])

    return {
        "token": token_jwt,
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


# ---------------------------------------------------------------
# Decorador de autenticacion
# ---------------------------------------------------------------

def requiere_token(rol_necesario=None):
    def decorador(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')

            if not token or not token.startswith('Bearer '):
                return jsonify({'error': 'Falta el token de autorización'}), 401

            token = token.split(" ")[1]

            try:
                datos_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

                request.usuario_id = datos_token['id']
                request.usuario_rol = datos_token['rol']

            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'El token expiró. Volvé a iniciar sesión.'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Token inválido.'}), 401

            if rol_necesario is not None and request.usuario_rol != rol_necesario:
                return jsonify({'error': "No tienes permiso de realizar esta acción"}), 403

            return f(*args, **kwargs)

        return decorated

    return decorador