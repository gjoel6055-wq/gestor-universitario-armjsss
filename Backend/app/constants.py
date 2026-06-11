import os

API_BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:8080')
FRONT_BASE_URL = os.getenv('FRONT_BASE_URL', 'http://127.0.0.1:5030')
REGEX_EMAIL = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
SECRET_KEY = os.getenv('SECRET_KEY', 'una-clave-secreta-temporal')