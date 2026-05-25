from datetime import datetime
from app.db import get_connection

def guardar_nota_bd(datos):
    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        
        query = "INSERT INTO notas (padron, evaluacion_id, nota, observacion) VALUES (%s, %s, %s, %s)"
        valores = (datos.get('padron'), datos.get('evaluacion_id'), datos.get('nota'), datos.get('observacion'))
        
        cursor.execute(query, valores)
        conexion.commit()
        cursor.close()
        conexion.close()
        return datos
    except Exception:
        return None

def modificar_nota_bd(id, datos):
    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        
        query = """
            UPDATE notas 
            SET padron = %s, evaluacion_id = %s, nota = %s, observacion = %s 
            WHERE nota_id = %s AND deleted_at IS NULL
        """
        valores = (datos.get('padron'), datos.get('evaluacion_id'), datos.get('nota'), datos.get('observacion'), id)
        
        cursor.execute(query, valores)
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception:
        return False

def borrar_nota_bd(id):
    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        
        fecha_actual = datetime.now()
        query = "UPDATE notas SET deleted_at = %s WHERE nota_id = %s"
        
        cursor.execute(query, (fecha_actual, id))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception:
        return False
