from celery import shared_task
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .parsers.asaxiy_parser import parse_asaxiy

# from .parsers.olcha_parser import parse_olcha
# from .parsers.zoodmall_parser import parse_zoodmall
# from .parsers.texnomart_parser import parse_texnomart
from .services.product_service import save_products_to_db


def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    return driver

@shared_task
def run_asaxiy_parser_task():
    print("Запуск парсера Asaxiy")
    driver = init_driver()

    try:
        products = parse_asaxiy(driver)
        save_products_to_db(products)
    finally:
        driver.quit()

@shared_task
def run_olcha_parser_task():
    print("Запуск парсера Olcha")
    driver = init_driver()

    try:
        products = parse_olcha(driver)
        save_products_to_db(products)
    finally:
        driver.quit()

@shared_task
def run_zoodmall_parser_task():
    print("Запуск парсера Zoodmall")
    driver = init_driver()

    try:
        products = parse_zoodmall(driver)
        save_products_to_db(products)
    finally:
        driver.quit()

@shared_task
def run_texnomart_parser_task():
    print("Запуск парсера Texnomart")
    driver = init_driver()

    try:
        products = parse_texnomart(driver)
        save_products_to_db(products)
    finally:
        driver.quit()
