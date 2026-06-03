from flask import Blueprint, request, jsonify
from app.services.auth_service import requiere_token
from app.db import get_connection
from app.services.nota_service import (
    crear_nota_servicio,
    modificar_nota_servicio,
    borrar_nota_servicio
)

notas_bp = Blueprint('notas', __name__)

@notas_bp.route('/notas', methods=['GET'])
@requiere_token()
def listar_todas_notas():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT n.nota_id, n.padron, n.evaluacion_id, n.nota, n.observacion, n.fecha_carga,
                   u.nombre AS alumno_nombre, u.apellido AS alumno_apellido,
                   e.nombre AS evaluacion_nombre, e.curso_id, c.nombre AS curso_nombre
            FROM notas n
            JOIN alumnos a ON n.padron = a.padron
            JOIN usuarios u ON a.usuario_id = u.usuario_id
            JOIN evaluaciones e ON n.evaluacion_id = e.evaluacion_id
            JOIN cursos c ON e.curso_id = c.curso_id
            WHERE n.deleted_at IS NULL
            ORDER BY n.fecha_carga DESC
        ''')
        notas = cursor.fetchall() or []
        cursor.close()
        conn.close()
        return jsonify(notas), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notas_bp.route('/notas/grupal', methods=['POST'])
@requiere_token(rol_necesario='docente')
def crear_nota_grupal():
    try:
        datos = request.get_json()
        equipo_id = datos.get('equipo_id')
        evaluacion_id = datos.get('evaluacion_id')
        nota = datos.get('nota')
        observacion = datos.get('observacion')

        if not equipo_id or not evaluacion_id or nota is None:
            return jsonify({'error': 'Faltan datos obligatorios (equipo_id, evaluacion_id, nota)'}), 400

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT padron FROM equipos_alumnos WHERE equipo_id = %s AND deleted_at IS NULL', (equipo_id,))
        alumnos = cursor.fetchall() or []

        if not alumnos:
            cursor.close()
            conn.close()
            return jsonify({'error': 'El equipo no tiene alumnos asociados o no existe.'}), 400

        cargadas = []
        for al in alumnos:
            padron = al['padron']
            cursor.execute('SELECT nota_id FROM notas WHERE padron = %s AND evaluacion_id = %s AND deleted_at IS NULL', (padron, evaluacion_id))
            existente = cursor.fetchone()
            if existente:
                cursor.execute('UPDATE notas SET nota = %s, observacion = %s WHERE nota_id = %s', (nota, observacion, existente['nota_id']))
            else:
                cursor.execute('INSERT INTO notas (padron, evaluacion_id, nota, observacion) VALUES (%s, %s, %s, %s)', (padron, evaluacion_id, nota, observacion))
            cargadas.append(padron)

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'mensaje': f'Nota grupal cargada con éxito a {len(cargadas)} alumnos.', 'padrones': cargadas}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
