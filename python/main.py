# main.py
from db import conexion
from logger import logger
from reporte import generar_excel
from telegram_bot import enviar_telegram
import os
import time
import sys
import shutil
import glob
from datetime import datetime

logger.info("Automatizacion Arrmar v1.0 iniciada")
# Obtener ruta del archivo
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

stock_minimo = 6
alertas = []
agotados = []

try:
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT 
            COD1_ART,
            DES1_ART,
            EXI_ACT
        FROM tblcatarticulos
    """)
    productos = cursor.fetchall()
    logger.info(f"Se consultaron {len(productos)} productos correctamente")

    for producto in productos:
        existencia = producto['EXI_ACT']
        if existencia <= 0:
            agotados.append({
                'codigo': producto['COD1_ART'],
                'nombre': producto['DES1_ART'],
                'existencia': existencia
            })
        elif existencia <= stock_minimo:
            alertas.append({
                'codigo': producto['COD1_ART'],
                'nombre': producto['DES1_ART'],
                'existencia': existencia
            })


    # Ruta de archivo maestro de proveedores
    archivo_proveedores = os.path.join(BASE_DIR, 'Maestro_Proveedores.xlsx')
    archivo_proveedores = os.path.abspath(archivo_proveedores)

    # Eliminar los ultimos 7 reportes diarios
    max_dias = 7
    archivos_anteriores = glob.glob(os.path.join(BASE_DIR, "Alertas_inventario_*.xlsx"))
    
    #Ordenar por fechas
    archivos_anteriores.sort(key=lambda x: os.path.getmtime(x))
    
    if len(archivos_anteriores) > max_dias:
        for archivo_antiguo in archivos_anteriores[:-max_dias]:
            try:
                os.remove(archivo_antiguo)
                logger.info(f"Archivo antiguo eliminado: {archivo_antiguo}")
            except Exception as error:
                logger.warning(f"No se pudo eliminar {archivo_antiguo}: {error}")

    # Genera el archivo Excel
    archivo = generar_excel(agotados, alertas, stock_minimo, BASE_DIR, archivo_proveedores)


    if archivo and os.path.exists(archivo):
        
        intentos = 4
        for i in range(intentos):
            try:
                enviar_telegram(archivo)
                logger.info("Archivo enviado por Telegram exitosamente")
                break
            except Exception as e:
                logger.error(f"Error al enviar archivo por Telegram: (intento {i+1}/{intentos}): {e}")
                if i < intentos - 1:
                    time.sleep(8)
                else:
                    logger.warning("No se pudo enviar el archivo por Telegram despues de varios intentos")
    else:
        logger.warning("No se generó el archivo reporte")

except Exception as error:
    logger.error(f"Error al consultar productos: {error}")
