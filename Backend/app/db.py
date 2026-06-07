import mysql.connector

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "gestor_universitario",
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)