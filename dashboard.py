"""
Módulo para generar un dashboard interactivo con información de clima y noticias.

Este módulo integra los servicios de clima, noticias y países para generar
un reporte completo y formateado que puede ser mostrado en consola o enviado por correo.
"""

import logging
import datetime
from typing import Dict, Any, List, Optional
from weather_service import WeatherService
from news_service import NewsService
from country_service import CountryService
from config import SETTINGS, EMAIL_RECIPIENT

# Configuración básica del logging
logging.basicConfig(
    level=SETTINGS["LOG_LEVEL"],
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="dashboard.log"
)
logger = logging.getLogger(__name__)

class Dashboard:
    """Clase para generar un dashboard con información de clima y noticias."""
    
    def __init__(self):
        """Inicializa el dashboard con los servicios necesarios."""
        self.weather_service = WeatherService()
        self.news_service = NewsService()
        self.country_service = CountryService()
        self.default_city = SETTINGS["DEFAULT_CITY"]
        self.default_country = SETTINGS["DEFAULT_COUNTRY"]
    
    def generate_report(self, city: str = None, country_code: str = None) -> str:
        """
        Genera un reporte completo con información de clima, noticias y país.
        
        Args:
            city (str, optional): Ciudad para obtener el clima.
            country_code (str, optional): Código de país para obtener información y noticias.
            
        Returns:
            str: Reporte formateado con toda la información.
        """
        # Usar valores predeterminados si no se proporcionan
        city = city or self.default_city
        country_code = country_code or self.default_country
        
        try:
            logger.info(f"Generando reporte para ciudad: {city}, país: {country_code}")
            
            # Obtener fecha y hora actual
            now = datetime.datetime.now()
            date_str = now.strftime("%d/%m/%Y")
            time_str = now.strftime("%H:%M:%S")
            
            # Obtener datos de clima
            weather_data = self.weather_service.get_weather(city)
            weather_text = self.weather_service.format_weather_data(weather_data)
            
            # Obtener noticias
            news_data = self.news_service.get_news()
            news_text = self.news_service.format_news_data(news_data)
            
            # Obtener información del país
            country_data = self.country_service.get_country_info(country_code)
            country_text = self.country_service.format_country_data(country_data)
            
            # Construir el reporte completo
            report = (
                f"📊 REPORTE DIARIO: CLIMA Y NOTICIAS DE CHILE\n"
                f"================================================\n"
                f"📅 Fecha: {date_str}\n"
                f"🕒 Hora: {time_str}\n"
                f"================================================\n"
                f"{weather_text}\n"
                f"{news_text}\n"
                f"{country_text}\n"
                f"================================================\n"
                f"🔄 Este reporte se actualiza diariamente.\n"
            )
            
            logger.info("Reporte generado exitosamente")
            return report
        
        except Exception as e:
            logger.error(f"Error al generar reporte: {e}")
            raise
    
    def generate_html_report(self, city: str = None, country_code: str = None) -> str:
        """
        Genera un reporte en formato HTML con información de clima, noticias y país.
        
        Args:
            city (str, optional): Ciudad para obtener el clima.
            country_code (str, optional): Código de país para obtener información y noticias.
            
        Returns:
            str: Reporte HTML con toda la información.
        """
        # Usar valores predeterminados si no se proporcionan
        city = city or self.default_city
        country_code = country_code or self.default_country
        
        try:
            logger.info(f"Generando reporte HTML para ciudad: {city}, país: {country_code}")
            
            # Obtener fecha y hora actual
            now = datetime.datetime.now()
            date_str = now.strftime("%d/%m/%Y")
            time_str = now.strftime("%H:%M:%S")
            
            # Obtener datos de clima
            weather_data = self.weather_service.get_weather(city)
            temp = weather_data.get("main", {}).get("temp", 0)
            feels_like = weather_data.get("main", {}).get("feels_like", 0)
            description = weather_data.get("weather", [{}])[0].get("description", "No disponible").capitalize()
            humidity = weather_data.get("main", {}).get("humidity", 0)
            wind_speed = weather_data.get("wind", {}).get("speed", 0)
            icon_code = weather_data.get("weather", [{}])[0].get("icon", "01d")
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            
            # Obtener noticias
            news_data = self.news_service.get_news()
            
            # Obtener información del país
            country_data = self.country_service.get_country_info(country_code)
            country_name = country_data.get("name", {}).get("common", "Chile")
            capital = ", ".join(country_data.get("capital", ["Santiago"]))
            population = country_data.get("population", 0)
            flag_url = country_data.get("flags", {}).get("png", "")
            
            # Construir el HTML para las noticias
            news_html = ""
            for i, news in enumerate(news_data, 1):
                title = news.get('title', 'Sin título')
                source = news.get('source_name', 'Fuente desconocida')
                url = news.get('url', '#')
                image_url = news.get('url_to_image', '')
                
                image_html = f'<img src="{image_url}" alt="{title}" style="max-width:100%; height:auto; margin-bottom:10px;">' if image_url else ''
                
                news_html += f"""
                <div style="margin-bottom:20px; padding:15px; background-color:#f8f9fa; border-radius:5px;">
                    {image_html}
                    <h3 style="margin-top:0; color:#1a73e8;">{title}</h3>
                    <p style="color:#5f6368;">Fuente: {source}</p>
                    <a href="{url}" style="color:#1a73e8; text-decoration:none; font-weight:bold;">Leer más →</a>
                </div>
                """
            
            # Construir el reporte HTML completo
            html = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Reporte Diario: Clima y Noticias de Chile</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 30px;
                        border-bottom: 2px solid #1a73e8;
                        padding-bottom: 10px;
                    }}
                    .date-time {{
                        color: #5f6368;
                        font-size: 14px;
                        margin-bottom: 20px;
                    }}
                    .section {{
                        margin-bottom: 30px;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    }}
                    .weather {{
                        background-color: #e8f0fe;
                    }}
                    .news {{
                        background-color: #fff;
                    }}
                    .country {{
                        background-color: #e6f4ea;
                    }}
                    .weather-icon {{
                        vertical-align: middle;
                        margin-right: 10px;
                    }}
                    .weather-main {{
                        display: flex;
                        align-items: center;
                        margin-bottom: 15px;
                    }}
                    .weather-details {{
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 10px;
                    }}
                    .weather-detail {{
                        padding: 8px;
                        background-color: rgba(255,255,255,0.7);
                        border-radius: 4px;
                    }}
                    .country-flag {{
                        max-width: 100px;
                        margin-right: 15px;
                        float: left;
                    }}
                    h1, h2 {{
                        color: #1a73e8;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 30px;
                        font-size: 12px;
                        color: #5f6368;
                        border-top: 1px solid #dadce0;
                        padding-top: 20px;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>📊 Reporte Diario: Clima y Noticias de Chile</h1>
                    <div class="date-time">
                        <p>📅 Fecha: {date_str} | 🕒 Hora: {time_str}</p>
                    </div>
                </div>
                
                <div class="section weather">
                    <h2>🌦️ Condiciones Meteorológicas en {city}</h2>
                    <div class="weather-main">
                        <img src="{icon_url}" alt="{description}" class="weather-icon" width="50" height="50">
                        <div>
                            <h3 style="margin:0;">{temp}°C</h3>
                            <p style="margin:0;">{description}</p>
                        </div>
                    </div>
                    <div class="weather-details">
                        <div class="weather-detail">
                            <strong>🤔 Sensación:</strong> {feels_like}°C
                        </div>
                        <div class="weather-detail">
                            <strong>💧 Humedad:</strong> {humidity}%
                        </div>
                        <div class="weather-detail">
                            <strong>🌬️ Viento:</strong> {wind_speed} m/s
                        </div>
                    </div>
                </div>
                
                <div class="section news">
                    <h2>📰 Últimas Noticias de Chile</h2>
                    {news_html}
                </div>
                
                <div class="section country">
                    <h2>🌎 Información de {country_name}</h2>
                    <img src="{flag_url}" alt="Bandera de {country_name}" class="country-flag">
                    <p><strong>Capital:</strong> {capital}</p>
                    <p><strong>Población:</strong> {population:,} habitantes</p>
                    <div style="clear:both;"></div>
                </div>
                
                <div class="footer">
                    <p>🔄 Este reporte se actualiza diariamente y se envía a {EMAIL_RECIPIENT}</p>
                    <p>Generado automáticamente el {date_str} a las {time_str}</p>
                </div>
            </body>
            </html>
            """
            
            logger.info("Reporte HTML generado exitosamente")
            return html
        
        except Exception as e:
            logger.error(f"Error al generar reporte HTML: {e}")
            raise

def main():
    """Función principal para pruebas del módulo."""
    print("\n" + "="*50)
    print("📊 DASHBOARD DE CLIMA Y NOTICIAS")
    print("="*50)
    
    dashboard = Dashboard()
    
    try:
        city = input("\nIngresa una ciudad (o presiona Enter para usar La Serena): ").strip() or "La Serena"
        country_code = input("Ingresa un código de país (o presiona Enter para usar CL): ").strip() or "CL"
        
        print("\nGenerando reporte...")
        report = dashboard.generate_report(city, country_code)
        print(report)
        
        save_html = input("\n¿Deseas guardar el reporte en HTML? (s/n): ").strip().lower()
        if save_html == 's':
            html_report = dashboard.generate_html_report(city, country_code)
            with open("reporte.html", "w", encoding="utf-8") as f:
                f.write(html_report)
            print("\n✅ Reporte HTML guardado como 'reporte.html'")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
