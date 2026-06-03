from flask import Blueprint, jsonify
from services.dashboard_service import obtener_estadisticas_dashboard


dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/estadisticas', methods=['GET'])
def estadisticas_dashboard():
    estadisticas = obtener_estadisticas_dashboard()
    return jsonify(estadisticas), 200
