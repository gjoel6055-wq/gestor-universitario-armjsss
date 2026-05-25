from datetime import datetime
from app.db import get_connection

def guardar_tipo_bd(datos):
    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        
        query = "INSERT INTO tipos_evaluacion (nombre, descripcion) VALUES (%s, %s)"
        valores = (datos.get('nombre'), datos.get('descripcion'))
        
        cursor.execute(query, valores)
        conexion.commit()
        cursor.close()
        conexion.close()
        return datos
    except Exception:
        return None

def modificar_tipo_bd(id, datos):
    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        
        query = "UPDATE tipos_evaluacion SET nombre = %s, descripcion = %s WHERE tipo_id = %s AND deleted_at IS NULL"
        valores = (datos.get('nombre'), datos.get('descripcion'), id)
        
        cursor.execute(query, valores)
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception:
        return False

def borrar_tipo_bd(id):
    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        
        fecha_actual = datetime.now()
        query = "UPDATE tipos_evaluacion SET deleted_at = %s WHERE tipo_id = %s"
        
        cursor.execute(query, (fecha_actual, id))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception:
        return False
