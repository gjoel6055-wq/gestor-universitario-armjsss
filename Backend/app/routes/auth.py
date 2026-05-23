from flask import Blueprint, request, jsonify, session
from app.services.auth_service import procesar_login, crear_nuevo_usuario
from functools import wraps
from app.services.log_service import registrar_log

auth_bp = Blueprint('auth', __name__)

def login_requerido(ruta):
    @wraps(ruta)
    def funcion_protegida(*args, **kwargs):
        if 'email' not in session:
            return jsonify({'error': 'Acceso denegado. Por favor, inicie sesión.'}), 401
        return ruta(*args, **kwargs)

    return funcion_protegida

def rol_requerido(rol_necesario):
    def decorador(ruta):
        @wraps(ruta)
        def funcion_protegida(*args, **kwargs):
            rol_usuario = session.get('rol')

            if rol_usuario != rol_necesario:
                return jsonify({'error': 'No tenés permisos para acceder a esta función.'}), 403

            return ruta(*args, **kwargs)

        return funcion_protegida

    return decorador

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

    if datos_usuario == None:
        accion = "Login con email no registrado"
        registrar_log(None, accion, ip_usuario)
        return jsonify({'error': 'El email ingresado no se encuentra registrado.'}), 404

    session['email'] = datos_usuario['email']
    session['rol'] = datos_usuario['rol']
    session['nombre'] = datos_usuario['nombre']
    session['usuario_id'] = datos_usuario['usuario_id']

    usuario_id = session.get('usuario_id')
    accion = "Inicio sesion"
    registrar_log(usuario_id, accion, ip_usuario)

    return jsonify({
        'mensaje':'Login exitoso',
        'datos': datos_usuario
    }), 200


@auth_bp.route('/registro', methods=['POST'])
def register():
    datos = request.get_json()
    nombre = datos.get('nombre')
    apellido = datos.get('apellido')
    email = datos.get('email')
    password = datos.get('password')

    situacion = crear_nuevo_usuario(nombre, apellido, email, password)

    if situacion == 'email en uso':
        return jsonify({'error': "El email ingresado ya se encuentra en uso."}), 409

    if situacion == True:
        ip_usuario = request.remote_addr
        accion = f"Nuevo usuario registrado: {email}"
        registrar_log(None, accion, ip_usuario)
        return  jsonify({'mensaje':'Se creó el usuario con exito.'}), 201

    return jsonify({'error': 'Ocurrio un error al crear el usuario, intentelo mas tarde.'}), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    ip_usuario = request.remote_addr
    accion = "Cerró sesion"
    usuario_id = session.get('usuario_id')
    registrar_log(usuario_id, accion, ip_usuario)

    session.clear()

    return jsonify({'mensaje': "Se cerró la sesión con exito"}), 200
