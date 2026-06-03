from flask import request, Blueprint, jsonify
from app.services.log_service import listar_registro_actividad, log_por_id
from app.services.auth_service import requiere_token

log_bp = Blueprint("log", __name__)

@log_bp.route('/historial_logs')
@requiere_token(rol_necesario='docente')
def listar_logs():
    filtro_accion = request.args.get('accion')

    historial = listar_registro_actividad(accion=filtro_accion)

    if historial is False:
        return jsonify({'error': 'No se pudo acceder al historial de actividad.'}), 500

    return jsonify({'historial': historial}), 200

@log_bp.route('/logs/<int:id_log>')
@requiere_token(rol_necesario='docente')
def buscar_log(id_log):
    log_buscado = log_por_id(id_log)

    if log_buscado == "no existe log con ese id":
        return jsonify({'error':"No se encontró un log con ese id."}), 404

    return  jsonify({"log": log_buscado}), 200
