from app.repositories.nota_repository import (
    guardar_nota_bd,
    modificar_nota_bd,
    borrar_nota_bd,
    listar_todas_notas,
    cargar_notas_grupal,
)

def crear_nota_servicio(datos):
    return guardar_nota_bd(datos)

def modificar_nota_servicio(id, datos):
    return modificar_nota_bd(id, datos)

def borrar_nota_servicio(id):
    return borrar_nota_bd(id)

def listar_todas_notas_servicio():
    return listar_todas_notas()

def cargar_nota_grupal_servicio(datos):
    equipo_id = datos.get('equipo_id')
    evaluacion_id = datos.get('evaluacion_id')
    nota = datos.get('nota')
    observacion = datos.get('observacion')

    if not equipo_id or not evaluacion_id or nota is None:
        return None

    return cargar_notas_grupal(equipo_id, evaluacion_id, nota, observacion)
