from datetime import datetime
from app.db import get_connection, RealDictCursor
import psycopg2

def guardar_nota_bd(datos):
    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        query = '''
            INSERT INTO notas (padron, evaluacion_id, nota, observacion)
            VALUES (%s, %s, %s, %s)
            RETURNING nota_id
        '''
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

def listar_todas_notas():
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute('''
        SELECT n.nota_id, n.padron, n.evaluacion_id, n.nota, n.observacion, n.fecha_carga,
               u.nombre AS alumno_nombre, u.apellido AS alumno_apellido,
               e.nombre AS evaluacion_nombre, e.curso_id, c.nombre AS curso_nombre
        FROM notas n
        JOIN alumnos a ON n.padron = a.padron
        JOIN usuarios u ON a.usuario_id = u.usuario_id
        JOIN evaluaciones e ON n.evaluacion_id = e.evaluacion_id
        JOIN cursos c ON e.curso_id = c.curso_id
        WHERE n.deleted_at IS NULL
        ORDER BY n.fecha_carga DESC
    ''')
    notas = cursor.fetchall() or []
    cursor.close()
    conexion.close()
    return notas

def cargar_notas_grupal(equipo_id, evaluacion_id, nota, observacion):
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        'SELECT padron FROM equipos_alumnos WHERE equipo_id = %s AND deleted_at IS NULL',
        (equipo_id,),
    )
    alumnos = cursor.fetchall() or []
    if not alumnos:
        cursor.close()
        conexion.close()
        return None
    cargadas = []
    for al in alumnos:
        padron = al['padron']
        cursor.execute(
            'SELECT nota_id FROM notas WHERE padron = %s AND evaluacion_id = %s AND deleted_at IS NULL',
            (padron, evaluacion_id),
        )
        existente = cursor.fetchone()
        if existente:
            cursor.execute(
                'UPDATE notas SET nota = %s, observacion = %s WHERE nota_id = %s',
                (nota, observacion, existente['nota_id']),
            )
        else:
            cursor.execute(
                'INSERT INTO notas (padron, evaluacion_id, nota, observacion) VALUES (%s, %s, %s, %s)',
                (padron, evaluacion_id, nota, observacion),
            )
        cargadas.append(padron)
    conexion.commit()
    cursor.close()
    conexion.close()
    return cargadas