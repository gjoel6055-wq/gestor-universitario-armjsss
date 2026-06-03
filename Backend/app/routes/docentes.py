from flask import Blueprint, request, jsonify
from app.services.docente_service import (
    listar_docentes,
    registrar_docente,
    borrar_docente
)
from services.log_service import registrar_log
from services.auth_service import requiere_token

docente_bp = Blueprint('docente', __name__)


@docente_bp.route('/docentes', methods=['GET'])
@requiere_token()
def obtener_todos_los_docentes():
    try:
        lista = listar_docentes()
        return jsonify(lista), 200
    except Exception as e:
        return jsonify({'error': 'Error interno al obtener la lista de docentes'}), 500


@docente_bp.route('/docentes', methods=['POST'])
@requiere_token(rol_necesario='admin')
def agregar_docente():
    datos = request.get_json()
    legajo = datos.get('legajo')
    usuario_id = datos.get('usuario_id')
    departamento = datos.get('departamento', '')

    if not legajo or not usuario_id:
        return jsonify({'error': 'El legajo y el usuario_id son obligatorios'}), 400

    try:
        nuevo_legajo = registrar_docente(legajo, usuario_id, departamento)

        ip_cliente = request.remote_addr
        usuario_actual = request.usuario_id

        accion = f"Registró al docente con legajo {legajo} (Asociado al Usuario ID: {usuario_id})"
        registrar_log(usuario_actual, accion, ip_cliente)

        return jsonify({
            'mensaje': 'Docente registrado exitosamente',
            'legajo': nuevo_legajo
        }), 201
    except Exception as e:
        return jsonify({'error': 'Error interno en la base de datos (verifique que el usuario_id exista)'}), 500


@docente_bp.route('/docentes/<int:legajo>', methods=['DELETE'])
@requiere_token(rol_necesario='admin')
def eliminar_docente(legajo):
    try:
        eliminado = borrar_docente(legajo)
        if eliminado:
            ip_cliente = request.remote_addr
            usuario_actual = request.usuario_id

            accion = f"Dio de baja al docente con legajo: {legajo}"
            registrar_log(usuario_actual, accion, ip_cliente)

            return jsonify({'mensaje': f'Docente con legajo {legajo} dado de baja correctamente'}), 200
        return jsonify({'error': 'Docente no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': 'Error interno al intentar eliminar al docente'}), 500