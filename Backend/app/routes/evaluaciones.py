from flask import Blueprint, request, jsonify
from app.services.evaluacion_service import (
     crear_evaluacion_servicio,
     modificar_evaluacion_servicio,
     borrar_evaluacion_servicio
)

evaluaciones_bp = Blueprint('evaluaciones', __name__)

@evaluaciones_bp.route('/evaluaciones', methods=['POST'])
def crear_evaluacion():
    datos = request.get_json()
    id_tipo = datos.get('id_tipo')
    fecha = datos.get('fecha')
    id_curso = datos.get ('id_curso')

    if not id_tipo or not fecha or not id_curso:
        return jsonify({'error':'Faltan datos obligatorios'}), 400
        
    resultado = crear_evaluacion_servicio (datos) 
    return jsonify({'mensaje': 'Evaluación programada con éxito.', 'datos': resultado}), 201

@evaluaciones_bp.route('/evaluaciones/<int:id>', methods=['PUT', 'DELETE'])
def gestionar_evaluacion(id):
    if request.method == 'PUT':
        datos = request.get_json()
        modificar_evaluacion_servicio (id, datos)
        return jsonify({'mensaje': f'Evaluación {id} actualizada con éxito.'}), 200
        
    if request.method == 'DELETE':
        borrar_evaluacion_servicio (id)
        return jsonify({'mensaje': f'Evaluación {id} eliminada correctamente.'}), 200
