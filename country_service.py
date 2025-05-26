import requests
import logging
from typing import Dict, Optional
from config import SETTINGS  # Nuevo import

class CountryService:  # Clase agregada
    @staticmethod
    def get_country_info(country_query: str) -> Optional[Dict]:
        """
        Obtiene información de un país usando la API REST Countries.
        """
        BASE_URL = "https://restcountries.com/v3.1"  # Variable movida aquí
        endpoints = [
            f"/name/{country_query}",
            f"/alpha/{country_query}"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if isinstance(data, list) and len(data) > 0:
                    return data[0]
                    
            except requests.exceptions.HTTPError as http_err:
                if response.status_code == 404:
                    continue
                logging.error(f"Error HTTP: {http_err}")
            except requests.exceptions.RequestException as req_err:
                logging.error(f"Error de conexión: {req_err}")
        
        return None

    @staticmethod
    def format_country_info(country_data: Dict) -> str:
        """Formatea la información del país para mostrarla."""
        if not country_data:
            return "❌ No se encontró información para el país especificado."
        
        name = country_data.get("name", {}).get("common", "Desconocido")
        capital = ", ".join(country_data.get("capital", ["N/A"]))
        languages = ", ".join(country_data.get("languages", {}).values())
        currencies = [
            f"{curr['name']} ({curr['symbol']})" if 'symbol' in curr else curr['name']
            for curr in country_data.get("currencies", {}).values()
        ]
        population = "{:,}".format(country_data.get("population", 0)).replace(",", ".")
        
        return (
            f"\n🌍 Información de {name}\n"
            f"----------------------------------------\n"
            f"🏙️  Capital: {capital}\n"
            f"🗣️  Idioma(s): {languages}\n"
            f"💰 Moneda(s): {', '.join(currencies)}\n"
            f"👥 Población: {population} habitantes\n"
            f"📍 Región: {country_data.get('region', 'N/A')}\n"
            f"🌐 Subregión: {country_data.get('subregion', 'N/A')}\n"
            f"🚩 Código Alpha-2: {country_data.get('cca2', 'N/A')}\n"
            f"📞 Prefijo telefónico: +{country_data.get('idd', {}).get('root', '')}"
            f"{country_data.get('idd', {}).get('suffixes', [''])[0]}\n"
            f"🗺️ Google Maps: {country_data.get('maps', {}).get('googleMaps', 'N/A')}\n"
            f"----------------------------------------\n"
        )

def main():
    print("\n" + "="*50)
    print("🌎 SERVICIO DE INFORMACIÓN DE PAÍSES")
    print("="*50)
    
    while True:
        country_query = input("\nIngresa el nombre o código del país (o 'salir' para terminar): ").strip()
        
        if country_query.lower() in ['exit', 'salir', 'quit', 'q']:
            print("\n¡Hasta pronto! 👋\n")
            break
            
        if not country_query:
            print("⚠️ Por favor ingresa un nombre o código de país.")
            continue
            
        service = CountryService()
        country_data = service.get_country_info(country_query)
        
        if country_data:
            print(service.format_country_info(country_data))
        else:
            print(f"⚠️ No se encontró información para: {country_query}")
            print("Prueba con:")
            print("- Nombre completo (ej: 'Colombia')")
            print("- Código de 2 letras (ej: 'co')")
            print("- Código de 3 letras (ej: 'col')")

# El menú interactivo se mantiene exactamente igual
if __name__ == "__main__":
    main()