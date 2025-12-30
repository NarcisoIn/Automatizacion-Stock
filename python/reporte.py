import pandas as pd
from datetime import datetime
from logger import logger
import os

def generar_excel(agotados, alertas, stock_minimo, carpeta_salida, archivo_proveedores):
    try:
        # Fecha para identificar el reporte
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        nombre_archivo = f"Alertas_inventario_{fecha_actual}.xlsx"

        ruta_excel = os.path.join(carpeta_salida, nombre_archivo)

        #Conversion de listas a DataFrame
        df_agotados = pd.DataFrame(agotados)
        df_alertas = pd.DataFrame(alertas)

        # Leer archivo maestro de proveedores
        df_proveedores = pd.read_excel(archivo_proveedores, usecols=['COD1_ART', 'DES1_ART','UNIDAD', 'Proveedor'])
        df_proveedores.rename(columns={
            "COD1_ART": "codigo",
            "DES1_ART": "nombre",
            "UNIDAD": "unidad",
            "Proveedor": "proveedor"
        }, inplace=True)

        # Productos agotados
        if not df_agotados.empty:
            df_agotados = df_agotados.merge(
                df_proveedores[['codigo','unidad','proveedor']],
                on="codigo",
                how="left"
            )
            # Reemplazar valores nulos en proveedor
            df_agotados['proveedor'] = df_agotados['proveedor'].fillna('SIN PROVEEDOR')
            df_agotados.rename(columns={"existencia":"stock"}, inplace=True)
            df_agotados = df_agotados[["codigo", "nombre", "unidad", "stock", "proveedor"]]
            df_agotados.sort_values(by="proveedor", inplace=True)

        # -----------------------------
        # Productos con bajo stock
        if not df_alertas.empty:
            df_alertas = df_alertas.merge(
                df_proveedores[['codigo','unidad','proveedor']],
                on='codigo',
                how='left'
            )
            # Reemplazar valores nulos en proveedor
            df_alertas['proveedor'] = df_alertas['proveedor'].fillna('SIN PROVEEDOR')
            df_alertas.rename(columns={"existencia":"stock"}, inplace=True)
            df_alertas = df_alertas[["codigo", "nombre", "unidad", "stock", "proveedor"]]
            df_alertas.sort_values(by="proveedor", inplace=True)

        # Creacion de archivos Excel
        with pd.ExcelWriter(ruta_excel, engine='xlsxwriter') as writer:
            workbook = writer.book

            # Hojas de productos agotados
            if not df_agotados.empty:
                df_agotados.to_excel(writer, sheet_name='Productos Agotados', index=False, startrow=1)
                worksheet = writer.sheets['Productos Agotados']

                # Formato de encabezado
                header_format = workbook.add_format({
                    'bold': True,
                    'align': 'center',
                    'valign': 'vcenter',
                    'font_size': 14
                })
                # Titulo de la hoja
                worksheet.merge_range('A1:E1', 'PRODUCTOS AGOTADOS', header_format)

                # Ajustar ancho de columnas
                for i, col in enumerate(df_agotados.columns):
                    max_len = max(df_agotados[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet.set_column(i, i, max_len)

            # Hoja de productos con bajo stock
            if not df_alertas.empty:
                nombre_hoja = f"Stock menor o igual a {stock_minimo}"
                df_alertas.to_excel(writer, sheet_name=nombre_hoja, index=False, startrow=1)
                worksheet2 = writer.sheets[nombre_hoja]

                # Titulo de la hoja
                worksheet2.merge_range('A1:E1', f'PRODUCTOS CON STOCK MENOR A {stock_minimo}', header_format)

                # Ajustar ancho de columnas
                for i, col in enumerate(df_alertas.columns):
                    max_len = max(df_alertas[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet2.set_column(i, i, max_len)

        logger.info(f"Se ha creado el reporte de stock exitosamente: {ruta_excel}")
        return ruta_excel

    except Exception as error:
        logger.error(f"Error al Generar reporte: {error}")