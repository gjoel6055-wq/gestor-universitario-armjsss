def guardar_evaluacion_bd(datos):
    print(f"Base de Datos: Guardando evaluación... {datos}")
    datos_guardados = datos.copy()
    datos_guardados['id'] = 1  # ID simulado
    return datos_guardados

def modificar_evaluacion_bd(id, datos):
    print(f"Base de Datos: Modificando evaluación con ID {id}")
    if id > 500:
        return False
    return True

def borrar_evaluacion_bd(id):
    print(f"Base de Datos: Eliminando evaluación con ID {id}")
    if id > 500:
        return False
    return True
