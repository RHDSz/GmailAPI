"""
Módulo para obtener noticias de Chile utilizando la biblioteca ChileScrapper.

Este módulo proporciona funciones para obtener las noticias más recientes
de los principales medios chilenos utilizando ChileScrapper.
"""

import logging
import random
from typing import Dict, Any, List, Optional
import chilescrapper
from config import CHILE_NEWS_SOURCES, CHILE_NEWS_MAX_PER_SOURCE, CHILE_NEWS_TOTAL_MAX, SETTINGS

# Configuración básica del logging
logging.basicConfig(
    level=SETTINGS["LOG_LEVEL"],
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="news_service.log"
)
logger = logging.getLogger(__name__)

class NewsService:
    """Clase para obtener y procesar noticias de medios chilenos."""
    
    def __init__(self):
        """Inicializa el servicio de noticias."""
        self.sources = CHILE_NEWS_SOURCES
        self.max_per_source = CHILE_NEWS_MAX_PER_SOURCE
        self.max_total = CHILE_NEWS_TOTAL_MAX
    
    def get_news(self, 
                sources: List[str] = None, 
                max_per_source: int = None, 
                max_total: int = None) -> List[Dict[str, Any]]:
        """
        Obtiene las noticias más recientes de los principales medios chilenos.
        
        Args:
            sources (List[str], optional): Lista de fuentes de noticias chilenas a consultar.
            max_per_source (int, optional): Número máximo de noticias a obtener por fuente.
            max_total (int, optional): Número máximo total de noticias a retornar.
            
        Returns:
            List[Dict[str, Any]]: Lista de noticias formateadas.
            
        Raises:
            ValueError: Si los parámetros no son válidos.
            Exception: Para otros errores no especificados.
        """
        # Usar valores predeterminados si no se proporcionan
        sources = sources or self.sources
        max_per_source = max_per_source or self.max_per_source
        max_total = max_total or self.max_total
        
        # Validar parámetros
        if not sources or not isinstance(sources, list):
            logger.error("Lista de fuentes inválida")
            raise ValueError("La lista de fuentes debe ser una lista no vacía")
        
        if not isinstance(max_per_source, int) or max_per_source < 1:
            logger.error("Cantidad máxima por fuente inválida")
            raise ValueError("La cantidad máxima por fuente debe ser un número entero positivo")
        
        if not isinstance(max_total, int) or max_total < 1:
            logger.error("Cantidad máxima total inválida")
            raise ValueError("La cantidad máxima total debe ser un número entero positivo")
        
        all_news = []
        
        try:
            # Obtener noticias de cada fuente
            for source in sources:
                try:
                    logger.info(f"Obteniendo noticias de: {source}")
                    scrapper = chilescrapper.Scrapper(source)
                    articles = scrapper.fetch(max_n=max_per_source)
                    
                    # Formatear y agregar artículos
                    for article in articles:
                        news_item = {
                            'title': article.title,
                            'description': article.description if hasattr(article, 'description') else "No disponible",
                            'url': article.url,
                            'source': source,
                            'source_name': self._get_source_name(source),
                            'published_at': str(article.date) if hasattr(article, 'date') else "No disponible",
                            'url_to_image': article.image if hasattr(article, 'image') else None
                        }
                        all_news.append(news_item)
                    
                    logger.info(f"Noticias obtenidas de {source}: {len(articles)}")
                    
                except Exception as e:
                    logger.error(f"Error al obtener noticias de {source}: {e}")
                    continue
            
            # Mezclar y limitar el número total de noticias
            random.shuffle(all_news)
            limited_news = all_news[:max_total]
            
            logger.info(f"Total de noticias obtenidas: {len(limited_news)}")
            return limited_news
        
        except Exception as e:
            logger.error(f"Error inesperado al obtener noticias: {e}")
            raise
    
    def _get_source_name(self, source_code: str) -> str:
        """
        Obtiene el nombre legible de una fuente de noticias a partir de su código.
        
        Args:
            source_code (str): Código de la fuente de noticias.
            
        Returns:
            str: Nombre legible de la fuente.
        """
        source_names = {
            "emol": "El Mercurio (Emol)",
            "la_tercera": "La Tercera",
            "el_mostrador": "El Mostrador",
            "biobio": "BioBioChile",
            "cooperativa": "Cooperativa",
            "24horas": "24 Horas",
            "meganoticias": "Meganoticias"
        }
        
        return source_names.get(source_code, source_code.capitalize())
    
    def format_news_data(self, news_list: List[Dict[str, Any]]) -> str:
        """
        Formatea una lista de noticias para mostrarlas en formato legible.
        
        Args:
            news_list (List[Dict[str, Any]]): Lista de noticias a formatear.
            
        Returns:
            str: Texto formateado con las noticias.
        """
        if not news_list:
            return "\n📰 NO HAY NOTICIAS DISPONIBLES\n"
        
        formatted_text = "\n📰 ÚLTIMAS NOTICIAS DE CHILE\n"
        formatted_text += "----------------------------------------\n"
        
        for i, news in enumerate(news_list, 1):
            title = news.get('title', 'Sin título')
            source = news.get('source_name', 'Fuente desconocida')
            url = news.get('url', '#')
            
            formatted_text += f"{i}. {title}\n"
            formatted_text += f"   Fuente: {source}\n"
            formatted_text += f"   Enlace: {url}\n\n"
        
        formatted_text += "----------------------------------------\n"
        return formatted_text

def main():
    """Función principal para pruebas del módulo."""
    print("\n" + "="*50)
    print("📰 SERVICIO DE NOTICIAS CHILENAS")
    print("="*50)
    
    service = NewsService()
    
    try:
        print("\nObteniendo noticias de medios chilenos...")
        news = service.get_news()
        formatted_news = service.format_news_data(news)
        print(formatted_news)
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
