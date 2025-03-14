from celery import shared_task

from .parsers.asaxiy_parser import parse_asaxiy
from .parsers.glotr_parser import parse_glotr
from .services.product_service import save_products_to_db


@shared_task
def run_asaxiy_parser_task():
    print("Запуск парсера Asaxiy")
    products = parse_asaxiy()
    save_products_to_db(products)


@shared_task
def run_glotr_parser_task():
    print("Запуск парсера Glotr")
    products = parse_glotr()
    save_products_to_db(products)
