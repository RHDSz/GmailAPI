"""
Módulo principal para la aplicación de reportes de clima y noticias de Chile.

Este módulo proporciona la interfaz principal para generar y enviar reportes
de clima y noticias de Chile, integrando todos los servicios disponibles.
"""

import os
import sys
import logging
import argparse
import datetime
from typing import Dict, Any, Optional

from dashboard import Dashboard
from gmail_service import GmailService
from config import SETTINGS, EMAIL_SUBJECT, EMAIL_RECIPIENT

# Configuración básica del logging
logging.basicConfig(
    level=SETTINGS["LOG_LEVEL"],
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="main.log"
)
logger = logging.getLogger(__name__)

def save_report_to_file(report: str, filename: str = "reporte.txt") -> str:
    """
    Guarda el reporte en un archivo de texto.
    
    Args:
        report (str): Contenido del reporte.
        filename (str, optional): Nombre del archivo donde guardar el reporte.
        
    Returns:
        str: Ruta completa al archivo guardado.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        
        logger.info(f"Reporte guardado exitosamente en: {filename}")
        return os.path.abspath(filename)
    
    except Exception as e:
        logger.error(f"Error al guardar el reporte: {e}")
        raise

def save_html_report(html_report: str, filename: str = "reporte.html") -> str:
    """
    Guarda el reporte HTML en un archivo.
    
    Args:
        html_report (str): Contenido HTML del reporte.
        filename (str, optional): Nombre del archivo donde guardar el reporte.
        
    Returns:
        str: Ruta completa al archivo guardado.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_report)
        
        logger.info(f"Reporte HTML guardado exitosamente en: {filename}")
        return os.path.abspath(filename)
    
    except Exception as e:
        logger.error(f"Error al guardar el reporte HTML: {e}")
        raise

def send_email_report(html_content: str, recipient: str = EMAIL_RECIPIENT, subject: str = EMAIL_SUBJECT) -> bool:
    """
    Envía el reporte por correo electrónico utilizando la API de Gmail.
    
    Args:
        html_content (str): Contenido HTML del reporte.
        recipient (str, optional): Dirección de correo del destinatario.
        subject (str, optional): Asunto del correo.
        
    Returns:
        bool: True si el correo se envió correctamente, False en caso contrario.
    """
    try:
        logger.info(f"Enviando correo a: {recipient}")
        
        # Crear el servicio de Gmail
        gmail_service = GmailService()
        
        # Autenticar con Gmail
        if not gmail_service.authenticate():
            logger.error("No se pudo autenticar con Gmail")
            print("\n❌ Error: No se pudo autenticar con Gmail")
            return False
        
        # Enviar el correo
        result = gmail_service.send_email(recipient, subject, html_content)
        
        logger.info(f"Correo enviado exitosamente. ID del mensaje: {result['id']}")
        print(f"\n✅ Correo enviado exitosamente a {recipient}")
        
        return True
    
    except Exception as e:
        logger.error(f"Error al enviar el correo: {e}")
        print(f"\n❌ Error al enviar el correo: {e}")
        return False

def main():
    """Función principal de la aplicación."""
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description="Generador de reportes de clima y noticias de Chile")
    
    parser.add_argument("--city", default=SETTINGS["DEFAULT_CITY"],
                        help=f"Ciudad para obtener datos del clima (predeterminado: {SETTINGS['DEFAULT_CITY']})")
    
    parser.add_argument("--country", default=SETTINGS["DEFAULT_COUNTRY"],
                        help=f"Código de país para obtener información (predeterminado: {SETTINGS['DEFAULT_COUNTRY']})")
    
    parser.add_argument("--email", default=EMAIL_RECIPIENT,
                        help=f"Correo electrónico del destinatario (predeterminado: {EMAIL_RECIPIENT})")
    
    parser.add_argument("--subject", default=EMAIL_SUBJECT,
                        help=f"Asunto del correo electrónico (predeterminado: {EMAIL_SUBJECT})")
    
    parser.add_argument("--save", action="store_true",
                        help="Guardar el reporte en archivos locales (texto y HTML)")
    
    parser.add_argument("--send", action="store_true",
                        help="Enviar el reporte por correo electrónico")
    
    # Parsear los argumentos
    args = parser.parse_args()
    
    try:
        print("\n" + "="*50)
        print("📊 GENERADOR DE REPORTES: CLIMA Y NOTICIAS DE CHILE")
        print("="*50)
        
        # Crear el dashboard
        dashboard = Dashboard()
        
        # Generar el reporte
        print(f"\nGenerando reporte para {args.city}, {args.country}...")
        text_report = dashboard.generate_report(args.city, args.country)
        html_report = dashboard.generate_html_report(args.city, args.country)
        
        # Mostrar el reporte en texto
        print("\n" + "="*50)
        print("📝 REPORTE EN FORMATO TEXTO")
        print("="*50)
        print(text_report)
        
        # Guardar el reporte si se solicita
        if args.save:
            text_file = save_report_to_file(text_report)
            html_file = save_html_report(html_report)
            print(f"\n✅ Reporte guardado en formato texto: {text_file}")
            print(f"✅ Reporte guardado en formato HTML: {html_file}")
        
        # Enviar el reporte por correo si se solicita
        if args.send:
            print(f"\nEnviando reporte por correo a {args.email}...")
            success = send_email_report(html_report, args.email, args.subject)
            if success:
                print(f"✅ Reporte enviado exitosamente a {args.email}")
        
        print("\n" + "="*50)
        print("✅ PROCESO COMPLETADO")
        print("="*50)
        
    except Exception as e:
        logger.error(f"Error en la aplicación principal: {e}")
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
