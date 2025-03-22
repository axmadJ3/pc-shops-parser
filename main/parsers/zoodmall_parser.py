import logging
import random
import tempfile
import time
import uuid
from collections import namedtuple

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ProductData = namedtuple('ProductData', ['site', 'name', 'price', 'url', 'image_url'])

def parse_zoodmall():
    """Парсер ноутбуков с сайта zoodnmall.uz с динамической пагинацией."""
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Уникальные настройки для профиля браузера
    user_data_dir = f"{tempfile.gettempdir()}/edge_profile_{uuid.uuid4().hex}"
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--remote-debugging-port={random.randint(1024, 49151)}")

    # Отключение автоматизации
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Edge(options=options)

    try:
        parsed_products = []
        seen_links = set()

        # Переход на первую страницу и получение общего количества страниц
        base_url = "https://www.zoodmall.uz/category/3053/noutbuklar/"
        first_page_url = f"{base_url}?page=1"

        logger.info(f"Загружаем первую страницу: {first_page_url}")
        driver.get(first_page_url)

        # Ждем появления элемента, чтобы страница полностью загрузилась
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-item-list"))
        )

        total_pages = 24
        logger.info(f"Обнаружено страниц: {total_pages}")

        # Проход по всем страницам
        for page_number in range(1, total_pages + 1):
            url = f"{base_url}?page={page_number}"
            logger.info(f"Обработка страницы {page_number}: {url}")

            try:
                driver.get(url)

                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "product-item-list"))
                )

                page_soup = BeautifulSoup(driver.page_source, "lxml")

                products = page_soup.find_all("div", class_="product-item-list")

                if not products:
                    logger.info(f"На странице {page_number} нет товаров")
                    continue

                for product in products:
                    try:
                        # Ссылка на товар
                        links = product.find_all("a", href=True)
                        full_link = None
                        for link_tag in links:
                            href = link_tag.get("href")
                            if href and "/product/" in href:
                                full_link = "https://zoodmall.uz" + href
                                break

                        # Пропуск повторов
                        if not full_link or full_link in seen_links:
                            continue

                        seen_links.add(full_link)

                        # Название товара
                        title = product.find("div", class_="product-mini__title").text.strip()

                        # Цена товара
                        price_element = product.find("div", class_="product-mini__totalLocalPrice")
                        price = price_element.text.strip().replace("UZS", "").replace(" ", "").replace("\xa0", "") if price_element else "0"

                        # Картинка товара
                        img_container = product.find("div", class_="product-mini__img")
                        img_tag = img_container.find("img") if img_container else None
                        image_url = img_tag.get('src', '') if img_tag else ''

                        parsed_products.append(ProductData(
                            site="Zoodmall",
                            name=title,
                            price=price,
                            url=full_link,
                            image_url=image_url
                        ))

                        # Вывод товара в консоль
                        logger.info(f'Zoodmall | {title} | {price} | {full_link} | {image_url}')

                    except Exception as e:
                        logger.error(f"Ошибка при парсинге товара на странице {page_number}: {e}", exc_info=True)

                # Задержка после обработки страницы
                time.sleep(random.uniform(1.5, 3.0))

            except Exception as e:
                logger.warning(f"Ошибка загрузки страницы {page_number}: {e}", exc_info=True)
                continue

        logger.info(f"Всего собрано товаров: {len(parsed_products)}")
        return parsed_products

    except Exception as e:
        logger.error(f"Критическая ошибка при парсинге: {e}", exc_info=True)
        return []

    finally:
        try:
            driver.quit()
            logger.info("Драйвер закрыт успешно")
        except Exception as e:
            logger.warning(f"Ошибка при закрытии драйвера: {e}")

# Запуск
if __name__ == '__main__':
    parse_zoodmall()
