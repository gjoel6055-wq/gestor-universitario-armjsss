from flask import Flask
from app.routes.cursos import cursos_bp
from app.routes.equipos import equipos_bp
from app.routes.docentes import docente_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(cursos_bp)
    app.register_blueprint(equipos_bp)
    app.register_blueprint(docente_bp)

    return app