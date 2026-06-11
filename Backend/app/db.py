import psycopg2
from psycopg2.extras import RealDictCursor
import os

DB_CONFIG = {
    "host": os.getenv('DB_HOST', ''),
    "port": int(os.getenv('DB_PORT', '5432')),
    "user": os.getenv('DB_USER', 'postgres'),
    "password": os.getenv('DB_PASSWORD', ''),
    "dbname": os.getenv('DB_NAME', 'postgres'),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# Exportar RealDictCursor para usar en repositorios
__all__ = ['get_connection', 'RealDictCursor']