# Automatización de Stock

Sistema de automatización para el monitoreo de inventario y generación de alertas por stock bajo.

## Contexto del proyecto

Este sistema fue desarrollado para automatizar la revisión de inventario en un entorno real de punto de venta (POS), donde los productos y existencias se almacenan en una base de datos MySQL.

## Objetivo del proyecto
Desarrollar una herramienta que permita automatizar la revisión de inventarios, reduciendo errores humanos y facilitando la detección temprana de faltantes de productos.

## Alcance
- Revisión automática de niveles de stock
- Detección de productos con stock bajo
- Generación de alertas
- Conexión a base de datos MySQL
- Empaquetado como ejecutable standalone

## Tecnologías utilizadas
- Python
- MySQL
- pandas
- dotenv
- PyInstaller

## Arquitectura general
El sistema sigue una arquitectura simple de una sola aplicación:
- Entrada: Base de datos y archivo de inventario
- Lógica: Procesamiento y validación de stock
- Salida: Alertas y reportes

(Ver documentación detallada en /docs)

## Estado del proyecto
Proyecto funcional en desarrollo activo.  
La documentación y el código están sujetos a mejoras y cambios.

## Documentación
- Instalación: `docs/instalacion.md`
- Uso: `docs/uso.md`
- Arquitectura: `docs/arquitectura.md`
- Mejoras futuras: `docs/futuras_mejoras.md`
