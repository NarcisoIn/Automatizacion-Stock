import requests
from logger import logger
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

Token = os.getenv('TOKEN_BOT')
CHAT_IDS=[os.getenv('CHAT_ID_1'), os.getenv('CHAT_ID_2')]

def enviar_telegram(archivo):
    try:

        if not os.path.isabs(archivo):
            archivo = os.path.join(BASE_DIR, archivo)

        if not os.path.exists(archivo):
            logger.warning(f'El archivo {archivo} no existe')
            return
        
        mensaje = "📦 *Reporte de inventario* 📦\nAdjunto encontrarás el archivo con productos agotados y bajo"

        for chat_id in CHAT_IDS:
            # Enviar mensaje inicial
            url_msg = f"https://api.telegram.org/bot{Token}/sendMessage"
            respuesta = requests.post(url_msg, data={"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"})
            logger.info(f"Respuesta mensaje: {respuesta.status_code} {respuesta.text}")

            # Enviar Archivo
            url_file=f"https://api.telegram.org/bot{Token}/sendDocument"
            with open(archivo, "rb") as f:
                requests.post(url_file, data={"chat_id": chat_id}, files={"document": f})

        logger.info("Reporte enviado por Telegram correctamente")
    except Exception as error:
        logger.error(f"Error al enviar por Telegram: {error}")