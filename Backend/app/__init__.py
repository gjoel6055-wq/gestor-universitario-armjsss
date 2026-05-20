from flask import Flask
from app.routes.cursos import cursos_bp
from app.routes.equipos import equipos_bp
from app.routes.docentes import docente_bp
from app.routes.auth import auth_bp
from app.routes.asistencia import asistencia_bp

def create_app():
    app = Flask(__name__)

    app.secret_key = 'una_clave_de_prueba_secreta_y_dificil_ARMJSSS_2026'
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    app.register_blueprint(auth_bp)
    app.register_blueprint(asistencia_bp)
    app.register_blueprint(cursos_bp)
    app.register_blueprint(equipos_bp)
    app.register_blueprint(docente_bp)

    return app