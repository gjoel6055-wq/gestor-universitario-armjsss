from flask import Blueprint, request, jsonify
from app.services.auth_service import procesar_login, crear_nuevo_usuario, requiere_token
from app.services.log_service import registrar_log
import re
from constants import REGEX_EMAIL

auth_bp = Blueprint('auth', __name__)


def es_email_valido(email):
    return re.match(REGEX_EMAIL, email) is not None


@auth_bp.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    email_usuario = datos.get('email')
    password = datos.get('password')
    ip_usuario = request.remote_addr

    datos_usuario = procesar_login(email_usuario, password)

    if datos_usuario == 'contrasena_incorrecta':
        accion = "Login fallido"
        registrar_log(None, accion, ip_usuario)
        return jsonify({'error': 'La contraseña ingresada es incorrecta'}), 401

    if datos_usuario is None:
        accion = "Login con email no registrado"
        registrar_log(None, accion, ip_usuario)
        return jsonify({'error': 'El email ingresado no se encuentra registrado.'}), 404

    usuario_id = datos_usuario['usuario_id']
    accion = "Inicio sesion"
    registrar_log(usuario_id, accion, ip_usuario)

    return jsonify({
        'mensaje': 'Login exitoso',
        'token': datos_usuario['token'],
        'datos': {
            'nombre': datos_usuario['nombre'],
            'email': datos_usuario['email'],
            'rol': datos_usuario['rol']
        }
    }), 200

@auth_bp.route('/registro', methods=['POST'])
def register():
    datos = request.get_json()
    nombre = datos.get('nombre')
    apellido = datos.get('apellido')
    email = datos.get('email')
    password = datos.get('password')
    padron_o_legajo = datos.get('padron')

    if not all([nombre, apellido, email, password]):
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400

    if not es_email_valido(email):
        return jsonify({'error': 'El formato del email no es válido'}), 400

    situacion = crear_nuevo_usuario(nombre, apellido, email, password, padron_o_legajo)

    if situacion == 'email en uso':
        return jsonify({'error': "El email ingresado ya se encuentra en uso."}), 409

    if situacion is True:
        ip_usuario = request.remote_addr
        accion = f"Nuevo usuario registrado con el email: {email}"
        registrar_log(None, accion, ip_usuario)
        return jsonify({'mensaje': 'Se creó el usuario con exito.'}), 201

    return jsonify({'error': 'Ocurrio un error al crear el usuario, intentelo mas tarde.'}), 500


@auth_bp.route('/logout', methods=['POST'])
@requiere_token()
def logout():
    ip_usuario = request.remote_addr
    accion = "Cerró sesion"
    usuario_id = request.usuario_id
    registrar_log(usuario_id, accion, ip_usuario)

    return jsonify({'mensaje': "Se cerró la sesión con exito."}), 200