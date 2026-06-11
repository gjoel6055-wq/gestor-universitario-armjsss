from sqlalchemy import create_engine, text
from app.constants import DB_URL

# Motor de conexion compartido por toda la aplicacion.
# El pool de conexiones lo maneja SQLAlchemy automaticamente.
motor = create_engine(DB_URL)


# ---------------------------------------------------------------
# Funciones de soporte
# ---------------------------------------------------------------

def fila_a_dict(fila) -> dict:
    """Convierte una fila del resultado de una query en un diccionario."""
    return dict(fila._mapping)


def ejecutar_consulta(sql: str, parametros: dict = None) -> list[dict]:
    """Ejecuta una SELECT y devuelve todas las filas como lista de dicts."""
    with motor.connect() as conexion:
        resultado = conexion.execute(text(sql), parametros or {})
        return [fila_a_dict(fila) for fila in resultado]


def ejecutar_mutacion(sql: str, parametros: dict = None) -> int:
    """
    Ejecuta un INSERT, UPDATE o DELETE y hace commit.
    Si la query incluye RETURNING id, retorna el id generado; de lo contrario retorna 0.
    """
    with motor.begin() as conexion:
        resultado = conexion.execute(text(sql), parametros or {})
        fila = resultado.fetchone() if resultado.returns_rows else None
        return fila[0] if fila else 0


# ---------------------------------------------------------------
# Funcion legacy para compatibilidad con codigo existente
# ---------------------------------------------------------------

def get_connection():
    """
    Funcion de compatibilidad legacy.
    Retorna el motor de SQLAlchemy para usar con el nuevo patron.
    """
    return motor