from flask import request, Blueprint, jsonify
from app.services.log_service import listar_registro_actividad
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
