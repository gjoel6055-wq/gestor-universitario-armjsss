from app.repositories.asistencia_repository import crear_nueva_asistencia, registrar_asistencia
import hashlib
import qrcode
import datetime
import io

def procesar_escaneo_qr(qr_token):
    return registrar_asistencia(qr_token)

def generar_qr_para_asistencia(padron, fecha_clase, duracion_qr=30):

    if isinstance(fecha_clase, (datetime.date, datetime.datetime)):
        fecha_str = fecha_clase.strftime('%Y-%m-%d')
    else:
        fecha_str = str(fecha_clase)

    estructura_base = f"asistencia_{padron}_{fecha_str}"

    qr_token = hashlib.md5(estructura_base.encode('utf-8')).hexdigest()

    expiracion_qr = datetime.datetime.now() + datetime.timedelta(minutes=duracion_qr)

    estado_creacion = crear_nueva_asistencia(padron, fecha_str, qr_token, expiracion_qr)

    if estado_creacion == None:
        return None

    url_registro_asistencia = f"http://localhost:8080/asistencia/validar/{qr_token}"

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url_registro_asistencia)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    return {
        "qr_token": qr_token,
        "qr_imagen_bytes": img_buffer
    }
