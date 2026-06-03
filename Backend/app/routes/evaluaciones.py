from flask import Blueprint, request, jsonify
from app.services.evaluacion_service import (
    crear_evaluacion_servicio,
    modificar_evaluacion_servicio,
    borrar_evaluacion_servicio
)
from app.services.auth_service import requiere_token

from app.db import get_connection

evaluaciones_bp = Blueprint('evaluaciones', __name__)

@evaluaciones_bp.route('/evaluaciones', methods=['GET'])
@requiere_token()
def listar_evaluaciones():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT e.evaluacion_id, e.tipo_id, e.curso_id, e.nombre, e.fecha, e.peso, e.descripcion,
                   te.nombre AS tipo_nombre, c.nombre AS curso_nombre
            FROM evaluaciones e
            JOIN tipos_evaluacion te ON e.tipo_id = te.tipo_id
            JOIN cursos c ON e.curso_id = c.curso_id
            WHERE e.deleted_at IS NULL
            ORDER BY e.fecha DESC
        ''')
        evaluaciones = cursor.fetchall() or []
        cursor.close()
        conn.close()
        return jsonify(evaluaciones), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@evaluaciones_bp.route('/evaluaciones', methods=['POST'])
@requiere_token()
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
@requiere_token()
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
