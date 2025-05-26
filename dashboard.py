import json
from datetime import datetime
from typing import Dict, List
import logging
from config import API_KEYS, SETTINGS
from weather_service import WeatherService
from news_service import NewsService

class Dashboard:
    def __init__(self):
        self.logger = self._setup_logging()

    def _setup_logging(self):
        """Configura el sistema de logging"""
        logging.basicConfig(
            level=SETTINGS["LOG_LEVEL"],
            format="%(asctime)s - %(levelname)s - %(message)s",
            filename="dashboard.log"
        )
        return logging.getLogger(__name__)

    def generate_report(self, weather_data: Dict, news_data: Dict) -> Dict:
        """Genera un reporte combinando datos de clima y noticias"""
        try:
            city_name = weather_data.get("name", "Ciudad desconocida")
            country_code = news_data.get("country", "país desconocido").upper()
        
            return {
                "date": datetime.now().isoformat(),
                "location": {
                    "city": city_name,
                    "country": country_code
                },
                "weather": self._format_weather_data(weather_data),
                "news": self._format_news_data(news_data.get("articles", []))
            }
        except Exception as e:
            self.logger.error(f"Error generando reporte: {e}")
            raise

    def _format_weather_data(self, weather_data: Dict) -> Dict:
        """Formatea los datos del clima"""
        if not weather_data:
            return None
            
        return {
            "temperature": weather_data["main"]["temp"],
            "feels_like": weather_data["main"]["feels_like"],
            "humidity": weather_data["main"]["humidity"],
            "description": weather_data["weather"][0]["description"].capitalize(),
            "wind_speed": weather_data["wind"]["speed"]
        }

    def _format_news_data(self, articles: List[Dict]) -> List[Dict]:
        """Formatea los datos de noticias"""
        return [{
            "title": article.get("title", "Sin título"),
            "source": article.get("source", {}).get("name", "Fuente desconocida"),
            "url": article.get("url", "#"),
            "published_at": article.get("publishedAt", "")
        } for article in articles]

    def display(self, report: Dict) -> None:
        """Muestra el reporte en la consola"""
        print("\n" + "="*50)
        print(f"REPORTE DIARIO - {report['date']}")
        print(f"Ubicación: {report['location']['city']}, {report['location']['country']}")
        
        if report['weather']:
            print("\n🌦️ CONDICIONES METEOROLÓGICAS:")
            print(f"  - Temperatura: {report['weather']['temperature']}°C")
            print(f"  - Sensación térmica: {report['weather']['feels_like']}°C")
            print(f"  - Humedad: {report['weather']['humidity']}%")
            print(f"  - Descripción: {report['weather']['description']}")
            print(f"  - Viento: {report['weather']['wind_speed']} km/h")
        else:
            print("\n⚠️ No se pudo obtener información meteorológica")
        
        if report['news']:
            print("\n📰 NOTICIAS PRINCIPALES:")
            for i, news in enumerate(report['news'], 1):
                print(f"  {i}. {news['title']} ({news['source']})")
        else:
            print("\n⚠️ No se encontraron noticias recientes")
        
        print("="*50 + "\n")

    def save_to_json(self, report: Dict, filename: str) -> None:
        """Guarda el reporte en formato JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            self.logger.info(f"Reporte guardado en {filename}")
        except Exception as e:
            self.logger.error(f"Error guardando reporte: {e}")
            raise

    def run_interactive(self):
        """Modo interactivo para ejecución desde VS Code"""
        print("\n" + "="*50)
        print("🌦️📰 DASHBOARD CLIMA Y NOTICIAS (Modo Interactivo)")
        print("="*50)
        
        city = input("📍 Ingresa la ciudad (ej: Bogotá): ").strip() or "Bogotá"
        country = input("🌍 Ingresa el código de país (ej: co): ").strip().lower() or "co"
        export_file = input("💾 Exportar a JSON (deja vacío para omitir): ").strip() or None
        
        print("\n⏳ Obteniendo datos...")
        
        try:
            weather = WeatherService().get_weather(city)
            news = NewsService().get_news(country)
            
            report = self.generate_report(weather, news)
            self.display(report)
            
            if export_file:
                self.save_to_json(report, export_file)
                print(f"✅ Reporte exportado a '{export_file}'")
                
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.run_interactive()