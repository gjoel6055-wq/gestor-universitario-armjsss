from flask import Blueprint, request, jsonify
from app.services import curso_service

cursos_bp = Blueprint('cursos', __name__)


@cursos_bp.route('/cursos', methods=['GET'])
def obtener_cursos():
    try:
        cursos = curso_service.obtener_todos()
        return jsonify(cursos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@cursos_bp.route('/cursos/<int:curso_id>', methods=['GET'])
def obtener_curso(curso_id):
    try:
        curso = curso_service.obtener_por_id(curso_id)
        return jsonify(curso), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@cursos_bp.route('/cursos', methods=['POST'])
def crear_curso():
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400
        curso = curso_service.crear(datos)
        return jsonify(curso), 201
    except ValueError as e:
        codigo = 409 if 'ya existe' in str(e).lower() else 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@cursos_bp.route('/cursos/<int:curso_id>', methods=['PUT'])
def actualizar_curso(curso_id):
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400
        curso = curso_service.actualizar(curso_id, datos)
        return jsonify(curso), 200
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

@cursos_bp.route('/cursos/<int:curso_id>', methods=['PATCH'])
def actualizar_parcial_curso(curso_id):
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400
        curso = curso_service.actualizar_parcial(curso_id, datos)
        return jsonify(curso), 200
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
    
    
@cursos_bp.route('/cursos/<int:curso_id>', methods=['DELETE'])
def eliminar_curso(curso_id):
    try:
        curso_service.eliminar(curso_id)
        return jsonify({'mensaje': f'Curso {curso_id} eliminado correctamente'}), 200
    except ValueError as e:
        mensaje = str(e).lower()
        if 'no encontrado' in mensaje:
            codigo = 404
        elif 'asociados' in mensaje:
            codigo = 409
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500