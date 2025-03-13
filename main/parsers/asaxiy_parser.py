from collections import namedtuple

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ProductData = namedtuple('ProductData', ['site', 'name', 'price', 'url', 'image_url'])

def parse_asaxiy(driver):
    parsed_products = []
    page_number = 1

    while True:
        url = f"https://asaxiy.uz/uz/product/kompyutery-i-orgtehnika/noutbuki/noutbuki-2?page={page_number}"
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product__item__info-title"))
            )
        except:
            break  # если нет продуктов или проблема с загрузкой

        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = soup.find_all("div", class_="col-6 col-xl-3 col-md-4")

        if not products:
            break

        for product in products:
            title = product.find("span", class_="product__item__info-title").text.strip()
            price_text = product.find("span", class_="product__item-price").text.strip()
            price = int(price_text.replace("so'm", "").replace(" ", "").replace("\xa0", ""))

            link_tag = product.find("a", href=True)
            full_link = "https://asaxiy.uz" + link_tag['href'] if link_tag else None

            img_tag = product.find("img")
            image_url = img_tag['src'] if img_tag else None

            parsed_products.append(ProductData(
                site="Asaxiy",
                name=title,
                price=price,
                url=full_link,
                image_url=image_url
            ))

        page_number += 1

    return parsed_products
