from flask import Flask
from app.routes.cursos import cursos_bp
from app.routes.equipos import equipos_bp
from app.routes.docentes import docente_bp
from app.routes.auth import auth_bp
from app.routes.asistencia import asistencia_bp
from app.routes.alumnos import alumnos_bp
from app.routes.dashboard import dashboard_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth_bp)
    app.register_blueprint(asistencia_bp)
    app.register_blueprint(cursos_bp)
    app.register_blueprint(equipos_bp)
    app.register_blueprint(docente_bp)
    app.register_blueprint(alumnos_bp)
    app.register_blueprint(dashboard_bp)

    return app