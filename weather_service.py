import requests
import logging
from typing import Dict, Optional
from config import API_KEYS, SETTINGS

# Configuración básica del logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="weather_service.log"
)

class WeatherService:
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    @staticmethod
    def get_weather(city: str) -> Optional[Dict]:
        """Obtiene el clima actual de una ciudad usando la API de OpenWeatherMap."""
        if not city or not isinstance(city, str):
            logging.error("Parámetro 'city' inválido. Debe ser un string no vacío.")
            raise ValueError("El nombre de la ciudad debe ser un string válido.")

        params = {
            "q": city,
            "appid": API_KEYS["OPENWEATHER"],
            "units": SETTINGS["UNITS"],
            "lang": SETTINGS["LANG"]
        }

        try:
            response = requests.get(WeatherService.BASE_URL, params=params)
            response.raise_for_status()
            logging.info(f"Request exitoso para la ciudad: {city}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"Error HTTP al obtener el clima: {http_err}")
            if response.status_code == 404:
                raise ValueError("Ciudad no encontrada. Verifica el nombre.")
            else:
                raise Exception(f"Error al conectarse a la API: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Error de conexión: {req_err}")
            raise Exception(f"Error de red: {req_err}")

    @staticmethod
    def format_weather_data(weather_data: Dict) -> str:
        """Formatea los datos del clima para mostrarlos de manera legible."""
        if not weather_data or "main" not in weather_data:
            return "Datos meteorológicos no disponibles."

        city = weather_data.get("name", "Ciudad desconocida")
        temp = weather_data["main"].get("temp", "N/A")
        humidity = weather_data["main"].get("humidity", "N/A")
        description = weather_data["weather"][0].get("description", "N/A").capitalize()

        return (
            f"\nClima en {city}:\n"
            f" - Temperatura: {temp}°C\n"
            f" - Humedad: {humidity}%\n"
            f" - Descripción: {description}\n"
        )

# Ejemplo de uso
if __name__ == "__main__":
    try:
        city = input("Ingresa el nombre de la ciudad: ").strip()
        weather_data = WeatherService().get_weather(city)
        print(WeatherService.format_weather_data(weather_data))
    except Exception as e:
        print(f"Error: {e}")