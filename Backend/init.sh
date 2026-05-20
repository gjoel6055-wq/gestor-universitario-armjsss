from flask import Flask
from app.routers.material_routes import material_bp # Importas tu blueprint

app = Flask(__name__)

app.register_blueprint(material_bp)

if __name__ == '__main__':
    app.run(debug=True)