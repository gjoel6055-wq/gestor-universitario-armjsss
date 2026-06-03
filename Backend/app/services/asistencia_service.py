from app.services.qr_service import generar_qr_para_asistencia
from app.services.mail_service import enviar_email_con_qr
from app.repositories.asistencia_repository import obtener_alumnos_curso, obtener_asistencias_por_fecha, registrar_asistencia
from datetime import datetime

def procesar_envio_masivo_asistencia(lista_alumnos):
    fecha_hoy = datetime.now().date()
    resultados = {"exito": 0, "fallo": 0}

    for alumno in lista_alumnos:
        datos_qr = generar_qr_para_asistencia(alumno['padron'], fecha_hoy)

        if datos_qr and datos_qr.get("qr_imagen_bytes"):
            qr_bytes = datos_qr["qr_imagen_bytes"]

            enviado = enviar_email_con_qr(
                email_destino=alumno['email'],
                nombre_alumno=alumno['nombre'],
                qr_bytes=qr_bytes
            )

            if enviado:
                resultados["exito"] += 1
            else:
                resultados["fallo"] += 1
        else:
            print(f"Error generando QR para {alumno['padron']}")
            resultados["fallo"] += 1

    return resultados

def obtener_alumnos_por_curso():
    return obtener_alumnos_curso()


def alumnos_asistencia_fecha(fecha_str):
    if fecha_str:
        try:
            fecha_consulta = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            fecha_consulta = datetime.now().date()
    else:
        fecha_consulta = datetime.now().date()

    alumnos = obtener_asistencias_por_fecha(fecha_consulta)

    if alumnos is None:
        return []

    for alumno in alumnos:
        if alumno['presente'] is None:
            alumno['presente'] = 0

    return alumnos
