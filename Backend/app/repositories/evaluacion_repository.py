from datetime import datetime
from app.db import get_connection

def guardar_evaluacion_bd(datos):
    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        
        query = """
            INSERT INTO evaluaciones (tipo_id, curso_id, nombre, fecha, peso, descripcion) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (
            datos.get('tipo_id'), 
            datos.get('curso_id'), 
            datos.get('nombre'), 
            datos.get('fecha'), 
            datos.get('peso'), 
            datos.get('descripcion')
        )
        
        cursor.execute(query, valores)
        conexion.commit()
        cursor.close()
        conexion.close()
        return datos
    except Exception:
        return None

def modificar_evaluacion_bd(id, datos):
    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        
        query = """
            UPDATE evaluaciones 
            SET tipo_id = %s, curso_id = %s, nombre = %s, fecha = %s, peso = %s, descripcion = %s 
            WHERE evaluacion_id = %s AND deleted_at IS NULL
        """
        valores = (
            datos.get('tipo_id'), 
            datos.get('curso_id'), 
            datos.get('nombre'), 
            datos.get('fecha'), 
            datos.get('peso'), 
            datos.get('descripcion'),
            id
        )
        
        cursor.execute(query, valores)
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception:
        return False

def borrar_evaluacion_bd(id):
    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        
        fecha_actual = datetime.now()
        query = "UPDATE evaluaciones SET deleted_at = %s WHERE evaluacion_id = %s"
        
        cursor.execute(query, (fecha_actual, id))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception:
        return False
