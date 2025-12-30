import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys

# Determinar la carpeta donde se ejucata el script o .exe
if getattr(sys, 'frozen', False):
    # Si es un .exe generado por PyInstaller
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Si es un script normal de Python
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta completa
log_file = os.path.join(BASE_DIR, "logs_automatizacion.log")

# Handler que rota semanalmente
handler = TimedRotatingFileHandler(
    "logs_automatizacion.log", # Archivo unico para todo el proyecto
    when="W0",
    interval=1,
    backupCount=4 # Mantiene logs de las ultimas 4 semanas
)

formato = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formato)

# Configuracion de logger global
logger = logging.getLogger("proyecto")
logger.setLevel(logging.INFO) # INFO, WARNING, ERROR
logger.addHandler(handler)
