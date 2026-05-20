from app.repositories.dashboard_repository import (
    contar_alumnos,
    contar_docentes,
    contar_cursos_activos,
    calcular_asistencia_promedio,
    promedio_notas,
    contar_evaluaciones,
    contar_materiales,
    contar_alumnos_en_abandono,
    asistencia_ultima_semana,
)


def obtener_estadisticas_dashboard():
    return {
        'totalAlumnos': contar_alumnos(),
        'totalDocentes': contar_docentes(),
        'cursosActivos': contar_cursos_activos(),
        'asistenciaPromedio': calcular_asistencia_promedio(),
        'promedioNotas': promedio_notas(),
        'totalEvaluaciones': contar_evaluaciones(),
        'totalMateriales': contar_materiales(),
        'alumnosAbandono': contar_alumnos_en_abandono(),
        'asistenciaUltimaSemana': asistencia_ultima_semana(),
    }
