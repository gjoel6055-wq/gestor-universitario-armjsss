import os
from dotenv import load_dotenv

load_dotenv()

# URLs de la aplicacion
API_BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:8080')
FRONT_BASE_URL = os.getenv('FRONT_BASE_URL', 'http://127.0.0.1:5030')

# Validacion de email
REGEX_EMAIL = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

# Configuracion de la base de datos Supabase (PostgreSQL)
DB_HOST = os.getenv('DB_HOST', '')
DB_PORT = int(os.getenv('DB_PORT', '5432'))
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Configuracion de Supabase (para Storage si se necesita)
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')

# Secret key para JWT
SECRET_KEY = os.getenv('SECRET_KEY', 'una-clave-secreta-temporal')

# Codigos de error
ERROR_CODE_INVALID_BODY = 'invalid.body'
ERROR_CODE_NOT_FOUND = 'not.found'
ERROR_CODE_CONFLICT = 'conflict'
ERROR_CODE_UNAUTHORIZED = 'unauthorized'