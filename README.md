# 📉 Mercado Libre Price Tracker Bot

Esta es una herramienta de automatización (RPA) diseñada para extraer, monitorear y analizar precios de productos en Mercado Libre Argentina en tiempo real. 

El bot es capaz de adaptarse dinámicamente a los diferentes diseños de interfaz (A/B Testing) de la plataforma, garantizando una extracción de datos robusta y continua. 

A modo de ejemplo, se realiza la búsqueda de **Teclados Gamer**.

## 🚀 Características

- **Búsqueda Inteligente:** Configurable mediante `config.json` para rastrear cualquier nicho de mercado.
- **Resiliencia de Frontend:** Sistema de selectores dinámicos que detecta automáticamente si la web carga el diseño "Clásico" o el nuevo diseño "Polymer" (2025).
- **Data Cleaning:** Limpieza automática de precios y normalización de datos numéricos.
- **Exportación:** Genera reportes estructurados en `.csv` listos para análisis en Excel, Power BI o Tableau.
- **Seguridad:** Navegación anónima simulando comportamiento humano para evitar bloqueos (User-Agent rotativo).

## 🛠 Tecnologías

* **Python 3.13 en adelante.**
* **Selenium WebDriver:** Para la navegación y renderizado de JavaScript.
* **BeautifulSoup4:** Para el parsing de alta velocidad del HTML.
* **Pandas:** Para la estructuración y exportación de datos.

## ⚙️ Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/guillermodolan/mercadolibre-scraper.git
   ```
2. **Crear entorno virtual(se usa PyCharm en este proyecto):**
   Si no se agregó el entorno virtual, seguir los siguientes pasos:
   1. Dentro de este proyecto en Pycharm, click en **File**.
   2. Seleccionar **Settings**.
   3. En el menú Python, buscar **Interpreter**.
   4. Seleccionar una versión como la de este proyecto o más nueva.
3. **Instalar Dependencias (Importante):**
   Para realizar este paso, es necesario estar posicionado en la ruta donde se encuentra el proyecto **mercadolibre-scraper**. Ejemplo: **C:\Users\tu_nombre\nombre_carpeta\mercadolibre-scraper**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configurar la búsqueda: Edita el archivo config.json en la raíz con el siguiente contenido:**
   ```bash
   {
      "search_term": "monitor 144hz",
      "output_file": "reporte_precios.csv"
    }
   ```
4. **Ejecutar el bot:**
   ```bash
   python mercadolibre_scraper.py
   ```
