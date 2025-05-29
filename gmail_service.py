"""
Módulo para enviar correos electrónicos utilizando la API de Gmail.

Este módulo proporciona funciones para autenticar con la API de Gmail
y enviar correos electrónicos con contenido HTML.
"""

import os
import base64
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import GMAIL_CREDENTIALS_FILE, GMAIL_TOKEN_FILE, GMAIL_SCOPES, SETTINGS

# Configuración básica del logging
logging.basicConfig(
    level=SETTINGS["LOG_LEVEL"],
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="gmail_service.log"
)
logger = logging.getLogger(__name__)

class GmailService:
    """Clase para enviar correos electrónicos utilizando la API de Gmail."""
    
    def __init__(self):
        """Inicializa el servicio de Gmail."""
        self.credentials_file = GMAIL_CREDENTIALS_FILE
        self.token_file = GMAIL_TOKEN_FILE
        self.scopes = GMAIL_SCOPES
        self.service = None
    
    def authenticate(self) -> bool:
        """
        Autentica con la API de Gmail utilizando OAuth 2.0.
        
        Returns:
            bool: True si la autenticación fue exitosa, False en caso contrario.
        """
        try:
            creds = None
            
            # Verificar si ya existe un token
            if os.path.exists(self.token_file):
                creds = Credentials.from_authorized_user_info(
                    eval(open(self.token_file, 'r').read()), self.scopes)
            
            # Si no hay credenciales válidas, solicitar autorización
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, self.scopes)
                    creds = flow.run_local_server(port=0)
                
                # Guardar el token para futuros usos
                with open(self.token_file, 'w') as token:
                    token.write(str(creds.to_json()))
            
            # Construir el servicio
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("Autenticación con Gmail exitosa")
            return True
        
        except Exception as e:
            logger.error(f"Error en la autenticación con Gmail: {e}")
            return False
    
    def send_email(self, to: str, subject: str, html_content: str, from_email: str = None) -> Dict[str, Any]:
        """
        Envía un correo electrónico utilizando la API de Gmail.
        
        Args:
            to (str): Dirección de correo del destinatario.
            subject (str): Asunto del correo.
            html_content (str): Contenido HTML del correo.
            from_email (str, optional): Dirección de correo del remitente.
                Si no se proporciona, se usa la dirección del usuario autenticado.
            
        Returns:
            Dict[str, Any]: Información sobre el correo enviado, incluyendo el ID del mensaje.
            
        Raises:
            ValueError: Si los parámetros no son válidos.
            Exception: Para otros errores no especificados.
        """
        # Validar parámetros
        if not to or not isinstance(to, str):
            logger.error("Destinatario inválido proporcionado")
            raise ValueError("El destinatario debe ser una cadena de texto no vacía")
        
        if not subject or not isinstance(subject, str):
            logger.error("Asunto inválido proporcionado")
            raise ValueError("El asunto debe ser una cadena de texto no vacía")
        
        if not html_content or not isinstance(html_content, str):
            logger.error("Contenido HTML inválido proporcionado")
            raise ValueError("El contenido HTML debe ser una cadena de texto no vacía")
        
        try:
            # Autenticar si es necesario
            if not self.service:
                if not self.authenticate():
                    raise Exception("No se pudo autenticar con Gmail")
            
            # Crear el mensaje
            message = MIMEMultipart('alternative')
            message['To'] = to
            message['Subject'] = subject
            
            # Agregar el contenido HTML
            message.attach(MIMEText(html_content, 'html'))
            
            # Codificar el mensaje
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            # Crear el cuerpo de la solicitud
            create_message = {
                'raw': encoded_message
            }
            
            # Enviar el mensaje
            send_message = self.service.users().messages().send(
                userId='me', body=create_message).execute()
            
            logger.info(f"Correo enviado exitosamente a {to}, ID: {send_message['id']}")
            
            return {
                'id': send_message['id'],
                'to': to,
                'subject': subject,
                'status': 'sent'
            }
        
        except HttpError as e:
            logger.error(f"Error HTTP al enviar el correo: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Error inesperado al enviar el correo: {e}")
            raise

def main():
    """Función principal para pruebas del módulo."""
    print("\n" + "="*50)
    print("📧 SERVICIO DE GMAIL")
    print("="*50)
    
    service = GmailService()
    
    try:
        print("\nAutenticando con Gmail...")
        if service.authenticate():
            print("✅ Autenticación exitosa")
            
            to = input("\nIngresa el correo del destinatario: ").strip()
            subject = input("Ingresa el asunto del correo: ").strip()
            
            html_content = f"""
            <html>
              <body>
                <h1>Prueba de envío de correo</h1>
                <p>Este es un correo de prueba enviado desde la API de Gmail.</p>
                <p>Si estás viendo este correo, la configuración funciona correctamente.</p>
              </body>
            </html>
            """
            
            print(f"\nEnviando correo a {to}...")
            result = service.send_email(to, subject, html_content)
            print(f"✅ Correo enviado exitosamente. ID del mensaje: {result['id']}")
        else:
            print("❌ Error en la autenticación")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
