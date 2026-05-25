from flask import Blueprint, request, jsonify
from app.services.tipo_evaluacion_service import (
    crear_tipo_servicio,
    modificar_tipo_servicio,
    borrar_tipo_servicio
)

tipos_evaluacion_bp = Blueprint('tipos_evaluacion', __name__)

@tipos_evaluacion_bp.route('/tipos_evaluacion', methods=['POST'])
def crear_tipo():
    datos = request.get_json()
    nombre = datos.get('nombre')

    if not nombre:
        return jsonify({'error': 'El nombre del tipo de evaluación es obligatorio'}), 400
        
    resultado = crear_tipo_servicio(datos) 
    if not resultado:
        return jsonify({'error': 'No se pudo crear el tipo de evaluación.'}), 400
        
    return jsonify({'mensaje': 'Tipo de evaluación creado con éxito.', 'datos': resultado}), 201

@tipos_evaluacion_bp.route('/tipos_evaluacion/<int:id>', methods=['PUT', 'DELETE'])
def gestionar_tipo(id):
    if request.method == 'PUT':
        datos = request.get_json()
        nombre = datos.get('nombre')

        if not nombre:
            return jsonify({'error': 'El nombre es obligatorio para actualizar'}), 400

        exito = modificar_tipo_servicio(id, datos)
        if not exito:
            return jsonify({'error': f'No se encontró el tipo de evaluación {id} o está eliminado.'}), 404
            
        return jsonify({'mensaje': f'Tipo de evaluación {id} actualizado con éxito.'}), 200
        
    if request.method == 'DELETE':
        exito = borrar_tipo_servicio(id)
        if not exito:
            return jsonify({'error': f'No se pudo eliminar el tipo de evaluación {id}.'}), 400
            
        return jsonify({'mensaje': f'Tipo de evaluación {id} eliminado correctamente (borrado logico).'}), 200
