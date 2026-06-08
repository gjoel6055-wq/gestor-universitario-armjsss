from flask import Blueprint, request, jsonify
from app.services.auth_service import requiere_token
from app.services.log_service import registrar_actividad
from app.services import evaluacion_service

evaluaciones_bp = Blueprint('evaluaciones', __name__)


@evaluaciones_bp.route('/evaluaciones', methods=['GET'])
@requiere_token()
def lista():
    try:
        curso_id = request.args.get('curso_id', type=int)
        evaluaciones = evaluacion_service.obtener_evaluaciones(curso_id=curso_id)
        return jsonify(evaluaciones), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@evaluaciones_bp.route('/evaluaciones/<int:evaluacion_id>', methods=['GET'])
@requiere_token()
def detalle(evaluacion_id):
    try:
        evaluacion = evaluacion_service.obtener_evaluacion(evaluacion_id)
        return jsonify(evaluacion), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@evaluaciones_bp.route('/evaluaciones', methods=['POST'])
@requiere_token('docente')
def crear():
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400
        resultado = evaluacion_service.crear_evaluacion(datos)

        ip_usuario = request.remote_addr
        usuario_id = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        accion = f"Creó evaluación: {resultado['nombre']} en curso {resultado['curso_id']}"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify(resultado), 201
    except ValueError as e:
        codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@evaluaciones_bp.route('/evaluaciones/<int:evaluacion_id>', methods=['PUT'])
@requiere_token('docente')
def actualizar(evaluacion_id):
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400
        resultado = evaluacion_service.actualizar_evaluacion(evaluacion_id, datos)

        ip_usuario = request.remote_addr
        usuario_id = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        accion = f"Actualizó completamente la evaluación con ID: {evaluacion_id}"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify(resultado), 200
    except ValueError as e:
        mensaje = str(e).lower()
        if 'no encontrado' in mensaje:
            codigo = 404
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@evaluaciones_bp.route('/evaluaciones/<int:evaluacion_id>', methods=['PATCH'])
@requiere_token('docente')
def actualizar_parcial(evaluacion_id):
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400
        resultado = evaluacion_service.actualizar_evaluacion_parcial(evaluacion_id, datos)

        ip_usuario = request.remote_addr
        usuario_id = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        accion = f"Modificó la evaluación con ID: {evaluacion_id}"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify(resultado), 200
    except ValueError as e:
        mensaje = str(e).lower()
        if 'no encontrado' in mensaje:
            codigo = 404
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@evaluaciones_bp.route('/evaluaciones/<int:evaluacion_id>', methods=['DELETE'])
@requiere_token('docente')
def eliminar(evaluacion_id):
    try:
        resultado = evaluacion_service.eliminar_evaluacion(evaluacion_id)

        ip_usuario = request.remote_addr
        usuario_id = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        accion = f"Eliminó la evaluación con ID: {evaluacion_id}"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify({'mensaje': f'Evaluación {evaluacion_id} eliminada correctamente'}), 200
    except ValueError as e:
        mensaje = str(e).lower()
        if 'no encontrado' in mensaje:
            codigo = 404
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500
