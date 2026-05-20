from app.db import get_connection 

def obtener_docentes_db():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True) 
    
    try:
        query = """
            SELECT d.legajo, d.departamento, u.nombre, u.apellido, u.email 
            FROM docentes d
            INNER JOIN usuarios u ON d.usuario_id = u.usuario_id
            WHERE d.deleted_at IS NULL
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conexion.close()

def crear_docente_db(legajo, usuario_id, departamento):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        query = "INSERT INTO docentes (legajo, usuario_id, departamento) VALUES (%s, %s, %s)"
        valores = (legajo, usuario_id, departamento)
        cursor.execute(query, valores)
        conexion.commit()
        return legajo 
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        cursor.close()
        conexion.close()

def eliminar_docente_db(legajo):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        query = "UPDATE docentes SET deleted_at = CURRENT_TIMESTAMP WHERE legajo = %s"
        cursor.execute(query, (legajo,))
        conexion.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        cursor.close()
        conexion.close()