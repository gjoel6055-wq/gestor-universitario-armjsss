from flask import Blueprint, request, jsonify, session
from services.alumno_service import (
    obtener_todos_alumnos,
    obtener_alumno,
    crear_alumno,
    actualizar_alumno,
    eliminar_alumno
)
from app.services.log_service import registrar_log
from app.services.auth_service import requiere_token

alumnos_bp = Blueprint('alumnos', __name__)

@alumnos_bp.route('/alumnos', methods=['GET'])
@requiere_token()
def obtener_alumnos():
    alumnos = obtener_todos_alumnos()
    return jsonify(alumnos), 200

@alumnos_bp.route('/alumnos/<int:id>', methods=['GET'])
@requiere_token()
def obtener_alumno_por_id(id):
    alumno = obtener_alumno(id)
    if alumno is None:
        return jsonify({'error': 'Alumno no encontrado.'}), 404
    return jsonify(alumno), 200

@alumnos_bp.route('/alumnos', methods=['POST'])
@requiere_token()
def crear_nuevo_alumno():
    datos = request.get_json() or {}
    padron = datos.get('padron')
    nombre = datos.get('nombre')
    apellido = datos.get('apellido')
    email = datos.get('email')
    password = datos.get('password')
    abandono = datos.get('abandono', False)

    missing = [campo for campo in ['padron', 'nombre', 'apellido', 'email', 'password'] if not datos.get(campo)]
    if missing:
        return jsonify({'error': f'Faltan campos obligatorios: {", ".join(missing)}.'}), 400

    situacion = crear_alumno(padron, nombre, apellido, email, password, abandono)

    if situacion == 'padron en uso':
        return jsonify({'error': 'El padrón ya está registrado.'}), 409
    if situacion == 'email en uso':
        return jsonify({'error': 'El email ya está registrado.'}), 409
    if situacion is True:

        ip_usuario = request.remote_addr
        usuario_id = session.get('usuario_id')
        accion = f"Registró al nuevo alumno: {nombre} {apellido} (Padrón: {padron})"
        registrar_log(usuario_id, accion, ip_usuario)

        alumno = obtener_alumno(padron)
        return jsonify(alumno), 201

    return jsonify({'error': 'No se pudo crear el alumno, intente de nuevo.'}), 500

@alumnos_bp.route('/alumnos/<int:id>', methods=['PUT'])
@requiere_token()
def actualizar_datos_alumno(id):
    datos = request.get_json() or {}
    nombre = datos.get('nombre')
    apellido = datos.get('apellido')
    email = datos.get('email')
    password = datos.get('password')
    abandono = datos.get('abandono')

    if nombre is None and apellido is None and email is None and password is None and abandono is None:
        return jsonify({'error': 'Se requiere al menos un campo para actualizar.'}), 400

    situacion = actualizar_alumno(id, nombre, apellido, email, password, abandono)

    if situacion == 'alumno no encontrado':
        return jsonify({'error': 'Alumno no encontrado.'}), 404
    if situacion == 'email en uso':
        return jsonify({'error': 'El email ya está registrado por otro usuario.'}), 409
    if situacion is True:

        ip_usuario = request.remote_addr
        usuario_id = session.get('usuario_id')
        accion = f"Actualizó los datos del alumno con ID: {id}"
        registrar_log(usuario_id, accion, ip_usuario)

        alumno = obtener_alumno(id)
        return jsonify(alumno), 200

    return jsonify({'error': 'No se pudo actualizar el alumno, intente de nuevo.'}), 500

@alumnos_bp.route('/alumnos/<int:id>', methods=['DELETE'])
@requiere_token()
def eliminar_alumno_por_id(id):
    situacion = eliminar_alumno(id)

    if situacion == 'alumno no encontrado':
        return jsonify({'error': 'Alumno no encontrado.'}), 404
    if situacion is True:

        ip_usuario = request.remote_addr
        usuario_id = session.get('usuario_id')
        accion = f"Eliminó al alumno con ID: {id}"
        registrar_log(usuario_id, accion, ip_usuario)

        return jsonify({'message': 'Alumno eliminado con éxito.', 'status': True}), 200

    return jsonify({'error': 'No se pudo eliminar el alumno, intente de nuevo.'}), 500
