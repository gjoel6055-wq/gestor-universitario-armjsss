from flask import Blueprint, request, jsonify
from app.services import equipo_service

equipos_bp = Blueprint('equipos', __name__)


@equipos_bp.route('/equipos', methods=['GET'])
def obtener_equipos():
    try:
        curso_id = request.args.get('curso_id', type=int)
        equipos = equipo_service.obtener_todos(curso_id)
        return jsonify(equipos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipos_bp.route('/equipos/<int:equipo_id>', methods=['GET'])
def obtener_equipo(equipo_id):
    try:
        equipo = equipo_service.obtener_por_id(equipo_id)
        return jsonify(equipo), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipos_bp.route('/equipos', methods=['POST'])
def crear_equipo():
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400
        equipo = equipo_service.crear(datos)
        return jsonify(equipo), 201
    except ValueError as e:
        mensaje = str(e).lower()
        if 'ya existe' in mensaje:
            codigo = 409
        elif 'no existe' in mensaje:
            codigo = 404
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipos_bp.route('/equipos/<int:equipo_id>', methods=['PUT'])
def actualizar_equipo(equipo_id):
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400
        equipo = equipo_service.actualizar(equipo_id, datos)
        return jsonify(equipo), 200
    except ValueError as e:
        mensaje = str(e).lower()
        if 'no encontrado' in mensaje:
            codigo = 404
        elif 'ya existe' in mensaje:
            codigo = 409
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipos_bp.route('/equipos/<int:equipo_id>', methods=['DELETE'])
def eliminar_equipo(equipo_id):
    try:
        equipo_service.eliminar(equipo_id)
        return jsonify({'mensaje': f'Equipo {equipo_id} eliminado correctamente'}), 200
    except ValueError as e:
        mensaje = str(e).lower()
        if 'no encontrado' in mensaje:
            codigo = 404
        elif 'asociadas' in mensaje:
            codigo = 409
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipos_bp.route('/equipos/<int:equipo_id>/alumnos', methods=['POST'])
def agregar_alumno(equipo_id):
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400
        resultado = equipo_service.agregar_alumno(equipo_id, datos)
        return jsonify(resultado), 201
    except ValueError as e:
        mensaje = str(e).lower()
        if 'no encontrado' in mensaje or 'no existe' in mensaje:
            codigo = 404
        elif 'ya pertenece' in mensaje:
            codigo = 409
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipos_bp.route('/equipos/<int:equipo_id>/alumnos/<int:padron>', methods=['DELETE'])
def quitar_alumno(equipo_id, padron):
    try:
        equipo_service.quitar_alumno(equipo_id, padron)
        return jsonify({'mensaje': f'Alumno {padron} quitado del equipo {equipo_id}'}), 200
    except ValueError as e:
        mensaje = str(e).lower()
        if 'no encontrado' in mensaje or 'no pertenece' in mensaje:
            codigo = 404
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipos_bp.route('/equipos/<int:equipo_id>/evaluaciones', methods=['POST'])
def agregar_evaluacion(equipo_id):
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400
        resultado = equipo_service.agregar_evaluacion(equipo_id, datos)
        return jsonify(resultado), 201
    except ValueError as e:
        mensaje = str(e).lower()
        if 'no encontrado' in mensaje or 'no existe' in mensaje:
            codigo = 404
        elif 'ya está asociada' in mensaje:
            codigo = 409
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipos_bp.route('/equipos/<int:equipo_id>/evaluaciones/<int:evaluacion_id>', methods=['DELETE'])
def quitar_evaluacion(equipo_id, evaluacion_id):
    try:
        equipo_service.quitar_evaluacion(equipo_id, evaluacion_id)
        return jsonify({'mensaje': f'Evaluación {evaluacion_id} quitada del equipo {equipo_id}'}), 200
    except ValueError as e:
        mensaje = str(e).lower()
        if 'no encontrado' in mensaje or 'no está asociada' in mensaje:
            codigo = 404
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500