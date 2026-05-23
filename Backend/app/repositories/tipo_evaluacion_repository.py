def guardar_tipo_bd(datos):
    print(f"Base de Datos: Guardando tipo de evaluación... {datos}")
    datos_guardados = datos.copy()
    datos_guardados['id'] = 1  
    return datos_guardados

def modificar_tipo_bd(id, datos):
    print(f"Base de Datos: Modificando tipo de evaluación con ID {id}")
    if id > 500:
        return False
    return True

def borrar_tipo_bd(id):
    print(f"Base de Datos: Eliminando tipo de evaluación con ID {id}")
    if id > 500:
        return False
    return True
