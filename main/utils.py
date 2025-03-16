from .parsers.asaxiy_parser import parse_asaxiy
from .parsers.glotr_parser import parse_glotr
from .services.product_service import save_products_to_db


def run_asaxiy_parser_task():
    print("Запуск парсера Asaxiy")
    products = parse_asaxiy()
    save_products_to_db(products)


def run_glotr_parser_task():
    print("Запуск парсера Glotr")
    products = parse_glotr()
    save_products_to_db(products)
