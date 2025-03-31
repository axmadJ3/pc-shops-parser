import logging
import time
from collections import namedtuple

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ProductData = namedtuple('ProductData', ['site', 'name', 'price', 'url', 'image_url'])

def parse_mediapark():
    """Парсинг списка товаров с сайта mediapark.uz и вывод информации в консоль."""

    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Edge(options=options)

    parsed_products = []
    seen_links = set()

    try:
        # Определяем количество страниц автоматически
        driver.get("https://mediapark.uz/products/category/noutbuki-i-ultrabuki-22/noutbuki-313")
        time.sleep(2)

        for page in range(1, 7):
            logger.info(f"Парсим страницу {page}")
            url = f"https://mediapark.uz/products/category/noutbuki-i-ultrabuki-22/noutbuki-313?page={page}"
            driver.get(url)
            time.sleep(3)

            wait = WebDriverWait(driver, 15)

            container = wait.until(EC.presence_of_element_located((
                By.XPATH,
                "//div[contains(@class, 'grid') and contains(@class, 'gap-[6px]')]"
            )))

            product_links = [a.get_attribute("href") for a in container.find_elements(By.XPATH, ".//a[contains(@class, 'w-full')]")]
            logger.info(f"Найдено товаров на странице: {len(product_links)}")

            for idx, link in enumerate(product_links, 1):
                if not link or link in seen_links:
                    continue

                seen_links.add(link)
                logger.info(f"Парсим товар {idx}: {link}")

                # Открываем товар в новой вкладке
                driver.execute_script(f"window.open('{link}', '_blank');")
                driver.switch_to.window(driver.window_handles[1])

                try:
                    wait = WebDriverWait(driver, 15)

                    product_name = wait.until(EC.presence_of_element_located((
                        By.XPATH, "//div[contains(@class, 'grow')]//p[contains(@class, 'text-dark')]"
                    ))).text

                    price_element = wait.until(EC.presence_of_element_located((
                        By.XPATH, "//span[@price]"
                    )))
                    product_price = price_element.get_attribute("price")

                    img_element = wait.until(EC.presence_of_element_located((
                        By.XPATH, "//img[contains(@class, 'object-contain')]"
                    )))
                    product_image = img_element.get_attribute("src")

                    parsed_products.append(ProductData(
                        site="Mediapark",
                        name=product_name,
                        price=int(product_price),
                        url=link,
                        image_url=product_image
                    ))

                    logger.info(f"{product_name} | {product_price} | {product_image}")

                except TimeoutException:
                    logger.warning(f"Не удалось получить информацию о товаре {idx}")

                finally:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                time.sleep(1.5)

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}", exc_info=True)

    finally:
        driver.quit()

    logger.info(f"Собрано товаров: {len(parsed_products)}")
    return parsed_products

if __name__ == '__main__':
    products = parse_mediapark()
