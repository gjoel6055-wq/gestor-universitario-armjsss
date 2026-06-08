from flask import Blueprint, request, jsonify
from app.services.auth_service import requiere_token
from app.services.log_service import registrar_actividad
from app.services import tipo_evaluacion_service

tipos_evaluacion_bp = Blueprint('tipos_evaluacion', __name__)


@tipos_evaluacion_bp.route('/tipos-evaluacion', methods=['GET'])
@requiere_token()
def lista():
    try:
        tipos = tipo_evaluacion_service.obtener_tipos()
        return jsonify(tipos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tipos_evaluacion_bp.route('/tipos-evaluacion/<int:tipo_id>', methods=['GET'])
@requiere_token()
def detalle(tipo_id):
    try:
        tipo = tipo_evaluacion_service.obtener_tipo(tipo_id)
        return jsonify(tipo), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tipos_evaluacion_bp.route('/tipos-evaluacion', methods=['POST'])
@requiere_token('docente')
def crear():
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400
        resultado = tipo_evaluacion_service.crear_tipo(datos)

        ip_usuario = request.remote_addr
        usuario_id = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        accion = f"Creó tipo de evaluación: {resultado['nombre']}"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify(resultado), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tipos_evaluacion_bp.route('/tipos-evaluacion/<int:tipo_id>', methods=['PUT'])
@requiere_token('docente')
def actualizar(tipo_id):
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400
        resultado = tipo_evaluacion_service.actualizar_tipo(tipo_id, datos)

        ip_usuario = request.remote_addr
        usuario_id = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        accion = f"Actualizó completamente el tipo de evaluación con ID: {tipo_id}"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify(resultado), 200
    except ValueError as e:
        mensaje = str(e).lower()
        codigo = 404 if 'no encontrado' in mensaje else 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tipos_evaluacion_bp.route('/tipos-evaluacion/<int:tipo_id>', methods=['PATCH'])
@requiere_token('docente')
def actualizar_parcial(tipo_id):
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400
        resultado = tipo_evaluacion_service.actualizar_tipo_parcial(tipo_id, datos)

        ip_usuario = request.remote_addr
        usuario_id = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        accion = f"Modificó el tipo de evaluación con ID: {tipo_id}"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify(resultado), 200
    except ValueError as e:
        mensaje = str(e).lower()
        codigo = 404 if 'no encontrado' in mensaje else 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tipos_evaluacion_bp.route('/tipos-evaluacion/<int:tipo_id>', methods=['DELETE'])
@requiere_token('docente')
def eliminar(tipo_id):
    try:
        tipo_evaluacion_service.eliminar_tipo(tipo_id)

        ip_usuario = request.remote_addr
        usuario_id = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        accion = f"Eliminó el tipo de evaluación con ID: {tipo_id}"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify({'mensaje': f'Tipo de evaluación {tipo_id} eliminado correctamente'}), 200
    except ValueError as e:
        mensaje = str(e).lower()
        codigo = 404 if 'no encontrado' in mensaje else 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500
