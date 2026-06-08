from flask import Blueprint, request, jsonify
from app.services.auth_service import requiere_token
from app.services.log_service import registrar_log
from app.services import tipo_evaluacion_service

tipos_evaluacion_bp = Blueprint('tipos_evaluacion', __name__)


@tipos_evaluacion_bp.route('/tipos-evaluacion', methods=['GET'])
@requiere_token()
def lista():
    tipos = tipo_evaluacion_service.obtener_tipos()
    return jsonify(tipos), 200


@tipos_evaluacion_bp.route('/tipos-evaluacion/<int:tipo_id>', methods=['GET'])
@requiere_token()
def detalle(tipo_id):
    tipo = tipo_evaluacion_service.obtener_tipo(tipo_id)
    if tipo is None:
        return jsonify({'error': f'Tipo de evaluación {tipo_id} no encontrado'}), 404
    return jsonify(tipo), 200


@tipos_evaluacion_bp.route('/tipos-evaluacion', methods=['POST'])
@requiere_token('docente')
def crear():
    datos = request.get_json()
    if not datos:
        return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400

    resultado = tipo_evaluacion_service.crear_tipo(datos)

    if resultado == 'campos_incompletos':
        return jsonify({'error': 'El nombre es obligatorio'}), 400
    if resultado is None:
        return jsonify({'error': 'Ocurrió un error al crear el tipo de evaluación'}), 500

    registrar_log(
        request.usuario_id,
        f"Creó tipo de evaluación: {resultado['nombre']}",
        request.remote_addr
    )
    return jsonify(resultado), 201


@tipos_evaluacion_bp.route('/tipos-evaluacion/<int:tipo_id>', methods=['PUT'])
@requiere_token('docente')
def actualizar(tipo_id):
    datos = request.get_json()
    if not datos:
        return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400

    resultado = tipo_evaluacion_service.actualizar_tipo(tipo_id, datos)

    if resultado == 'no_encontrado':
        return jsonify({'error': f'Tipo de evaluación {tipo_id} no encontrado'}), 404
    if resultado == 'campos_incompletos':
        return jsonify({'error': 'El nombre es obligatorio'}), 400
    if resultado is None:
        return jsonify({'error': 'Ocurrió un error al actualizar'}), 500

    registrar_log(
        request.usuario_id,
        f"Actualizó tipo de evaluación {tipo_id}",
        request.remote_addr
    )
    return jsonify(resultado), 200


@tipos_evaluacion_bp.route('/tipos-evaluacion/<int:tipo_id>', methods=['PATCH'])
@requiere_token('docente')
def actualizar_parcial(tipo_id):
    datos = request.get_json()
    if not datos:
        return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400

    resultado = tipo_evaluacion_service.actualizar_tipo_parcial(tipo_id, datos)

    if resultado == 'no_encontrado':
        return jsonify({'error': f'Tipo de evaluación {tipo_id} no encontrado'}), 404
    if resultado is None:
        return jsonify({'error': 'Ocurrió un error al actualizar'}), 500

    registrar_log(
        request.usuario_id,
        f"Actualizó parcialmente tipo de evaluación {tipo_id}",
        request.remote_addr
    )
    return jsonify(resultado), 200


@tipos_evaluacion_bp.route('/tipos-evaluacion/<int:tipo_id>', methods=['DELETE'])
@requiere_token('docente')
def eliminar(tipo_id):
    resultado = tipo_evaluacion_service.eliminar_tipo(tipo_id)

    if resultado == 'no_encontrado':
        return jsonify({'error': f'Tipo de evaluación {tipo_id} no encontrado'}), 404

    registrar_log(
        request.usuario_id,
        f"Eliminó tipo de evaluación {tipo_id}",
        request.remote_addr
    )
    return jsonify({'mensaje': f'Tipo de evaluación {tipo_id} eliminado correctamente'}), 200
