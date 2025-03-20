import logging
import random
import shutil
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


def parse_glotr():
    """Парсер ноутбуков с сайта glotr.uz."""
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    ]
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")

    user_data_dir = f"{tempfile.gettempdir()}/edge_profile_{uuid.uuid4().hex}"
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--remote-debugging-port={random.randint(1024, 49151)}")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Edge(options=options)

    try:
        parsed_products = []
        seen_links = set()

        base_url = "https://glotr.uz/noutbuklar/"
        first_page_url = f"{base_url}?page=1"

        driver.get(first_page_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-card__content"))
        )
        # first_page_soup = BeautifulSoup(driver.page_source, "lxml")

        # pagination = first_page_soup.find("ul", class_="pagination")
        # if pagination:
        #     last_page = pagination.find_all("li")[-1].find("a")
        #     total_pages = int(last_page.text.strip()) if last_page and last_page.text.isdigit() else 1
        # else:
        #     total_pages = 1

        total_pages = 5
        logger.info(f"Найдено страниц: {total_pages}")

        for page_number in range(1, total_pages + 1):
            url = f"{base_url}?page={page_number}"
            driver.get(url)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "row.products-wrap"))
            )

            page_soup = BeautifulSoup(driver.page_source, "lxml")

            products = page_soup.find_all("div", class_="col-lg-20 col-6 product-card__parent")
            if not products:
                logger.info(f"На странице {page_number} нет товаров")
                continue

            for product in products:
                try:
                    link = product.find("a")
                    full_link = f"https://glotr.uz{link.get('href')}" if link else ""
                    if not full_link or full_link in seen_links:
                        continue
                    seen_links.add(full_link)

                    title = product.find("a", class_="product-card__link text-overflow-two-line").text
                    if not title:
                        title = link.get('href').replace("/", "").replace("-", " ")

                    price_element = product.find("div", class_="price-retail")
                    price = price_element.get_text(strip=True).replace("so'm", "").replace(" ", "") if price_element else "0"

                    # Картинка товара
                    img_container = product.find("div", class_="product-card__header").find("div", class_="product-card__swiper-item")
                    img_tag = img_container.find("img") if img_container else None

                    image_url = ""
                    if img_tag:
                        image_url = img_tag.get("src", "").strip()

                        if not image_url or image_url.startswith("data:image"):
                            image_url = (
                                img_tag.get("data-src") or
                                img_tag.get("data-original") or
                                img_tag.get("srcset") or
                                ""
                            )

                            if image_url and "," in image_url:
                                image_url = image_url.split(",")[0].split()[0]

                        if image_url and image_url.startswith("/"):
                            image_url = "https://glotr.uz" + image_url

                    parsed_products.append(ProductData(
                        site="Glotr",
                        name=title,
                        price=price,
                        url=full_link,
                        image_url=image_url
                    ))

                    print(f'glotr | {title} | {price} | {full_link} | {image_url}')

                except Exception as e:
                    logger.error(f"Ошибка при парсинге товара на странице {page_number}: {e}", exc_info=True)

            time.sleep(random.uniform(1.5, 3.0))

        logger.info(f"Собрано товаров: {len(parsed_products)}")
        return parsed_products

    except Exception as e:
        logger.error(f"Критическая ошибка парсинга: {e}", exc_info=True)
        return []

    finally:
        driver.quit()
        shutil.rmtree(user_data_dir, ignore_errors=True)
        logger.info("Драйвер закрыт и профиль удалён")


# Запуск
if __name__ == '__main__':
    parse_glotr()
