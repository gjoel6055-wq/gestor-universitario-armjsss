from app.repositories.material_repository import crear_material_db
from flask import Blueprint, request, jsonify

material_bp = Blueprint('material', __name__)

@material_bp.route('/materiales', methods=['POST'])
def agregar_material():
    datos = request.get_json()
    
    titulo = datos.get('titulo')
    descripcion = datos.get('descripcion')
    url_archivo = datos.get('url_archivo')
    curso_id = datos.get('curso_id')
    
    if not titulo or not curso_id:
        return jsonify({'error': 'El título y el ID del curso son obligatorios'}), 400
        
    try:
        nuevo_id = crear_material_db(titulo, descripcion, url_archivo, curso_id)
        
        return jsonify({
            'mensaje': 'Se ha registrado el material de estudio con éxito.',
            'id': nuevo_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Error interno en la base de datos'}), 500