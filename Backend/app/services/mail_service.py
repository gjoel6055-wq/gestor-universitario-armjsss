import os
from flask_mail import Message
from flask import render_template
from app.extensions import mail
from datetime import datetime

def enviar_email_con_qr(email_destino, nombre_alumno, qr_bytes):
    fecha_clase = datetime.now().strftime('%Y-%m-%d')
    try:
        msg = Message("Tu QR de asistencia - FIUBA",
                      sender=os.getenv("EMAIL_SENDER"),
                      recipients=[email_destino])

        msg.body = f"Hola {nombre_alumno}, en este email se ha adjuntado tu código QR para marcar tu asistencia."

        msg.html = render_template('emails/asistencia_email.html',
                                   nombre=nombre_alumno,
                                   fecha=fecha_clase,
                                   url_qr="cid:qrcode")

        msg.attach(
            filename="asistencia.png",
            content_type="image/png",
            data=qr_bytes.getvalue(),
            headers={
                'Content-ID': '<qrcode>',
                'Content-Disposition': 'inline'
            }
        )

        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error con Flask-Mail: {e}")
        return False