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
    tipo_id = datos.get('tipo_id')
    curso_id = datos.get('curso_id')
    nombre = datos.get('nombre')
    fecha = datos.get('fecha')
    peso = datos.get('peso')

    if not tipo_id or not curso_id or not nombre or not fecha or peso is None:
        return jsonify({'error': 'Faltan datos obligatorios (tipo_id, curso_id, nombre, fecha o peso)'}), 400
        
    resultado = crear_evaluacion_servicio(datos) 
    
    if not resultado:
        return jsonify({'error': 'No se pudo crear la evaluación. Verifique los datos ingresados.'}), 400
        
    return jsonify({'mensaje': 'Evaluación creada con éxito.', 'datos': resultado}), 201

@evaluaciones_bp.route('/evaluaciones/<int:id>', methods=['PUT', 'DELETE'])
def gestionar_evaluacion(id):
    if request.method == 'PUT':
        datos = request.get_json()
        tipo_id = datos.get('tipo_id')
        curso_id = datos.get('curso_id')
        nombre = datos.get('nombre')
        fecha = datos.get('fecha')
        peso = datos.get('peso')

        if not tipo_id or not curso_id or not nombre or not fecha or peso is None:
            return jsonify({'error': 'Faltan datos obligatorios para actualizar la evaluación'}), 400

        exito = modificar_evaluacion_servicio(id, datos)
        if not exito:
            return jsonify({'error': f'No se pudo actualizar la evaluación {id}. Puede que esté eliminada o no exista.'}), 404
            
        return jsonify({'mensaje': f'Evaluación {id} actualizada con éxito.'}), 200
        
    if request.method == 'DELETE':
        exito = borrar_evaluacion_servicio(id)
        if not exito:
            return jsonify({'error': f'No se pudo eliminar la evaluación {id}.'}), 400
            
        return jsonify({'mensaje': f'Evaluación {id} eliminada correctamente (borrado logico).'}), 200
