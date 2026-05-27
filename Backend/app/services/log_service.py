from app.repositories.log_repository import registrar_log, listar_logs, buscar_log_especifico

def registrar_actividad(usuario_id, accion, ip):
    if not accion:
        return "no se aclaro la accion"

    if not ip:
        return "no se ingreso una ip"

    estado_registro = registrar_log(usuario_id, accion, ip)

    if estado_registro is True:
        return True

    return "error al guardar el log en la base de datos"


def listar_registro_actividad(accion=None):
    return listar_logs(accion=accion)

def log_por_id(id_log):
    return buscar_log_especifico(id_log)