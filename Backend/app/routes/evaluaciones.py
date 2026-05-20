from flask import Blueprint, request, jsonify

evaluaciones_bp = Blueprint('evaluaciones', __name__)

@evaluaciones_bp.route('/evaluaciones', methods=['POST'])
def crear_evaluacion():
    datos = request.get_json()
    id_tipo = datos.get('id_tipo')
    fecha = datos.get('fecha')
    
    
    return jsonify({'mensaje': 'Evaluación programada con éxito.'}), 201

@evaluaciones_bp.route('/evaluaciones/<int:id>', methods=['PUT', 'DELETE'])
def gestionar_evaluacion(id):
    if request.method == 'PUT':
        datos = request.get_json()
        return jsonify({'mensaje': f'Evaluación {id} actualizada con éxito.'}), 200
        
    if request.method == 'DELETE':
        return jsonify({'mensaje': f'Evaluación {id} eliminada correctamente.'}), 200
