"""
Módulo de configuración para la aplicación de reportes de clima y noticias.

Este módulo contiene todas las configuraciones y constantes utilizadas
por los diferentes servicios de la aplicación.
"""

import os
import logging

# Configuración general
SETTINGS = {
    "LOG_LEVEL": logging.INFO,
    "DEFAULT_CITY": "La Serena",
    "DEFAULT_COUNTRY": "CL",
    "DEFAULT_LANGUAGE": "es"
}

# Configuración para la API de OpenWeatherMap
OPENWEATHER_API_KEY = "9ffad1e087f82aca9d11ed5655edecfc"  # API key proporcionada

# Configuración para la API de NewsAPI
NEWSAPI_API_KEY = "09a2d0a76f304fcb943631e48a589b5c"  # API key proporcionada

# Configuración para noticias chilenas
CHILE_NEWS_SOURCES = ["emol", "la_tercera", "el_mostrador", "biobio", "cooperativa"]
CHILE_NEWS_MAX_PER_SOURCE = 3
CHILE_NEWS_TOTAL_MAX = 10

# Configuración para correo electrónico
EMAIL_SENDER = "Servicio de Reportes <noreply@example.com>"
EMAIL_RECIPIENT = "fcer14.2002@gmail.com"
EMAIL_SUBJECT = "Reporte Diario: Clima y Noticias de Chile"

# Configuración para la API de Gmail
GMAIL_CREDENTIALS_FILE = "credentials.json"
GMAIL_TOKEN_FILE = "token.json"
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']
