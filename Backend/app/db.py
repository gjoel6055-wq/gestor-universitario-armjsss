import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    url_conexion = os.getenv("DATABASE_URL")
    return psycopg2.connect(url_conexion)