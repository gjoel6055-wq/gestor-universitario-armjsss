from app.services.qr_service import procesar_escaneo_qr
from flask import Blueprint, request, jsonify
from app.services.auth_service import requiere_token
from app.services.asistencia_service import procesar_envio_masivo_asistencia, obtener_alumnos_por_curso, alumnos_asistencia_fecha

asistencia_bp = Blueprint('asistencia', __name__)

@asistencia_bp.route('/asistencia/validar-qr/<string:token>', methods=['POST'])
@requiere_token()
def validar_asistencia(token):

    situacion = procesar_escaneo_qr(token)

    if situacion == 'QR invalido':
        return jsonify({'error':'El qr escaneado es invalido'}), 404

    if situacion == 'token expirado':
        return jsonify({'error':'El codigo escaneado ya expiró, pruebe con un codigo vigente'}), 410

    if situacion == 'ya presente':
        return jsonify({'mensaje': 'Tu asistencia ya fue registrada previamente.'}), 200

    if situacion == True:
        return jsonify({'mensaje':'Se ha registrado su asistencia con exito.'}), 201

    return jsonify({'error':'Ha ocurrido un error al registrar su asistencia, intentelo otra vez.'}), 500


@asistencia_bp.route('/enviar_mails_asistencia', methods=['POST'])
@requiere_token(rol_necesario='docente')
def enviar_qr_curso():
    alumnos = obtener_alumnos_por_curso()

    if alumnos is None:
        return jsonify({"error":'No se pudo realizar el envio de emails'}), 400

    stats = procesar_envio_masivo_asistencia(alumnos)

    return jsonify({"mensaje": "Proceso finalizado", "detalles": stats}), 201



@asistencia_bp.route('/asistencias_curso', methods=['GET'])
@requiere_token(rol_necesario='docente')
def asistencias_estudiantes_curso():
    fecha = request.args.get('fecha')

    lista_asistencias_fecha_buscada = alumnos_asistencia_fecha(fecha)

    return jsonify({'mensaje':'se a devuelto la lista de asistencia con exito',
                    'lista_alumnos':lista_asistencias_fecha_buscada}),200



