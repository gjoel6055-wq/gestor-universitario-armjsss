from flask import Blueprint, request, jsonify, session
from app.services.auth_service import procesar_login, crear_nuevo_usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    email_usuario = datos.get('email')
    password = datos.get('password')

    datos_usuario = procesar_login(email_usuario, password)

    if datos_usuario == 'contrasena_incorrecta':
        return jsonify({'error': 'La contraseña ingresada es incorrecta'}), 401

    if datos_usuario == None:
        return jsonify({'error': 'El email ingresado no se encuentra registrado.'}), 404

    session['email'] = datos_usuario['email']
    session['rol'] = datos_usuario['rol']
    session['nombre'] = datos_usuario['nombre']
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
        return  jsonify({'mensaje':'Se creó el usuario con exito.'}), 201

    return jsonify({'error': 'Ocurrio un error al crear el usuario, intentelo mas tarde.'}), 500


@auth_bp.route('/logout', methods=['[POST'])
def logout():
    session.clear()

    return jsonify({'mensaje': "Se cerró la sesión con exito"}), 200
