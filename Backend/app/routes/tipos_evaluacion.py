from flask import Blueprint, request, jsonify
from app.services.tipo_evaluacion_service import (
     crear_tipo_servicio,
     modificar_tipo_servicio,
     borrar_tipo_servicio
)
from app.services.auth_service import requiere_token

tipos_evaluacion_bp = Blueprint('tipos_evaluacion', __name__)

@tipos_evaluacion_bp.route('/tipos-evaluacion', methods=['POST'])
@requiere_token()
def crear_tipo_evaluacion():
    datos = request.get_json()
    nombre = datos.get('nombre')
    
    if not nombre:
        return jsonify({'error': 'El campo nombre es obligatorio'}), 400

    resultado = crear_tipo_servicio(datos)
    return jsonify({'mensaje': 'Tipo de evaluación creado con éxito.','datos': resultado}), 201 

@tipos_evaluacion_bp.route('/tipos-evaluacion/<int:id>', methods=['PUT', 'DELETE'])
@requiere_token()
def gestionar_tipo_evaluacion(id):
    if request.method == 'PUT':
        datos = request.get_json()
        nombre = datos.get('nombre')

        if not nombre:
            return jsonify ({'error': 'El campo nombre es obligatorio para actualizar'}), 400

        encontrado = modificar_tipo_servicio(id,datos)
        if not encontrado:
            return jsonify ({'error': f'No se encontró el tipo de evaluación con ID {id}'}), 404

        return jsonify ({'mensaje': f'Tipo de evaluación {id} actualizada con éxito.'}), 200

    if request.method == 'DELETE':
        encontrado=borrar_tipo_servicio(id)
        if not encontrado:
            return jsonify({'error': f'No se encontró el tipo de evaluación con ID {id}'}), 404

        return jsonify({'mensaje': f'Tipo de evaluación {id} eliminado correctamente'}), 200
