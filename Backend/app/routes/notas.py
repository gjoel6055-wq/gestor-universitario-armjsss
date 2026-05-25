from flask import Blueprint, request, jsonify
from app.services.nota_service import (
    crear_nota_servicio,
    modificar_nota_servicio,
    borrar_nota_servicio
)

notas_bp = Blueprint('notas', __name__)

@notas_bp.route('/notas', methods=['POST'])
def crear_nota():
    datos = request.get_json()
    padron = datos.get('padron')
    evaluacion_id = datos.get('evaluacion_id')
    nota = datos.get('nota')

    if not padron or not evaluacion_id or nota is None:
        return jsonify({'error': 'Faltan datos obligatorios (padron, evaluacion_id o nota)'}), 400
        
    resultado = crear_nota_servicio(datos) 
    if not resultado:
        return jsonify({'error': 'No se pudo cargar la nota. Verifique que el padron y la evaluacion existan.'}), 400
        
    return jsonify({'mensaje': 'Nota cargada con éxito.', 'datos': resultado}), 201

@notas_bp.route('/notas/<int:id>', methods=['PUT', 'DELETE'])
def gestionar_nota(id):
    if request.method == 'PUT':
        datos = request.get_json()
        padron = datos.get('padron')
        evaluacion_id = datos.get('evaluacion_id')
        nota = datos.get('nota')

        if not padron or not evaluacion_id or nota is None:
            return jsonify({'error': 'Faltan datos obligatorios para actualizar la nota'}), 400

        exito = modificar_nota_servicio(id, datos)
        if not exito:
            return jsonify({'error': f'No se pudo actualizar la nota {id}. Puede que no exista o esté eliminada.'}), 404
            
        return jsonify({'mensaje': f'Nota {id} actualizada con éxito.'}), 200
        
    if request.method == 'DELETE':
        exito = borrar_nota_servicio(id)
        if not exito:
            return jsonify({'error': f'No se pudo eliminar la nota {id}.'}), 400
            
        return jsonify({'mensaje': f'Nota {id} eliminada correctamente (borrado logico).'}), 200
