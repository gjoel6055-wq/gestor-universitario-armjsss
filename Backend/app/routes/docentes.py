from flask import Blueprint, request, jsonify, session
from app.services.docente_service import (
    listar_docentes,
    obtener_docente,
    registrar_docente,
    modificar_docente,
    borrar_docente
)
from app.services.log_service import registrar_actividad
from app.services.auth_service import requiere_token
from werkzeug.security import generate_password_hash

docente_bp = Blueprint('docente', __name__)


@docente_bp.route('/docentes', methods=['GET'])
@requiere_token()
def obtener_todos_los_docentes():
    try:
        lista = listar_docentes()
        return jsonify(lista), 200
    except Exception as e:
        return jsonify({'error': 'Error interno al obtener la lista de docentes'}), 500


@docente_bp.route('/docentes/<int:legajo>', methods=['GET'])
@requiere_token()
def obtener_docente_por_legajo(legajo):
    try:
        docente = obtener_docente(legajo)
        if docente is None:
            return jsonify({'error': 'Docente no encontrado'}), 404
        return jsonify(docente), 200
    except Exception as e:
        return jsonify({'error': 'Error interno al obtener el docente'}), 500


@docente_bp.route('/docentes', methods=['POST'])
@requiere_token(rol_necesario='docente')
def agregar_docente():
    datos = request.get_json()
    legajo      = datos.get('legajo')
    nombre      = datos.get('nombre')
    apellido    = datos.get('apellido')
    email       = datos.get('email')
    password    = datos.get('password')
    departamento = datos.get('departamento', '')

    if not all([legajo, nombre, apellido, email, password]):
        return jsonify({'error': 'legajo, nombre, apellido, email y password son obligatorios'}), 400

    password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        resultado = registrar_docente(legajo, nombre, apellido, email, password_hash, departamento)

        if resultado == 'legajo en uso':
            return jsonify({'error': 'El legajo ya está en uso'}), 409
        if resultado == 'email en uso':
            return jsonify({'error': 'El email ya está en uso'}), 409
        if resultado is None:
            return jsonify({'error': 'Error interno al registrar el docente'}), 500

        ip_usuario = request.remote_addr
        usuario_id = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        accion = f"Registró al docente con legajo {legajo}"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify({'mensaje': 'Docente registrado exitosamente', 'legajo': resultado}), 201
    except Exception as e:
        return jsonify({'error': 'Error interno en la base de datos'}), 500


@docente_bp.route('/docentes/<int:legajo>', methods=['PUT', 'PATCH'])
@requiere_token(rol_necesario='docente')
def actualizar_docente(legajo):
    datos = request.get_json()
    nombre      = datos.get('nombre')
    apellido    = datos.get('apellido')
    departamento = datos.get('departamento')

    if not any([nombre, apellido, departamento]):
        return jsonify({'error': 'Debés enviar al menos un campo para actualizar'}), 400

    try:
        resultado = modificar_docente(legajo, nombre, apellido, departamento)

        if resultado == 'docente no encontrado':
            return jsonify({'error': 'Docente no encontrado'}), 404
        if resultado is None:
            return jsonify({'error': 'Error interno al actualizar'}), 500

        ip_usuario = request.remote_addr
        usuario_id = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        accion = f"Actualizó al docente con legajo {legajo}"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify({'mensaje': f'Docente {legajo} actualizado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': 'Error interno al actualizar el docente'}), 500


@docente_bp.route('/docentes/<int:legajo>', methods=['DELETE'])
@requiere_token(rol_necesario='docente')
def eliminar_docente(legajo):
    try:
        eliminado = borrar_docente(legajo)

        if eliminado is None:
            return jsonify({'error': 'Docente no encontrado'}), 404

        ip_usuario = request.remote_addr
        usuario_id = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        accion = f"Dio de baja al docente con legajo {legajo}"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify({'mensaje': f'Docente {legajo} dado de baja correctamente'}), 200
    except Exception as e:
        return jsonify({'error': 'Error interno al intentar eliminar al docente'}), 500