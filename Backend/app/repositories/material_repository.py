from app.db import get_connection

def crear_material_db(titulo, descripcion, url_archivo, curso_id):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        query = """
            INSERT INTO materiales (titulo, descripcion, url_archivo, curso_id) 
            VALUES (%s, %s, %s, %s)
        """
        valores = (titulo, descripcion, url_archivo, curso_id)
        
        cursor.execute(query, valores)
        conexion.commit()
        
        return cursor.lastrowid
        
    except Exception as e:
        conexion.rollback()
        raise e
        
    finally:
        cursor.close()
        conexion.close()

def obtener_materiales_db():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    
    try:
        query = "SELECT id, titulo, descripcion, url_archivo, curso_id FROM materiales WHERE deleted_at IS NULL"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conexion.close()

def actualizar_material_db(id, titulo, descripcion, url_archivo, curso_id):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        query = """
            UPDATE materiales 
            SET titulo = %s, descripcion = %s, url_archivo = %s, curso_id = %s 
            WHERE id = %s AND deleted_at IS NULL
        """
        valores = (titulo, descripcion, url_archivo, curso_id, id)
        cursor.execute(query, valores)
        conexion.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        cursor.close()
        conexion.close()

def eliminar_material_db(id):
    conexion = get_connection()
    cursor = conexion.cursor()
    
    try:
        query = "UPDATE materiales SET deleted_at = CURRENT_TIMESTAMP WHERE id = %s"
        cursor.execute(query, (id,))
        conexion.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        cursor.close()
        conexion.close()