from flask import Blueprint, request, jsonify
from app.services.material_service import registrar_nuevo_material

material_bp = Blueprint('material', __name__)

@material_bp.route('/materiales', methods=['POST'])
def agregar_material():
    datos = request.get_json()
    
    titulo = datos.get('titulo')
    descripcion = datos.get('descripcion')
    url = datos.get('url')        
    curso_id = datos.get('cursoId') 
    
    if not titulo or not curso_id:
        return jsonify({'error': 'El título y el ID del curso son obligatorios'}), 400
        
    try:
        nuevo_id = registrar_nuevo_material(titulo, descripcion, url, curso_id)
        
        return jsonify({
            'mensaje': 'Se ha registrado el material de estudio con éxito.',
            'id': nuevo_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Error interno en la base de datos'}), 500