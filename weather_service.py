"""
Módulo para obtener datos del clima utilizando la API de OpenWeatherMap.

Este módulo proporciona funciones para obtener información meteorológica
actual de una ciudad específica utilizando la API de OpenWeatherMap.
"""

import requests
import logging
from typing import Dict, Any, Optional
from config import OPENWEATHER_API_KEY, SETTINGS

# Configuración básica del logging
logging.basicConfig(
    level=SETTINGS["LOG_LEVEL"],
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="weather_service.log"
)
logger = logging.getLogger(__name__)

class WeatherService:
    """Clase para obtener y procesar datos meteorológicos."""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    
    def __init__(self):
        """Inicializa el servicio de clima."""
        self.api_key = OPENWEATHER_API_KEY
        self.units = "metric"  # Unidades métricas (Celsius)
        self.lang = SETTINGS["DEFAULT_LANGUAGE"]
        
    def get_weather(self, city: str = SETTINGS["DEFAULT_CITY"]) -> Dict[str, Any]:
        """
        Obtiene los datos meteorológicos actuales para una ciudad específica.
        
        Args:
            city (str): Nombre de la ciudad para la cual obtener el clima.
            
        Returns:
            Dict[str, Any]: Diccionario con la información del clima.
            
        Raises:
            ValueError: Si la ciudad no es válida o está vacía.
            ConnectionError: Si hay problemas de conexión con la API.
            Exception: Para otros errores no especificados.
        """
        if not city or not isinstance(city, str):
            logger.error("Ciudad inválida proporcionada")
            raise ValueError("La ciudad debe ser una cadena de texto no vacía")
        
        try:
            # Parámetros para la solicitud a la API
            params = {
                'q': city,
                'appid': self.api_key,
                'units': self.units,
                'lang': self.lang
            }
            
            # Realizar la solicitud HTTP
            logger.info(f"Obteniendo datos del clima para: {city}")
            response = requests.get(self.BASE_URL, params=params)
            
            # Verificar si la solicitud fue exitosa
            response.raise_for_status()
            
            # Convertir la respuesta a formato JSON
            weather_data = response.json()
            logger.info(f"Datos del clima obtenidos exitosamente para: {city}")
            
            return weather_data
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.error(f"Ciudad no encontrada: {city}")
                raise ValueError(f"No se encontró la ciudad: {city}")
            elif e.response.status_code == 401:
                logger.error("API key inválida o no proporcionada")
                raise ValueError("API key inválida o no proporcionada para OpenWeatherMap")
            else:
                logger.error(f"Error HTTP al obtener el clima: {e}")
                raise
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Error de conexión al obtener el clima: {e}")
            raise ConnectionError(f"No se pudo conectar con la API de OpenWeatherMap: {e}")
        
        except Exception as e:
            logger.error(f"Error inesperado al obtener el clima: {e}")
            raise

    def format_weather_data(self, weather_data: Dict[str, Any]) -> str:
        """
        Formatea los datos del clima para mostrarlos en formato legible.
        
        Args:
            weather_data (Dict[str, Any]): Datos del clima obtenidos de la API.
            
        Returns:
            str: Texto formateado con la información del clima.
        """
        try:
            city = weather_data.get("name", "Ciudad desconocida")
            country = weather_data.get("sys", {}).get("country", "CL")
            temp = weather_data.get("main", {}).get("temp", 0)
            feels_like = weather_data.get("main", {}).get("feels_like", 0)
            description = weather_data.get("weather", [{}])[0].get("description", "No disponible").capitalize()
            humidity = weather_data.get("main", {}).get("humidity", 0)
            wind_speed = weather_data.get("wind", {}).get("speed", 0)
            
            return (
                f"\n🌦️ CONDICIONES METEOROLÓGICAS EN {city.upper()}, {country}\n"
                f"----------------------------------------\n"
                f"🌡️  Temperatura: {temp}°C\n"
                f"🤔 Sensación térmica: {feels_like}°C\n"
                f"💧 Humedad: {humidity}%\n"
                f"🌬️  Viento: {wind_speed} m/s\n"
                f"☁️  Condición: {description}\n"
                f"----------------------------------------\n"
            )
        except Exception as e:
            logger.error(f"Error al formatear datos del clima: {e}")
            return "Error al formatear datos del clima"

def main():
    """Función principal para pruebas del módulo."""
    print("\n" + "="*50)
    print("🌦️ SERVICIO DE CLIMA")
    print("="*50)
    
    service = WeatherService()
    
    try:
        city = input("\nIngresa una ciudad (o presiona Enter para usar La Serena): ").strip() or "La Serena"
        weather_data = service.get_weather(city)
        formatted_weather = service.format_weather_data(weather_data)
        print(formatted_weather)
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
