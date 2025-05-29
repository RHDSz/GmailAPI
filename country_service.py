"""
Módulo para obtener información de países utilizando la API REST Countries.

Este módulo proporciona funciones para obtener información detallada
sobre países utilizando la API REST Countries.
"""

import requests
import logging
from typing import Dict, Any, Optional
from config import SETTINGS

# Configuración básica del logging
logging.basicConfig(
    level=SETTINGS["LOG_LEVEL"],
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="country_service.log"
)
logger = logging.getLogger(__name__)

class CountryService:
    """Clase para obtener y procesar información de países."""
    
    BASE_URL = "https://restcountries.com/v3.1"
    
    def __init__(self):
        """Inicializa el servicio de información de países."""
        self.default_country = SETTINGS["DEFAULT_COUNTRY"]
    
    def get_country_info(self, country_code: str = None) -> Dict[str, Any]:
        """
        Obtiene información detallada sobre un país específico.
        
        Args:
            country_code (str, optional): Código ISO 3166-1 alpha-2 del país.
                                         Si no se proporciona, se usa el país predeterminado.
            
        Returns:
            Dict[str, Any]: Diccionario con la información del país.
            
        Raises:
            ValueError: Si el código de país no es válido o está vacío.
            ConnectionError: Si hay problemas de conexión con la API.
            Exception: Para otros errores no especificados.
        """
        # Usar valor predeterminado si no se proporciona
        country_code = country_code or self.default_country
        
        # Validar parámetros
        if not country_code or not isinstance(country_code, str):
            logger.error("Código de país inválido proporcionado")
            raise ValueError("El código de país debe ser una cadena de texto no vacía")
        
        try:
            # Construir URL para la solicitud
            url = f"{self.BASE_URL}/alpha/{country_code}"
            
            # Realizar la solicitud HTTP
            logger.info(f"Obteniendo información para el país con código: {country_code}")
            response = requests.get(url)
            
            # Verificar si la solicitud fue exitosa
            response.raise_for_status()
            
            # Convertir la respuesta a formato JSON
            country_data = response.json()
            
            # La API devuelve una lista con un solo elemento
            if isinstance(country_data, list) and len(country_data) > 0:
                country_data = country_data[0]
            
            logger.info(f"Información obtenida exitosamente para código: {country_code}")
            
            return country_data
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.error(f"País no encontrado: {country_code}")
                raise ValueError(f"No se encontró el país con código: {country_code}")
            else:
                logger.error(f"Error HTTP al obtener información del país: {e}")
                raise
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Error de conexión al obtener información del país: {e}")
            raise ConnectionError(f"No se pudo conectar con la API de REST Countries: {e}")
        
        except Exception as e:
            logger.error(f"Error inesperado al obtener información del país: {e}")
            raise
    
    def format_country_data(self, country_data: Dict[str, Any]) -> str:
        """
        Formatea la información de un país para mostrarla en formato legible.
        
        Args:
            country_data (Dict[str, Any]): Datos del país obtenidos de la API.
            
        Returns:
            str: Texto formateado con la información del país.
        """
        try:
            # Extraer información relevante
            name = country_data.get("name", {}).get("common", "Nombre desconocido")
            official_name = country_data.get("name", {}).get("official", "Nombre oficial desconocido")
            capital = ", ".join(country_data.get("capital", ["Capital desconocida"]))
            region = country_data.get("region", "Región desconocida")
            subregion = country_data.get("subregion", "Subregión desconocida")
            population = country_data.get("population", 0)
            languages = ", ".join(country_data.get("languages", {}).values())
            currencies = ", ".join([f"{c.get('name', 'Desconocida')} ({c.get('symbol', '?')})" 
                                  for c in country_data.get("currencies", {}).values()])
            
            # Formatear texto
            formatted_text = (
                f"\n🌎 INFORMACIÓN DE PAÍS: {name.upper()}\n"
                f"----------------------------------------\n"
                f"🏛️  Nombre oficial: {official_name}\n"
                f"🏙️  Capital: {capital}\n"
                f"🗺️  Región: {region} ({subregion})\n"
                f"👥 Población: {population:,}\n"
                f"🗣️  Idiomas: {languages}\n"
                f"💰 Monedas: {currencies}\n"
                f"----------------------------------------\n"
            )
            
            return formatted_text
        
        except Exception as e:
            logger.error(f"Error al formatear datos del país: {e}")
            return "Error al formatear datos del país"

def main():
    """Función principal para pruebas del módulo."""
    print("\n" + "="*50)
    print("🌎 SERVICIO DE INFORMACIÓN DE PAÍSES")
    print("="*50)
    
    service = CountryService()
    
    try:
        country_code = input("\nIngresa un código de país (o presiona Enter para usar CL): ").strip() or "CL"
        country_data = service.get_country_info(country_code)
        formatted_country = service.format_country_data(country_data)
        print(formatted_country)
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
