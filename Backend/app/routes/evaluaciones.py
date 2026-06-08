from flask import Blueprint, request, jsonify
from app.services.auth_service import requiere_token
from app.services.log_service import registrar_log
from app.services import evaluacion_service

evaluaciones_bp = Blueprint('evaluaciones', __name__)


@evaluaciones_bp.route('/evaluaciones', methods=['GET'])
@requiere_token()
def lista():
    curso_id = request.args.get('curso_id', type=int)
    evaluaciones = evaluacion_service.obtener_evaluaciones(curso_id=curso_id)
    return jsonify(evaluaciones), 200


@evaluaciones_bp.route('/evaluaciones/<int:evaluacion_id>', methods=['GET'])
@requiere_token()
def detalle(evaluacion_id):
    evaluacion = evaluacion_service.obtener_evaluacion(evaluacion_id)
    if evaluacion is None:
        return jsonify({'error': f'Evaluación {evaluacion_id} no encontrada'}), 404
    return jsonify(evaluacion), 200


@evaluaciones_bp.route('/evaluaciones', methods=['POST'])
@requiere_token('docente')
def crear():
    datos = request.get_json()
    if not datos:
        return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400

    resultado = evaluacion_service.crear_evaluacion(datos)

    if resultado == 'campos_incompletos':
        return jsonify({'error': 'Nombre, tipo_id, curso_id, fecha y peso son obligatorios'}), 400
    if resultado is None:
        return jsonify({'error': 'Ocurrió un error al crear la evaluación'}), 500

    registrar_log(
        request.usuario_id,
        f"Creó evaluación: {resultado['nombre']} en curso {resultado['curso_id']}",
        request.remote_addr
    )
    return jsonify(resultado), 201


@evaluaciones_bp.route('/evaluaciones/<int:evaluacion_id>', methods=['PUT'])
@requiere_token('docente')
def actualizar(evaluacion_id):
    datos = request.get_json()
    if not datos:
        return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400

    resultado = evaluacion_service.actualizar_evaluacion(evaluacion_id, datos)

    if resultado == 'no_encontrado':
        return jsonify({'error': f'Evaluación {evaluacion_id} no encontrada'}), 404
    if resultado == 'campos_incompletos':
        return jsonify({'error': 'Nombre, tipo_id, curso_id, fecha y peso son obligatorios'}), 400
    if resultado is None:
        return jsonify({'error': 'Ocurrió un error al actualizar'}), 500

    registrar_log(
        request.usuario_id,
        f"Actualizó evaluación {evaluacion_id}",
        request.remote_addr
    )
    return jsonify(resultado), 200


@evaluaciones_bp.route('/evaluaciones/<int:evaluacion_id>', methods=['PATCH'])
@requiere_token('docente')
def actualizar_parcial(evaluacion_id):
    datos = request.get_json()
    if not datos:
        return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400

    resultado = evaluacion_service.actualizar_evaluacion_parcial(evaluacion_id, datos)

    if resultado == 'no_encontrado':
        return jsonify({'error': f'Evaluación {evaluacion_id} no encontrada'}), 404
    if resultado is None:
        return jsonify({'error': 'Ocurrió un error al actualizar'}), 500

    registrar_log(
        request.usuario_id,
        f"Actualizó parcialmente evaluación {evaluacion_id}",
        request.remote_addr
    )
    return jsonify(resultado), 200


@evaluaciones_bp.route('/evaluaciones/<int:evaluacion_id>', methods=['DELETE'])
@requiere_token('docente')
def eliminar(evaluacion_id):
    resultado = evaluacion_service.eliminar_evaluacion(evaluacion_id)

    if resultado == 'no_encontrado':
        return jsonify({'error': f'Evaluación {evaluacion_id} no encontrada'}), 404

    registrar_log(
        request.usuario_id,
        f"Eliminó evaluación {evaluacion_id}",
        request.remote_addr
    )
    return jsonify({'mensaje': f'Evaluación {evaluacion_id} eliminada correctamente'}), 200
