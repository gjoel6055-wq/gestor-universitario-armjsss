from app.repositories.log_repository import registrar_log, listar_logs

def registrar_actividad(usuario_id, accion, ip, email):
    return registrar_log(usuario_id, accion, ip, email)

def listar_registro_actividad(accion=None):
    return listar_logs(accion=accion)
