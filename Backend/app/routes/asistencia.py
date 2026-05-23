from app.services.qr_service import procesar_escaneo_qr
from flask import Blueprint, request, jsonify
from app.services.auth_service import requiere_token

asistencia_bp = Blueprint('asistencia', __name__)

@asistencia_bp.route('/asistencia/validar/<string:token>', methods=['POST'])
@requiere_token()
def validar_asistencia(token):

    situacion = procesar_escaneo_qr(token)

    if situacion == 'QR invalido':
        return jsonify({'error':'El qr escaneado es invalido'}), 404

    if situacion == 'token expirado':
        return jsonify({'error':'El codigo escaneado ya expiró, pruebe con un codigo vigente'}), 410

    if situacion == True:
        return jsonify({'mensaje':'Se ha registrado su asistencia con exito.'}), 201

    return jsonify({'error':'Ha ocurrido un error al registrar su asistencia, intentelo otra vez.'}), 500
