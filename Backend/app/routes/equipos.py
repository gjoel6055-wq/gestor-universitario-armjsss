from flask import Blueprint, request, jsonify
from app.services import equipo_service
from app.services.auth_service import requiere_token
from app.services.log_service import registrar_actividad

equipos_bp = Blueprint('equipos', __name__)


@equipos_bp.route('/equipos', methods=['GET'])
@requiere_token()
def obtener_equipos():
    try:
        curso_id = request.args.get('curso_id', type=int)
        equipos = equipo_service.obtener_todos(curso_id)
        return jsonify(equipos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipos_bp.route('/equipos/<int:equipo_id>', methods=['GET'])
@requiere_token()
def obtener_equipo(equipo_id):
    try:
        equipo = equipo_service.obtener_por_id(equipo_id)
        return jsonify(equipo), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipos_bp.route('/equipos', methods=['POST'])
@requiere_token(rol_necesario='docente')
def crear_equipo():
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400
        equipo = equipo_service.crear(datos)

        ip_usuario    = request.remote_addr
        usuario_id    = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        accion        = "Creó un nuevo equipo"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify(equipo), 201
    except ValueError as e:
        mensaje = str(e).lower()
        if 'ya existe' in mensaje:
            codigo = 409
        elif 'no existe' in mensaje:
            codigo = 404
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipos_bp.route('/equipos/<int:equipo_id>', methods=['PUT'])
@requiere_token(rol_necesario='docente')
def actualizar_equipo(equipo_id):
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400
        equipo = equipo_service.actualizar(equipo_id, datos)

        ip_usuario    = request.remote_addr
        usuario_id    = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        accion        = f"Actualizó por completo el equipo de ID: {equipo_id}"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify(equipo), 200
    except ValueError as e:
        mensaje = str(e).lower()
        if 'no encontrado' in mensaje:
            codigo = 404
        elif 'ya existe' in mensaje:
            codigo = 409
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipos_bp.route('/equipos/<int:equipo_id>', methods=['DELETE'])
@requiere_token(rol_necesario='docente')
def eliminar_equipo(equipo_id):
    try:
        equipo_service.eliminar(equipo_id)

        ip_usuario    = request.remote_addr
        usuario_id    = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        accion        = f"Eliminó el equipo ID: {equipo_id}"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify({'mensaje': f'Equipo {equipo_id} eliminado correctamente'}), 200
    except ValueError as e:
        mensaje = str(e).lower()
        if 'no encontrado' in mensaje:
            codigo = 404
        elif 'asociadas' in mensaje:
            codigo = 409
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipos_bp.route('/equipos/<int:equipo_id>/alumnos', methods=['POST'])
@requiere_token(rol_necesario='docente')
def agregar_alumno(equipo_id):
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400
        resultado = equipo_service.agregar_alumno(equipo_id, datos)

        ip_usuario    = request.remote_addr
        usuario_id    = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        padron        = datos.get('padron')
        accion        = f"Registró al alumno {padron} en el equipo {equipo_id}"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify(resultado), 201
    except ValueError as e:
        mensaje = str(e).lower()
        if 'no encontrado' in mensaje or 'no existe' in mensaje:
            codigo = 404
        elif 'ya pertenece' in mensaje:
            codigo = 409
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipos_bp.route('/equipos/<int:equipo_id>/alumnos/<int:padron>', methods=['DELETE'])
@requiere_token(rol_necesario='docente')
def quitar_alumno(equipo_id, padron):
    try:
        equipo_service.quitar_alumno(equipo_id, padron)

        # CORRECCIÓN #4: registrar_actividad faltaba en esta ruta pivot.
        ip_usuario    = request.remote_addr
        usuario_id    = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        accion        = f"Eliminó al alumno {padron} del equipo {equipo_id}"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify({'mensaje': f'Alumno {padron} quitado del equipo {equipo_id}'}), 200
    except ValueError as e:
        mensaje = str(e).lower()
        if 'no encontrado' in mensaje or 'no pertenece' in mensaje:
            codigo = 404
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipos_bp.route('/equipos/<int:equipo_id>/evaluaciones', methods=['POST'])
@requiere_token(rol_necesario='docente')
def agregar_evaluacion(equipo_id):
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400
        resultado = equipo_service.agregar_evaluacion(equipo_id, datos)

        ip_usuario    = request.remote_addr
        usuario_id    = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        evaluacion_id = datos.get('evaluacion_id')
        accion        = f"Registró la evaluación {evaluacion_id} en el equipo {equipo_id}"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify(resultado), 201
    except ValueError as e:
        mensaje = str(e).lower()
        if 'no encontrado' in mensaje or 'no existe' in mensaje:
            codigo = 404
        elif 'ya está asociada' in mensaje:
            codigo = 409
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipos_bp.route('/equipos/<int:equipo_id>', methods=['PATCH'])
@requiere_token(rol_necesario='docente')
def actualizar_parcial_equipo(equipo_id):
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({'error': 'El cuerpo de la solicitud no puede estar vacío'}), 400
        equipo = equipo_service.actualizar_parcial(equipo_id, datos)

        ip_usuario    = request.remote_addr
        usuario_id    = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        accion        = f"Modificó parcialmente el equipo ID: {equipo_id}"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify(equipo), 200
    except ValueError as e:
        mensaje = str(e).lower()
        if 'no encontrado' in mensaje:
            codigo = 404
        elif 'ya existe' in mensaje:
            codigo = 409
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@equipos_bp.route('/equipos/<int:equipo_id>/evaluaciones/<int:evaluacion_id>', methods=['DELETE'])
@requiere_token(rol_necesario='docente')
def quitar_evaluacion(equipo_id, evaluacion_id):
    try:
        equipo_service.quitar_evaluacion(equipo_id, evaluacion_id)

        ip_usuario    = request.remote_addr
        usuario_id    = getattr(request, 'usuario_id', None)
        email_usuario = getattr(request, 'email_usuario', None)
        accion        = f"Eliminó la evaluación {evaluacion_id} del equipo {equipo_id}"
        registrar_actividad(usuario_id, accion, ip_usuario, email_usuario)

        return jsonify({'mensaje': f'Evaluación {evaluacion_id} quitada del equipo {equipo_id}'}), 200
    except ValueError as e:
        mensaje = str(e).lower()
        if 'no encontrado' in mensaje or 'no está asociada' in mensaje:
            codigo = 404
        else:
            codigo = 400
        return jsonify({'error': str(e)}), codigo
    except Exception as e:
        return jsonify({'error': str(e)}), 500