from flask import Blueprint, request, jsonify
from app.services.material_service import (
    registrar_nuevo_material,
    listar_materiales,
    modificar_material,
    eliminar_material
)
from services.auth_service import requiere_token

material_bp = Blueprint('material', __name__)

@material_bp.route('/materiales', methods=['POST'])
@requiere_token()
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
        return jsonify({'mensaje': 'Se ha registrado el material de estudio con éxito.', 'id': nuevo_id}), 201
    except Exception as e:
        return jsonify({'error': 'Error interno en la base de datos'}), 500

@material_bp.route('/materiales', methods=['GET'])
@requiere_token()
def obtener_todos_los_materiales():
    try:
        lista = listar_materiales()
        return jsonify(lista), 200
    except Exception as e:
        return jsonify({'error': 'Error al obtener los materiales de estudio'}), 500

@material_bp.route('/materiales/<int:id>', methods=['PUT'])
@requiere_token()
def actualizar_material(id):
    datos = request.get_json()
    titulo = datos.get('titulo')
    descripcion = datos.get('descripcion')
    url = datos.get('url')
    curso_id = datos.get('cursoId')
    
    if not titulo or not curso_id:
        return jsonify({'error': 'El título y el ID del curso son obligatorios'}), 400
        
    try:
        actualizado = modificar_material(id, titulo, descripcion, url, curso_id)
        if actualizado:
            return jsonify({'id': id, 'titulo': titulo, 'descripcion': descripcion, 'url': url, 'cursoId': curso_id}), 200
        return jsonify({'error': 'Material no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': 'Error interno al actualizar el material'}), 500

@material_bp.route('/materiales/<int:id>', methods=['DELETE'])
@requiere_token()
def borrar_material(id):
    try:
        eliminado = eliminar_material(id)
        if eliminado:
            return jsonify({'mensaje': f'Material con ID {id} eliminado correctamente (lógico)'}), 200
        return jsonify({'error': 'Material no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': 'Error interno al eliminar el material'}), 500