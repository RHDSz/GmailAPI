from weather_service import WeatherService
from news_service import NewsService
from dashboard import Dashboard
import argparse
import sys

def get_user_input():
    """Solicita entrada al usuario cuando se ejecuta desde VS Code"""
    print("\n" + "="*50)
    print("🌦️📰 DASHBOARD CLIMA Y NOTICIAS (Modo Interactivo)")
    print("="*50)
    
    city = input("📍 Ingresa la ciudad (ej: Bogotá): ").strip() or "Bogotá"
    country = input("🌍 Ingresa el código de país (ej: co): ").strip().lower() or "co"
    
    return city, country

def run_app(city: str, country_code: str, export_file: str = None):
    """
    Ejecuta la aplicación principal con los parámetros proporcionados.
    """
    try:
        print("\n⏳ Obteniendo datos...")
        
        # 1. Obtener clima
        weather = WeatherService().get_weather(city)
        if not weather:
            print("❌ No se pudo obtener datos del clima")
            return
        
        # 2. Obtener noticias (pasamos el código de país para mantener consistencia)
        news = NewsService().get_news(country_code)
        if not news:
            print("⚠️ No se encontraron noticias recientes")
            news = {"country": country_code.upper(), "articles": []}  # Mantenemos el código de país
        
        # 3. Generar y mostrar reporte
        dashboard = Dashboard()
        report = dashboard.generate_report(weather, news)
        dashboard.display(report)
        
        # 4. Exportar si se especificó
        if export_file:
            dashboard.save_to_json(report, export_file)
            print(f"✅ Reporte exportado a '{export_file}'")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

def main():
    # Detectar si se ejecuta desde VS Code (sin argumentos)
    if len(sys.argv) == 1:
        city, country = get_user_input()
        run_app(city, country)
    else:
        # Modo CLI tradicional
        parser = argparse.ArgumentParser(description="Dashboard de Clima y Noticias")
        parser.add_argument("city", help="Ciudad para el reporte meteorológico", nargs='?', default="Bogotá")
        parser.add_argument("country", help="Código de país para noticias (ej: co, mx, us)", nargs='?', default="co")
        parser.add_argument("--export", help="Exportar reporte a archivo JSON")
        args = parser.parse_args()
        run_app(args.city, args.country, args.export)

if __name__ == "__main__":
    main()