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