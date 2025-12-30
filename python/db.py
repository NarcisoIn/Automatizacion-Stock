import os
os.environ["LANG"] = "en_US"
os.environ["LC_ALL"] = "en_US"

from dotenv import load_dotenv
import pymysql
from logger import logger

if getattr(os, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.abspath(os.path.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=dotenv_path)

try:
    # Conexión a Base de Datos
    conexion = pymysql.connect (
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_DATABASE"),
        port=int(os.getenv("DB_PORT", 3307)),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    logger.info("Conexión a DB exitosa")

except Exception as error:
    logger.error(f"Error de Conexión: {error}")
    raise