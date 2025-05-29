#!/usr/bin/env python
"""
Script para programar el envío automático diario de reportes de clima y noticias.

Este script está diseñado para ser ejecutado por un programador de tareas
(cron, Task Scheduler, launchd) para enviar reportes diarios automáticamente.
"""

import os
import sys
import logging
import argparse
import datetime
from main import send_email_report
from dashboard import Dashboard
from config import SETTINGS, EMAIL_SUBJECT, EMAIL_RECIPIENT

# Configuración básica del logging
logging.basicConfig(
    level=SETTINGS["LOG_LEVEL"],
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="envio_automatico.log"
)
logger = logging.getLogger(__name__)

def enviar_reporte_automatico(
    ciudad: str = SETTINGS["DEFAULT_CITY"],
    pais: str = SETTINGS["DEFAULT_COUNTRY"],
    destinatario: str = EMAIL_RECIPIENT,
    asunto: str = EMAIL_SUBJECT,
    guardar_copia: bool = True
) -> bool:
    """
    Genera y envía un reporte automáticamente.
    
    Args:
        ciudad (str): Ciudad para obtener el clima.
        pais (str): Código de país para obtener información y noticias.
        destinatario (str): Correo electrónico del destinatario.
        asunto (str): Asunto del correo electrónico.
        guardar_copia (bool): Si se debe guardar una copia local del reporte.
        
    Returns:
        bool: True si el envío fue exitoso, False en caso contrario.
    """
    try:
        # Registrar inicio del proceso
        ahora = datetime.datetime.now()
        fecha_str = ahora.strftime("%d/%m/%Y")
        hora_str = ahora.strftime("%H:%M:%S")
        
        logger.info(f"Iniciando envío automático en {fecha_str} a las {hora_str}")
        logger.info(f"Parámetros: ciudad={ciudad}, país={pais}, destinatario={destinatario}")
        
        # Crear el dashboard y generar el reporte
        dashboard = Dashboard()
        html_report = dashboard.generate_html_report(ciudad, pais)
        
        # Guardar una copia local si se solicita
        if guardar_copia:
            fecha_archivo = ahora.strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"reporte_{fecha_archivo}.html"
            
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write(html_report)
            
            logger.info(f"Copia local guardada en: {nombre_archivo}")
        
        # Enviar el reporte por correo
        logger.info(f"Enviando reporte a {destinatario}")
        exito = send_email_report(html_report, destinatario, asunto)
        
        if exito:
            logger.info("Reporte enviado exitosamente")
            return True
        else:
            logger.error("Error al enviar el reporte")
            return False
    
    except Exception as e:
        logger.error(f"Error en el envío automático: {e}")
        return False

def main():
    """Función principal del script."""
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(
        description="Envío automático de reportes de clima y noticias de Chile"
    )
    
    parser.add_argument("--ciudad", default=SETTINGS["DEFAULT_CITY"],
                        help=f"Ciudad para obtener datos del clima (predeterminado: {SETTINGS['DEFAULT_CITY']})")
    
    parser.add_argument("--pais", default=SETTINGS["DEFAULT_COUNTRY"],
                        help=f"Código de país para obtener información (predeterminado: {SETTINGS['DEFAULT_COUNTRY']})")
    
    parser.add_argument("--email", default=EMAIL_RECIPIENT,
                        help=f"Correo electrónico del destinatario (predeterminado: {EMAIL_RECIPIENT})")
    
    parser.add_argument("--asunto", default=EMAIL_SUBJECT,
                        help=f"Asunto del correo electrónico (predeterminado: {EMAIL_SUBJECT})")
    
    parser.add_argument("--no-guardar", action="store_true",
                        help="No guardar una copia local del reporte")
    
    # Parsear los argumentos
    args = parser.parse_args()
    
    # Enviar el reporte
    exito = enviar_reporte_automatico(
        ciudad=args.ciudad,
        pais=args.pais,
        destinatario=args.email,
        asunto=args.asunto,
        guardar_copia=not args.no_guardar
    )
    
    # Retornar código de salida
    return 0 if exito else 1

if __name__ == "__main__":
    sys.exit(main())
