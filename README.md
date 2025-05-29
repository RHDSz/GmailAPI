# Sistema de Reportes Automáticos: Clima y Noticias de Chile

Este proyecto implementa un sistema automatizado para generar y enviar reportes diarios que combinan información del clima, noticias actualizadas de medios chilenos e información del país, todo enviado por correo electrónico mediante la API de Gmail.

## Características Principales

- **Clima de La Serena**: Obtiene datos meteorológicos actualizados usando OpenWeatherMap
- **Noticias de Chile**: Extrae noticias de los principales medios chilenos usando ChileScrapper
- **Información de País**: Proporciona datos relevantes sobre Chile usando REST Countries API
- **Envío Automático**: Envía reportes diarios por correo electrónico usando la API de Gmail
- **Personalizable**: Permite configurar ciudad, país, destinatario y otros parámetros
- **Programable**: Incluye scripts para automatizar el envío en Windows, Linux y macOS

## Requisitos

- Python 3.6 o superior
- Conexión a Internet
- Cuenta de Gmail para el envío de correos
- Credenciales OAuth 2.0 para la API de Gmail (incluidas en el proyecto)

## Instalación

1. **Descomprimir el archivo ZIP** en una carpeta de su elección

2. **Instalar las dependencias necesarias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verificar que las credenciales estén en su lugar**:
   - El archivo `credentials.json` debe estar en la carpeta raíz del proyecto
   - Este archivo contiene las credenciales OAuth 2.0 para la API de Gmail

## Uso Básico

### Generar y Ver un Reporte

Para generar y ver un reporte sin enviarlo por correo:

```bash
python main.py
```

Esto mostrará el reporte en la consola y guardará una copia en formato HTML.

### Personalizar el Reporte

Puede personalizar varios parámetros del reporte:

```bash
python main.py --city "Santiago" --country "CL" --save
```

Parámetros disponibles:
- `--city`: Ciudad para obtener datos del clima (predeterminado: "La Serena")
- `--country`: Código de país para obtener información (predeterminado: "CL")
- `--save`: Guardar el reporte en archivos locales (texto y HTML)

### Enviar un Reporte por Correo

Para generar y enviar un reporte por correo electrónico:

```bash
python envio_automatico.py --email destinatario@example.com --ciudad "La Serena" --pais "CL"
```

Parámetros disponibles:
- `--ciudad`: Ciudad para obtener datos del clima (predeterminado: "La Serena")
- `--pais`: Código de país para obtener información (predeterminado: "CL")
- `--email`: Correo electrónico del destinatario (predeterminado: configurado en config.py)
- `--asunto`: Asunto del correo electrónico (predeterminado: configurado en config.py)
- `--no-guardar`: No guardar una copia local del reporte

**Nota**: La primera vez que ejecute el envío, se abrirá una ventana del navegador para autorizar el acceso a Gmail. Después de esta autorización inicial, los próximos envíos serán automáticos.

## Automatización del Envío

### En Windows (usando Task Scheduler)

1. **Crear un archivo batch** (por ejemplo, `envio_diario.bat`) con el siguiente contenido:
   ```batch
   @echo off
   cd /d "C:\ruta\donde\extrajiste\clima_noticias_chile"
   python envio_automatico.py
   ```

2. **Abrir el Programador de tareas**:
   - Buscar "Programador de tareas" en el menú de inicio
   - Hacer clic en "Crear tarea básica"
   - Darle un nombre como "Envío diario de reporte clima y noticias"
   - Seleccionar "Diariamente" y configurar la hora (por ejemplo, 8:00 AM)
   - En la acción, seleccionar "Iniciar un programa"
   - Buscar y seleccionar el archivo batch creado

### En Linux (usando cron)

1. **Abrir el editor de crontab**:
   ```bash
   crontab -e
   ```

2. **Añadir una línea** para ejecutar el script diariamente a las 8:00 AM:
   ```
   0 8 * * * cd /ruta/donde/extrajiste/clima_noticias_chile && python envio_automatico.py
   ```

### En macOS (usando launchd)

1. **Crear un archivo plist** en `~/Library/LaunchAgents/com.usuario.climanoticias.plist`:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.usuario.climanoticias</string>
       <key>ProgramArguments</key>
       <array>
           <string>/usr/bin/python3</string>
           <string>/ruta/donde/extrajiste/clima_noticias_chile_v2/envio_automatico.py</string>
       </array>
       <key>StartCalendarInterval</key>
       <dict>
           <key>Hour</key>
           <integer>8</integer>
           <key>Minute</key>
           <integer>0</integer>
       </dict>
   </dict>
   </plist>
   ```

2. **Cargar el archivo plist**:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.usuario.climanoticias.plist
   ```

## Personalización Avanzada

### Modificar la Configuración

Puede personalizar varios aspectos del sistema editando el archivo `config.py`:

- **API Keys**: Cambiar las claves API para OpenWeatherMap o NewsAPI
- **Fuentes de Noticias**: Modificar la lista de medios chilenos a consultar
- **Correo Electrónico**: Cambiar el destinatario predeterminado o el asunto
- **Configuración General**: Ajustar ciudad predeterminada, país, idioma, etc.

### Personalizar el Formato del Reporte

El formato del reporte HTML se puede personalizar editando la función `generate_html_report` en el archivo `dashboard.py`. Esto le permite cambiar colores, fuentes, disposición y otros aspectos visuales del reporte.

## Estructura del Proyecto

- `main.py`: Punto de entrada principal
- `config.py`: Configuración centralizada
- `weather_service.py`: Servicio de clima
- `news_service.py`: Servicio de noticias chilenas
- `country_service.py`: Servicio de información de países
- `dashboard.py`: Integración de todos los servicios
- `gmail_service.py`: Servicio de envío de correos
- `envio_automatico.py`: Script para envío automático
- `requirements.txt`: Dependencias del proyecto
- `credentials.json`: Credenciales para la API de Gmail

## Solución de Problemas

### Error de Autenticación con Gmail

Si encuentra problemas con la autenticación de Gmail:

1. Elimine el archivo `token.json` si existe
2. Ejecute nuevamente el script de envío
3. Siga las instrucciones en el navegador para autorizar el acceso

### Error al Obtener Noticias

Si no se obtienen noticias de algún medio chileno:

1. Verifique su conexión a Internet
2. Compruebe que ChileScrapper esté instalado correctamente
3. Intente con diferentes fuentes de noticias en `config.py`

### Error al Obtener Datos del Clima

Si no se obtienen datos del clima:

1. Verifique que la API key de OpenWeatherMap sea válida
2. Compruebe que la ciudad especificada exista y esté bien escrita
3. Verifique su conexión a Internet

## Créditos y Licencias

- **OpenWeatherMap**: Proporciona datos meteorológicos
- **ChileScrapper**: Biblioteca para extraer noticias de medios chilenos
- **REST Countries API**: Proporciona información de países
- **Google API**: Proporciona acceso a la API de Gmail

Este proyecto está licenciado bajo los términos de la licencia MIT.

## Contacto y Soporte

Para preguntas, sugerencias o reportes de errores, por favor contacte a:
- Correo: fcer14.2002@gmail.com

---

Desarrollado como parte del desafío de integración de APIs y automatización de reportes.
