import requests
import logging
from typing import Dict, List, Optional
from config import API_KEYS, SETTINGS  # Importamos las configuraciones

class NewsService:
    GNEWS_API_URL = "https://gnews.io/api/v4/"

    @staticmethod
    def get_news(
        country: Optional[str] = None,
        query: Optional[str] = None,
        category: Optional[str] = None,
        max_results: int = 5
    ) -> Optional[Dict]:
        """Obtiene noticias de GNews.io por país, término o categoría."""
        if not country and not query and not category:
            logging.error("Se requiere al menos un parámetro: country, query o category.")
            raise ValueError("Debes especificar un país, término o categoría.")

        params = {
            "token": API_KEYS["GNEWS"],  # Usamos la API key de config.py
            "max": max_results,
        }

        if country:
            params["country"] = country.lower()
        if query:
            params["q"] = query
        if category:
            params["category"] = category.lower()

        try:
            response = requests.get(f"{NewsService.GNEWS_API_URL}top-headlines", params=params)
            response.raise_for_status()
            logging.info(f"Request exitoso: {params}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"Error HTTP: {http_err}")
            if response.status_code == 401:
                raise ValueError("API Key inválida o no proporcionada.")
            elif response.status_code == 429:
                raise Exception("Límite de requests excedido.")
            else:
                raise Exception(f"Error en la API: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Error de conexión: {req_err}")
            raise Exception(f"Error de red: {req_err}")

    @staticmethod
    def get_weather_news(country: str) -> List[Dict]:
        """Busca noticias meteorológicas usando términos clave en el país."""
        weather_keywords = " OR ".join([
            "clima",
            "tiempo",
            "pronóstico meteorológico",
            "lluvia",
            "temperatura",
            "huracán",
            "sequía"
        ])
        query = f"({weather_keywords}) AND {country}"
        news_data = NewsService.get_news(query=query, max_results=5)
        return news_data.get("articles", [])

    @staticmethod
    def format_news(news: List[Dict]) -> str:
        """Formatea noticias para mostrarlas legiblemente."""
        if not news:
            return "No se encontraron noticias recientes."

        formatted = []
        for idx, article in enumerate(news, 1):
            title = article.get("title", "Sin título")
            source = article.get("source", {}).get("name", "Fuente desconocida")
            url = article.get("url", "#")
            formatted.append(
                f"\n{idx}. {title} ({source})\n"
                f"   Enlace: {url}\n"
            )
        return "\n".join(formatted)

# Menú interactivo (se mantiene igual para cuando se ejecute directamente)
if __name__ == "__main__":
    # Configuración de logging para el modo standalone
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="news_service.log"
    )

    print("🔍 Servicio de Noticias (GNews API) 🔍")
    print("1. Noticias por país (ej: 'co', 'mx')")
    print("2. Buscar por término (ej: 'deportes')")
    print("3. Noticias meteorológicas del país")
    print("4. Salir")

    try:
        option = input("\nElige una opción (1-4): ").strip()
        if option == "1":
            country = input("Ingresa el código de país (ej: 'co' para Colombia): ").strip()
            news_data = NewsService.get_news(country=country)
            articles = news_data.get("articles", [])
            if not articles:
                print(f"⚠️ No hay noticias recientes para {country.upper()}.")
            else:
                print(f"\n📰 Últimas noticias en {country.upper()}:")
                print(NewsService.format_news(articles))

        elif option == "2":
            query = input("Ingresa el término a buscar (ej: 'fútbol'): ").strip()
            news_data = NewsService.get_news(query=query)
            print(f"\n🔎 Resultados para '{query}':")
            print(NewsService.format_news(news_data.get("articles", [])))

        elif option == "3":
            country = input("Ingresa el código de país (ej: 'co'): ").strip()
            weather_news = NewsService.get_weather_news(country)
            if not weather_news:
                print(f"⚠️ No se encontraron noticias meteorológicas recientes para {country.upper()}.")
            else:
                print(f"\n🌦️ Noticias meteorológicas en {country.upper()}:")
                print(NewsService.format_news(weather_news))

        elif option == "4":
            print("¡Hasta luego! 👋")
        else:
            print("Opción inválida.")
    except Exception as e:
        print(f"❌ Error: {e}")