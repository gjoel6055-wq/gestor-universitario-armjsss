from flask import Blueprint, request, jsonify

tipos_evaluacion_bp = Blueprint('tipos_evaluacion', __name__)

@tipos_evaluacion_bp.route('/tipos-evaluacion', methods=['POST'])
def crear_tipo_evaluacion():
    datos = request.get_json()
    nombre = datos.get('nombre') # Ej: "Primer Parcial"
    
    if not nombre:
        return jsonify({'error': 'El nombre del tipo de evaluación es requerido.'}), 400
        
    return jsonify({'mensaje': f'Tipo de evaluación "{nombre}" creado con éxito.'}), 201
