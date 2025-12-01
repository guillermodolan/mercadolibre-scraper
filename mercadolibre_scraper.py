import time
import logging
import os
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Configuramos el logging para luego realizar el proceso RPA.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MercadoLibreScraper:
    def __init__(self, search_term):
        self.search_term = search_term
        self.base_url = f"https://listado.mercadolibre.com.ar/{search_term}_Desde_1_NoIndex_True"
        self.driver = self._setup_driver()
        self.data = []

    def _setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def scrape_items(self):
        logging.info(f"Inica búsqueda para: {self.search_term}")
        try:
            self.driver.get(self.base_url)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'ol.ui-search-layout'))
            )

            self._scroll_page()
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            items = soup.find_all('li', class_='ui-search-layout__item')

            logging.info(f"Se encontraron {len(items)} publicaciones.")

            for item in items:
                try:
                    # Paso 1. Realizamos la extracción del título.
                    # Comprobamos que no se ejecute el diseño "Polymer"
                    title_tag = item.find('a', class_='poly-component__title')

                    # Si el diseño "Polymer" no está, intentamos el diseño "Clásico"
                    if not title_tag:
                        title_tag = item.find('h2', class_='ui-search-item__title')

                    if not title_tag:
                        continue

                    title = title_tag.text.strip()

                    # Paso 2. Realizamos la extracción del link.
                    # En el diseño "Polymer", el título es el link. En el clásico también suele serlo o ahí cerca.
                    link = title_tag['href'] if title_tag.has_attr('href') else "N/A"

                    # Paso 3. Realizamos la extracción del precio.
                    price = "0"

                    # Estrategia Polymer: Buscar el precio ACTUAL (no el tachado anterior)
                    poly_price_div = item.find('div', class_='poly-price__current')

                    if poly_price_div:
                        # Si encontramos el contenedor de precio nuevo, buscamos el valor adentro.
                        price_tag = poly_price_div.find('span', class_='andes-money-amount__fraction')
                        if price_tag:
                            price = price_tag.text.strip()
                    else:
                        # Fallback Diseño Clásico (busca el primer precio que encuentre)
                        price_container = item.find('span', class_='andes-money-amount__fraction')
                        if price_container:
                            price = price_container.text.strip()

                    # Realizamos una limpieza numérica (convertimos "326.799" a float 326799.0)
                    clean_price = float(price.replace('.', '').replace(',', '.')) if price != "0" else 0.0

                    self.data.append({
                        "Producto": title,
                        "Precio": clean_price,
                        "Link": link
                    })

                except Exception as e:
                    # Logueamos errores puntuales sin frenar el robot.
                    logging.warning(f"Error en un producto: {e}")

        except Exception as e:
            logging.error(f"Error crítico en la ejecución: {e}")
        finally:
            self.driver.quit()
            logging.info("Navegador cerrado.")

    def _scroll_page(self):
        """Scrolleamos hasta abajo para asegurar carga de elementos."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Pequeña pausa humana

    def save_to_csv(self, filename='resultados.csv'):
        if not self.data:
            logging.warning("No hay datos para guardar.")
            return

        df = pd.DataFrame(self.data)
        # Ordenamos por precio.
        df = df.sort_values(by='Precio')
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        logging.info(f"Datos guardados exitosamente en {filename}")


# Realizamos la ejecución del programa principal
if __name__ == "__main__":
    # Ruta al archivo de configuración
    # Recordar que como precondición, el archivo "config.json" está en la carpeta raíz, un nivel arriba de src.
    base_path = os.path.dirname(os.path.abspath(__file__))  # Ruta de este script
    config_path = os.path.join(base_path, 'config.json')

    try:
        # Abrimos y leemos el archivo de configuración
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        logging.info("Configuración cargada correctamente.")

        # Extraemos las variables del JSON
        term = config['search_term']
        file_name = config['output_file']

        # Iniciamos el robot con los datos del config
        bot = MercadoLibreScraper(term)
        bot.scrape_items()
        bot.save_to_csv(file_name)

    except FileNotFoundError:
        logging.error("No se encontró el archivo config.json. Asegurate de crearlo en la raíz.")
    except Exception as e:
        logging.error(f"Ocurrió un error: {e}")