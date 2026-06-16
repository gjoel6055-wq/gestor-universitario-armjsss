from app.db import get_connection
import logging

logger = logging.getLogger(__name__)

def contar_alumnos():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT COUNT(*) FROM alumnos')
        return cursor.fetchone()[0] or 0
    except Exception as e:
        logger.error(f'Error al contar alumnos: {e}')
        return 0
    finally:
        cursor.close()
        conn.close()


def contar_docentes():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT COUNT(*) FROM docentes')
        return cursor.fetchone()[0] or 0
    except Exception as e:
        logger.error(f'Error al contar docentes: {e}')
        return 0
    finally:
        cursor.close()
        conn.close()


def contar_cursos_activos():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT COUNT(*) FROM cursos')
        return cursor.fetchone()[0] or 0
    except Exception as e:
        logger.error(f'Error al contar cursos activos: {e}')
        return 0
    finally:
        cursor.close()
        conn.close()


def calcular_asistencia_promedio():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT SUM(presente), COUNT(*) FROM asistencias')
        resultado = cursor.fetchone()
        if not resultado or resultado[1] == 0:
            return '0%'

        asistencias_presentes = resultado[0] or 0
        total_asistencias = resultado[1]
        porcentaje = round((asistencias_presentes / total_asistencias) * 100, 2)
        return f"{porcentaje}%"
    except Exception as e:
        logger.error(f'Error al calcular asistencia promedio: {e}')
        return '0%'
    finally:
        cursor.close()
        conn.close()


def promedio_notas():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT AVG(nota) FROM notas')
        promedio = cursor.fetchone()[0]
        if promedio is None:
            return 0.0
        return round(float(promedio), 2)
    except Exception as e:
        logger.error(f'Error al calcular promedio de notas: {e}')
        return 0.0
    finally:
        cursor.close()
        conn.close()


def contar_evaluaciones():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT COUNT(*) FROM evaluaciones')
        return cursor.fetchone()[0] or 0
    except Exception as e:
        logger.error(f'Error al contar evaluaciones: {e}')
        return 0
    finally:
        cursor.close()
        conn.close()


def contar_materiales():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT COUNT(*) FROM materiales')
        return cursor.fetchone()[0] or 0
    except Exception as e:
        logger.error(f'Error al contar materiales: {e}')
        return 0
    finally:
        cursor.close()
        conn.close()


def contar_alumnos_en_abandono():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT COUNT(*) FROM alumnos WHERE abandono = 1')
        return cursor.fetchone()[0] or 0
    except Exception as e:
        logger.error(f'Error al contar alumnos en abandono: {e}')
        return 0
    finally:
        cursor.close()
        conn.close()


def asistencia_ultima_semana():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'SELECT SUM(presente), COUNT(*) FROM asistencias WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)'
        )
        resultado = cursor.fetchone()
        presentes = resultado[0] or 0
        total = resultado[1] or 0
        if total == 0:
            return {'presentes': 0, 'total': 0, 'porcentaje': '0%'}

        porcentaje = round((presentes / total) * 100, 2)
        return {'presentes': presentes, 'total': total, 'porcentaje': f"{porcentaje}%"}
    except Exception as e:
        logger.error(f'Error al calcular asistencia de la última semana: {e}')
        return {'presentes': 0, 'total': 0, 'porcentaje': '0%'}
    finally:
        cursor.close()
        conn.close()