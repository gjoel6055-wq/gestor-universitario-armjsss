def guardar_evaluacion_bd(id_tipo, fecha, id_curso):
    print(f"Base de Datos: Guardando evaluacion tipo {id_tipo} para curso {id_curso} el {fecha}")
    return {"id": 100, "id_tipo": id_tipo, "fecha": fecha, "id_curso": id_curso}

def actualizar_evaluacion_bd(id_evaluacion, fecha, id_tipo):
    print(f"Base de Datos: Modificando evaluacion ID {id_evaluacion}")
    return True

def eliminar_evaluacion_bd(id_evaluacion):
    print(f"Base de Datos: Borrando de la tabla la evaluacion ID {id_evaluacion}")
    return True
