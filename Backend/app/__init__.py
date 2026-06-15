import os
import logging
from flask import Flask
from .extensions import mail
from dotenv import load_dotenv
from .routes.cursos import cursos_bp
from .routes.equipos import equipos_bp
from .routes.docentes import docente_bp
from .routes.auth import auth_bp
from .routes.asistencia import asistencia_bp
from .routes.alumnos import alumnos_bp
from .routes.dashboard import dashboard_bp
from .routes.log import log_bp
from .routes.notas import notas_bp
from .routes.evaluaciones import evaluaciones_bp
from .routes.tipos_evaluacion import tipos_evaluacion_bp

def create_app():
    app = Flask(__name__)
    load_dotenv()

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('EMAIL_SENDER')
    app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')


    mail.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(asistencia_bp)
    app.register_blueprint(cursos_bp)
    app.register_blueprint(equipos_bp)
    app.register_blueprint(docente_bp)
    app.register_blueprint(alumnos_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(log_bp)
    app.register_blueprint(notas_bp)
    app.register_blueprint(evaluaciones_bp)
    app.register_blueprint(tipos_evaluacion_bp)


    return app