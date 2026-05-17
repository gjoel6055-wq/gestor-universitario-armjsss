from app.repositories.asistencia_repository import registrar_asistencia
from flask import Blueprint, request, jsonify

asistencia_bp = Blueprint('asistencia', __name__)

@asistencia_bp.route('/asistencia/validar/<string:token>', methods=['POST'])
def validar_asistencia(token):
    situacion = registrar_asistencia(token)

    if situacion == 'QR invalido':
        return jsonify({'error':'El qr escaneado es invalido'}), 404

    if situacion == 'token expirado':
        return jsonify({'error':'El codigo escaneado ya expiró, pruebe con un codigo vigente'}), 400

    if situacion == True:
        return jsonify({'mensaje':'Se ha registrado su asistencia con exito.'}), 201

    return jsonify({'error':'Ha ocurrido un error al registrar su asistencia, intentelo otra vez.'}), 500
